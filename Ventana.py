from tkinter import *
import sqlite3
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pip
from Producto import Producto


class Ventana(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master, width=1000, height=400)
        self.master = master
        self.pack()
        self.create_widgets()
        self.mostrar_productos()

    def mostrar_productos(self):
        conexion = sqlite3.connect('base_caducidad.db')
        cursor = conexion.cursor()

        cursor.execute("SELECT id, codigo_interno, producto, fecha_caducidad, codigo_barras FROM productos")
        productos = cursor.fetchall()
    
        for producto in productos:
        # Insertar los valores en el orden correcto
            id_producto, codigo_interno, producto_nombre, fecha_caducidad, codigo_barras = producto
            self.grid.insert("", END, values=(id_producto, codigo_interno, producto_nombre, fecha_caducidad, codigo_barras))

        conexion.close()

    def create_widgets(self):

  # Cargar el logo
        logo_image = PhotoImage(file="C:\\Users\\Alexa\\OneDrive\\Escritorio\\Proyectos Python\\CADUCIDADES MARVIMUNDO\\logo.gif")  
        logo_image = logo_image.subsample(3)

          # Mostrar el logo en un Label y ubicarlo en la esquina superior izquierda de la ventana
        logo_label = Label(self, image=logo_image)
        logo_label.image = logo_image  # ¡IMPORTANTE! - Esto evita que la imagen sea eliminada por el recolector de basura de Python
        logo_label.place(x=0, y=0)

        logo_label.lift()

        # botones laterales
        frame1 = Frame(self, bg="#98FB98")
        frame1.place(x=0, y=0, width=93, height=259)
        frame1.lower()

        self.btnModificar = Button(frame1, text="Modificar", command=self.fModificar, bg="green", fg="white")
        self.btnModificar.place(x=5, y=100, width=80, height=30)

        self.btnEliminar = Button(frame1, text="Eliminar", command=self.fEliminar, bg="green", fg="white")
        self.btnEliminar.place(x=5, y=150, width=80, height=30)

        # cajas para ingresar datos
        frame2 = Frame(self, bg="#F5FFFA")
        frame2.place(x=95, y=0, width=150, height=259)

        lbl1 = Label(frame2, text="Código Interno")
        lbl1.place(x=3, y=5)
        self.txtCodigoInterno = Entry(frame2)
        self.txtCodigoInterno.place(x=3, y=25, width=100, height=20)

        lbl2 = Label(frame2, text="Producto")
        lbl2.place(x=3, y=55)
        self.txtProducto = Entry(frame2)
        self.txtProducto.place(x=3, y=75, width=100, height=20)

        lbl3 = Label(frame2, text="Fecha Caducidad")
        lbl3.place(x=3, y=105)
        self.txtFechaCaducidad = Entry(frame2)
        self.txtFechaCaducidad.place(x=3, y=125, width=100, height=20)

        lbl4 = Label(frame2, text="Código de Barras")
        lbl4.place(x=3, y=155)
        self.txtCodigodeBarras = Entry(frame2)
        self.txtCodigodeBarras.place(x=3, y=175, width=100, height=20)

        self.btnGuardar = Button(frame2, text="Guardar", command=self.fGuardar)
        self.btnGuardar.place(x=10, y=210, width=60, height=30)

        self.btnCancelar = Button(frame2, text="Cancelar", command=self.fCancelar)
        self.btnCancelar.place(x=80, y=210, width=60, height=30)

        # ventana derecha donde se muestran los datos
        self.grid = ttk.Treeview(self, columns = ("col1", "col2", "col3", "col4"))
        
        
     #creating the headings for the table

        self.grid.column("#0", width=20)
        self.grid.column("col1", width=60, anchor=CENTER)
        self.grid.column("col2", width=90, anchor=CENTER)
        self.grid.column("col3", width=90, anchor=CENTER)
        self.grid.column("col4", width=90, anchor=CENTER)

        # ventana derecha donde se muestran los datos nombre de columnas
        self.grid.heading("#0", text="Id", anchor=CENTER)
        self.grid.heading("col1", text="Código Interno", anchor=CENTER)
        self.grid.heading("col2", text="Producto", anchor=CENTER)
        self.grid.heading("col3", text="Fecha Caducidad", anchor=CENTER)
        self.grid.heading("col4", text="Código de Barras", anchor=CENTER)

        
        self.grid.place(x=247, y=0, width=600, height=259)
        self.grid.bind("<Double-1>", self.mostrar_detalles_producto)  # Evento de doble clic en la lista de productos

    def fModificar(self, *args, **kwargs):
        # Obtener el índice del elemento seleccionado en la lista de productos
        seleccion = self.grid.selection()
    
    # Verificar si se ha seleccionado un elemento
        if seleccion:
        # Obtener los datos del producto seleccionado
            producto_seleccionado = self.grid.item(seleccion)
            codigo_interno = producto_seleccionado['values'][0]
            producto = producto_seleccionado['values'][1]
            fecha_caducidad = producto_seleccionado['values'][2]
            codigo_barras = producto_seleccionado['values'][3]

        # Llenar los campos de entrada con los datos del producto seleccionado
            self.txtCodigoInterno.delete(0, tk.END)
            self.txtCodigoInterno.insert(0, codigo_interno)
            self.txtProducto.delete(0, tk.END)
            self.txtProducto.insert(0, producto)
            self.txtFechaCaducidad.delete(0, tk.END)
            self.txtFechaCaducidad.insert(0, fecha_caducidad)
            self.txtCodigodeBarras.delete(0, tk.END)
            self.txtCodigodeBarras.insert(0, codigo_barras)

        # Cambiar el texto del botón Guardar para indicar que se están realizando modificaciones
            self.btnGuardar.config(text="Guardar Cambios", command=self.guardar_cambios)
            
        else:
        # Si no se ha seleccionado ningún producto, mostrar un mensaje de advertencia
            messagebox.showwarning("Advertencia", "Por favor, selecciona un producto para modificar.")

            
    def fEliminar(self):
    # Obtener el índice del elemento seleccionado en la lista de productos
        seleccion = self.grid.selection()
    
    # Verificar si se ha seleccionado un elemento
        if seleccion:
        # Obtener el ID del producto seleccionado
            id_producto = self.grid.item(seleccion)['values'][0]

        # Conectar a la base de datos
            conexion = sqlite3.connect('base_caducidad.db')
            cursor = conexion.cursor()

        # Ejecutar la consulta SQL DELETE
            cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))

        # Confirmar la eliminación
            conexion.commit()

        # Cerrar la conexión
            conexion.close()

        # Actualizar la vista de la lista de productos (opcional)
            self.mostrar_productos()
        else:
        # Si no se ha seleccionado ningún producto, mostrar un mensaje de advertencia
            messagebox.showwarning("Advertencia", "Por favor, selecciona un producto para eliminar.")

    def guardar_cambios(self):
    # Obtener los nuevos datos del producto desde los campos de entrada
        nuevo_codigo_interno = self.txtCodigoInterno.get()
        nuevo_producto = self.txtProducto.get()
        nueva_fecha_caducidad = self.txtFechaCaducidad.get()
        nuevo_codigo_barras = self.txtCodigodeBarras.get()

    # Obtener el índice del elemento seleccionado en la lista de productos
        seleccion = self.grid.selection()

    # Verificar si se ha seleccionado un elemento
        if seleccion:
            try:
            # Obtener el ID del producto seleccionado
                id_producto = self.grid.item(seleccion)['values'][0]

            # Imprimir los datos antes de ejecutar la consulta SQL (para debugging)
                print("ID del producto:", id_producto)
                print("Nuevos valores:", nuevo_codigo_interno, nuevo_producto, nueva_fecha_caducidad, nuevo_codigo_barras)

            # Conectar a la base de datos
                conn = sqlite3.connect('base_caducidad.db')
                cursor = conn.cursor()

            # Ejecutar la consulta SQL UPDATE para modificar los datos del producto
                cursor.execute("UPDATE productos SET codigo_interno = ?, producto = ?, fecha_caducidad = ?, codigo_barras = ? WHERE id = ?", (nuevo_codigo_interno, nuevo_producto, nueva_fecha_caducidad, nuevo_codigo_barras, id_producto))

            # Confirmar los cambios
                conn.commit()
                messagebox.showinfo("Éxito", "Los cambios se han guardado correctamente.")


            except sqlite3.Error as e:
                messagebox.showerror("Error", f"No se pudieron guardar los cambios: {e}")
                
            finally:
            # Cerrar la conexión
                conn.close()

            # Limpiar los campos de entrada después de modificar el producto
                self.txtCodigoInterno.delete(0, tk.END)
                self.txtProducto.delete(0, tk.END)
                self.txtFechaCaducidad.delete(0, tk.END)
                self.txtCodigodeBarras.delete(0, tk.END)

            # Actualizar la vista de la lista de productos (opcional)
                self.mostrar_productos()
        else:
        # Si no se ha seleccionado ningún producto, mostrar un mensaje de advertencia
            messagebox.showwarning("Advertencia", "Por favor, selecciona un producto para guardar los cambios.")
        
    def mostrar_detalles_producto(self, event):
        item_seleccionado = self.grid.selection()  # Obtener el elemento seleccionado
        if item_seleccionado:
            # Obtener los datos del producto seleccionado
            id, codigo_interno, producto, fecha_caducidad, codigo_barras = self.grid.item(item_seleccionado, 'values')

            # Simula datos adicionales del producto (puedes obtenerlos de la base de datos si los tienes)
            uso_producto = "Uso del producto: Este producto se utiliza para..."
            otros_detalles = "Otros detalles del producto: Lorem ipsum..."

            
            # Crear una ventana para mostrar los detalles del producto
            detalles_ventana = tk.Toplevel(self)
            detalles_ventana.title("Detalles del Producto")

            # Mostrar los detalles del producto en la nueva ventana
            detalles_frame = tk.Frame(detalles_ventana)
            detalles_frame.pack(padx=20, pady=10)

            tk.Label(detalles_frame, text="ID:").grid(row=0, column=0, sticky="w")
            tk.Label(detalles_frame, text=id).grid(row=0, column=1, sticky="w")
            tk.Label(detalles_frame, text="Código Interno:").grid(row=1, column=0, sticky="w")
            tk.Label(detalles_frame, text=codigo_interno).grid(row=1, column=1, sticky="w")
            tk.Label(detalles_frame, text="Producto:").grid(row=2, column=0, sticky="w")
            tk.Label(detalles_frame, text=producto).grid(row=2, column=1, sticky="w")
            tk.Label(detalles_frame, text="Fecha Caducidad:").grid(row=3, column=0, sticky="w")
            tk.Label(detalles_frame, text=fecha_caducidad).grid(row=3, column=1, sticky="w")
            tk.Label(detalles_frame, text="Código de Barras:").grid(row=4, column=0, sticky="w")
            tk.Label(detalles_frame, text=codigo_barras).grid(row=4, column=1, sticky="w")
        
        # Mostrar detalles adicionales
            tk.Label(detalles_frame, text="Detalles adicionales:").grid(row=4, column=0, sticky="w")
            tk.Label(detalles_frame, text=uso_producto).grid(row=5, column=0, columnspan=2, sticky="w")
            tk.Label(detalles_frame, text=otros_detalles).grid(row=6, column=0, columnspan=2, sticky="w")
        
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un producto para ver detalles.")
    
    
    def fGuardar(self):
    # Obtener los datos de la interfaz gráfica
        codigo_interno = self.txtCodigoInterno.get()
        producto = self.txtProducto.get()
        fecha_caducidad = self.txtFechaCaducidad.get()
        codigo_barras = self.txtCodigodeBarras.get()

    # Conectar a la base de datos
        conn = sqlite3.connect('base_caducidad.db')
        cursor = conn.cursor()

    # Verificar si el producto ya existe en la base de datos
        cursor.execute("SELECT * FROM productos WHERE codigo_interno = ?", (codigo_interno,))
        existing_product = cursor.fetchone()
        if existing_product:
        # Si el producto ya existe, mostrar un mensaje de advertencia
            messagebox.showwarning("Advertencia", "El producto ya existe en la base de datos.")
        else:
        # Si el producto no existe, insertarlo en la base de datos
            consulta = "INSERT INTO productos (codigo_interno, producto, fecha_caducidad, codigo_barras) VALUES (?, ?, ?, ?)"
            cursor.execute(consulta, (codigo_interno, producto, fecha_caducidad, codigo_barras))

        # Guardar los cambios y cerrar la conexión
        conn.commit()
        conn.close()

        # Limpiar los campos de entrada después de agregar el registro
        self.txtCodigoInterno.delete(0, 'end')  
        self.txtProducto.delete(0, 'end')        
        self.txtFechaCaducidad.delete(0, 'end')  
        self.txtCodigodeBarras.delete(0, 'end')
   

    def fCancelar(self):
        pass

   

    def verificar_productos(self):
        hoy = datetime.now()
        alerta_fecha = hoy + timedelta(days=4 * 30)  # 4 meses de antelación

        productos_caducar = [producto for producto in self.productos if producto["caducidad"] <= alerta_fecha]

        if productos_caducar:
            mensaje = "Productos a punto de caducar:\n\n"
            for producto in productos_caducar:
                mensaje += f"{producto['nombre']} - Caduca el {producto['caducidad'].strftime('%d/%m/%Y')}\n"

            messagebox.showinfo("Notificación de Productos", mensaje)

        # Agregar más lógica

        # Verificar cada día (86400 segundos = 1 día)
        self.master.after(86400000, self.verificar_productos)