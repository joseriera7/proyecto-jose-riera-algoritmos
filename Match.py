from Stadium import *
from Country import*


class Match:
    def __init__(self,m_id,number,home,away,date,stadium,boletos_vendidos,asistencia):
        self.number=number
        self.m_id=m_id
        self.home = home
        self.away = away
        self.date = date
        self.stadium = stadium
        self.taken_g = []
        self.taken_v = []
        self.boletos_vendidos=boletos_vendidos
        self.asistencia=asistencia


    def show(self):
        return f"{self.home.name} vs {self.away.name} el {self.date} en {self.stadium.name}"
    
    def show_sinestadio(self):
        return f"{self.home.name} vs {self.away.name} el {self.date}"
    
    def show_sinfecha(self):
        return f"{self.home.name} vs {self.away.name} en {self.stadium.name}"
    def show_estadio(self):
        return f"{self.stadium}"