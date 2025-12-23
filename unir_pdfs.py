import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from pypdf import PdfWriter

class AppUnidorPDF:
    def __init__(self, root):
        self.root = root
        self.root.title("Unidor de PDFs Inteligente")
        self.root.geometry("500x350")

        # Variables para guardar las rutas
        self.ruta_a = tk.StringVar()
        self.ruta_b = tk.StringVar()
        self.ruta_c = tk.StringVar()

        # --- Interfaz ---
        tk.Label(root, text="1. Selecciona la Carpeta A (Origen 1)", font=("Arial", 10, "bold")).pack(pady=5)
        tk.Entry(root, textvariable=self.ruta_a, width=60).pack(pady=2)
        tk.Button(root, text="Examinar...", command=self.seleccionar_a).pack(pady=2)

        tk.Label(root, text="2. Selecciona la Carpeta B (Origen 2)", font=("Arial", 10, "bold")).pack(pady=5)
        tk.Entry(root, textvariable=self.ruta_b, width=60).pack(pady=2)
        tk.Button(root, text="Examinar...", command=self.seleccionar_b).pack(pady=2)

        tk.Label(root, text="3. Selecciona Carpeta Salida (Destino C)", font=("Arial", 10, "bold")).pack(pady=5)
        tk.Entry(root, textvariable=self.ruta_c, width=60).pack(pady=2)
        tk.Button(root, text="Examinar...", command=self.seleccionar_c).pack(pady=2)

        tk.Label(root, text="--------------------------------").pack(pady=10)

        # Botón Grande de Acción
        self.btn_accion = tk.Button(root, text="VALIDAR Y UNIR ARCHIVOS", bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), command=self.procesar)
        self.btn_accion.pack(pady=10, ipady=5, ipadx=10)

        self.lbl_status = tk.Label(root, text="Esperando...", fg="gray")
        self.lbl_status.pack()

    # --- Funciones de Selección ---
    def seleccionar_a(self):
        ruta = filedialog.askdirectory(title="Seleccionar Carpeta A")
        if ruta: self.ruta_a.set(ruta)

    def seleccionar_b(self):
        ruta = filedialog.askdirectory(title="Seleccionar Carpeta B")
        if ruta: self.ruta_b.set(ruta)

    def seleccionar_c(self):
        ruta = filedialog.askdirectory(title="Seleccionar Carpeta de Salida")
        if ruta: self.ruta_c.set(ruta)

    # --- Lógica Principal ---
    def procesar(self):
        dir_a = self.ruta_a.get()
        dir_b = self.ruta_b.get()
        dir_c = self.ruta_c.get()

        if not dir_a or not dir_b or not dir_c:
            messagebox.showwarning("Faltan datos", "Por favor selecciona las 3 carpetas.")
            return

        # 1. Obtener archivos PDF
        try:
            archivos_a = sorted([f for f in os.listdir(dir_a) if f.lower().endswith('.pdf')])
            archivos_b = sorted([f for f in os.listdir(dir_b) if f.lower().endswith('.pdf')])
        except Exception as e:
            messagebox.showerror("Error de lectura", f"No se pudo leer las carpetas:\n{e}")
            return

        # --- VALIDACIÓN 1: CANTIDAD ---
        if len(archivos_a) != len(archivos_b):
            msg = (f"ERROR DE CANTIDAD:\n\n"
                   f"Carpeta A tiene {len(archivos_a)} archivos.\n"
                   f"Carpeta B tiene {len(archivos_b)} archivos.\n\n"
                   f"Deben tener la misma cantidad exacta.")
            messagebox.showerror("Validación Fallida", msg)
            return

        # --- VALIDACIÓN 2: NOMBRES IDENTICOS ---
        set_a = set(archivos_a)
        set_b = set(archivos_b)
        
        if set_a != set_b:
            diferencias = set_a.symmetric_difference(set_b)
            lista_diff = "\n".join(list(diferencias)[:5]) # Muestra solo los primeros 5 errores
            msg = (f"ERROR DE NOMBRES:\n\n"
                   f"Los archivos no coinciden exactamente.\n"
                   f"Archivos conflictivos (ejemplos):\n{lista_diff}\n\n"
                   f"Revisa que se llamen EXACTAMENTE igual.")
            messagebox.showerror("Validación Fallida", msg)
            return

        # --- PROCESO DE UNIÓN ---
        self.lbl_status.config(text="Procesando...", fg="blue")
        self.root.update()
        
        exitos = 0
        errores = []

        for archivo in archivos_a:
            path_a = os.path.join(dir_a, archivo)
            path_b = os.path.join(dir_b, archivo)
            path_salida = os.path.join(dir_c, archivo)

            try:
                merger = PdfWriter()
                merger.append(path_a)
                merger.append(path_b)
                merger.write(path_salida)
                merger.close()
                exitos += 1
            except Exception as e:
                errores.append(f"{archivo}: {str(e)}")

        # Reporte Final
        if len(errores) == 0:
            messagebox.showinfo("Éxito", f"¡Proceso Terminado!\nSe unieron {exitos} archivos correctamente en la carpeta C.")
            self.lbl_status.config(text="Listo.", fg="green")
        else:
            msg_err = "\n".join(errores)
            messagebox.showwarning("Terminado con errores", f"Se unieron {exitos}, pero fallaron estos:\n{msg_err}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppUnidorPDF(root)
    root.mainloop()