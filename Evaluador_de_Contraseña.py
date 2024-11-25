import re
import streamlit as st

def evaluar_contrasena(contrasena):
    """Evalúa la fortaleza de una contraseña.

    Args:
        contrasena (str): La contraseña a evaluar.

    Returns:
        bool: True si la contraseña es fuerte, False si no lo es.
    """

    # Patrones para verificar la complejidad de la contraseña
    patron_mayuscula = r"[A-Z]"
    patron_minuscula = r"[a-z]"
    patron_numero = r"\d"
    patron_especial = r"[^\w\s]"  # Cualquier caracter que no sea alfanumérico o espacio

    # Verificar si la contraseña cumple con todos los criterios
    es_fuerte = (
        len(contrasena) >= 8 and
        re.search(patron_mayuscula, contrasena) and
        re.search(patron_minuscula, contrasena) and
        re.search(patron_numero, contrasena) and
        re.search(patron_especial, contrasena)
    )

    return es_fuerte

def app():
    st.title("Evaluador de Contraseñas")

    contrasena = st.text_input("Ingrese su contraseña")

    if st.button("Evaluar"):
        if evaluar_contrasena(contrasena):
            st.success("¡Excelente! Tu contraseña es muy segura.")
        else:
            st.error("Tu contraseña es débil. Asegúrate de incluir:")
            if not re.search(r"[A-Z]", contrasena):
                st.write("- Al menos una letra mayúscula")
            if not re.search(r"[a-z]", contrasena):
                st.write("- Al menos una letra minúscula")
            if not re.search(r"\d", contrasena):
                st.write("- Al menos un número")
            if not re.search(r"[^\w\s]", contrasena):
                st.write("- Al menos un carácter especial")

    st.write("Programado por Kevin Guio")

if __name__ == "__main__":
    app()
