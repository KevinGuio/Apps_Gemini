import streamlit as st
import random
import re

def generar_numero_secreto():
    """Genera un número secreto aleatorio de 4 dígitos."""
    return str(random.randint(1000, 9999))

def comparar_numero(usuario, secreto):
    """Compara el número del usuario con el número secreto y genera las pistas."""
    pista = [""] * len(usuario)  # Inicializamos la lista con valores vacíos para cada dígito del número
    usado_secreto = [False] * len(secreto)  # Para marcar qué dígitos ya han sido usados en el número secreto
    usuario_usado = [False] * len(usuario)  # Para marcar qué dígitos del intento del usuario ya han sido verificados

    # Primero, se marca con verde los dígitos en la posición correcta
    for i, digito in enumerate(usuario):
        if digito == secreto[i]:
            pista[i] = f"<span style='color:green'>{digito}</span>"  # Número en la posición correcta (verde)
            usado_secreto[i] = True  # Marcamos el dígito como usado
            usuario_usado[i] = True  # Marcamos el dígito como verificado

    # Luego, se marca con amarillo los números que están en la secuencia pero en la posición incorrecta
    for i, digito in enumerate(usuario):
        if digito != secreto[i] and digito in secreto:
            # Asegurarse de que el dígito no se haya marcado como usado anteriormente
            for j in range(len(secreto)):
                if digito == secreto[j] and not usado_secreto[j] and not usuario_usado[i]:
                    pista[i] = f"<span style='color:yellow'>{digito}</span>"  # Número en la secuencia pero en lugar incorrecto (amarillo)
                    usado_secreto[j] = True  # Marcamos ese dígito como usado
                    usuario_usado[i] = True  # Marcamos el dígito del usuario como verificado
                    break

    # Finalmente, los números que no están en la secuencia no se colorean (gris)
    for i, digito in enumerate(usuario):
        if pista[i] == "":  # Si no se ha asignado color, significa que el dígito no está ni en el lugar correcto ni en la secuencia
            pista[i] = f"<span style='color:gray'>{digito}</span>"  # Número no está en la secuencia (gris)

    return "".join(pista)

def app():
    st.title("🔢 Adivina el Número Secreto con Regex 🔢")

    # Instrucciones del juego
    st.write("""
    **Instrucciones:**
    1. Se te dará un número secreto de 4 dígitos que debes adivinar.
    2. Cada vez que intentes, el juego te dará pistas sobre el número.
    3. Verde indica que el número está en la posición correcta, amarillo indica que el número está en la secuencia pero no en la posición correcta, y gris indica que el número no está en la secuencia.
    4. Si el número que introduces es correcto, ganarás el juego.
    5. Puedes volver a jugar despues de haber ganado dandole al boton "Jugar de nuevo".
    
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

        # Verificar que el intento sea exactamente un número de 4 dígitos
        if len(regex) != 4 or not regex.isdigit():
            st.error("¡Debes ingresar un número de 4 dígitos!")
        else:
            # Verificar si el número ingresado es correcto
            if regex == st.session_state.numero_secreto:
                st.success(f"🎉 ¡Correcto! El número secreto es {st.session_state.numero_secreto}.")
                st.session_state.adivinada = True
            else:
                st.warning(f"No es correcto. Intenta con otro patrón. Intentos: {st.session_state.intentos}")

                # Comparar el intento con el número secreto y mostrar pistas interactivas
                pistas = comparar_numero(regex, st.session_state.numero_secreto)
                st.markdown(f"**Pistas:** {pistas}", unsafe_allow_html=True)

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
