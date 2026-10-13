import tkinter as tk
from tkinter import ttk
from productos import VistaProductos

# NOTA: A medida que creemos productos.py, proveedores.py, etc.,
# descomentaremos los imports reales. Por ahora usa vistas provisionales
# para que puedas ejecutar main.py inmediatamente y ver la interfaz.

class InventarioApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión de Inventarios y Ventas")
        self.geometry("1100x680")
        self.minsize(950, 600)

        # Configuración de estilos visuales
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self._configurar_estilos()

        # Construcción de la distribución visual
        self.crear_layout()

    def _configurar_estilos(self):
        self.style.configure(".", font=("Segoe UI", 10))
        self.style.configure("Sidebar.TFrame", background="#1e293b")
        self.style.configure(
            "Menu.TButton",
            font=("Segoe UI", 10, "bold"),
            background="#334155",
            foreground="#ffffff"
        )
        self.style.map("Menu.TButton", background=[("active", "#475569")])
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        self.style.configure("Treeview", rowheight=26)

    def crear_layout(self):
        # 1. Menú lateral (Sidebar)
        self.sidebar = ttk.Frame(self, style="Sidebar.TFrame", width=220)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        lbl_titulo = tk.Label(
            self.sidebar,
            text="MI SISTEMA",
            bg="#1e293b",
            fg="#38bdf8",
            font=("Segoe UI", 14, "bold"),
            pady=20
        )
        lbl_titulo.pack(fill=tk.X)

        # Botones de navegación
        opciones = [
            ("1. Productos", lambda: self.cambiar_vista("Productos")),
            ("2. Proveedores", lambda: self.cambiar_vista("Proveedores")),
            ("3. Registrar Venta", lambda: self.cambiar_vista("Ventas")),
            ("4. Mov. Inventario", lambda: self.cambiar_vista("Movimientos")),
            ("5. Estadísticas", lambda: self.cambiar_vista("Estadísticas")),
            ("6. Salir", self.destroy)
        ]

        for texto, comando in opciones:
            btn = ttk.Button(self.sidebar, text=texto, style="Menu.TButton", command=comando)
            btn.pack(fill=tk.X, padx=12, pady=5)

        # 2. Contenedor dinámico (donde se montan las pantallas secundarias)
        self.contenedor_vistas = ttk.Frame(self)
        self.contenedor_vistas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Vista inicial por defecto
        self.cambiar_vista("Productos")

    def limpiar_contenedor(self):
        """Elimina la vista actual antes de montar la siguiente."""
        for widget in self.contenedor_vistas.winfo_children():
            widget.destroy()

    def cambiar_vista(self, nombre_modulo):
        """Gestiona el reemplazo de módulos en el contenedor."""
        self.limpiar_contenedor()

        # Al quitarle los comentarios a este bloque, ya carga productos.py:
        if nombre_modulo == "Productos":
            from productos import VistaProductos
            vista = VistaProductos(self.contenedor_vistas)
            vista.pack(fill=tk.BOTH, expand=True)
            return

        # Vista esqueleto mientras se van implementando los demás archivos:
        lbl = ttk.Label(
            self.contenedor_vistas,
            text=f"Módulo: {nombre_modulo}",
            font=("Segoe UI", 16, "bold")
        )
        lbl.pack(anchor=tk.W, pady=10)

        sub_lbl = ttk.Label(
            self.contenedor_vistas,
            text=f"Aquí se cargará la interfaz de {nombre_modulo.lower()}.py.",
            font=("Segoe UI", 11)
        )
        sub_lbl.pack(anchor=tk.W)

if __name__ == "__main__":
    app = InventarioApp()
    app.mainloop()