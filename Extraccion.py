import csv
from tkinter import Tk, filedialog

def extraer_bloque_climatico(nombre_bloque, anio_inicio=2015, anio_fin=2025):
    # Abrir un diálogo para seleccionar el archivo
    Tk().withdraw()  # Oculta la ventana principal de Tkinter
    ruta_archivo = filedialog.askopenfilename(title="Selecciona el archivo .txt", filetypes=[("Archivos de texto", "*.txt")])

    if not ruta_archivo:
        print("❌ No se seleccionó ningún archivo.")
        return

    extraer = False
    datos = []

    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        for linea in archivo:
            linea = linea.strip()

            if nombre_bloque.upper() in linea.upper():
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

    # Nombre de salida dinámico
    salida_csv = f"{nombre_bloque.replace(' ', '_').lower()}_{anio_inicio}_{anio_fin}.csv"

    with open(salida_csv, "w", newline='', encoding='utf-8') as salida:
        escritor = csv.writer(salida)
        escritor.writerows(datos)

    print(f"✅ Datos guardados como '{salida_csv}'")

