import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

# Título principal con un estilo diferente
st.markdown("<h1 style='text-align: center; color: #FFC0CB;'>Conversión de Texto a Audio</h1>", unsafe_allow_html=True)

# Nueva imagen
image = Image.open('nueva_imagen.png')
st.image(image, width=400)

# Sidebar para la interacción del usuario
with st.sidebar:
    st.subheader("Escribe o selecciona texto para convertirlo en audio.")
    st.info("¡Convierte tus palabras en sonido!")

# Sección de fábula
st.markdown("## Una Nueva Fábula")
st.write("""
Había una vez un ciervo que, al verse reflejado en el agua, admiró la majestuosidad de sus cuernos, pero se quejó de sus delgadas patas.
De repente, un león apareció, y el ciervo huyó a gran velocidad, pero sus cuernos se enredaron en las ramas de un árbol.
Mientras el león se acercaba, el ciervo pensó: 'Lo que admiraba me traiciona, y lo que despreciaba me salva la vida'.
""")

# Entrada de texto para el usuario
st.markdown("### ¿Quieres escucharlo? Ingresa el texto a continuación:")
text = st.text_area("Ingrese el texto que desea convertir a audio:")

# Selección del idioma
option_lang = st.selectbox("Selecciona el idioma", ("Español", "English"))
lg = 'es' if option_lang == "Español" else 'en'

# Función de conversión de texto a voz
def text_to_speech(text, lg):
    tts = gTTS(text, lang=lg)
    my_file_name = text[:20] if len(text) > 20 else "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, text

# Conversión y reproducción de audio
if st.button("Convertir a Audio"):
    if text:
        result, output_text = text_to_speech(text, lg)
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()
        st.markdown("## Tu Audio:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)

        # Botón de descarga
        with open(f"temp/{result}.mp3", "rb") as f:
            data = f.read()

        def get_binary_file_downloader_html(bin_file, file_label='File'):
            bin_str = base64.b64encode(data).decode()
            href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Descargar {file_label}</a>'
            return href

        st.markdown(get_binary_file_downloader_html("audio.mp3", file_label="Archivo de Audio"), unsafe_allow_html=True)
    else:
        st.warning("Por favor, ingrese un texto para convertir.")

# Eliminar archivos después de 7 días
def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if mp3_files:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Archivo eliminado:", f)

remove_files(7)


