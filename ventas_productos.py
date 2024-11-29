import streamlit as st
import pandas as pd
import re


def procesar_archivo(archivo_csv):
    """
    Procesa el archivo CSV cargado para reorganizar los datos según el formato deseado.

    Args:
        archivo_csv (file-like): Archivo CSV cargado por el usuario.

    Returns:
        pd.DataFrame: DataFrame con los datos reorganizados.

    Example:
        >>> procesar_archivo(archivo_csv)
        pd.DataFrame
    """
    # Leer el archivo CSV como texto
    data = archivo_csv.decode("utf-8").strip().split("\n")

    # Regex para extraer los campos necesarios
    pattern = (r"(\S+@\S+)\s+(\d+\.\d+)\s+([\+\d\s]+)\s+(\d{2}/\d{2}/\d{2})"
               r"\s+([\w\s]+)\s+(\d+)\s+([\w\s]+)")

    # Almacenar los datos en una lista
    rows = []
    for line in data:
        match = re.match(pattern, line)
        if match:
            rows.append(match.groups())

    # Crear el DataFrame
    df = pd.DataFrame(
        rows,
        columns=[
            "Correo_electrónico", "Precio_producto", "Número_telefono",
            "Fecha_compra", "Nombre_cliente1", "Código_producto",
            "Nombre_cliente2"
        ]
    )

    # Reorganizar las columnas
    df = df[[
        "Código_producto", "Precio_producto", "Fecha_compra",
        "Nombre_cliente1", "Nombre_cliente2", "Correo_electrónico",
        "Número_telefono"
    ]]

    return df


def guardar_excel(df):
    """
    Guarda el DataFrame en un archivo Excel en memoria.

    Args:
        df (pd.DataFrame): DataFrame a guardar.

    Returns:
        BytesIO: Archivo Excel generado.

    Example:
        >>> guardar_excel(df)
        BytesIO
    """
    from io import BytesIO

    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Datos")
    output.seek(0)
    return output


def main():
    """Función principal de la app."""
    st.title("Organizador de Datos - Kevin Guio")

    st.write("""
    **Cómo usar:**
    - Sube un archivo CSV con los datos en el formato original.
    - El programa reorganizará los datos y generará un archivo Excel con el formato deseado.
    """)

    # Subir archivo CSV
    archivo_csv = st.file_uploader("Sube un archivo CSV", type=["csv"])

    if archivo_csv:
        # Leer y procesar el archivo
        contenido_csv = archivo_csv.read()
        df = procesar_archivo(contenido_csv)

        # Mostrar el DataFrame en la app
        st.write("### Datos procesados:")
        st.dataframe(df)

        # Generar archivo Excel
        archivo_excel = guardar_excel(df)

        # Botón para descargar el archivo Excel
        st.download_button(
            label="Descargar archivo Excel",
            data=archivo_excel,
            file_name="datos_organizados.xls",
            mime="application/vnd.ms-excel"
        )

    # Mensaje final
    st.write("Programado por Kevin Guio")


if __name__ == "__main__":
    main()
