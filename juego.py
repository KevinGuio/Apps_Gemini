import streamlit as st
import random
import re

def generar_numero_secreto():
    """Genera un número secreto aleatorio de 4 dígitos."""
    return str(random.randint(1000, 9999))

def app():
    st.title("🔢 Adivina el Número Secreto con Regex 🔢")

    # Instrucciones del juego
    st.write("""
    **Instrucciones:**
    1. Se te dará un número secreto de 4 dígitos.
    2. Tienes que adivinar el número secreto utilizando expresiones regulares.
    3. Cada vez que intentes, el juego te dará pistas sobre el número.
    4. Si el número que introduces es correcto, ganarás el juego.
    
    ¡Buena suerte!
    """)

    # Inicializar el juego
    if 'intentos' not in st.session_state:
        st.session_state.intentos = 0
        st.session_state.numero_secreto = generar_numero_secreto()
        st.session_state.adivinada = False

    # Solicitar el patrón regex
    regex = st.text_input("Escribe una expresión regular para adivinar el número secreto:")

    # Botón para comprobar el regex
    if st.button("Comprobar Regex"):
        st.session_state.intentos += 1

        # Verificar si el patrón coincide con el número secreto
        try:
            if re.match(regex, st.session_state.numero_secreto):
                st.success(f"🎉 ¡Correcto! El número secreto es {st.session_state.numero_secreto}.")
                st.session_state.adivinada = True
            else:
                st.warning(f"No es correcto. Intenta con otro patrón. Intentos: {st.session_state.intentos}")
                
                # Dar pistas basadas en la longitud o el valor del número
                if len(regex) > len(st.session_state.numero_secreto):
                    st.write("Pista: El número es más corto que tu intento.")
                elif len(regex) < len(st.session_state.numero_secreto):
                    st.write("Pista: El número es más largo que tu intento.")
                
                # Pistas adicionales para hacer el juego más fácil
                if st.session_state.numero_secreto[0] == regex[0]:
                    st.write("Pista: El primer dígito del número es correcto.")
                if st.session_state.numero_secreto[-1] == regex[-1]:
                    st.write("Pista: El último dígito del número es correcto.")
                if regex.count(r"\d") == 4:
                    st.write("Pista: Estás buscando un número de 4 dígitos.")
                
        except re.error:
            st.error("¡Expresión regular inválida! Asegúrate de escribir una expresión válida.")

    # Mostrar el número de intentos
    st.write(f"Intentos realizados: {st.session_state.intentos}")

    # Si adivinó el número, permitir reiniciar el juego
    if st.session_state.adivinada:
        if st.button("Jugar de nuevo"):
            st.session_state.intentos = 0
            st.session_state.numero_secreto = generar_numero_secreto()
            st.session_state.adivinada = False
            st.experimental_rerun()

    # Créditos
    st.write("---")
    st.write("Programado por **Kevin Guio**")

if __name__ == "__main__":
    app()
