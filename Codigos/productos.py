import tkinter as tk
from tkinter import ttk, messagebox
from conexion import get_db_connection
from validaciones import Validador

class VistaProductos(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.inputs = {}
        self.id_producto_seleccionado = None  # Guarda el ID si se va a editar
        self.construir_interfaz()
        self.cargar_productos()

    def construir_interfaz(self):
        # Título
        lbl_titulo = ttk.Label(self, text="Gestión de Productos", font=("Segoe UI", 15, "bold"))
        lbl_titulo.pack(anchor=tk.W, pady=(0, 10))

        # -------------------------------------------------------------
        # 1. Formulario de Datos
        # -------------------------------------------------------------
        self.frame_form = ttk.LabelFrame(self, text="Datos del Producto", padding=12)
        self.frame_form.pack(fill=tk.X, pady=(0, 10))

        # Fila 1
        ttk.Label(self.frame_form, text="Cód. Prod (opc):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=4)
        self.inputs["codigo"] = ttk.Entry(self.frame_form, width=12)
        self.inputs["codigo"].grid(row=0, column=1, padx=5, pady=4)

        ttk.Label(self.frame_form, text="Nombre *:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=4)
        self.inputs["nombre"] = ttk.Entry(self.frame_form, width=22)
        self.inputs["nombre"].grid(row=0, column=3, padx=5, pady=4)

        ttk.Label(self.frame_form, text="Cód. Barras (13 dígs) *:").grid(row=0, column=4, sticky=tk.W, padx=5, pady=4)
        self.inputs["barras"] = ttk.Entry(self.frame_form, width=16)
        self.inputs["barras"].grid(row=0, column=5, padx=5, pady=4)

        # Fila 2
        ttk.Label(self.frame_form, text="Stock Disp. *:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=4)
        self.inputs["stock"] = ttk.Entry(self.frame_form, width=12)
        self.inputs["stock"].grid(row=1, column=1, padx=5, pady=4)

        ttk.Label(self.frame_form, text="P. Unitario (S/.) *:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=4)
        self.inputs["precio"] = ttk.Entry(self.frame_form, width=12)
        self.inputs["precio"].grid(row=1, column=3, padx=5, pady=4)

        ttk.Label(self.frame_form, text="Descripción:").grid(row=1, column=4, sticky=tk.W, padx=5, pady=4)
        self.inputs["descripcion"] = ttk.Entry(self.frame_form, width=25)
        self.inputs["descripcion"].grid(row=1, column=5, padx=5, pady=4)

        # -------------------------------------------------------------
        # Botones de Acción (Guardar, Modificar, Eliminar, Limpiar)
        # -------------------------------------------------------------
        frame_botones = ttk.Frame(self.frame_form)
        frame_botones.grid(row=2, column=0, columnspan=7, pady=(10, 0), sticky=tk.E)

        self.btn_guardar = ttk.Button(frame_botones, text="Guardar Nuevo", command=self.guardar_producto)
        self.btn_guardar.pack(side=tk.LEFT, padx=4)

        self.btn_modificar = ttk.Button(frame_botones, text="Modificar Selección", command=self.modificar_producto)
        self.btn_modificar.pack(side=tk.LEFT, padx=4)

        self.btn_eliminar = ttk.Button(frame_botones, text="Eliminar Selección", command=self.eliminar_producto)
        self.btn_eliminar.pack(side=tk.LEFT, padx=4)

        self.btn_limpiar = ttk.Button(frame_botones, text="Limpiar Formulario", command=self.limpiar_formulario)
        self.btn_limpiar.pack(side=tk.LEFT, padx=4)

        # -------------------------------------------------------------
        # 2. Buscador
        # -------------------------------------------------------------
        frame_busqueda = ttk.Frame(self)
        frame_busqueda.pack(fill=tk.X, pady=(5, 8))

        ttk.Label(frame_busqueda, text="Buscar:").pack(side=tk.LEFT, padx=(0, 5))
        self.entry_busqueda = ttk.Entry(frame_busqueda, width=30)
        self.entry_busqueda.pack(side=tk.LEFT, padx=(0, 8))
        self.entry_busqueda.bind("<KeyRelease>", lambda event: self.buscar_productos())

        btn_refrescar = ttk.Button(frame_busqueda, text="Refrescar Tabla", command=self.cargar_productos)
        btn_refrescar.pack(side=tk.RIGHT)

        # -------------------------------------------------------------
        # 3. Tabla (Treeview)
        # -------------------------------------------------------------
        frame_tabla = ttk.Frame(self)
        frame_tabla.pack(fill=tk.BOTH, expand=True)

        columnas = ("id", "codigo", "nombre", "barras", "descripcion", "stock", "precio", "total_vendido")
        self.tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings", selectmode="browse")

        self.tree.heading("id", text="ID")
        self.tree.heading("codigo", text="Cód. Prod")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("barras", text="Cód. Barras")
        self.tree.heading("descripcion", text="Descripción")
        self.tree.heading("stock", text="Stock")
        self.tree.heading("precio", text="P. Unitario")
        self.tree.heading("total_vendido", text="Total Vendido")

        self.tree.column("id", width=45, anchor=tk.CENTER)
        self.tree.column("codigo", width=85, anchor=tk.CENTER)
        self.tree.column("nombre", width=180)
        self.tree.column("barras", width=120, anchor=tk.CENTER)
        self.tree.column("descripcion", width=160)
        self.tree.column("stock", width=70, anchor=tk.E)
        self.tree.column("precio", width=90, anchor=tk.E)
        self.tree.column("total_vendido", width=100, anchor=tk.E)

        scroll_y = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll_y.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Evento: Clic en la tabla para rellenar campos
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_fila)

    # -------------------------------------------------------------
    # Métodos y Acciones
    # -------------------------------------------------------------
    def limpiar_formulario(self):
        """Limpia los campos y desmarca la edición."""
        for entry in self.inputs.values():
            entry.delete(0, tk.END)
        self.id_producto_seleccionado = None
        self.frame_form.configure(text="Datos del Producto")

    def seleccionar_fila(self, event):
        """Toma la fila elegida y coloca los datos en los inputs."""
        seleccion = self.tree.selection()
        if not seleccion:
            return

        item = self.tree.item(seleccion[0])
        valores = item["values"]

        self.id_producto_seleccionado = valores[0]
        self.frame_form.configure(text=f"Editando Producto ID: {self.id_producto_seleccionado}")

        # Rellenar formulario
        self.inputs["codigo"].delete(0, tk.END)
        if valores[1] != "-":
            self.inputs["codigo"].insert(0, valores[1])

        self.inputs["nombre"].delete(0, tk.END)
        self.inputs["nombre"].insert(0, valores[2])

        self.inputs["barras"].delete(0, tk.END)
        self.inputs["barras"].insert(0, valores[3])

        self.inputs["descripcion"].delete(0, tk.END)
        if valores[4] != "-":
            self.inputs["descripcion"].insert(0, valores[4])

        self.inputs["stock"].delete(0, tk.END)
        self.inputs["stock"].insert(0, valores[5])

        # Quitar 'S/. ' para colocar el número limpio en precio
        precio_limpio = str(valores[6]).replace("S/.", "").strip()
        self.inputs["precio"].delete(0, tk.END)
        self.inputs["precio"].insert(0, precio_limpio)

    def validar_entradas(self):
        """Valida que los campos cumplan los formatos requeridos."""
        ok, res_nombre = Validador.es_texto_no_vacio(self.inputs["nombre"].get(), "Nombre")
        if not ok:
            messagebox.showwarning("Atención", res_nombre)
            return None

        ok, res_barras = Validador.es_codigo_barras_ean13(self.inputs["barras"].get())
        if not ok:
            messagebox.showwarning("Atención", res_barras)
            return None

        ok, res_stock = Validador.es_entero_positivo(self.inputs["stock"].get(), "Stock Disponible")
        if not ok:
            messagebox.showwarning("Atención", res_stock)
            return None

        ok, res_precio = Validador.es_decimal_positivo(self.inputs["precio"].get(), "Precio Unitario")
        if not ok:
            messagebox.showwarning("Atención", res_precio)
            return None

        ok, res_codigo = Validador.es_codigo_formato(self.inputs["codigo"].get(), 9, "Código Producto")
        if not ok:
            messagebox.showwarning("Atención", res_codigo)
            return None

        descripcion = self.inputs["descripcion"].get().strip() or None
        return (res_codigo, res_nombre, res_barras, descripcion, res_stock, res_precio)

    def guardar_producto(self):
        datos = self.validar_entradas()
        if not datos:
            return

        res_codigo, res_nombre, res_barras, descripcion, res_stock, res_precio = datos

        conn = get_db_connection()
        if not conn:
            messagebox.showerror("Error", "Sin conexión con la base de datos.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Producto (Codigo_producto, nombre_P, Codigo_barra_P, Descripcion_P, Stock_disponible, UnitPrice, TotalVendido)
                VALUES (?, ?, ?, ?, ?, ?, 0.00)
            """, (res_codigo, res_nombre, res_barras, descripcion, res_stock, res_precio))
            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Producto agregado exitosamente.")
            self.limpiar_formulario()
            self.cargar_productos()
        except Exception as e:
            conn.close()
            messagebox.showerror("Error SQL", f"No se pudo guardar:\n{e}")

    def modificar_producto(self):
        """Actualiza el producto actualmente seleccionado."""
        if not self.id_producto_seleccionado:
            messagebox.showwarning("Atención", "Selecciona primero un producto de la tabla para modificarlo.")
            return

        datos = self.validar_entradas()
        if not datos:
            return

        res_codigo, res_nombre, res_barras, descripcion, res_stock, res_precio = datos

        conn = get_db_connection()
        if not conn:
            messagebox.showerror("Error", "Sin conexión con la base de datos.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Producto 
                SET Codigo_producto = ?, nombre_P = ?, Codigo_barra_P = ?, Descripcion_P = ?, Stock_disponible = ?, UnitPrice = ?
                WHERE ID_producto = ?
            """, (res_codigo, res_nombre, res_barras, descripcion, res_stock, res_precio, self.id_producto_seleccionado))
            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Producto modificado exitosamente.")
            self.limpiar_formulario()
            self.cargar_productos()
        except Exception as e:
            conn.close()
            messagebox.showerror("Error SQL", f"No se pudo modificar:\n{e}")

    def eliminar_producto(self):
        """Elimina el producto seleccionado."""
        if not self.id_producto_seleccionado:
            messagebox.showwarning("Atención", "Selecciona un producto de la tabla para eliminarlo.")
            return

        confirmar = messagebox.askyesno("Confirmar Eliminación", "¿Seguro que deseas eliminar este producto?")
        if not confirmar:
            return

        conn = get_db_connection()
        if not conn:
            messagebox.showerror("Error", "Sin conexión con la base de datos.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Producto WHERE ID_producto = ?", (self.id_producto_seleccionado,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
            self.limpiar_formulario()
            self.cargar_productos()
        except Exception as e:
            conn.close()
            messagebox.showerror("Error SQL", f"No se pudo eliminar (puede tener ventas o movimientos vinculados):\n{e}")

    def cargar_productos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = get_db_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT ID_producto, Codigo_producto, nombre_P, Codigo_barra_P, Descripcion_P, Stock_disponible, UnitPrice, TotalVendido 
                FROM Producto
                ORDER BY ID_producto DESC
            """)
            rows = cursor.fetchall()
            for r in rows:
                self.tree.insert("", tk.END, values=(
                    r[0],
                    r[1] or "-",
                    r[2],
                    r[3],
                    r[4] or "-",
                    r[5],
                    f"S/. {r[6]:.2f}",
                    f"S/. {(r[7] or 0):.2f}"
                ))
            conn.close()
        except Exception as e:
            conn.close()
            messagebox.showerror("Error SQL", f"Error al leer datos:\n{e}")

    def buscar_productos(self):
        criterio = self.entry_busqueda.get().strip().lower()
        for item in self.tree.get_children():
            valores = [str(v).lower() for v in self.tree.item(item, "values")]
            if any(criterio in val for val in valores):
                self.tree.reattach(item, "", tk.END)
            else:
                self.tree.detach(item)