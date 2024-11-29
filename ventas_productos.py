import streamlit as st
import pandas as pd
import re
from io import BytesIO
import xlsxwriter


def procesar_archivo_con_regex(contenido_csv):
    """
    Procesa el archivo CSV y organiza la información en columnas específicas.

    Args:
        contenido_csv (str): Contenido del archivo CSV cargado por el usuario.

    Returns:
        pd.DataFrame: DataFrame con los datos procesados y organizados.
    """
    # Crear listas para almacenar los datos extraídos
    codigos, precios, fechas, nombres, correos, telefonos = [], [], [], [], [], []

    # Procesar cada línea del archivo CSV
    for linea in contenido_csv.splitlines():
        # Extraer código del producto (exactamente 6 dígitos)
        codigo = re.search(r"\b\d{6}\b", linea)
        codigos.append(codigo.group() if codigo else "N/A")

        # Extraer precio del producto (con punto decimal y hasta dos decimales)
        precio = re.search(r"\b\d+\.\d{1,2}\b", linea)
        precios.append(precio.group() if precio else "N/A")

        # Extraer fecha de compra (formato DD/MM/YY)
        fecha = re.search(r"\b\d{2}/\d{2}/\d{2}\b", linea)
        fechas.append(fecha.group() if fecha else "N/A")

        # Extraer nombres de los clientes (suponiendo que hay nombres de tipo "Nombre Apellido")
        nombres_cliente = re.findall(r"[A-Z][a-z]+ [A-Z][a-z]+", linea)
        nombres_cliente = ' '.join(nombres_cliente) if nombres_cliente else "N/A"
        nombres.append(nombres_cliente)

        # Extraer correo electrónico
        correo = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", linea)
        if correo:
            # Validar que el nombre del correo coincida con el nombre del cliente
            correo_usuario = correo.group().split('@')[0]
            nombre_cliente = nombres_cliente.lower().replace(" ", "")
            if correo_usuario.lower() == nombre_cliente:
                correos.append(correo.group())
            else:
                correos.append("N/A")
        else:
            correos.append("N/A")

        # Extraer número de teléfono (formato internacional + código de país)
        telefono = re.search(r"\+\d{1,3} \d{9,10}", linea)
        telefonos.append(telefono.group() if telefono else "N/A")

    # Eliminar duplicados en los nombres (solo una columna de nombres)
    nombres_unicos = list(set(nombres))
    
    # Crear un DataFrame con los datos procesados
    df = pd.DataFrame({
        "Código_producto": codigos,
        "Precio_producto": precios,
        "Fecha_compra": fechas,
        "Nombre_cliente": nombres_unicos,  # Usar solo una columna de nombres
        "Correo_electrónico": correos,
        "Número_telefono": telefonos,
    })

    return df


def convertir_df_a_excel(df):
    """
    Convierte un DataFrame en un archivo Excel para su descarga.

    Args:
        df (pd.DataFrame): DataFrame con la información procesada.

    Returns:
        BytesIO: Flujo de datos en formato Excel.
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

        # Mostrar los datos originales cargados
        st.write("### Datos cargados originalmente:")
        # Dividir las líneas del archivo por tabulación (\t)
        original_data = [row.split(",") for row in contenido_csv.splitlines()]
        # Crear un DataFrame para visualizar los datos originales en columnas
        df_original = pd.DataFrame(original_data)
        st.dataframe(df_original)

        # Procesar el archivo con regex
        st.write("### Datos procesados:")
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
