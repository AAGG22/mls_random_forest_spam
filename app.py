import streamlit as st
import joblib
import base64
from pathlib import Path

# 1. Configuración de la interfaz visual de la pestaña
st.set_page_config(page_title="Filtro Anti-Spam IA", page_icon="🛡️")
st.title("🛡️ Filtro Anti-Spam Inteligente")
st.write("Copia y pega el contenido de cualquier correo para analizarlo con Inteligencia Artificial (NLP).")
st.write("Algoritmo Random Forest: Bosque Aleatorio (muchos árboles de decisión juntos)")

PERFIL_IMG = Path(__file__).parent / "images" / "profile" / "developer3.jpg"
LINKEDIN_URL = "https://www.linkedin.com/in/adgalvan/"
GITHUB_URL = "https://github.com/AAGG22"
BSKY_URL = "https://bsky.app/profile/adgalvan.bsky.social"


@st.dialog("Perfil del desarrollador")
def mostrar_perfil_desarrollador():
    col_foto, col_info = st.columns([1, 2], vertical_alignment="center")
    with col_foto:
        if PERFIL_IMG.exists():
            b64 = base64.b64encode(PERFIL_IMG.read_bytes()).decode()
            st.markdown(
                f'<img src="data:image/jpeg;base64,{b64}" '
                'style="width:112px;height:112px;border-radius:50%;'
                'object-fit:cover;border:2px solid #ddd;display:block;margin:auto;" '
                'alt="Foto de perfil">',
                unsafe_allow_html=True,
            )
        else:
            st.info("Sin foto")
    with col_info:
        st.markdown("### Alfredo David Galván")
        st.caption("Desarrollador Web [ UNSL ]")
        st.markdown("[📧 alfredodgalvan@gmail.com](mailto:alfredodgalvan@gmail.com)")
        st.markdown(
            f"[LinkedIn]({LINKEDIN_URL}) · "
            f"[GitHub]({GITHUB_URL}) · "
            f"[Bluesky]({BSKY_URL})"
        )


# Nombre clickeable → abre la misma ventana de info que en Lactancia Materna
autor_cols = st.columns([1.4, 6], vertical_alignment="center")
with autor_cols[0]:
    if st.button("**Alfredo Galván**", type="tertiary", help="Ver perfil del desarrollador"):
        mostrar_perfil_desarrollador()
with autor_cols[1]:
    st.markdown("(TUW-UNSL)")


# 2. Función optimizada para abrir los archivos joblib (cargar el modelo en el futuro)
@st.cache_resource  # Hace que el modelo se cargue una sola vez en memoria
def cargar_componentes_ia():
    try:
        modelo = joblib.load('modelo_spam.joblib')
        vectorizador = joblib.load('vectorizador.joblib')
        return modelo, vectorizador
    except FileNotFoundError:
        return None, None

modelo, vectorizador = cargar_componentes_ia()

# 3. Validar si los archivos existen antes de continuar
if modelo is None or vectorizador is None:
    st.error("❌ No se encontraron los archivos 'modelo_spam.joblib' o 'vectorizador.joblib'.")
    st.info("💡 Por favor, ejecuta primero el script 'entrenar.py' en tu computadora para generarlos.")
else:
    # 4. Cuadro de texto para que el usuario interactúe con la App
    texto_usuario = st.text_area("Texto del correo electrónico:", height=200, 
                                 placeholder="Escribe o pega el correo aquí...")

    # Botón de acción para ejecutar el análisis
    if st.button("Verificar Correo"):
        if texto_usuario.strip() == "":
            st.warning("⚠️ Por favor, ingresa algún texto para poder analizarlo.")
        else:
            # 5. Traducir el nuevo texto a números usando el diccionario guardado
            texto_num = vectorizador.transform([texto_usuario])
            
            # 6. El algoritmo deduce si es spam (1) o legítimo (0)
            prediccion = modelo.predict(texto_num)

            # 7. Mostrar alertas visuales según el resultado
            st.markdown("### Veredicto del algoritmo:")
            if prediccion[0] == 1:
                st.error("🚨 **¡Alerta! Este correo fue clasificado como SPAM.**")
            else:
                st.success("✅ **Seguro. Este correo parece legítimo.**")
