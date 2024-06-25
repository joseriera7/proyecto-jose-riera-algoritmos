import requests
import random
from Country import*
from Stadium import*
from Restaurant import *
from Match import*
from Product import *
from Ticket import *


def generar_permutaciones(arr):
    # Genera todas las permutaciones posibles de una lista
        if len(arr) == 0:
            return []
        if len(arr) == 1:
            return [arr]
        perms = []
        for i in range(len(arr)):
            m = arr[i]
            rem_lista = arr[:i] + arr[i+1:]
            for p in generar_permutaciones(rem_lista):
                perms.append([m] + p)
        return perms

def es_vampiro(num):

        num_str = str(num)
        num_len = len(num_str)
        
        # Un número vampiro debe tener un número par de dígitos
        if num_len % 2 != 0:
            return False
        
        # Obtener la mitad del número de dígitos
        half_len = num_len // 2
        
        # Generar todas las combinaciones posibles de la mitad de los dígitos del número
        num_list = list(num_str)
        possible_fangs = set()
        
        permutaciones = generar_permutaciones(num_list)
        for perm in permutaciones:
            fang1 = int("".join(perm[:half_len]))
            fang2 = int("".join(perm[half_len:]))
            
            # Verificar que los factores no terminen ambos en cero
            if not (str(fang1).endswith('0') and str(fang2).endswith('0')):
                possible_fangs.add((fang1, fang2))
        
        # Verificar si alguno de los pares encontrados es un par de colmillos válido
        for fang1, fang2 in possible_fangs:
            if fang1 * fang2 == num:
                return True
        
        return False

class Sistema:
    def __init__(self):
        self.country_list=[]
        self.stadium_list=[]
        self.match_list=[]
        self.ticket_list=[]
        self.products=[]
        self.food=[]
        self.drinks=[]


    def register_all(self,url1,url2,url3):
        self.registrar_equipos(url1)
        self.registrar_estadios(url2)
        self.registrar_partidos(url3)


    def menu(self):
        print("Bienvenido al sistema de la Euro 2024")
        while True:
            opcion_menu = input('¿Que desea hacer?\n1- Busqueda de partidos \n2- Realizar compra de entradas \n3- Busqueda de productos \n4- Chequear entradas \n7- Salir \n====>')
            while opcion_menu not in ['1','2','3','4','7']:
                print("Opcion no valida")
                opcion_menu = input('¿Que desea hacer?\n1- Busqueda de partidos\n2- Realizar compra de entradas \n3- Busqueda de productos \n4- Chequear entradas \n7- Salir \n====>')
            if opcion_menu == '1':
                opcion_busqueda = input('De  que forma desea realizar la busqueda?\n1- Buscar partidos por pais\n2- Buscar partidos por estadio\n3- Buscar partidos por fecha\n4- Regresar===>  ')
                while opcion_busqueda not in ['1','2','3','4']:
                    print("Opcion no valida")
                    opcion_busqueda = input('De  que forma desea realizar la busqueda?\n1- Buscar partidos por pais\n2- Buscar partidos por estadio\n3- Buscar partidos por fecha\n4-Regresar===>  ')  
                if opcion_busqueda == '1':
                    self.buscar_porpais()
                elif opcion_busqueda == '2':
                    self.buscar_porestadio()
                elif opcion_busqueda == '3':
                    self.buscar_porfecha()
                else:
                    pass
            elif opcion_menu=='2':
                self.registrar_venta()
            elif opcion_menu=='3':
                 self.ver_productos()

            elif opcion_menu=='4':
                 self.chequear_entradas()

            else: 
                print('Vuelva pronto!')
                break

    def registrar_equipos(self,url):
        response=requests.get(url)
        if response.status_code == 200:
            data=response.json()
            for team in data:
                team_obj=Country(team['id'], team['name'], team['code'],team['group'])
                self.country_list.append(team_obj)
        else:
             print("Error al obtener los datos de los equipos")
    

    def registrar_estadios(self,url):
        response=requests.get(url)
        
        if response.status_code == 200:
            data=response.json()
            for stadium in data:
                lista_restaurants = []
                for restaurant in stadium['restaurants'] :
                    name_rest=restaurant['name']
                    product_list=[]
                    for product in restaurant['products']:
                        name_prod=product['name']
                        price=product['price']
                        adicional=product['adicional']
                        if adicional in ['plate','package']:
                            tipo='food'
                            product_obj=Product(name_prod,price,tipo,adicional)
                            product_list.append(product_obj)
                        else:
                            tipo='drink'
                            product_obj=Product(name_prod,price,tipo,adicional)
                            product_list.append(product_obj)
                    restaurant_obj=Restaurant(name_rest,product_list)
                    lista_restaurants.append(restaurant_obj)
                match_obj=Stadium(stadium['name'],stadium['id'],stadium['city'],stadium['capacity'],lista_restaurants)
                self.stadium_list.append(match_obj)
        else:
             print('Error al obtener los estadios')
                

    def ver_estadios(self):
        for stadium in self.stadium_list:
            print(stadium.show_conrest())


    def registrar_partidos(self,url):
        response=requests.get(url)
        
        if response.status_code == 200:
            data=response.json()
            for match in data:
                for  stadium in self.stadium_list:
                    if match['stadium_id']== stadium.id:
                        home= Country(match['home']['id'],match['home']['name'],match['home']['code'],match['home']['group'])
                        away= Country(match['away']['id'],match['away']['name'],match['away']['code'],match['away']['group'])
                        match_obj=Match(match['id'],match['number'],home,away,match['date'], stadium)
                        
                        self.match_list.append(match_obj)

        else:
             print('Error al obtener los partidos')
              

    def buscar_porpais(self):
        name=input("Ingresa el nombre del pais: ").capitalize().strip()
        while not name.isalpha():
             print('por favor ingrese un nombre adecuado: ')
             name=input("Ingresa el nombre del pais: ").capitalize().strip()
        cadena_partidos=''
        for match in self.match_list:
            if match.home.name == name or match.away.name == name:
                cadena_partidos += f'{match.show()}\n'
        if cadena_partidos == '':
            return print(f'No se encontraron partidos para el equipo {name}')
        else: return print(f'\nlos partidos de {name} son:\n----------------\n{cadena_partidos}')

    def buscar_porestadio(self):
        print("Seleccione un estadio:")
        for i, estadio in enumerate(self.stadium_list, start=1):
            print(f"{i}. {estadio.name}")
        estadio_idx = (input("Ingrese el número del estadio: "))
        while not estadio_idx.isnumeric() or int(estadio_idx) not in range(0,len(self.stadium_list)) :
            print('por favor ingrese un numero valido')
            estadio_idx = (input("Ingrese el número del estadio: "))
        estadio = self.stadium_list[int(estadio_idx) - 1].name
        cadena_partidos = ''
        for match in self.match_list:
            if match.stadium.name == estadio:
                cadena_partidos += f'{match.show_sinestadio()}\n'
        if cadena_partidos == '':
           return print('No se encontraron partidos en esa fecha')
        else: 
            print(f'\nlos partidos en {estadio} son:\n----------------\n{cadena_partidos}')
        

    def buscar_porfecha(self):
        date=input("Ingresa que dia deseas insertar en 2024-06-__: ").strip()
        while not date.isdigit or int(date) not in range(0,30):
            print('por favor ingrese un numero valido')
            date=input("Ingresa que dia deseas insertar en 2024-06-__: ").strip()
        date=f'2024-06-{date}'
        
        cadena_partidos=''
        for match in self.match_list:
            if match.date == date:
                cadena_partidos += f'{match.show_sinfecha()}\n'
        if cadena_partidos == '':
            return print('No se encontraron partidos en esa fecha')
        else: 
              return print(f'\nlos partidos que hay el {date} son:\n----------------\n {cadena_partidos}')
        
    def registrar_venta(self):
        nombre_cliente=input('ingrese su nombre: ')
        while not nombre_cliente.isalpha():
            print('por favor ingrese un nombre adecuado (solo su nombre)')
            nombre_cliente=input('ingrese su nombre: ')
        apellido_cliente=input('ingrese su apellido: ')
        while not apellido_cliente.isalpha():
            print('por favor ingrese un nombre adecuado')
            apellido_cliente=input('ingrese su apellido: ')
        
        nombre_cliente=nombre_cliente.capitalize().strip()
        apellido_cliente=apellido_cliente.capitalize().strip()
        cedula=input('Ingrese su cedula: ')
        while not cedula.isdigit() or len(cedula)>8 or len(cedula)<5:
            print('por favor ingrese un numero de cedula valido')
            cedula=input('Ingrese su cedula: ')

        edad=input('Ingrese su edad: ')
        while not edad.isdigit() or int(edad) > 80:
            print('por favor ingrese una edad valida')
            edad=input('Ingrese su edad: ')
        print('Que partido desea comprar: ')
        for i, match in enumerate(self.match_list):
            print(f'{i+1}. {match.show()}')
        partido_idx = input("Ingrese el número del partido: ")
        while not partido_idx.isdigit() or int(partido_idx) not in range(1, len(self.match_list)):
            print('por favor ingrese un numero de partido valido')
            partido_idx = input("Ingrese el número del partido: ")
        
        partido_idx = int(partido_idx) - 1
        partido = self.match_list[partido_idx]
        tipo=input('Que tipo de entrada quiere, general(G) o vip (V)?')
        while tipo.upper() not in ['G', 'V']:
            print('por favor ingrese un tipo de entrada valido')
            tipo=input('Que tipo de entrada quiere, general - $35 [G] o vip - $75 [V]?')
        cantidad=input('Cuantas entradas desea?: ')
        while not cantidad.isdigit() or int(cantidad) < 1:
             print('por favor ingrese una cantidad valida')
             cantidad=input('Cuantas entradas desea?: ')
        
        if tipo.upper() == 'V':
            subtotal=75*int(cantidad)
        else:
             subtotal=35*int(cantidad)
        iva=subtotal*0.16
        total=subtotal+iva
        descuento=0
        if es_vampiro(int(cedula)):
            descuento=total*0.5

        total=subtotal+iva-descuento
        entradas=[]
        for entrada in range(1,int(cantidad)+1):
             nro_entrada=random.randint(100000,999999)
             while nro_entrada in entradas:
                 nro_entrada=random.randint(100000,999999)
                 
             entradas.append(nro_entrada)
           


        print(f'''
              ENTRADA
              ---------------
              DATOS DEL CLIENTE
              Nombre: {nombre_cliente} {apellido_cliente}
              Cedula: {cedula}
              ----------------
              Partido: {partido.show()}
              Tipo: {tipo}
              entrada(s): {entradas}
              ----------------
              Subtotal:${subtotal}
              IVA: ${iva}
              Descuento:${descuento} 
              Total: ${total}''')
        
        print('¿Desea comprar la entrada? (S/N)')
        respuesta=input('===>')
        while respuesta.upper() not in ['S', 'N']:
            print('por favor ingrese una respuesta valida')
            respuesta=input('¿Desea comprar la entrada? (S/N)\n ===> ')
        if respuesta.upper() == 'S':
            for i in range(len(entradas)):
                 cliente_obj=Ticket(entradas[i],nombre_cliente+''+apellido_cliente,cedula,edad,partido, False)
                 self.ticket_list.append(cliente_obj)
            print('¡Entrada comprada con exito!')

        

    def ver_ventas(self):
        if len(self.ticket_list) == 0:
            print('No hay entradas vendidas')
        else:
            for ticket in self.ticket_list:
                print(f'"Nombre: {ticket.nombre} Cedula:{ticket.cedula} Edad:{ticket.edad} Entrada Nro: {ticket.numero} chequeado: {ticket.chequeado}')

    
    
    def ver_productos(self):
        print('\nEn cual estadio quiere buscar?:')
        for i, estadio in enumerate((self.stadium_list),1):
            print(f"{i}. {estadio.name}")
        estadio_idx = (input("Ingrese el número del estadio: "))
        while not estadio_idx.isnumeric() or int(estadio_idx) not in range(0,len(self.stadium_list)) :
            print('por favor ingrese un numero valido')
            estadio_idx = (input("\nIngrese el número del estadio: "))
        estadio = self.stadium_list[int(estadio_idx) - 1]
        print('\nEn cual restaurante quiere buscar?:')
        for i, restaurantes in enumerate(estadio.restaurants, start=1):
            print(f"{i}. {restaurantes.name}")
        restaurante_idx = (input("Ingrese el número del restaurante: "))
        while not restaurante_idx.isnumeric() or int(restaurante_idx) not in range(len(estadio.restaurants)):
                print('por favor ingrese un numero valido')
                restaurante_idx = (input("Ingrese el número del restaurante: "))
        restaurante = estadio.restaurants[int(restaurante_idx) - 1]
        opcion_busqueda = input('\nDe  que forma desea realizar la busqueda?\n1- Buscar producto por nombre\n2- Buscar producto por tipo\n3- Buscar producto por rango de precio\n4- Regresar===>  ')
        while opcion_busqueda not in ['1','2','3','4']:
                        print("Opcion no valida")
                        opcion_busqueda = input('De  que forma desea realizar la busqueda?\n1- Buscar producto por nombre\n2- Buscar producto por tipo\n3- Buscar producto por rango de precio\n4- Regresar===>  ') 
        if opcion_busqueda == '1':
             cadena_productos=''
             nombre=input('Que producto quieres buscar?').strip().title()
             for product in restaurante.products:
                  if product.nombre==nombre:
                        cadena_productos += f'{product.show()}\n-----------------\n'
             if cadena_productos == '':
                print('-----------------')
                print('No se encontraron productos con ese nombre')
                print('-----------------')
             else:
                  print(cadena_productos)
                    
        elif opcion_busqueda == '2':
            tipo=input('Que tipo de producto quieres buscar? (food/bebida)').strip().lower()
            while tipo not in ['food', 'bebida']:
                print('por favor ingrese un tipo valido')
                tipo=input('Que tipo de producto quieres buscar? (food/bebida)').strip().lower()
                print('-----------------')
            for product in restaurante.products:
                    if product.tipo==tipo:
                        print(product.show())
                        print('-----------------')
                    
        
        elif opcion_busqueda == '3':
             cadena_productos=''
             min_price=float(input('Precio minimo: '))
             max_price=float(input('Precio maximo: '))
             while min_price > max_price:
                  print('por favor ingrese un rango de precio valido')
                  min_price=float(input('Precio minimo: '))
                  max_price=float(input('Precio maximo: \n'))
             print('-----------------')
             for product in restaurante.products:
                  if min_price <= float(product.precio) and float(product.precio) <= max_price:
                       cadena_productos += f'{product.show()}\n-----------------\n'
             if cadena_productos == '':
                print('No se encontraron productos en ese rango')
                print('-----------------')
             else:
                  print(cadena_productos)

    def buscar_prod_pornombre(self):
        nombre=input('Que producto quieres buscar?').strip().title()
        for product in self.products:
            if product.nombre==nombre:
                        print(product.show())
                        print('-----------------')

    def buscar_prod_portipo(self):
        tipo=input('Que tipo de producto quieres buscar? (food/bebida)').strip().lower()
        while tipo not in ['food', 'bebida']:
            print('por favor ingrese un tipo valido')
            tipo=input('Que tipo de producto quieres buscar? (food/bebida)').strip().lower()
            for product in self.products:
                    if product.tipo==tipo:
                        print(product.show())
                        print('-----------------')

    def chequear_entradas(self):
        while True:
         entrada_revisando=input("Por favor ingrese el numero de entrada a chequear: ").strip()
         while not entrada_revisando.isdigit() or int(entrada_revisando) not in range(100000,999999):
              print('Por favor ingrese un numero de entrada valido')
              entrada_revisando=input("Por favor ingrese el numero de entrada a chequear: ")
         estatus=''
         for entrada in self.ticket_list:
              if int(entrada_revisando) == entrada.numero:
                if entrada.chequeado==False:
                   estatus='Bienvenido a su partido, que disfrute!'
                   entrada.chequeado=True
                   break          
                else:
                     estatus=(f'Ya la entrada {entrada_revisando}  fue revisada, no puede pasar')
                     break
                     
              else:
                   estatus=(f'No hay entrada numero: {entrada_revisando}')
         print(estatus)
         opcion=input('desea registrar otra entrada?(S/N): ').upper()
         while opcion.upper() not in ['S', 'N']:
            print('por favor ingrese una respuesta valida')
            opcion=input('Desea registrar otra entrada (S/N): ')
         if opcion.upper() == 'S':
             pass
         else:
             break
