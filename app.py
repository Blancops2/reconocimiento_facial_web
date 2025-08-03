import streamlit as st
import trackeo_multinucleo

def main():
    st.set_page_config(
        page_title="Reconocimiento Facial UNAH",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("Sistema de Reconocimiento Facial")
    st.markdown("---")
    
    if st.button("🎬 Iniciar Reconocimiento"):
        with st.spinner("Cargando modelo de IA..."):
            trackeo_multinucleo.main(web_mode=True)
    
    st.markdown("---")
    st.caption("Proyecto de Investigación - Facultad de Ingeniería, UNAH")

if __name__ == "__main__":
    main()