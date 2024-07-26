import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import hashlib

class ConfiguracionEmpresa:
    def __init__(self, root):
        self.root = root
        self.root.title("Configuración de la Empresa")
        self.root.geometry("600x400+400+100")
        self.root.configure(bg="#f0f0f0")
        self.root.resizable(True, True)

        self.conn = sqlite3.connect('cash_register.db')
        self.create_tables()

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 12))
        self.style.configure("TEntry", fieldbackground="#ffffff")
        self.style.configure("TButton", background="#4CAF50", foreground="#ffffff", font=("Helvetica", 12))
        self.style.map("TButton", background=[("active", "#45a049")])

        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=3)
        for i in range(6):
            self.frame.grid_rowconfigure(i, weight=1)

        ttk.Label(self.frame, text="Nombre de la Empresa:", font=("Helvetica", 14)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.nombre_entry = ttk.Entry(self.frame, font=("Helvetica", 14))
        self.nombre_entry.grid(row=0, column=1, padx=10, pady=5, sticky="we")

        ttk.Label(self.frame, text="Dirección:", font=("Helvetica", 14)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.direccion_entry = ttk.Entry(self.frame, font=("Helvetica", 14))
        self.direccion_entry.grid(row=1, column=1, padx=10, pady=5, sticky="we")

        ttk.Label(self.frame, text="Teléfono:", font=("Helvetica", 14)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.telefono_entry = ttk.Entry(self.frame, font=("Helvetica", 14))
        self.telefono_entry.grid(row=2, column=1, padx=10, pady=5, sticky="we")

        ttk.Label(self.frame, text="Email:", font=("Helvetica", 14)).grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.email_entry = ttk.Entry(self.frame, font=("Helvetica", 14))
        self.email_entry.grid(row=3, column=1, padx=10, pady=5, sticky="we")

        self.load_config()

        self.save_button = ttk.Button(self.frame, text="Guardar Configuración", command=self.save_config, style="TButton")
        self.save_button.grid(row=4, column=0, columnspan=2, pady=10, sticky="we")

        self.product_button = ttk.Button(self.frame, text="Ir a Gestión de Productos", command=self.ir_a_gestion_productos, style="TButton")
        self.product_button.grid(row=5, column=0, columnspan=2, pady=10, sticky="we")

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS configuracion_empresa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                direccion TEXT NOT NULL,
                telefono TEXT NOT NULL,
                email TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def load_config(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM configuracion_empresa LIMIT 1")
        config = cursor.fetchone()
        if config:
            self.nombre_entry.insert(0, config[1])
            self.direccion_entry.insert(0, config[2])
            self.telefono_entry.insert(0, config[3])
            self.email_entry.insert(0, config[4])

    def save_config(self):
        nombre = self.nombre_entry.get()
        direccion = self.direccion_entry.get()
        telefono = self.telefono_entry.get()
        email = self.email_entry.get()

        if nombre and direccion and telefono and email:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM configuracion_empresa LIMIT 1")
            config = cursor.fetchone()
            if config:
                cursor.execute("UPDATE configuracion_empresa SET nombre=?, direccion=?, telefono=?, email=? WHERE id=?",
                               (nombre, direccion, telefono, email, config[0]))
            else:
                cursor.execute("INSERT INTO configuracion_empresa (nombre, direccion, telefono, email) VALUES (?, ?, ?, ?)",
                               (nombre, direccion, telefono, email))
            self.conn.commit()
            messagebox.showinfo("Éxito", "Configuración guardada exitosamente.")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

    def ir_a_gestion_productos(self):
        self.root.destroy()
        from productos import GestionProductos
        product_manager_root = tk.Tk()
        GestionProductos(product_manager_root, "admin")  # Puedes cambiar "admin" por "usuario" para probar ambos casos
        product_manager_root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = ConfiguracionEmpresa(root)
    root.mainloop()