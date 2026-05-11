# Contador TXT — Entregable para el ejercicio de PLN
**Autores**: Laura Figueredo, Daniel Reyes
Contenido del folder `deliverable`:

- `txt_counter_gui.py` — Interfaz gráfica (Tkinter) que carga un `.txt`, cuenta palabras, muestra estadísticas (tokens, vocabulario, hapax, top N) y guarda un reporte.
- `train_embeddings_svd.py` — Script de entrenamiento de embeddings (fallback) que calcula matriz de coocurrencia y obtiene embeddings via SVD. Guarda salida en `models/`.
- `requirements.txt` — Dependencias mínimas para construir el ejecutable (`pyinstaller`, `numpy`).
- `build_exe.ps1` — Script de PowerShell para reproducir la generación del ejecutable en Windows.
- `README.md` — Este archivo con la documentación completa.

Objetivo
--------
Es un ejercicio de Procesamiento de Lenguaje Natural (PLN) que incluye:

- Preparación y conteo de tokens sobre un corpus `.txt`.
- Entrenamiento de embeddings por co-ocurrencia + SVD (alternativa ligera a `gensim`).
- Interfaz simple para cargar textos y generar reportes.
- Instrucciones para generar un ejecutable standalone en Windows 11.

Archivos incluidos
------------------
- `txt_counter_gui.py`: Es posible ejecutar desde consola con `python txt_counter_gui.py`.
- `train_embeddings_svd.py`: ejecutar para generar embeddings en `models/`.
- `requirements.txt`: lista de paquetes requeridos para build.
- `build_exe.ps1`: script para automatizar la construcción del `.exe` (PowerShell, Windows).

Ejecutar localmente (Windows, PowerShell)
---------------------------------------
1. Abrir PowerShell en la carpeta `deliverable`.

2. Crear y activar entorno virtual (recomendado):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Instalar dependencias:

```powershell
pip install --upgrade pip
pip install -r ..\requirements.txt
```

4. (Opcional) Entrenar embeddings SVD:

```powershell
python ..\train_embeddings_svd.py
```

Los embeddings se guardarán en `models/embeddings_svd.npz` y el vocab en `models/vocab_svd.json`.

5. Generar el ejecutable (incluyendo la carpeta `models` si la tienes):

```powershell
pyinstaller --onefile --windowed --add-data "models;models" ..\txt_counter_gui.py
```

El ejecutable aparecerá en `dist\txt_counter_gui.exe`.

Notas técnicas
--------------
- El limpiador en `txt_counter_gui.py` normaliza a minúsculas y elimina caracteres que no sean letras, con soporte básico para tildes y `ñ`.
- `train_embeddings_svd.py` construye una matriz de co-ocurrencia con ventana de 4 y calcula SVD completa; para vocabularios grandes puede ser lento y consumir memoria.
- Se incluyeron `numpy` y `pyinstaller` en `requirements.txt`. Si prefieres usar `gensim` para Word2Vec, instala `gensim` manualmente (puede requerir ruedas precompiladas para Python 3.14).

Recomendaciones
---------------
- Para datasets pequeños/medios, el pipeline SVD funciona bien para prácticas educativas. Para producción o embeddings de alta calidad, usar `gensim` o modelos preentrenados.
- Cuando construyas el `.exe`, añade `--add-data "models;models"` para incluir los modelos entrenados dentro del ejecutable.