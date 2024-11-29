import streamlit as st
import random
import re

# Lista de palabras
palabras = ["manzana", "jirafa", "elefante", "computadora", "flor", "abogado", "construccion"]

# Generar el desafío de regex
def generar_desafio():
    palabra = random.choice(palabras)
    letra_oculta = random.choice(palabra)
    
    # Crear un patrón de la palabra con la letra oculta representada por "_"
    patron_oculto = "".join([letra if letra == letra_oculta else "_" for letra in palabra])
    
    # Desafío: adivinar la letra oculta
    return patron_oculto, letra_oculta, palabra

def app():
    st.title("🎉 Adivina la Letra Oculta con Regex 🎉")
    
    # Instrucciones del juego
    st.write("""
    **Instrucciones:**
    1. Elige una palabra aleatoria que está parcialmente oculta.
    2. El objetivo es adivinar la letra oculta en la palabra utilizando expresiones regulares (regex).
    3. Escribe una expresión regular que coincida con la letra oculta de la palabra.
    4. Si adivinas correctamente, se te notificará y podrás seguir con un nuevo desafío.
    5. Cada intento cuenta, ¡así que asegúrate de probar diferentes expresiones regulares!
    
    ¡Buena suerte y diviértete aprendiendo Regex!
    """)

    # Inicializar estado del juego
    if 'intentos' not in st.session_state:
        st.session_state.intentos = 0
        st.session_state.patron, st.session_state.letra_oculta, st.session_state.palabra = generar_desafio()
        st.session_state.adivinada = False
    
    # Mostrar patrón oculto
    st.write(f"Patrón de palabra: {st.session_state.patron}")
    
    # Entrada del usuario para regex
    regex = st.text_input("Escribe una expresión regular para adivinar la letra oculta:")
    
    # Verificar el regex
    if st.button("Comprobar Regex"):
        st.session_state.intentos += 1
        try:
            # Intentamos hacer coincidir el regex con la letra oculta
            if re.match(regex, st.session_state.letra_oculta):
                st.success(f"¡Bien hecho! La letra '{st.session_state.letra_oculta}' es correcta.")
                st.session_state.adivinada = True
            else:
                st.warning("¡No es la letra correcta! Intenta de nuevo.")
        
        except re.error:
            st.error("¡Expresión regular inválida!")
    
    # Mostrar número de intentos
    st.write(f"Intentos: {st.session_state.intentos}")
    
    # Botón para iniciar un nuevo desafío
    if st.button("Nuevo desafío"):
        st.session_state.patron, st.session_state.letra_oculta, st.session_state.palabra = generar_desafio()
        st.session_state.intentos = 0
        st.session_state.adivinada = False
        st.experimental_rerun()

    # Mostrar la palabra completa al final del juego
    if st.session_state.adivinada:
        st.write(f"¡Has adivinado la letra oculta! La palabra completa es: {st.session_state.palabra}")
    
    # Crédito final
    st.write("Esta app fue creada por **Kevin Guio**")

if __name__ == "__main__":
    app()
