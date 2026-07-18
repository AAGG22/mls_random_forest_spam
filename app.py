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


def _svg_data_uri(svg: str) -> str:
    """Convierte un SVG en data URI para usarlo como <img> (Streamlit no filtra img)."""
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode("utf-8")).decode()


# Iconos SVG (misma marca visual que en Lactancia Materna)
ICONO_LINKEDIN = _svg_data_uri(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none">'
    '<path d="M16 8a6 6 0 016 6v7h-4v-7a2 2 0 00-2-2 2 2 0 00-2 2v7h-4v-7a6 6 0 016-6zM2 9h4v12H2V9z" '
    'stroke="#333" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"/>'
    '<path d="M4 6a2 2 0 100-4 2 2 0 000 4z" '
    'stroke="#333" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"/>'
    "</svg>"
)
ICONO_GITHUB = _svg_data_uri(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none">'
    '<path d="M15 22v-4a4.8 4.8 0 00-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5'
    ".28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 "
    "0 3.5A5.403 5.403 0 004 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23"
    '-.15 1.85v4" stroke="#333" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"/>'
    '<path d="M9 18c-4.51 2-5-2-7-2" '
    'stroke="#333" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"/>'
    "</svg>"
)
ICONO_BLUESKY = _svg_data_uri(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
    '<path fill="#1185FE" d="M12 10.8c-1.087-2.114-4.046-6.053-6.798-7.995C2.566.944 '
    "1.561 1.266.902 1.565.139 1.908 0 3.08 0 3.768c0 .69.378 5.65.624 6.479.815 2.736 "
    "3.713 3.66 6.383 3.364.136-.02.275-.039.415-.056-.138.022-.276.04-.415.056-3.912.58-"
    "7.387 2.005-2.83 7.078 5.013 5.19 6.87-1.113 7.823-4.308.953 3.195 2.05 9.271 7.733 "
    "4.308 4.267-4.308 1.172-6.498-2.74-7.078a8.741 8.741 0 0 1-.415-.056c.14.017.279.036"
    ".415.056 2.67.297 5.568-.628 6.383-3.364.246-.828.624-5.79.624-6.478 0-.69-.139-1.861"
    '-.902-2.206-.659-.298-1.664-.62-4.3 1.24C16.046 4.748 13.087 8.687 12 10.8Z"/>'
    "</svg>"
)


def _enlace_red_social(url: str, aria_label: str, icono_src: str) -> str:
    return (
        f'<a href="{url}" target="_blank" rel="noopener noreferrer" '
        f'aria-label="{aria_label}" title="{aria_label}" '
        'style="display:inline-flex;align-items:center;justify-content:center;'
        "width:40px;height:40px;border-radius:50%;border:1px solid #ccc;"
        'text-decoration:none;margin-right:10px;">'
        f'<img src="{icono_src}" width="20" height="20" alt="{aria_label}">'
        "</a>"
    )


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
            '<div style="margin-top:0.5rem;">'
            f'{_enlace_red_social(LINKEDIN_URL, "Perfil de LinkedIn", ICONO_LINKEDIN)}'
            f'{_enlace_red_social(GITHUB_URL, "Perfil de GitHub", ICONO_GITHUB)}'
            f'{_enlace_red_social(BSKY_URL, "Perfil en Bluesky", ICONO_BLUESKY)}'
            "</div>",
            unsafe_allow_html=True,
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
