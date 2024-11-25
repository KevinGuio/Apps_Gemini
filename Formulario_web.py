import re
import streamlit as st

# Funciones de validación
def validar_nombre(nombre: str) -> tuple:
    """
    Valida si el nombre ingresado es válido.

    Un nombre válido solo contiene caracteres alfabéticos y 
    comienza con una letra mayúscula.

    Args:
        nombre (str): El nombre ingresado por el usuario.

    Returns:
        tuple: (bool, str) indicando si es válido y el mensaje correspondiente.

    Example:
        >>> validar_nombre("Juan")
        (True, "Nombre válido")
    """
    patron = r"^[A-Z][a-zA-Z]*$"
    if re.fullmatch(patron, nombre):
        return True, "Nombre válido"
    return False, "El nombre debe iniciar con mayúscula y contener solo letras."


def validar_correo(correo: str) -> tuple:
    """
    Valida si la dirección de correo ingresada es válida.

    Args:
        correo (str): El correo ingresado por el usuario.

    Returns:
        tuple: (bool, str) indicando si es válido y el mensaje correspondiente.

    Example:
        >>> validar_correo("test@example.com")
        (True, "Correo electrónico válido")
    """
    patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if re.fullmatch(patron, correo):
        return True, "Correo electrónico válido"
    return False, "El correo debe ser en formato usuario@dominio.com."


def validar_telefono(telefono: str) -> tuple:
    """
    Valida si el número de teléfono ingresado es válido.

    Args:
        telefono (str): El número de teléfono ingresado por el usuario.

    Returns:
        tuple: (bool, str) indicando si es válido y el mensaje correspondiente.

    Example:
        >>> validar_telefono("+573001234567")
        (True, "Número de teléfono válido")
    """
    patron = r"^\+?\d{10,15}$"
    if re.fullmatch(patron, telefono):
        return True, "Número de teléfono válido"
    return False, "El número debe tener entre 10 y 15 dígitos, opcionalmente con '+'."


def validar_fecha(fecha: str) -> tuple:
    """
    Valida si la fecha de nacimiento ingresada es válida.

    Args:
        fecha (str): La fecha ingresada por el usuario en formato DD/MM/AAAA.

    Returns:
        tuple: (bool, str) indicando si es válido y el mensaje correspondiente.

    Example:
        >>> validar_fecha("15/08/1990")
        (True, "Fecha de nacimiento válida")
    """
    patron = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/([0-9]{4})$"
    if re.fullmatch(patron, fecha):
        return True, "Fecha de nacimiento válida"
    return False, "La fecha debe estar en formato DD/MM/AAAA y ser válida."


# Función para mostrar resultados gráficos
def mostrar_resultado(valido: bool, mensaje: str):
    """
    Muestra un resultado gráfico en verde si es válido y en rojo si no.

    Args:
        valido (bool): Indica si el resultado es válido.
        mensaje (str): Mensaje descriptivo del resultado.
    """
    if valido:
        st.success(mensaje)
    else:
        st.error(mensaje)


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
        valido, mensaje = validar_nombre(nombre)
        mostrar_resultado(valido, f"**Nombre**: {mensaje}")
        valido, mensaje = validar_correo(correo)
        mostrar_resultado(valido, f"**Correo electrónico**: {mensaje}")
        valido, mensaje = validar_telefono(telefono)
        mostrar_resultado(valido, f"**Número de teléfono**: {mensaje}")
        valido, mensaje = validar_fecha(fecha)
        mostrar_resultado(valido, f"**Fecha de nacimiento**: {mensaje}")

    # Créditos
    st.write("---")
    st.write("Programado por **Kevin Guio**")


# Ejecutar la aplicación
if __name__ == "__main__":
    app()
