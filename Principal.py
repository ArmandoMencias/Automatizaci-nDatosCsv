import streamlit as st
import pandas as pd
import csv
import io

st.set_page_config(page_title="Limpieza de datos", layout="centered")
st.title("Limpieza y conversión de archivos")

opcion = st.radio("¿Qué tipo de archivo vas a subir?", ["Archivo TXT", "Archivo CSV"])

archivo = st.file_uploader("📁 Selecciona tu archivo", type=["txt", "csv"])

if archivo:
    if opcion == "Archivo TXT":
        bloque = st.text_input("🔍 Nombre del bloque a extraer (ej. LLUVIA MÁXIMA 24 H.)", "")
        anio_inicio = st.number_input("Año inicial", min_value=1900, max_value=2100, value=2015)
        anio_fin = st.number_input("Año final", min_value=1900, max_value=2100, value=2025)

        if st.button("Procesar archivo TXT") and bloque:
            contenido = archivo.read().decode('utf-8').splitlines()
            extraer = False
            datos = []

            for linea in contenido:
                linea = linea.strip()
                if bloque.upper() in linea.upper():
                    extraer = True
                    continue
                if extraer and linea.upper().startswith("AÑO"):
                    encabezados = linea.split()
                    datos.append(encabezados)
                    continue
                if extraer:
                    if linea and linea[0:4].isdigit():
                        anio = int(linea[0:4])
                        if anio_inicio <= anio <= anio_fin:
                            fila = linea.split()
                            datos.append(fila)
                    elif linea == "":
                        break

            if datos:
                df = pd.DataFrame(datos[1:], columns=datos[0])
                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False)
                st.success("✅ Archivo procesado correctamente.")
                st.download_button("📥 Descargar CSV", data=csv_buffer.getvalue(), file_name="bloque_extraido.csv", mime="text/csv")
            else:
                st.error("❌ No se encontraron datos para ese bloque.")

    elif opcion == "Archivo CSV":
        if st.button("Limpiar archivo CSV"):
            try:
                df = pd.read_csv(archivo)

                # Normalizar nombres para eliminar columnas sin importar mayúsculas y espacios
                columnas_normalizadas = [col.strip().upper() for col in df.columns]
                eliminar = ['ACUM', 'PROM', 'MESES']
                cols_a_eliminar = [df.columns[i] for i, col_norm in enumerate(columnas_normalizadas) if col_norm in eliminar]

                if cols_a_eliminar:
                    df = df.drop(columns=cols_a_eliminar)
                    st.write("Columnas eliminadas:", cols_a_eliminar)
                else:
                    st.write("No se encontraron columnas ACUM, PROM o MESES para eliminar.")

                columnas = list(df.columns)
                if len(columnas) < 2:
                    st.error("❌ No hay columnas suficientes para renombrar.")
                else:
                    nuevas_columnas = [columnas[0]] + [str(i) for i in range(1, len(columnas))]
                    df.columns = nuevas_columnas
                    st.write("Nuevos nombres de columnas:", list(df.columns))

                    csv_buffer = io.StringIO()
                    df.to_csv(csv_buffer, index=False)
                    st.success("✅ Archivo limpiado correctamente.")
                    st.download_button("📥 Descargar CSV limpio", data=csv_buffer.getvalue(), file_name="archivo_limpio.csv", mime="text/csv")

            except Exception as e:
                st.error(f"❌ Error al procesar el archivo: {e}")
