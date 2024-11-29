import streamlit as st
import pandas as pd
import re
from io import BytesIO
import xlsxwriter


def procesar_archivo_con_regex(contenido_csv):
    """
    Procesa el archivo CSV y organiza la información en columnas específicas.
    """
    datos_procesados = []
    nombres_procesados = {}

    for linea in contenido_csv.splitlines():
        # Extraer código del producto
        codigo = re.search(r"\b\d{6}\b", linea)
        codigo = codigo.group() if codigo else "N/A"

        # Extraer precio del producto
        precio = re.search(r"\b\d+\.\d{1,2}\b", linea)
        precio = precio.group() if precio else "N/A"

        # Extraer fecha de compra
        fecha = re.search(r"\b\d{2}/\d{2}/\d{2}\b", linea)
        fecha = fecha.group() if fecha else "N/A"

        # Extraer correo electrónico
        correo = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", linea)
        correo = correo.group() if correo else "N/A"

        # Extraer número de teléfono
        telefono = re.search(r"\+\d{1,3} \d{9,10}", linea)
        telefono = telefono.group() if telefono else "N/A"

        # Extraer nombres de los clientes
        nombres = re.findall(r"[A-Z][a-z]+ [A-Z][a-z]+", linea)
        
        # Extraer nombre antes del @ del correo
        nombre_correo = correo.split('@')[0] if correo != "N/A" else None

        # Encontrar nombre que coincida con el nombre del correo
        nombre_coincidente = None
        for nombre in nombres:
            # Remover espacios y convertir a minúsculas para comparación
            nombre_limpio = nombre.replace(' ', '').lower()
            if nombre_correo and nombre_limpio == nombre_correo.lower():
                nombre_coincidente = nombre
                break

        # Si no se encuentra coincidencia, tomar el primer nombre
        if not nombre_coincidente and nombres:
            nombre_coincidente = nombres[0]

        # Verificar si el nombre ya ha sido procesado
        if nombre_coincidente and nombre_coincidente not in nombres_procesados:
            nombres_procesados[nombre_coincidente] = True
            
            datos_procesados.append({
                "Código_producto": codigo,
                "Precio_producto": precio,
                "Fecha_compra": fecha,
                "Nombre_cliente": nombre_coincidente,
                "Correo_electrónico": correo,
                "Número_telefono": telefono,
            })

    return pd.DataFrame(datos_procesados)


def convertir_df_a_excel(df):
    """
    Convierte un DataFrame en un archivo Excel para su descarga.
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
        original_data = [row.split(",") for row in contenido_csv.splitlines()]
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
