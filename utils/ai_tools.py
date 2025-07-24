import os
import pytesseract
from PIL import Image
from openai import OpenAI
from dotenv import load_dotenv
from pytesseract import TesseractNotFoundError

# Forzar ruta en Windows
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

load_dotenv()
client = OpenAI()

def extraer_texto_empaque(imagen_path):
    try:
        imagen = Image.open(imagen_path)
        texto = pytesseract.image_to_string(imagen, lang='eng+spa')
        return texto.strip()
    except TesseractNotFoundError:
        return (
            "ERROR: Tesseract no está instalado o no se encuentra en la ruta configurada. "
            "Descárgalo desde https://github.com/UB-Mannheim/tesseract/wiki"
        )
    except Exception as e:
        return f"ERROR inesperado durante OCR: {e}"

def generar_descripcion(desde_ocr, nombre_producto):
    prompt = f"""Eres un redactor creativo de snacks saludables para jóvenes.
Usa esta información real extraída del empaque para redactar una descripción promocional profesional y atractiva.

🟢 {nombre_producto}
✨ ¡Crunchy, sabroso y natural!

Información del empaque: {desde_ocr}

Escribe una descripción clara del producto resaltando beneficios, sabor, ingredientes clave, ocasión de consumo y textura. 
Termina con una frase estilo '¡{nombre_producto}, el placer saludable que sí cruje!'."""
    respuesta = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return respuesta.choices[0].message.content.strip()

def generar_campania(descripcion, imagen_path):
    nombre_producto = os.path.splitext(os.path.basename(imagen_path))[0]
    prompt = (
        f"Campaña visual para un snack saludable llamado '{nombre_producto}'. "
        f"Descripción: {descripcion[:200]}. "
        f"Estilo moderno, amigable, con colores vivos, fondo naranja o blanco, tipografía juvenil. "
        f"Debe parecer una imagen promocional para redes sociales dirigida a jóvenes."
    )
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        n=1
    )
    return response.data[0].url

def buscar_info_rag(consulta, producto):
    try:
        ruta_txt = os.path.join("rag_docs", f"{producto}.txt")
        with open(ruta_txt, "r", encoding="utf-8") as f:
            contenido = f.read()
    except FileNotFoundError:
        return "No encontré información para este producto."

    prompt = (
        f"Responde la siguiente pregunta sobre el producto '{producto}' usando únicamente esta información:\n\n"
        f"==== CONTENIDO DEL PRODUCTO ====\n"
        f"{contenido}\n"
        f"================================\n\n"
        f"Pregunta: {consulta}\n\n"
        f"Si no encuentras la información en el texto, responde de manera amable que no está disponible."
    )
    try:
        respuesta = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        return respuesta.choices[0].message.content.strip()
    except Exception as e:
        return f"Error al generar respuesta: {e}"