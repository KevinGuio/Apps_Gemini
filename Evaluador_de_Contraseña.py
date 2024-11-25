import streamlit as st
import re

def evaluar_contrasena(contrasena):
    """Evalúa la fortaleza de una contraseña y proporciona sugerencias.

    Args:
        contrasena (str): La contraseña a evaluar.

    Returns:
        dict: Un diccionario con los criterios evaluados (True/False).
    """

    # Patrones para cada criterio
    tiene_mayusculas = re.search(r"[A-Z]", contrasena)
    tiene_minusculas = re.search(r"[a-z]", contrasena)
    tiene_numeros = re.search(r"\d", contrasena)
    tiene_especiales = re.search(r"[^\w\s]", contrasena)
    longitud_suficiente = len(contrasena) >= 8

    # Crear diccionario con resultados
    resultados = {
        "Mayúsculas": tiene_mayusculas,
        "Minúsculas": tiene_minusculas,
        "Números": tiene_numeros,
        "Caracteres especiales": tiene_especiales,
        "Longitud suficiente": longitud_suficiente
    }
    return resultados

def mostrar_resultados(resultados):
    """Muestra los resultados de la evaluación en una interfaz amigable."""

    for criterio, cumple in resultados.items():
        if cumple:
            st.success(f"✅ Cumple con el criterio: {criterio}")
        else:
            st.error(f"❌ No cumple con el criterio: {criterio}")

st.title("Evaluador de Contraseñas")

# Input de contraseña (oculto)
with st.form("my_form"):
    contrasena = st.text_input("Ingrese su contraseña", type="password")
    submitted = st.form_submit_button("Evaluar")

# Mostrar resultados si se ha enviado el formulario
if submitted:
    resultados = evaluar_contrasena(contrasena)
    mostrar_resultados(resultados)

# Mostrar botón para mostrar/ocultar la contraseña
if contrasena:
    if st.button("Mostrar Contraseña"):
        st.text(contrasena)

st.write("Programado por Kevin Guio")
