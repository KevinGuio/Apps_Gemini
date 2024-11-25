import re
import streamlit as st

# Funciones de validación
def validar_nombre(nombre: str) -> str:
    """
    Valida si el nombre ingresado es válido.

    Un nombre válido solo contiene caracteres alfabéticos y 
    comienza con una letra mayúscula.

    Args:
        nombre (str): El nombre ingresado por el usuario.

    Returns:
        str: Mensaje indicando si el nombre es válido o no.

    Example:
        >>> validar_nombre("Juan")
        'Nombre válido'
    """
    patron = r"^[A-Z][a-zA-Z]*$"
    if re.fullmatch(patron, nombre):
        return "Nombre válido"
    return "El nombre debe iniciar con mayúscula y contener solo letras."


def validar_correo(correo: str) -> str:
    """
    Valida si la dirección de correo ingresada es válida.

    Args:
        correo (str): El correo ingresado por el usuario.

    Returns:
        str: Mensaje indicando si el correo es válido o no.

    Example:
        >>> validar_correo("test@example.com")
        'Correo electrónico válido'
    """
    patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if re.fullmatch(patron, correo):
        return "Correo electrónico válido"
    return "El correo debe ser en formato usuario@dominio.com."


def validar_telefono(telefono: str) -> str:
    """
    Valida si el número de teléfono ingresado es válido.

    Args:
        telefono (str): El número de teléfono ingresado por el usuario.

    Returns:
        str: Mensaje indicando si el teléfono es válido o no.

    Example:
        >>> validar_telefono("+573001234567")
        'Número de teléfono válido'
    """
    patron = r"^\+?\d{10,15}$"
    if re.fullmatch(patron, telefono):
        return "Número de teléfono válido"
    return "El número debe tener entre 10 y 15 dígitos, opcionalmente con '+'."


def validar_fecha(fecha: str) -> str:
    """
    Valida si la fecha de nacimiento ingresada es válida.

    Args:
        fecha (str): La fecha ingresada por el usuario en formato DD/MM/AAAA.

    Returns:
        str: Mensaje indicando si la fecha es válida o no.

    Example:
        >>> validar_fecha("15/08/1990")
        'Fecha de nacimiento válida'
    """
    patron = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/([0-9]{4})$"
    if re.fullmatch(patron, fecha):
        return "Fecha de nacimiento válida"
    return ("La fecha debe estar en formato DD/MM/AAAA y ser una fecha válida.")


# Función principal para la app
def app():
    """
    App principal para validar formularios web con Streamlit y regex.
    """
    st.title("Validación de Formulario con Regex")
    st.write(
        """
        Esta aplicación valida los siguientes campos:
        - **Nombre**: Solo caracteres alfabéticos, iniciando con mayúscula.
        - **Correo electrónico**: En formato usuario@dominio.com.
        - **Número de teléfono**: De 10 a 15 dígitos, opcionalmente con '+'.
        - **Fecha de nacimiento**: En formato DD/MM/AAAA.
        """
    )

    # Entrada de datos del usuario
    nombre = st.text_input("Ingrese su nombre:")
    correo = st.text_input("Ingrese su correo electrónico:")
    telefono = st.text_input("Ingrese su número de teléfono:")
    fecha = st.text_input("Ingrese su fecha de nacimiento (DD/MM/AAAA):")

    # Validación de datos
    if st.button("Validar"):
        st.write("### Resultados de validación:")
        st.write(f"**Nombre**: {validar_nombre(nombre)}")
        st.write(f"**Correo electrónico**: {validar_correo(correo)}")
        st.write(f"**Número de teléfono**: {validar_telefono(telefono)}")
        st.write(f"**Fecha de nacimiento**: {validar_fecha(fecha)}")

    # Créditos
    st.write("---")
    st.write("Programado por **Kevin Guio**")


# Ejecutar la aplicación
if __name__ == "__main__":
    app()
