import re
import streamlit as st

def evaluar_contraseña(contraseña):
    """Evalúa la fortaleza de una contraseña y proporciona sugerencias.

    Args:
        contraseña (str): La contraseña a evaluar.

    Returns:
        bool: True si la contraseña es fuerte, False si no lo es.
    """

    # Patrones para validar los requisitos de la contraseña
    patron_mayusculas = re.compile(r'[A-Z]')
    patron_minusculas = re.compile(r'[a-z]')
    patron_numeros = re.compile(r'\d')
    patron_especiales = re.compile(r'[^\w\s]')

    # Validar la longitud y los caracteres requeridos
    es_fuerte = (
        len(contraseña) >= 8 and
        patron_mayusculas.search(contraseña) and
        patron_minusculas.search(contraseña) and
        patron_numeros.search(contraseña) and
        patron_especiales.search(contraseña)
    )

    return es_fuerte

# Interfaz de usuario con Streamlit
st.title("Evaluador de Contraseñas")

contraseña = st.text_input("Ingrese su contraseña:")

if contraseña:
    es_fuerte = evaluar_contraseña(contraseña)
    if es_fuerte:
        st.success("¡La contraseña es fuerte!")
    else:
        st.error("La contraseña no es lo suficientemente fuerte.")
        if not re.search(r'[A-Z]', contraseña):
            st.warning("La contraseña debe contener al menos una mayúscula.")
        if not re.search(r'[a-z]', contraseña):
            st.warning("La contraseña debe contener al menos una minúscula.")
        if not re.search(r'\d', contraseña):
            st.warning("La contraseña debe contener al menos un número.")
        if not re.search(r'[^\w\s]', contraseña):
            st.warning("La contraseña debe contener al menos un caracter especial.")

st.write("Programado por Kevin Guio")
