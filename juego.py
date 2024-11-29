import streamlit as st
import random
import re

def generar_numero_secreto():
    """Genera un número secreto aleatorio de 4 dígitos."""
    return str(random.randint(1000, 9999))

def comparar_numero(usuario, secreto):
    """Compara el número del usuario con el número secreto y genera las pistas."""
    pista = []
    for i, digito in enumerate(usuario):
        if digito == secreto[i]:
            pista.append(f"<span style='color:green'>{digito}</span>")  # Número en la posición correcta (verde)
        elif digito in secreto:
            pista.append(f"<span style='color:yellow'>{digito}</span>")  # Número en la secuencia pero en el lugar incorrecto (amarillo)
        else:
            pista.append(f"<span>{digito}</span>")  # Número no está en la secuencia (sin color)
    return "".join(pista)

def app():
    st.title("🔢 Adivina el Número Secreto con Regex 🔢")

    # Instrucciones del juego
    st.write("""
    **Instrucciones:**
    1. Se te dará un número secreto de 4 dígitos.
    2. Tienes que adivinar el número secreto utilizando.
    3. Cada vez que intentes, el juego te dará pistas sobre el número, verde esta en la posición correcta, amarillo no esta en la posición correcta.
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

                # Comparar el intento con el número secreto y mostrar pistas interactivas
                pistas = comparar_numero(regex, st.session_state.numero_secreto)
                st.markdown(f"**Pistas:** {pistas}", unsafe_allow_html=True)

        except re.error:
            st.error("¡Expresión regular inválida! Asegúrate de escribir una expresión válida.")

    # Mostrar el número de intentos
    st.write(f"Intentos realizados: {st.session_state.intentos}")

    # Si adivinó el número, permitir reiniciar el juego
    if st.session_state.adivinada:
        if st.button("Jugar de nuevo"):
            # Restablecer las variables de estado para iniciar un nuevo juego
            st.session_state.intentos = 0
            st.session_state.numero_secreto = generar_numero_secreto()
            st.session_state.adivinada = False
            # No es necesario hacer rerun; solo se reinicia el estado del juego.

    # Créditos
    st.write("---")
    st.write("Programado por **Kevin Guio**")

if __name__ == "__main__":
    app()
