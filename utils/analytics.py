import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def mostrar_analisis_feedback(nombre_producto):
    path = f"feedback/{nombre_producto}.csv"
    if not os.path.exists(path):
        st.warning("No se encontró feedback.")
        return
    try:
        df = pd.read_csv(path, encoding="utf-8-sig")
    except Exception as e:
        st.error(f"Error al leer CSV: {e}")
        return

    st.write(df.head())

    if "sentimiento" in df.columns:
        st.write("📈 Distribución de Sentimientos")
        fig, ax = plt.subplots()
        sns.countplot(data=df, x="sentimiento", ax=ax)
        st.pyplot(fig)