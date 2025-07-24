import streamlit as st
import os
from PIL import Image
from utils.ai_tools import extraer_texto_empaque, generar_descripcion, generar_campania, buscar_info_rag
from utils.analytics import mostrar_analisis_feedback

st.set_page_config(page_title="Snacks saludables", layout="wide")

# Sidebar con estilo personalizado
with st.sidebar:
    st.markdown(
        "<div style='background-color:#C62828;padding:15px;border-radius:8px'>"
        "<h3 style='color:white;text-align:center;'>Selecciona el producto</h3>"
        "</div>",
        unsafe_allow_html=True
    )

# Cargar productos
carpeta_img = "imagenes_snacks"
imagenes = sorted([f for f in os.listdir(carpeta_img) if f.endswith(('.png', '.jpg'))])
productos = [os.path.splitext(img)[0] for img in imagenes]
selected = st.sidebar.selectbox("", productos)

# Mostrar producto
if selected:
    nombre_pretty = selected
    img_path = os.path.join(carpeta_img, f"{selected}.png")

    st.title("Snacks saludables")
    st.header(f"{nombre_pretty}")
    st.image(Image.open(img_path), caption=nombre_pretty, width=400)

    if st.button("Generar descripción"):
        ocr_text = extraer_texto_empaque(img_path)
        if ocr_text.startswith("ERROR:"):
            st.error(ocr_text)
        else:
            descripcion = generar_descripcion(ocr_text, nombre_pretty)
            st.markdown("<div style='background-color:#C62828;padding:10px'><h4 style='color:white'>Generar descripción</h4></div>", unsafe_allow_html=True)
            st.write(descripcion)
            st.session_state["descripcion_generada"] = descripcion
            st.session_state["img_path"] = img_path

    if st.button("Generar imagen promocional"):
        if "descripcion_generada" not in st.session_state:
            st.warning("Primero genera una descripción")
        else:
            url = generar_campania(st.session_state["descripcion_generada"], st.session_state["img_path"])
            st.markdown("<div style='background-color:#C62828;padding:10px'><h4 style='color:white'>Generar imagen promocional</h4></div>", unsafe_allow_html=True)
            st.image(url, caption="Imagen Promocional Generada", use_container_width=True)

    st.markdown("<div style='background-color:#C62828;padding:10px'><h4 style='color:white'>Análisis de comentarios</h4></div>", unsafe_allow_html=True)
    mostrar_analisis_feedback(selected)

    st.markdown("<div style='background-color:#C62828;padding:10px'><h4 style='color:white'>Pregunta sobre el producto</h4></div>", unsafe_allow_html=True)
    consulta = st.text_input("¿Qué quieres saber?")
    if consulta:
        resultado = buscar_info_rag(consulta, selected)
        st.write(resultado)