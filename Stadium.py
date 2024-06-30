import requests
from Restaurant import *
class Stadium:
    def __init__(self,name,id,location,capacity_g,capacity_v,restaurants):
        self.name = name
        self.id=id
        self.location = location
        self.capacity_g = capacity_g
        self.capacity_v = capacity_v
        self.restaurants = restaurants


    def show(self):
        """
    Devuelve una representación en cadena del objeto, mostrando sus atributos.

    Returns:
        str: Una cadena con la información del objeto
    """
        return f"----------------\nStadium Name: {self.name}\n Location: {self.location}\n Capacity: {self.capacity}"
    
    def show_conrest(self):
        """
    Devuelve una representación en cadena del objeto, mostrando sus atributos, añadiendo todos los restaurantes del estadio.

    Returns:
        str: Una cadena con la información del objeto
    """
        return f"----------------\nStadium Name: {self.name}\n Location: {self.location}\n Capacity: {self.capacity}\n restaurantes: {self.restaurants}"
    
    def getCapacidadGeneral(self):
        """
    Devuelve la capacidad general del estadio.

    Returns:
        int: La capacidad general del estadio.
    """
        return self.capacity_g
    
    def getCapacidadVip(self):
        """
    Devuelve la capacidad vip del estadio.

    Returns:
        int: La capacidad vip del estadio.
    """
        return self.capacity_v
    
    def get_name_stadium(self):
        """
    Devuelve el nombre del estadio.

    Returns:
        str: El nombre del estadio.
    """
        return self.name
    
   