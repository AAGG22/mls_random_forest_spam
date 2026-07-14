import streamlit as st
import joblib

# 1. Configuración de la interfaz visual de la pestaña
st.set_page_config(page_title="Filtro Anti-Spam IA", page_icon="🛡️")
st.title("🛡️ Filtro Anti-Spam Inteligente")
st.write("Copia y pega el contenido de cualquier correo para analizarlo con Inteligencia Artificial (NLP).")
st.write("Algoritmo Random Forest: Bosque Aleatorio (muchos árboles de decisión juntos)")
st.write("**Alfredo Galván** (TUW-UNSL)")


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
