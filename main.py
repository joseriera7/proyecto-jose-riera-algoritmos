from Sistema import *
from Stadium import *

prueba= Sistema()
url_equipos='https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/teams.json'
url_estadios='https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json'
url_partidos='https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/matches.json'

prueba.register_all(url_equipos,url_estadios,url_partidos)
prueba.menu()