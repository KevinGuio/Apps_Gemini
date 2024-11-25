import streamlit as st
import pandas as pd
import re
from io import BytesIO
import xlsxwriter

def procesar_archivo_con_regex(contenido_csv):
    """
    Procesa el archivo CSV y extrae información mediante expresiones regulares.

    Args:
        contenido_csv (str): Contenido del archivo CSV cargado por el usuario.

    Returns:
        pd.DataFrame: DataFrame con la información procesada.

    Example:
        >>> procesar_archivo_con_regex("regex_productos.csv")
        DataFrame con columnas: ["Número de serie", "Nombre del producto", ...]
    """
    # Crear listas para almacenar los datos extraídos
    series, nombres, valores, fechas, contactos = [], [], [], [], []

    # Procesar cada línea del archivo CSV
    for linea in contenido_csv.splitlines():
        # Extraer el número de serie (formato alfanumérico largo)
        serie = re.search(r"\b[A-Z0-9]{8,}\b", linea)
        series.append(serie.group() if serie else "N/A")

        # Extraer el nombre del producto (palabras con espacios)
        nombre = re.search(r"[a-zA-Z ]+", linea)
        nombres.append(nombre.group().strip() if nombre else "N/A")

        # Extraer el valor (formato de moneda con decimales opcionales)
        valor = re.search(r"\$\d+(\.\d{2})?", linea)
        valores.append(valor.group() if valor else "N/A")

        # Extraer la fecha de compra (formato DD/MM/YY)
        fecha = re.search(r"\b\d{2}/\d{2}/\d{2}\b", linea)
        fechas.append(fecha.group() if fecha else "N/A")

        # Extraer información de contacto (nombre, email, teléfono)
        contacto = re.search(
            r"[A-Z][a-z]+ [A-Z][a-z]+.*\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b.*"
            r"\b\d{10}\b", 
            linea
        )
        contactos.append(contacto.group() if contacto else "N/A")

    # Crear un DataFrame con los datos procesados
    df = pd.DataFrame({
        "Número de serie": series,
        "Nombre del producto": nombres,
        "Valor": valores,
        "Fecha de compra (DD/MM/YY)": fechas,
        "Información de contacto": contactos,
    })

    return df


def convertir_df_a_excel(df):
    """
    Convierte un DataFrame en un archivo Excel para su descarga.

    Args:
        df (pd.DataFrame): DataFrame con la información procesada.

    Returns:
        BytesIO: Flujo de datos en formato Excel.

    Example:
        >>> convertir_df_a_excel(mi_dataframe)
        BytesIO con el contenido del archivo Excel.
    """
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Productos")
    output.seek(0)
    return output


def app():
    """
    Construye la interfaz principal de la aplicación en Streamlit.
    """
    st.title("Procesador de Información de Productos")
    st.write("""
        **Objetivo:** Cargar un archivo CSV con información de productos,
        procesarlo usando regex, y generar un archivo Excel estructurado.
    """)
    st.write("Programado por **Kevin Guio**")

    # Subir archivo
    archivo_subido = st.file_uploader("Sube un archivo CSV", type=["csv"])

    if archivo_subido is not None:
        # Leer el contenido del archivo CSV
        contenido_csv = archivo_subido.read().decode("utf-8")

        # Procesar el archivo con regex
        st.write("### Archivo procesado:")
        df_procesado = procesar_archivo_con_regex(contenido_csv)
        st.dataframe(df_procesado)

        # Convertir el DataFrame a Excel para su descarga
        archivo_excel = convertir_df_a_excel(df_procesado)

        # Botón de descarga
        st.download_button(
            label="Descargar archivo Excel",
            data=archivo_excel,
            file_name="productos_procesados.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )


if __name__ == "__main__":
    app()
