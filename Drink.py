from Product import *

class Drink(Product):
    def __init__(self, nombre,precio,alcohol):
        super().__init__(nombre,precio)
        self.alcohol = alcohol

    def show(self):
        super().show()
        print(f"Tipo de bebida: {self.alcohol}")