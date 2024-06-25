import requests
from Stadium import *
from Product import *

class Restaurant():
    def __init__(self,name,products):
        self.name = name
        self.products = products

    def mostrar_comida(self):
        for product in self.food_list:
            print(product.show_comida())

