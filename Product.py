class Product:
    def __init__(self, nombre,precio, tipo, adicional,stock):
        self.nombre = nombre
        self.precio = precio
        self.tipo = tipo
        self.adicional = adicional
        self.stock = stock

    def show(self):
        return f"Nombre: {self.nombre} \nPrecio: {self.precio} \nTipo: {self.tipo}\nAdicional: {self.adicional}"

    def show_bebida(self):
        return f"Nombre: {self.nombre}\n Precio: {self.precio}\n Tipo: {self.tipo}\nAdicional: {self.adicional}"
    
    def show_comida(self):
        return f"Nombre: {self.nombre}\n Precio: {self.precio}\n Tipo: {self.tipo}\nAdicional: {self.adicional} "
