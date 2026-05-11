import re
from collections import Counter
import tkinter as tk
from tkinter import filedialog, messagebox


def limpiar_texto(texto: str):
    texto = texto.lower()
    texto = re.sub(r"[^a-záéíóúüñ\s]", "", texto)
    tokens = texto.split()
    return tokens


def abrir_archivo():
    path = filedialog.askopenfilename(title="Abrir archivo TXT",
                                      filetypes=[("Text files", "*.txt")])
    if not path:
        return
    try:
        with open(path, "r", encoding="utf-8") as f:
            contenido = f.read()
    except UnicodeDecodeError:
        try:
            with open(path, "r", encoding="latin-1") as f:
                contenido = f.read()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo:\n{e}")
            return

    tokens = limpiar_texto(contenido)
    contador = Counter(tokens)
    mostrar_resultados(path, tokens, contador)


def mostrar_resultados(path, tokens, contador: Counter):
    total = len(tokens)
    unicas = len(contador)
    top10 = contador.most_common(10)
    hapax = [w for w, n in contador.items() if n == 1]

    salida = []
    salida.append(f"Archivo: {path}")
    salida.append(f"Tokens totales: {total}")
    salida.append(f"Palabras únicas: {unicas}")
    salida.append(f"Palabras hapax (ocurren 1 vez): {len(hapax)}")
    if hapax:
        salida.append(f"Ejemplos hapax: {', '.join(hapax[:8])}")
    salida.append("\nTop 10 palabras:")
    for w, n in top10:
        salida.append(f"  {w}: {n}")

    text_out.config(state="normal")
    text_out.delete(1.0, tk.END)
    text_out.insert(tk.END, "\n".join(salida))
    text_out.config(state="disabled")

    # enable save button and attach data
    btn_save.config(state="normal")
    btn_save.counter = contador
    btn_save.path = path


def guardar_reporte():
    contador = getattr(btn_save, "counter", None)
    path_in = getattr(btn_save, "path", "")
    if contador is None:
        messagebox.showinfo("Info", "No hay resultados para guardar.")
        return

    save_path = filedialog.asksaveasfilename(title="Guardar reporte",
                                             defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt")])
    if not save_path:
        return

    total = sum(contador.values())
    uniques = len(contador)
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(f"Reporte de conteo de palabras\nArchivo origen: {path_in}\n\n")
        f.write(f"Tokens totales: {total}\n")
        f.write(f"Palabras únicas: {uniques}\n\n")
        f.write("Top palabras:\n")
        for w, n in contador.most_common():
            f.write(f"{w}\t{n}\n")

    messagebox.showinfo("Guardado", f"Reporte guardado en:\n{save_path}")


def about():
    messagebox.showinfo("Acerca de", "Contador de palabras - TXT\nSimple GUI para Windows")


root = tk.Tk()
root.title("Contador de Palabras - TXT")
root.geometry("700x480")

frm = tk.Frame(root, padx=10, pady=10)
frm.pack(fill="both", expand=True)

btn_open = tk.Button(frm, text="Cargar archivo TXT", width=20, command=abrir_archivo)
btn_open.pack(anchor="nw")

btn_save = tk.Button(frm, text="Guardar reporte", width=20, state="disabled", command=guardar_reporte)
btn_save.pack(anchor="nw", pady=(6, 10))

btn_about = tk.Button(frm, text="Acerca de", width=12, command=about)
btn_about.pack(anchor="ne")

text_out = tk.Text(frm, wrap="word", state="disabled")
text_out.pack(fill="both", expand=True)

root.mainloop()
