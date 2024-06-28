class Ticket:
    def __init__(self,numero, nombre, cedula, edad,partido,chequeado,tipo,gasto):
        self.numero = numero
        self.nombre = nombre
        self.cedula = cedula
        self.edad = edad
        self.partido = partido
        self.chequeado=chequeado
        self.tipo=tipo
        self.gasto=gasto

    def show(self):
        print(f"Nombre: {self.nombre} Cedula:{self.cedula} Edad:{self.edad} Partido")
    
    def getname_estadio(self):
        return self.partido.show_estadio()