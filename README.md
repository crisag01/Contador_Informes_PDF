# 📄 Contador de Informes en PDF (Python)

Herramienta que revisa una carpeta de **PDFs con informes de maestros** y genera un **resumen en CSV**: cuántos informes trae cada PDF y cuántos maestros distintos aparecen.

Cada PDF junta varios informes de 4 páginas. Contarlos a mano era lento; este programa lo hace en segundos y deja la tabla lista para abrir en Excel.

Funciona **100 % en local**: solo lee el texto de los PDFs, sin servicios en línea ni IA.

## ⚙️ Cómo funciona

1. Lee todos los archivos `.pdf` de la carpeta `20231/`.
2. Recorre cada PDF de **4 en 4 páginas**, porque cada informe ocupa 4 páginas y el nombre está en la primera.
3. En esa primera página busca el texto `Nombre:` y guarda el nombre que sigue.
4. Cuenta los **informes** (todos los nombres encontrados) y los **maestros únicos** (sin repetir).
5. Si un PDF está dañado o protegido, avisa del error y sigue con el siguiente.
6. Guarda el resumen en `reporte_maestros.csv`, con acentos y ñ que Excel muestra bien.

### Columnas del CSV

`Nombre del PDF` · `Cantidad de Informes` · `Número de Maestros Únicos`

## ▶️ Cómo ejecutarlo

1. Instala [Python 3](https://www.python.org/downloads/).
2. Clona el repositorio e instala las librerías:

```bash
git clone https://github.com/crisag01/Contador_Informes_PDF.git
cd Contador_Informes_PDF
pip install -r requirements.txt
```

3. Pon tus PDFs en la carpeta `20231/`. Si tu carpeta tiene otro nombre, cámbialo en la línea `ruta_de_mis_pdfs = r"20231"` del código.
4. Ejecuta:

```bash
python contar_informes.py
```

### Ejemplo de salida

```text
Iniciando el procesamiento de 3 archivos...

✔ Procesado: informes_1.pdf
✔ Procesado: informes_2.pdf
✔ Procesado: informes_3.pdf

¡Listo! Se ha creado el archivo 'reporte_maestros.csv' con 3 registros.
```

> Los PDFs y el CSV generado **no se suben al repositorio**, porque contienen nombres de maestros. Así lo indica el `.gitignore`.

## 👤 Autor

**Cristian Armenta**, ingeniero industrial y analista de datos.
Más proyectos en [crisag.com](https://crisag.com).
