import pandas as pd
from tkinter import Tk, filedialog, simpledialog

def limpiar_y_renombrar_csv():
    # Ocultar ventana raíz de tkinter
    Tk().withdraw()

    # Seleccionar el archivo CSV
    ruta_archivo = filedialog.askopenfilename(
        title="Selecciona el archivo CSV",
        filetypes=[("CSV files", "*.csv")]
    )

    if not ruta_archivo:
        print("❌ No se seleccionó ningún archivo.")
        return

    # Leer el archivo CSV
    try:
        datos = pd.read_csv(ruta_archivo)
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return

    print("Columnas originales:", list(datos.columns))

    # Normalizar nombres para buscar columnas a eliminar (sin espacios y en mayúsculas)
    columnas_normalizadas = [col.strip().upper() for col in datos.columns]
    eliminar = ['ACUM', 'PROM', 'MESES']

    # Crear lista de columnas que existen y que deben eliminarse
    cols_a_eliminar = [datos.columns[i] for i, col_norm in enumerate(columnas_normalizadas) if col_norm in eliminar]

    if cols_a_eliminar:
        datos = datos.drop(columns=cols_a_eliminar)
        print("Columnas eliminadas:", cols_a_eliminar)
    else:
        print("No se encontraron columnas ACUM, PROM o MESES para eliminar.")

    # Ahora renombrar columnas de meses por números, dejando "AÑO" intacto
    # Asumimos que la primera columna es "AÑO" y el resto son meses
    columnas = list(datos.columns)
    if len(columnas) < 2:
        print("❌ No hay columnas suficientes para renombrar.")
        return

    nuevas_columnas = [columnas[0]] + [str(i) for i in range(1, len(columnas))]
    datos.columns = nuevas_columnas
    print("Nuevos nombres de columnas:", list(datos.columns))

    # Pedir nombre de salida
    nombre_salida = simpledialog.askstring("Guardar como", "¿Cómo quieres llamar al archivo CSV de salida?")
    if not nombre_salida:
        print("❌ No se proporcionó nombre de salida.")
        return

    if not nombre_salida.lower().endswith(".csv"):
        nombre_salida += ".csv"

    # Guardar CSV
    datos.to_csv(nombre_salida, index=False)
    print(f"✅ Archivo guardado como '{nombre_salida}'")
