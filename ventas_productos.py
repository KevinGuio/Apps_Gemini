import streamlit as st
import pandas as pd
import re
from io import BytesIO
import xlsxwriter


def procesar_archivo_con_regex(contenido_csv):
    """
    Procesa el archivo CSV organizando nombres y correos en una sola fila.
    """
    # Extraer todos los datos originales
    datos_originales = []
    for linea in contenido_csv.splitlines():
        # Extraer nombres completos
        nombres = re.findall(r"[A-Z][a-z]+ [A-Z][a-z]+", linea)
        
        # Extraer correo
        correo = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", linea)
        correo = correo.group() if correo else "N/A"
        
        # Extraer información adicional
        codigo = re.search(r"\b\d{6}\b", linea)
        codigo = codigo.group() if codigo else "N/A"

        precio = re.search(r"\b\d+\.\d{1,2}\b", linea)
        precio = precio.group() if precio else "N/A"

        fecha = re.search(r"\b\d{2}/\d{2}/\d{2}\b", linea)
        fecha = fecha.group() if fecha else "N/A"

        telefono = re.search(r"\+\d{1,3} \d{9,10}", linea)
        telefono = telefono.group() if telefono else "N/A"

        datos_originales.append({
            "nombres": nombres,
            "correo": correo,
            "codigo": codigo,
            "precio": precio,
            "fecha": fecha,
            "telefono": telefono
        })

    # Mapear nombres a correos
    mapeo_nombres = {}
    for dato in datos_originales:
        if dato["correo"] != "N/A":
            nombre_correo = dato["correo"].split('@')[0].replace('.', '').lower()
            for nombre in dato["nombres"]:
                nombre_limpio = nombre.replace(' ', '').lower()
                if nombre_limpio == nombre_correo:
                    mapeo_nombres[nombre] = dato["correo"]
                    break

    # Procesar datos finales
    datos_procesados = []
    nombres_usados = set()

    for dato in datos_originales:
        # Encontrar nombre que no se haya usado
        nombre_candidato = None
        for nombre in dato["nombres"]:
            if nombre not in nombres_usados:
                nombre_candidato = nombre
                break

        # Verificar si hay un mapeo de nombre a correo
        correo_final = "N/A"
        if nombre_candidato:
            nombres_usados.add(nombre_candidato)
            correo_final = mapeo_nombres.get(nombre_candidato, dato["correo"])

            datos_procesados.append({
                "Código_producto": dato["codigo"],
                "Precio_producto": dato["precio"],
                "Fecha_compra": dato["fecha"],
                "Nombre_cliente": nombre_candidato,
                "Correo_electrónico": correo_final,
                "Número_telefono": dato["telefono"]
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
