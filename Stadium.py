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
        return f"----------------\nStadium Name: {self.name}\n Location: {self.location}\n Capacity: {self.capacity}"
    
    def show_conrest(self):
        return f"----------------\nStadium Name: {self.name}\n Location: {self.location}\n Capacity: {self.capacity}\n restaurantes: {self.restaurants}"
    
    def getCapacidadGeneral(self):
        return self.capacity_g
    
    def getCapacidadVip(self):
        return self.capacity_v
    
    def get_name_stadium(self):
        return self.name
    
   