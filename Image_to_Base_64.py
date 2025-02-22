'''Created by: Alejandro Enriquez Rivera
at 2025-02-21'''

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image
import base64
import os
from pathlib import Path
import csv
from datetime import datetime
import io

class ImageConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Convertidor de Imágenes para WML")
        self.root.geometry("800x600")
        
        # Centrar la ventana en la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 800) // 2
        y = (screen_height - 600) // 2
        self.root.geometry(f"800x600+{x}+{y -33}")
        
        # Cambiar los íconos de la aplicación
        icon_path = "icon.ico"
        if os.path.exists(icon_path):
            # Cambiar el ícono tanto de la ventana como de la barra de tareas
            self.root.iconbitmap(default=icon_path)
            self.root.iconbitmap(icon_path)
        
        # Variables
        self.folder_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.wh_id = tk.StringVar(value="")  # Warehouse ID
        self.image_list = []
        self.max_file_size = 5 * 1024 * 1024  # 5MB por defecto
        
        # Crear la interfaz
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Selector de carpeta de entrada
        ttk.Label(main_frame, text="Carpeta de imágenes:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(main_frame, textvariable=self.folder_path, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(main_frame, text="Buscar", command=self.select_input_folder).grid(row=0, column=2)
        
        # Selector de carpeta de salida
        ttk.Label(main_frame, text="Guardar CSV en:").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(main_frame, textvariable=self.output_path, width=50).grid(row=1, column=1, padx=5)
        ttk.Button(main_frame, text="Buscar", command=self.select_output_folder).grid(row=1, column=2)
        
        # Campo para Warehouse ID
        ttk.Label(main_frame, text="Warehouse ID:").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(main_frame, textvariable=self.wh_id, width=20).grid(row=2, column=1, sticky=tk.W, padx=5)
        
        # Lista de archivos
        ttk.Label(main_frame, text="Imágenes encontradas:").grid(row=3, column=0, columnspan=3, sticky=tk.W, pady=(10,0))
        
        # Frame para la lista con scroll
        list_frame = ttk.Frame(main_frame)
        list_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.file_listbox = tk.Listbox(list_frame, width=70, height=15)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.file_listbox.yview)
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.file_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Barra de progreso
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, length=300, mode='determinate', variable=self.progress_var)
        self.progress_bar.grid(row=5, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
        
        # Etiqueta de estado
        self.status_label = ttk.Label(main_frame, text="")
        self.status_label.grid(row=6, column=0, columnspan=3, sticky=tk.W)
        
        # Botón de conversión
        ttk.Button(main_frame, text="Convertir Imágenes", command=self.convert_images).grid(row=7, column=0, columnspan=3, pady=10)
        
        # Configurar el grid
        main_frame.columnconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
    def select_input_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)
            self.update_file_list()
            
    def select_output_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_path.set(folder)
            
    def update_file_list(self):
        self.file_listbox.delete(0, tk.END)
        self.image_list = []
        
        if not self.folder_path.get():
            return
            
        valid_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
        
        for file in os.listdir(self.folder_path.get()):
            if file.lower().endswith(valid_extensions):
                full_path = os.path.join(self.folder_path.get(), file)
                if os.path.isfile(full_path):
                    self.image_list.append(full_path)
                    self.file_listbox.insert(tk.END, file)
                    
        self.status_label.config(text=f"Encontradas {len(self.image_list)} imágenes")

    def get_image_base64(self, image_path):
        """Convierte la imagen a base64 manteniendo su formato original"""
        with open(image_path, 'rb') as image_file:
            return f"[{base64.b64encode(image_file.read()).decode('utf-8')}]"
            
    def convert_images(self):
        if not self.image_list:
            messagebox.showwarning("Advertencia", "No hay imágenes para convertir")
            return
            
        if not self.output_path.get():
            messagebox.showwarning("Advertencia", "Por favor seleccione una carpeta de destino")
            return
            
        if not self.wh_id.get().strip():
            messagebox.showwarning("Advertencia", "Por favor ingrese el Warehouse ID")
            return
        
        # Preparar el archivo CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_path = os.path.join(self.output_path.get(), f"WML_Media_Upload_{timestamp}.csv")
        
        headers = ['file_name', 'user', 'title', 'seq', 'tag', 'media', 'wh_id', 'file_type']
        
        try:
            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, quoting=csv.QUOTE_NONE, delimiter=',')
                writer.writerow(headers)
                
                total_files = len(self.image_list)
                
                for i, image_path in enumerate(self.image_list):
                    try:
                        # Actualizar progreso
                        self.progress_var.set((i + 1) / total_files * 100)
                        self.status_label.config(text=f"Procesando: {os.path.basename(image_path)}")
                        self.root.update()
                        
                        # Verificar tamaño del archivo
                        file_size = os.path.getsize(image_path)
                        if file_size > self.max_file_size:
                            if not messagebox.askyesno("Advertencia", 
                                f"El archivo {os.path.basename(image_path)} excede el tamaño recomendado "
                                f"({file_size/1024/1024:.2f}MB). ¿Desea continuar con este archivo?"):
                                continue
                        
                        # Obtener el nombre base del archivo y la extensión
                        base_name = os.path.splitext(os.path.basename(image_path))[0]
                        extension = os.path.splitext(image_path)[1][1:].lower()
                        
                        # Si es jpeg, convertir a jpg para mantener consistencia
                        if extension == 'jpeg':
                            extension = 'jpg'
                        
                        # Convertir imagen a base64
                        base64_data = self.get_image_base64(image_path)
                        
                        # Escribir fila al CSV
                        row_data = [
                            base_name,           # file_name (sin extensión)
                            base_name,           # user (mismo que file_name)
                            base_name,           # title (mismo que file_name)
                            1,                   # seq (valor por defecto)
                            base_name,           # tag (mismo que file_name)
                            base64_data,         # media (base64 entre corchetes)
                            self.wh_id.get(),    # wh_id
                            extension            # file_typ
                        ]
                        writer.writerow(row_data)
                        
                    except Exception as e:
                        messagebox.showerror("Error", f"Error procesando {os.path.basename(image_path)}: {str(e)}")
            
            self.status_label.config(text="Proceso completado exitosamente")
            messagebox.showinfo("Éxito", f"Archivo CSV guardado en:\n{csv_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error guardando el archivo CSV: {str(e)}")
            
        self.progress_var.set(100)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageConverterApp(root)
    root.mainloop()