import os          # Para trabajar con rutas y listar archivos del sistema
import re          # Expresiones regulares: buscar patrones dentro del texto
import pandas as pd  # Para armar la tabla de resultados y exportarla a CSV
import PyPDF2      # Para leer PDFs y extraer el texto de sus páginas


def procesar_carpeta_pdfs(ruta_carpeta):
    """
    Recorre todos los PDFs de una carpeta y, por cada uno, cuenta:
      - cuántos informes contiene (un informe cada 4 páginas)
      - cuántos maestros distintos aparecen en esos informes
    Al final guarda un resumen en 'reporte_maestros.csv'.
    """

    # Lista donde se irá acumulando una fila (diccionario) por cada PDF
    datos_finales = []

    # --- VALIDACIONES INICIALES ---

    # Si la carpeta no existe, avisamos y terminamos la función
    if not os.path.exists(ruta_carpeta):
        print(f"Error: La ruta {ruta_carpeta} no existe.")
        return

    # Filtramos el contenido de la carpeta para quedarnos solo con los .pdf

    archivos = [f for f in os.listdir(ruta_carpeta) if f.endswith('.pdf')]

    # Si no hay PDFs, no tiene sentido continuar
    if not archivos:
        print("No se encontraron archivos PDF en la carpeta.")
        return

    print(f"Iniciando el procesamiento de {len(archivos)} archivos...\n")

    # --- PROCESAMIENTO DE CADA PDF ---

    for archivo_nombre in archivos:
        # Construimos la ruta completa (carpeta + nombre del archivo)
        ruta_completa = os.path.join(ruta_carpeta, archivo_nombre)

        # Lista para guardar los nombres de maestros encontrados en ESTE PDF
        nombres_maestros = []

        # try/except: si un PDF está dañado o falla, el programa
        # no se detiene; solo reporta el error y sigue con el siguiente
        try:
            # Abrimos el PDF en modo lectura binaria ('rb'), necesario para PDFs
            with open(ruta_completa, 'rb') as archivo:
                lector = PyPDF2.PdfReader(archivo)

                # Número total de páginas del documento

                total_paginas = len(lector)

                # Se avanza de 4 en 4 páginas (0, 4, 8, ...) porque se asume que
                # cada informe ocupa 4 páginas y el nombre aparece en la primera.
                for i in range(0, total_paginas, 4):
                    # Esta condición siempre es verdadera (range ya limita el valor
                    # de i); es redundante pero no causa problemas.
                    if i < total_paginas:
                        pagina = lector.pages[i]        # Tomamos la primera página del informe
                        texto = pagina.extract_text()   # Extraemos su texto plano

                        # Buscamos el patrón "Nombre:" seguido de cualquier texto.
                        #   \s*  -> cero o más espacios/saltos tras los dos puntos
                        #   (.*) -> captura el resto de la línea (el nombre)
                        match = re.search(r"Nombre:\s*(.*)", texto)

                        # Si se encontró el patrón, guardamos el nombre limpio
                        if match:
                            nombre_extraido = match.group(1).strip()  # strip() quita espacios sobrantes
                            nombres_maestros.append(nombre_extraido)

            # --- MÉTRICAS DEL PDF ---

            # Cantidad total de informes detectados (incluye repetidos)
            cantidad_informes = len(nombres_maestros)

            # set() elimina duplicados; su len() da el número de maestros distintos
            maestros_unicos = len(set(nombres_maestros))

            # Guardamos los resultados de este PDF como una fila del reporte
            datos_finales.append({
                "Nombre del PDF": archivo_nombre,
                "Cantidad de Informes": cantidad_informes,
                "Número de Maestros Únicos": maestros_unicos
            })
            print(f"✔ Procesado: {archivo_nombre}")

        except Exception as e:
            # Cualquier error (PDF corrupto, protegido, etc.) se muestra y se continúa
            print(f"✘ Error en {archivo_nombre}: {e}")

    # --- EXPORTACIÓN DE RESULTADOS ---

    # Convertimos la lista de diccionarios en una tabla (DataFrame)
    df = pd.DataFrame(datos_finales)

    # Guardamos en CSV sin la columna de índice.
    # 'utf-8-sig' agrega un BOM para que Excel muestre bien acentos y ñ.
    df.to_csv('reporte_maestros.csv', index=False, encoding='utf-8-sig')

    print(f"\n¡Listo! Se ha creado el archivo 'reporte_maestros.csv' con {len(df)} registros.")


# --- CONFIGURACIÓN ---
# Ruta de la carpeta con los PDFs. El prefijo r"" (raw string) evita que las
# diagonales invertidas de Windows se interpreten como caracteres especiales.
# Aquí es una ruta relativa: busca la carpeta "20231" junto al script.
ruta_de_mis_pdfs = r"20231"

# Ejecutamos la función principal
procesar_carpeta_pdfs(ruta_de_mis_pdfs)
