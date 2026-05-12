# Contador TXT — Entregable para el ejercicio de PLN

**Autores**: Laura Figueredo, Daniel Reyes

## Contenido

- `txt_counter_gui.py` — Interfaz gráfica (Tkinter) para cargar un `.txt`, contar palabras y exportar un reporte.
- `train_embeddings_svd.py` — Entrenamiento ligero de embeddings por co-ocurrencia + SVD.
- `requirements.txt` — Dependencias mínimas (`numpy`, `pyinstaller`).
- `corpus.txt` — Ejemplo de corpus en español.
- `build_exe.ps1` — Script PowerShell para construir el `.exe` en Windows.
- `cleanup_repo.ps1` — Script para limpiar el repositorio dejando solo esta carpeta.

## Tamaño y formato recomendado del texto / corpus

- Formato: archivo de texto plano `.txt`, preferible en `UTF-8` (si no, `latin-1` se intenta leer). Evitar archivos binarios o con mezclas de codificación.
- Estructura: una oración por línea o párrafos separados por líneas en blanco facilitan la tokenización; los saltos de línea y puntuación se manejan en los scripts.
- Tamaño mínimo para prácticas (conteo, hapax, visualización simple): 500–1.000 palabras (~1 KB) es suficiente para un ejercicio demostrativo.
- Tamaño recomendado para embeddings por SVD (train_embeddings_svd.py): al menos 500–2.000 oraciones (varios miles de tokens). La SVD usa memoria O(V^2) en la matriz de coocurrencia, por lo que vocabularios muy grandes (>5.000 palabras) pueden consumir mucha memoria.
- Tamaño recomendado para Word2Vec (si decides usar `gensim`): idealmente decenas o cientos de miles de tokens; para resultados útiles busque >100k tokens (mejor: millones para modelos de calidad).
- Consejo práctico: si tu corpus es pequeño, el resultado de los embeddings será ruidoso pero útil para aprendizaje; para experimentos reproducibles usa un corpus con al menos algunas decenas de miles de tokens.

## Sobre el ejecutable

- El repositorio entrega los scripts fuente en esta carpeta (`txt_counter_gui.py`, `train_embeddings_svd.py`) y el ejemplo `corpus.txt`.
- El ejecutable no está incluido por defecto en este deliverable; para crear un `.exe` que incluya los modelos entrenados debes ejecutar primero `python train_embeddings_svd.py` (generará `models/`) y luego reconstruir el ejecutable con PyInstaller incluyendo `models` usando `--add-data "models;models"`.
- Si generas el `.exe` sin incluir `models/`, el ejecutable sólo ofrece la interfaz para cargar archivos `.txt` y contar palabras (no contiene embeddings pre-cargados).

## Qué hace el ejercicio (resumen)

1. Preparación del corpus: limpieza básica (minúsculas y eliminación de puntuación) y tokenización.
2. Conteo y estadísticas: tokens totales, tamaño del vocabulario, palabras "hapax" (ocurren una sola vez) y listado de palabras más frecuentes.
3. Entrenamiento de embeddings (opcional): `train_embeddings_svd.py` crea una matriz de co-ocurrencia y reduce dimensionalidad con SVD para producir vectores de palabras (guardados en `models/`).
4. Interfaz: `txt_counter_gui.py` permite cargar cualquier `.txt`, mostrar las estadísticas anteriores y guardar un reporte en `.txt`.

## Recomendación final sobre tamaño del corpus

- Para el ejercicio de conteo y exploración: 500–1.000 palabras (pequeño corpus) suficientes para prácticas.
- Para obtener embeddings SVD con cierta estabilidad: miles de oraciones (500–2.000 oraciones o varios miles de tokens).
- Para modelos Word2Vec útiles en tareas reales: busque al menos 100k tokens; para calidad óptima, millones de tokens.

Si quieres, puedo generar aquí el `.exe` que incluya el modelo entrenado usando el `corpus.txt` de ejemplo (reconstruiré `models/` y ejecutaré PyInstaller). ¿Lo ejecuto ahora? 

## Cómo ejecutar (Windows, PowerShell)

1. Abrir PowerShell en la carpeta `deliverable`.

2. Crear y activar entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Instalar dependencias:

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

4. (Opcional) Entrenar embeddings SVD sobre `corpus.txt`:

```powershell
python train_embeddings_svd.py
```

Los archivos generados irán a `models/`:
- `embeddings_svd.npz` — matriz de embeddings
- `vocab_svd.json` — vocabulario (palabra -> id)

5. Generar el ejecutable (incluye `models` si existe):

```powershell
pyinstaller --onefile --windowed --add-data "models;models" txt_counter_gui.py
```

El ejecutable quedará en `dist\txt_counter_gui.exe`.

## Notas

- El entregable está pensado para tareas educativas de PLN: conteo, hapax, tokens y un pipeline de embeddings básico.
- Para modelos de producción o embeddings de alta calidad usa corpora mucho más grandes y herramientas especializadas (`gensim`, `fasttext`, modelos preentrenados).
