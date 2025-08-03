import os
import cv2
import face_recognition
import numpy as np
import pickle
import time
from collections import defaultdict
from multiprocessing import Process, Queue, cpu_count
import sys

# Detección automática de entorno Streamlit
WEB_MODE = 'streamlit' in sys.modules

if WEB_MODE:
    import streamlit as st
    from PIL import Image

def resource_path(relative_path):
    """Maneja rutas para ejecutables y desarrollo normal"""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

# --- CONFIGURACIÓN ---
MODEL_TYPE = "hog"  # "hog" más rápido, "cnn" más preciso
SCALE_FACTOR = 0.25
ENCODINGS_FILE = resource_path("base_biometrica.pkl")
FRAME_THICKNESS = 2
FONT_THICKNESS = 1
TOLERANCE = 0.45
MIN_CONFIDENCE_MATCHES = 3

# Parámetros de seguimiento
STALE_THRESHOLD = 30
BASE_DETECTION_INTERVAL = 15
MAX_DETECTION_INTERVAL = 60
MIN_DETECTION_INTERVAL = 5
IOU_STABLE_THRESHOLD = 0.6
EMA_ALPHA = 0.3

class FacialRecognitionSystem:
    def __init__(self):
        self.encodings, self.names = self.load_encodings()
        self.face_trackers = {}
        self.face_positions = {}
        self.face_confidences = defaultdict(int)
        self.name_history = {}
        self.face_stale = {}
        self.next_face_id = 0
        self.frame_count = 0
        self.detection_interval = BASE_DETECTION_INTERVAL
        self.last_processed_frame_id = -1
        self.matched_total = 0
        self.created_total = 0
        
        if WEB_MODE:
            self.status_text = st.empty()
            self.video_placeholder = st.empty()
            self.stop_button = st.button("⏹ Detener Reconocimiento")
        else:
            self.window_name = "Reconocimiento Facial Paralelo"
            cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)

    def load_encodings(self):
        """Carga las codificaciones faciales desde archivo"""
        if WEB_MODE:
            st.info("Cargando base de datos biométrica...")
        
        if os.path.exists(ENCODINGS_FILE):
            with open(ENCODINGS_FILE, "rb") as f:
                data = pickle.load(f)
                if isinstance(data.get("encodings", None), dict):
                    return list(data["encodings"].values()), list(data["encodings"].keys())
                return data["encodings"], data["names"]
        else:
            error_msg = f"Archivo no encontrado: {ENCODINGS_FILE}"
            if WEB_MODE:
                st.error(error_msg)
            raise FileNotFoundError(error_msg)

    @staticmethod
    def iou(boxA, boxB):
        """Calcula Intersección sobre Unión para bounding boxes"""
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[0] + boxA[2], boxB[0] + boxB[2])
        yB = min(boxA[1] + boxA[3], boxB[1] + boxB[3])
        interArea = max(0, xB - xA) * max(0, yB - yA)
        union = boxA[2]*boxA[3] + boxB[2]*boxB[3] - interArea
        return interArea / union if union > 0 else 0

    @staticmethod
    def blend_box(old_box, new_box, alpha=EMA_ALPHA):
        """Suavizado de movimiento para bounding boxes"""
        return tuple(int(old * (1 - alpha) + new * alpha) for old, new in zip(old_box, new_box))

    def worker_process(self, q_in, q_out):
        """Proceso paralelo para reconocimiento facial"""
        while True:
            item = q_in.get()
            if item is None:
                break
                
            frame_id, small_rgb = item
            face_locations = face_recognition.face_locations(small_rgb, model=MODEL_TYPE)
            
            if not face_locations and MODEL_TYPE == "hog":
                face_locations = face_recognition.face_locations(small_rgb, model="cnn")

            face_encodings = face_recognition.face_encodings(small_rgb, face_locations)
            detections = []
            
            for encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
                distances = face_recognition.face_distance(self.encodings, encoding)
                min_distance = np.min(distances) if len(distances) > 0 else 1.0
                best_match = np.argmin(distances) if len(distances) > 0 else -1
                
                name = self.names[best_match] if min_distance < TOLERANCE and best_match >= 0 else "Desconocido"
                
                detections.append({
                    "name": name,
                    "box": (
                        int(left / SCALE_FACTOR), 
                        int(top / SCALE_FACTOR),
                        int((right - left) / SCALE_FACTOR), 
                        int((bottom - top) / SCALE_FACTOR)
                    ),
                    "distance": min_distance
                })
            
            q_out.put((frame_id, detections))

    def process_detections(self, frame, detections):
        """Procesa las detecciones y actualiza los trackers"""
        used_detection_indices = set()
        stable_matches = 0
        matched_this_frame = 0

        # Emparejar detecciones con trackers existentes
        for fid, (x, y, w, h) in list(self.face_positions.items()):
            best_match_idx, best_iou = None, 0
            
            for idx, det in enumerate(detections):
                if idx in used_detection_indices:
                    continue
                    
                det_box = det["box"]
                tracker_box = (x, y, w, h)
                score = self.iou(det_box, tracker_box)
                
                if score > best_iou:
                    best_iou = score
                    best_match_idx = idx

            if best_iou > 0.3 and best_match_idx is not None:
                det = detections[best_match_idx]
                name = det["name"]
                left, top, w_new, h_new = det["box"]

                # Actualizar posición y confianza
                self.face_positions[fid] = self.blend_box(
                    self.face_positions.get(fid, (left, top, w_new, h_new)), 
                    (left, top, w_new, h_new)
                )

                # Manejar tracker
                if best_iou < 0.5 or fid not in self.face_trackers:
                    tracker = cv2.TrackerKCF_create()
                    tracker.init(frame, (left, top, w_new, h_new))
                    self.face_trackers[fid] = tracker

                # Actualizar historial de nombres y confianza
                if name != "Desconocido":
                    if fid in self.name_history:
                        if self.name_history[fid] == name:
                            self.face_confidences[fid] = min(self.face_confidences[fid] + 1, 10)
                        else:
                            self.face_confidences[fid] = max(self.face_confidences[fid] - 1, 0)
                            self.name_history[fid] = name
                    else:
                        self.name_history[fid] = name
                        self.face_confidences[fid] = 1
                else:
                    self.face_confidences[fid] = max(self.face_confidences.get(fid, 0) - 1, 0)

                self.face_stale[fid] = 0
                used_detection_indices.add(best_match_idx)
                matched_this_frame += 1
                
                if best_iou > IOU_STABLE_THRESHOLD:
                    stable_matches += 1

        # Crear nuevos trackers para detecciones no emparejadas
        created_this_frame = 0
        for idx, det in enumerate(detections):
            if idx in used_detection_indices:
                continue
                
            name = det["name"]
            left, top, w_new, h_new = det["box"]

            # Verificar duplicados
            if any(self.iou((left, top, w_new, h_new), (x, y, w, h)) > 0.5 
               for x, y, w, h in self.face_positions.values()):
                continue

            # Crear nuevo tracker
            tracker = cv2.TrackerKCF_create()
            tracker.init(frame, (left, top, w_new, h_new))
            self.face_trackers[self.next_face_id] = tracker
            self.face_positions[self.next_face_id] = (left, top, w_new, h_new)
            self.face_stale[self.next_face_id] = 0
            self.face_confidences[self.next_face_id] = 1 if name != "Desconocido" else 0
            
            if name != "Desconocido":
                self.name_history[self.next_face_id] = name
                
            self.next_face_id += 1
            created_this_frame += 1

        # Ajustar intervalo de detección dinámicamente
        if stable_matches > 0:
            self.detection_interval = min(MAX_DETECTION_INTERVAL, self.detection_interval + 1)
        else:
            self.detection_interval = max(MIN_DETECTION_INTERVAL, BASE_DETECTION_INTERVAL)

        self.matched_total += matched_this_frame
        self.created_total += created_this_frame
        
        return matched_this_frame, created_this_frame

    def update_trackers(self, frame):
        """Actualiza los trackers existentes y limpia los inactivos"""
        # Actualizar posiciones
        for fid in list(self.face_trackers.keys()):
            success, box = self.face_trackers[fid].update(frame)
            if success:
                self.face_positions[fid] = self.blend_box(
                    self.face_positions.get(fid, box), 
                    box
                )
        
        # Limpiar trackers inactivos
        for fid in list(self.face_positions.keys()):
            self.face_stale[fid] = self.face_stale.get(fid, 0) + 1
            
            if self.face_stale[fid] > 0 and self.face_confidences.get(fid, 0) > 0:
                self.face_confidences[fid] = max(self.face_confidences[fid] - 0.01, 0)
                
            if self.face_stale[fid] > STALE_THRESHOLD:
                self.face_trackers.pop(fid, None)
                self.face_positions.pop(fid, None)
                self.face_confidences.pop(fid, None)
                self.name_history.pop(fid, None)
                self.face_stale.pop(fid, None)

    def draw_results(self, frame):
        """Dibuja los resultados en el frame"""
        for fid, (x, y, w, h) in self.face_positions.items():
            confidence = self.face_confidences.get(fid, 0)
            name = self.name_history.get(fid, "Desconocido")

            # Determinar color y texto
            if name != "Desconocido":
                if confidence < MIN_CONFIDENCE_MATCHES:
                    display_name = f"Verificando {name}..."
                    color = (0, 165, 255)  # Naranja
                else:
                    display_name = name
                    color = (0, 255, 0)  # Verde
            else:
                display_name = "Desconocido"
                color = (0, 0, 255)  # Rojo

            # Dibujar bounding box y etiqueta
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, FRAME_THICKNESS)
            cv2.rectangle(frame, (x, y + h), (x + w, y + h + 35), color, -1)
            cv2.putText(
                frame, display_name, (x + 6, y + h + 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), FONT_THICKNESS
            )

            # Barra de confianza
            if name != "Desconocido":
                conf_width = int(w * min(1, confidence / MIN_CONFIDENCE_MATCHES))
                cv2.rectangle(
                    frame, (x, y - 10), (x + conf_width, y), 
                    (0, 255, 255), 2  # Amarillo
                )

    def run(self):
        """Ejecuta el sistema principal de reconocimiento"""
        # Configurar cámara
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            error_msg = "Error al acceder a la cámara"
            if WEB_MODE:
                st.error(error_msg)
            raise RuntimeError(error_msg)

        # Configurar multiprocesamiento
        q_in, q_out = Queue(maxsize=5), Queue()
        workers = [
            Process(target=self.worker_process, args=(q_in, q_out))
            for _ in range(min(cpu_count(), 4))
        ]
        
        for p in workers:
            p.daemon = True
            p.start()

        try:
            while True:
                if WEB_MODE and getattr(self, 'stop_button', False):
                    break
                    
                start_time = time.time()
                ret, frame = cap.read()
                if not ret:
                    if WEB_MODE:
                        time.sleep(0.1)
                        continue
                    break
                    
                frame = cv2.flip(frame, 1)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.frame_count += 1

                # 1. Actualizar trackers existentes
                self.update_trackers(frame)

                # 2. Enviar frame para detección paralela
                if self.frame_count % self.detection_interval == 0 and not q_in.full():
                    small_rgb = cv2.resize(rgb_frame, (0, 0), fx=SCALE_FACTOR, fy=SCALE_FACTOR)
                    q_in.put((self.frame_count, small_rgb))

                # 3. Procesar detecciones recibidas
                matched_this_frame, created_this_frame = 0, 0
                while not q_out.empty():
                    frame_id, detections = q_out.get()
                    if frame_id > self.last_processed_frame_id:
                        matched, created = self.process_detections(frame, detections)
                        matched_this_frame += matched
                        created_this_frame += created
                        self.last_processed_frame_id = frame_id

                # 4. Dibujar resultados
                display_frame = frame.copy()
                self.draw_results(display_frame)

                # 5. Mostrar métricas
                fps = 1.0 / (time.time() - start_time)
                metrics_text = (
                    f"FPS: {fps:.1f} | Rostros: {len(self.face_positions)} | "
                    f"Emparejados: {matched_this_frame} | Nuevos: {created_this_frame}"
                )

                if WEB_MODE:
                    self.status_text.info(metrics_text)
                    self.video_placeholder.image(cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB))
                else:
                    cv2.putText(
                        display_frame, metrics_text, (10, 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2
                    )
                    cv2.imshow(self.window_name, display_frame)
                    if cv2.waitKey(1) == 27:
                        break

        finally:
            # Limpieza
            for _ in workers:
                q_in.put(None)
            for p in workers:
                p.join()
            cap.release()
            if not WEB_MODE:
                cv2.destroyAllWindows()

            print(f"Total emparejamientos: {self.matched_total}, creados: {self.created_total}")

def main():
    """Función principal con detección automática de entorno"""
    if WEB_MODE:
        st.set_page_config(
            page_title="Reconocimiento Facial UNAH",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        st.title("Sistema de Reconocimiento Facial")
    
    system = FacialRecognitionSystem()
    system.run()

if __name__ == "__main__":
    main()