class Product:
    def __init__(self, nombre,precio, tipo, adicional,stock,vendido):
        self.nombre = nombre
        self.precio = precio
        self.tipo = tipo
        self.adicional = adicional
        self.stock = stock
        self.vendido = vendido

    def show(self):
        """
    Devuelve una representación en cadena del objeto, mostrando sus atributos.

    Returns:
        str: Una cadena con la información del objeto
    """
        return f"Nombre: {self.nombre} \nPrecio: {self.precio}$ \nTipo: {self.tipo}\nAdicional: {self.adicional}"
