import requests
from Stadium import *
from Product import *

class Restaurant():
    def __init__(self,name,products):
        self.name = name
        self.products = products

    def mostrar_comida(self):
        """
    Devuelve una representación en cadena del objeto, mostrando los productos en el restaurante.

    Returns:
        str: Una cadena con los productos
    """
        for product in self.food_list:
            print(product.show())

