import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import multiprocessing
from PIL import Image, ImageTk
import webbrowser
import trackeo_multinucleo  # llamado al script de reconocimeinto facial

# Configuración de CustomTkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class SistemaReconocimientoFacial:
    def __init__(self):
        # Configuración de la ventana principal
        self.root = ctk.CTk()
        self.root.title("Sistema de Reconocimiento Facial - UNAH")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        
        # Datos del proyecto
        self.integrantes = [
            {
                "nombre": "Yeison Blanco",
                "correo": "yeison.blanco@unah.hn",
                "github": "https://github.com/Blancops2",
                "rol": "Especialista en IA, Ingeniero de datos"
            },
            {
                "nombre": "Juan Marcia", 
                "correo": "juan.marcia@unah.hn",
                "github": "https://github.com/JuanMarcia",
                "rol": "Especialista en IA, Ingeniero de datos"
            },
            {
                "nombre": "Eduin Chavarria",
                "correo": "erchavarria@unah.hn", 
                "github": "https://github.com/Eduin271",
                "rol": "Especialista en IA, Ingeniero de datos"
            },
            {
                "nombre": "Jose Urquia",
                "correo": "jurquia@unah.hn",
                "github": "https://github.com/RobertoUrquia", 
                "rol": "Especialista en IA, Ingeniero de datos"
            }
        ]
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Frame principal con scroll
        self.main_frame = ctk.CTkScrollableFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        self.crear_header()
        
        # Título principal
        self.crear_titulo_principal()
        
        # Descripción del proyecto
        self.crear_descripcion_proyecto()
        
        # Proceso del sistema
        self.crear_proceso_sistema()
        
        # Frame para docente e integrantes
        self.crear_seccion_equipo()
        
        # Información institucional
        self.crear_info_institucional()
        
        # Botón de inicio
        self.crear_boton_inicio()
    
    def crear_header(self):
        header_frame = ctk.CTkFrame(self.main_frame, height=80)
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Logo y título UNAH
        logo_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        logo_frame.pack(side="left", padx=20, pady=15)
        
        ctk.CTkLabel(logo_frame, text="🏛️", font=("Arial", 30)).pack(side="left", padx=(0, 10))
        
        info_frame = ctk.CTkFrame(logo_frame, fg_color="transparent")
        info_frame.pack(side="left")
        
        ctk.CTkLabel(info_frame, text="UNAH", font=("Arial", 20, "bold")).pack(anchor="w")
        ctk.CTkLabel(info_frame, text="Universidad Nacional Autónoma de Honduras", 
                    font=("Arial", 12), text_color="gray").pack(anchor="w")
        
        # Badge
        badge = ctk.CTkLabel(header_frame, text="Proyecto de Investigación", 
                           font=("Arial", 12), fg_color="#E3F2FD", text_color="#1976D2",
                           corner_radius=15)
        badge.pack(side="right", padx=20, pady=25)
    
    def crear_titulo_principal(self):
        titulo_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        titulo_frame.pack(fill="x", pady=(0, 30))
        
        ctk.CTkLabel(titulo_frame, text="Sistema de Reconocimiento Facial", 
                    font=("Arial", 32, "bold")).pack()
        
        ctk.CTkLabel(titulo_frame, 
                    text="Tecnología avanzada de inteligencia artificial para detección y reconocimiento facial\nen tiempo real con procesamiento paralelo optimizado",
                    font=("Arial", 16), text_color="gray", justify="center").pack(pady=(10, 0))
    
    def crear_descripcion_proyecto(self):
        desc_frame = ctk.CTkFrame(self.main_frame)
        desc_frame.pack(fill="x", pady=(0, 20))
        
        # Título de la sección
        titulo_frame = ctk.CTkFrame(desc_frame, fg_color="transparent")
        titulo_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(titulo_frame, text="👁️", font=("Arial", 20)).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(titulo_frame, text="Descripción del Proyecto", 
                    font=("Arial", 18, "bold")).pack(side="left")
        
        # Contenido
        desc_text = """Este sistema detecta y reconoce rostros en tiempo real usando una base de datos biométrica, trackers y procesamiento paralelo para un rendimiento optimizado. Ideal para entornos educativos o de control de acceso, implementa algoritmos de machine learning avanzados para garantizar precisión y velocidad en la identificación facial."""
        
        ctk.CTkLabel(desc_frame, text=desc_text, font=("Arial", 14), 
                    wraplength=1100, justify="left").pack(padx=20, pady=(0, 20))
    
    def crear_proceso_sistema(self):
        proceso_frame = ctk.CTkFrame(self.main_frame)
        proceso_frame.pack(fill="x", pady=(0, 20))
        
        # Título
        titulo_frame = ctk.CTkFrame(proceso_frame, fg_color="transparent")
        titulo_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(titulo_frame, text="⚙️", font=("Arial", 20)).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(titulo_frame, text="Proceso del Sistema", 
                    font=("Arial", 18, "bold")).pack(side="left")
        
        # Grid de procesos
        grid_frame = ctk.CTkFrame(proceso_frame, fg_color="transparent")
        grid_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        procesos = [
            ("💾", "Captura", "Adquisición de imágenes\nen tiempo real", "#E3F2FD"),
            ("👁️", "Detección", "Identificación de rostros\nen la imagen", "#E8F5E8"),
            ("⚡", "Procesamiento", "Análisis biométrico\nmultinúcleo", "#F3E5F5"),
            ("👥", "Reconocimiento", "Identificación y\nverificación", "#FFF3E0")
        ]
        
        for i, (icono, titulo, desc, color) in enumerate(procesos):
            col = i % 4
            proceso_card = ctk.CTkFrame(grid_frame, fg_color=color, width=250, height=120)
            proceso_card.grid(row=0, column=col, padx=10, pady=10, sticky="ew")
            proceso_card.pack_propagate(False)
            
            ctk.CTkLabel(proceso_card, text=icono, font=("Arial", 24)).pack(pady=(15, 5))
            ctk.CTkLabel(proceso_card, text=titulo, font=("Arial", 14, "bold")).pack()
            ctk.CTkLabel(proceso_card, text=desc, font=("Arial", 11), 
                        text_color="gray", justify="center").pack(pady=(5, 0))
        
        # Configurar grid weights
        for i in range(4):
            grid_frame.grid_columnconfigure(i, weight=1)
    
    def crear_seccion_equipo(self):
        equipo_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        equipo_frame.pack(fill="x", pady=(0, 20))
        
        # Frame para docente (izquierda)
        docente_frame = ctk.CTkFrame(equipo_frame, width=350)
        docente_frame.pack(side="left", fill="y", padx=(0, 10))
        docente_frame.pack_propagate(False)
        
        # Título docente
        titulo_docente = ctk.CTkFrame(docente_frame, fg_color="transparent")
        titulo_docente.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(titulo_docente, text="🎓", font=("Arial", 20)).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(titulo_docente, text="Docente", 
                    font=("Arial", 16, "bold")).pack(side="left")
        
        # Info docente
        ctk.CTkLabel(docente_frame, text="👨‍🏫", font=("Arial", 48)).pack(pady=(10, 10))
        ctk.CTkLabel(docente_frame, text="Dra. Asalia Zavala", 
                    font=("Arial", 16, "bold")).pack()
        ctk.CTkLabel(docente_frame, text="Catedrático de Inteligencia Artificial", 
                    font=("Arial", 12), text_color="gray").pack(pady=(5, 0))
        ctk.CTkLabel(docente_frame, text="Facultad de Ingeniería", 
                    font=("Arial", 11), text_color="gray").pack()
        
        
        # Frame para integrantes (derecha)
        integrantes_frame = ctk.CTkFrame(equipo_frame)
        integrantes_frame.pack(side="right", fill="both", expand=True)
        
        # Título integrantes
        titulo_integrantes = ctk.CTkFrame(integrantes_frame, fg_color="transparent")
        titulo_integrantes.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(titulo_integrantes, text="👥", font=("Arial", 20)).pack(side="left", padx=(0, 10))
        info_integrantes = ctk.CTkFrame(titulo_integrantes, fg_color="transparent")
        info_integrantes.pack(side="left")
        
        ctk.CTkLabel(info_integrantes, text="Equipo de Desarrollo", 
                    font=("Arial", 16, "bold")).pack(anchor="w")
        ctk.CTkLabel(info_integrantes, text="Estudiantes de Ingeniería en Sistemas", 
                    font=("Arial", 12), text_color="gray").pack(anchor="w")
        
        # Grid de integrantes
        grid_integrantes = ctk.CTkFrame(integrantes_frame, fg_color="transparent")
        grid_integrantes.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        for i, integrante in enumerate(self.integrantes):
            row = i // 2
            col = i % 2
            
            card = ctk.CTkFrame(grid_integrantes, fg_color="#F8F9FA")
            card.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
            
            # Header del card
            header_card = ctk.CTkFrame(card, fg_color="transparent")
            header_card.pack(fill="x", padx=15, pady=(15, 5))
            
            info_left = ctk.CTkFrame(header_card, fg_color="transparent")
            info_left.pack(side="left", fill="x", expand=True)
            
            ctk.CTkLabel(info_left, text=integrante["nombre"], 
                        font=("Arial", 14, "bold")).pack(anchor="w")
            ctk.CTkLabel(info_left, text=integrante["rol"], 
                        font=("Arial", 11), text_color="#1976D2").pack(anchor="w")
            
            # Avatar
            iniciales = "".join([n[0] for n in integrante["nombre"].split()])
            ctk.CTkLabel(header_card, text=iniciales, font=("Arial", 12, "bold"),
                        fg_color="#E3F2FD", text_color="#1976D2", 
                        width=40, height=40, corner_radius=20).pack(side="right")
            
            # Contacto
            contacto_frame = ctk.CTkFrame(card, fg_color="transparent")
            contacto_frame.pack(fill="x", padx=15, pady=(0, 15))
            
            # Email
            email_frame = ctk.CTkFrame(contacto_frame, fg_color="transparent")
            email_frame.pack(fill="x", pady=2)
            ctk.CTkLabel(email_frame, text="📧", font=("Arial", 12)).pack(side="left", padx=(0, 5))
            email_btn = ctk.CTkButton(email_frame, text=integrante["correo"], 
                                    font=("Arial", 10), height=20, fg_color="transparent",
                                    text_color="#666", hover_color="#F0F0F0",
                                    command=lambda e=integrante["correo"]: self.abrir_email(e))
            email_btn.pack(side="left")
            
            # GitHub
            github_frame = ctk.CTkFrame(contacto_frame, fg_color="transparent")
            github_frame.pack(fill="x", pady=2)
            ctk.CTkLabel(github_frame, text="🔗", font=("Arial", 12)).pack(side="left", padx=(0, 5))
            github_btn = ctk.CTkButton(github_frame, text="GitHub Profile", 
                                     font=("Arial", 10), height=20, fg_color="transparent",
                                     text_color="#666", hover_color="#F0F0F0",
                                     command=lambda g=integrante["github"]: self.abrir_github(g))
            github_btn.pack(side="left")
        
        # Configurar grid weights
        for i in range(2):
            grid_integrantes.grid_columnconfigure(i, weight=1)
    
    def crear_info_institucional(self):
        info_frame = ctk.CTkFrame(self.main_frame)
        info_frame.pack(fill="x", pady=(0, 20))
        
        # Título
        titulo_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        titulo_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(titulo_frame, text="🏛️", font=("Arial", 20)).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(titulo_frame, text="Información Institucional", 
                    font=("Arial", 18, "bold")).pack(side="left")
        
        # Contenido
        contenido_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        contenido_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Logo grande
        ctk.CTkLabel(contenido_frame, text="🏛️", font=("Arial", 60), 
                    fg_color="#1976D2", text_color="white", 
                    width=80, height=80, corner_radius=15).pack(side="left", padx=(0, 20))
        
        # Info texto
        info_texto = ctk.CTkFrame(contenido_frame, fg_color="transparent")
        info_texto.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(info_texto, text="Universidad Nacional Autónoma de Honduras", 
                    font=("Arial", 18, "bold")).pack(anchor="w")
        ctk.CTkLabel(info_texto, text="Facultad de Ingeniería - Carrera de Ingeniería en Sistemas", 
                    font=("Arial", 14), text_color="gray").pack(anchor="w", pady=(5, 10))
        
        # Badges
        badges_frame = ctk.CTkFrame(info_texto, fg_color="transparent")
        badges_frame.pack(anchor="w")
        
        badges = ["Investigación", "Inteligencia Artificial", "Visión Computacional", "Machine Learning"]
        for badge_text in badges:
            ctk.CTkLabel(badges_frame, text=badge_text, font=("Arial", 10),
                        fg_color="#F5F5F5", text_color="#666", corner_radius=10).pack(side="left", padx=(0, 5))
    
    def crear_boton_inicio(self):
        boton_frame = ctk.CTkFrame(self.main_frame, fg_color="#1976D2", corner_radius=15)
        boton_frame.pack(pady=30)
        
        ctk.CTkLabel(boton_frame, text="¿Listo para comenzar?", 
                    font=("Arial", 18, "bold"), text_color="white").pack(pady=(20, 10))
        
        self.boton_iniciar = ctk.CTkButton(boton_frame, text="▶️ Iniciar Reconocimiento Facial",
                                          font=("Arial", 14, "bold"), height=50, width=300,
                                          fg_color="white", text_color="#1976D2",
                                          hover_color="#F0F0F0",
                                          command=self.iniciar_sistema)
        self.boton_iniciar.pack(pady=(0, 20))
    
    def iniciar_sistema(self):
        respuesta = messagebox.askyesno("Confirmación", 
                                    "¿Deseas iniciar el reconocimiento facial?")
        if respuesta:
            self.boton_iniciar.configure(text="🔄 Iniciando Sistema...", state="disabled")
            self.root.update()
        
            # Lanza el proceso de reconocimiento facial
            self.proceso = multiprocessing.Process(target=trackeo_multinucleo.main)
            self.proceso.start()
            
            # Simulación para demo
            self.root.after(2000, self.sistema_iniciado)
    
    def sistema_iniciado(self):
        self.boton_iniciar.configure(text="▶️ Iniciar Reconocimiento Facial", state="normal")
    
    def abrir_email(self, email):
        webbrowser.open(f"mailto:{email}")
    
    def abrir_github(self, github_url):
        webbrowser.open(github_url)
    
    def ejecutar(self):
        self.root.mainloop()

if __name__ == "__main__":
    multiprocessing.freeze_support()
    app = SistemaReconocimientoFacial()
    app.ejecutar()
