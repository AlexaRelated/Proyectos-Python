class Producto:
    def __init__(self, codigo_interno, producto, fecha_caducidad, codigo_barras):
        self.codigo_interno = codigo_interno
        self.producto = producto
        self.fecha_caducidad = fecha_caducidad
        self.codigo_barras = codigo_barras

    def __str__(self):
        return f"Código Interno: {self.codigo_interno}, Producto: {self.producto}, Fecha de Caducidad: {self.fecha_caducidad}, Código de Barras: {self.codigo_barras}"

    def consulta_productos(self):
        cur = self.cnn.cursor()
        cur.execute("SELECT * FROM Producto")
        datos = cur.fetchall()
        cur.close()
        return datos

    def buscar_producto(self, Id):
        cur = self.cnn.cursor()
        sqlite3 = "SELECT * FROM Productos WHERE Id = {}".format(Id)
        cur.execute(sqlite3)
        datos = cur.fetchone()
        cur.close()
        return datos

    def inserta_producto(self, CodigoInterno, Producto, FechaCaducidad, CodigoBarras):
        cur = self.cnn.cursor()
        sqlite3 = '''INSERT INTO Productos (CodigoInterno, Producto, FechaCaducidad, CodigoBarras) 
        VALUES('{}', '{}', '{}', '{}')'''.format(CodigoInterno, Producto, FechaCaducidad, CodigoBarras)
        cur.execute(sqlite3)
        n = cur.rowcount
        self.cnn.commit()
        cur.close()
        return n

    def elimina_producto(self, Id):
        cur = self.cnn.cursor()
        sqlite3 = '''DELETE FROM Productos WHERE Id = {}'''.format(Id)
        cur.execute(sqlite3)
        n = cur.rowcount
        self.cnn.commit()
        cur.close()
        return n

    def modifica_producto(self, Id, CodigoInterno, Producto, FechaCaducidad, CodigoBarras):
        cur = self.cnn.cursor()
        sqlite3 = '''UPDATE Productos SET CodigoInterno='{}', Producto='{}', FechaCaducidad='{}',
        CodigoBarras='{}' WHERE Id={}'''.format(CodigoInterno, Producto, FechaCaducidad, CodigoBarras, Id)
        cur.execute(sqlite3)
        n = cur.rowcount
        self.cnn.commit()
        cur.close()
        return n