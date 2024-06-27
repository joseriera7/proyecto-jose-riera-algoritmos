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
        

        if num_len % 2 != 0:
            return False
        
       
        half_len = num_len // 2
        
        
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
def es_perfecto(num):
    suma = []
    for i in range(1, num):
        if num % i == 0:
            suma.append(i)
    if sum(suma) == num:
        return True
    else:
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
            opcion_menu = input('¿Que desea hacer?\n1- Busqueda de partidos \n2- Realizar compra de entradas \n3- Busqueda de productos \n4- Chequear entradas \n5- Comprar productos \n7- Salir \n====>')
            while opcion_menu not in ['1','2','3','4','5','7']:
                print("Opcion no valida")
                opcion_menu = input('¿Que desea hacer?\n1- Busqueda de partidos\n2- Realizar compra de entradas \n3- Busqueda de productos \n4- Chequear entradas \n5- Comprar productos \n7- Salir \n====>')
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
                self.registrar_entradas()
            elif opcion_menu=='3':
                 self.ver_productos()

            elif opcion_menu=='4':
                 self.chequear_entradas()

            elif opcion_menu=='5':
                 self.venta_productos()

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
                        stock=product['stock']
                        if adicional in ['plate','package']:
                            tipo='food'
                            product_obj=Product(name_prod,price,tipo,adicional,stock)
                            product_list.append(product_obj)
                        else:
                            tipo='drink'
                            product_obj=Product(name_prod,price,tipo,adicional,stock)
                            product_list.append(product_obj)
                    restaurant_obj=Restaurant(name_rest,product_list)
                    lista_restaurants.append(restaurant_obj)
                match_obj=Stadium(stadium['name'],stadium['id'],stadium['city'],stadium['capacity'][0],stadium['capacity'][1],lista_restaurants)
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
                for stadium in self.stadium_list:
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
        
    def mostrarAsientosGeneral(self,partido):
            
            diccionario = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8 : 'I', 9 : 'J'}
            total = partido.stadium.getCapacidadGeneral()
            filas = total // 10
            resto = total % 10
            for i in range(len(diccionario)):
                if i == 0:
                    print('  ', end='| ')
                print(diccionario[i], end='  | ')
            print('\n')
            for i in range(filas + 1):
                if i == filas:
                    print(i +1, end= '| ')
                    for j in range(resto):
                        if f'{diccionario[j]}{i+1}' not in partido.taken_g:
                            print(0, end='    ')
                        else: print('X', end='    ')
                    print('\n')
                elif i < 9:
                    print(i +1, end= ' | ')
                    for j in range(10):
                        if f'{diccionario[j]}{i+1}' not in partido.taken_g:
                            print(0, end='    ')
                        else: print('X', end='    ')
                    print('\n')
                
                else:
                    print(i +1, end= '| ')
                    for j in range(10):
                        if f'{diccionario[j]}{i+1}' not in partido.taken_g:
                            print(0, end='    ')
                        else: print('X', end='    ')
                    print('\n')
    def mostrarAsientosVip(self,partido):
            
            diccionario = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8 : 'I', 9 : 'J'}
            total = partido.stadium.getCapacidadVip()
            filas = total // 10
            resto = total % 10
            for i in range(len(diccionario)):
                if i == 0:
                    print('  ', end='| ')
                print(diccionario[i], end='  | ')
            print('\n')
            for i in range(filas + 1):
                if i == filas:
                    print(i +1, end= '| ')
                    for j in range(resto):
                        if f'{diccionario[j]}{i+1}' not in partido.taken_v:
                            print(0, end='    ')
                        else: print('X', end='    ')
                    print('\n')
                elif i < 9:
                    print(i +1, end= ' | ')
                    for j in range(10):
                        if f'{diccionario[j]}{i+1}' not in partido.taken_v:
                            print(0, end='    ')
                        else: print('X', end='    ')
                    print('\n')
                
                else:
                    print(i +1, end= '| ')
                    for j in range(10):
                        if f'{diccionario[j]}{i+1}' not in partido.taken_v:
                            print(0, end='    ')
                        else: print('X', end='    ')
                    print('\n')
            
                    
            
    def registrar_entradas(self):
        """
    Registra una entrada para un partido de fútbol.

    Este método solicita al usuario que ingrese sus datos personales, seleccione un partido
    y un tipo de entrada (general o VIP), y especifique la cantidad de entradas que desea
    comprar. Luego, asigna asientos disponibles para cada entrada y muestra un resumen de
    la compra.

    El método también aplica un descuento del 50% para los clientes con numero de cedula vampiros.

    Parámetros:
    Ninguno

    Retorna:
    Ninguno
    """
        asientos=[]
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
            tipo='V'
            subtotal=75*int(cantidad)
        else:
             tipo='G'
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
        
        asientos=[]
        for entrada in range(1,int(cantidad)+1):
            if tipo.upper()=='G':
                print("------------------------")
                print("Entrada: ",entrada)
                self.mostrarAsientosGeneral(partido)
                while True:
                    asiento_fila=input('En que fila desea comprar?: ')
                    while not asiento_fila.isnumeric and  int(asiento_fila) not in range(1,(partido.stadium.getCapacidadGeneral()//10)+2):
                        print('Escoja una fila existente')
                        asiento_fila=input('En que fila desea comprar?: ')
                    asiento_columna=input('En que columna desea comprar?: ').upper()
                    while asiento_columna not in ["A","B","C","D","E","F","G","H","I","J"]:
                        print('Escoja una columna existente')
                        asiento_columna=input('En que columna desea comprar?: ').upper()
                    asiento=f'{asiento_columna}{asiento_fila}'
                    if asiento in partido.taken_g:
                        print('Este asiento ya esta ocupado')
                        continue
                    else:
                        asientos.append(asiento)
                        partido.taken_g.append(asiento)
                        print(f'Asiento {asiento} reservado')
                        break
            else:
                print("------------------------")
                print("Entrada: ",entrada)
                self.mostrarAsientosVip(partido)
                while True:
                    asiento_fila=input('En que fila desea comprar?: ')
                    while not asiento_fila.isnumeric and  int(asiento_fila) not in range(1,(partido.stadium.getCapacidadVip()//10)+2):
                        print('Escoja una fila existente')
                        asiento_fila=input('En que fila desea comprar?: ')
                    asiento_columna=input('En que columna desea comprar?: ').upper()
                    while asiento_columna not in ["A","B","C","D","E","F","G","H","I","J"]:
                        print('Escoja una columna existente')
                        asiento_columna=input('En que columna desea comprar?: ').upper()
                    asiento=f'{asiento_columna}{asiento_fila}'
                    if asiento in partido.taken_v:
                        print('Este asiento ya esta ocupado')
                        continue
                    else:
                        asientos.append(asiento)
                        partido.taken_v.append(asiento)
                        print(f'Asiento {asiento} reservado')
                        break


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
              asiento(s): {asientos}
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
                 cliente_obj=Ticket(entradas[i],f'{nombre_cliente} {apellido_cliente}',cedula,edad,partido, False,tipo)
                 self.ticket_list.append(cliente_obj)
            print('¡Entrada comprada con exito!')

        else:
            for asiento in asientos:
                if tipo.upper() == 'V':
                    self.taken_v.pop(asiento)
                else:
                    self.taken_g.pop(asiento)
            print('¡Operacion cancelada!')


        

    def ver_ventas(self):
        if len(self.ticket_list) == 0:
            print('No hay entradas vendidas')
        else:
            for ticket in self.ticket_list:
                print(f'"Nombre: {ticket.nombre} Cedula:{ticket.cedula} Edad:{ticket.edad} Entrada Nro: {ticket.numero} chequeado: {ticket.chequeado}')

    
    
    def ver_productos(self):
        """
    Description:
    Muestra un menú para buscar productos en los restaurantes de un estadio.

    El método primero muestra una lista de estadios disponibles y solicita al usuario
    que ingrese el número del estadio deseado. Luego, muestra una lista de restaurantes
    disponibles en ese estadio y solicita al usuario que ingrese el número del restaurante
    deseado.

    Una vez seleccionado el restaurante, el método proporciona cuatro opciones de búsqueda:
    buscar productos por nombre, buscar productos por tipo (comida o bebida), buscar productos
    por rango de precio y regresar al menú anterior.

    Dependiendo de la opción seleccionada, el método solicita al usuario que ingrese
    la información necesaria para realizar la búsqueda y muestra los resultados
    correspondientes.

    Parameters:
    Ninguno

    Returns:
    Ninguno """
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
        """
    Busca un producto por nombre en la lista de productos.

    Description:
    Pide al usuario que ingrese el nombre del producto que desea buscar.
    Itera sobre la lista de productos y muestra el producto que coincide con el nombre
    ingresado.

    Parameters:
    self (object): Instancia de la clase que contiene la lista de productos (products)

    Returns:
    None
    """
        nombre=input('Que producto quieres buscar?').strip().title()
        for product in self.products:
            if product.nombre==nombre:
                        print(product.show())
                        print('-----------------')

    def buscar_prod_portipo(self):
        """
    Busca productos por tipo (food o drink) en la lista de productos.

    Description:
    Pide al usuario que ingrese el tipo de producto que desea buscar (food o drink).
    Verifica que el tipo ingresado sea válido y luego itera sobre la lista de productos
    para mostrar los productos que coinciden con el tipo seleccionado.

    Parameters:
    self (object): Instancia de la clase que contiene la lista de productos (products)

    """
        tipo=input('Que tipo de producto quieres buscar? (food/bebida)').strip().lower()
        while tipo not in ['food', 'bebida']:
            print('por favor ingrese un tipo valido')
            tipo=input('Que tipo de producto quieres buscar? (food/bebida)').strip().lower()
            for product in self.products:
                    if product.tipo==tipo:
                        print(product.show())
                        print('-----------------')

    def chequear_entradas(self):
        """
        Chequea las entradas de un partido y permite registrar nuevas entradas.

        Parameters:
        self (object): Instancia de la clase que contiene la lista de entradas (ticket_list)

        Description:
        Pide al usuario que ingrese un número de entrada y verifica si es válido.
        Si la entrada existe y no ha sido revisada anteriormente, la marca como revisada
        y muestra un mensaje de bienvenida. Si la entrada ya fue revisada, muestra un
        mensaje indicando que no puede pasar.

        Continúa pidiendo entradas hasta que el usuario decida salir.

        """
        while True:
         entrada_revisando=input("Por favor ingrese el numero de entrada a chequear: ").strip()
         while not entrada_revisando.isdigit() or int(entrada_revisando) not in range(100000,999999):
              print('Por favor ingrese un numero de entrada valido')
              entrada_revisando=input("Por favor ingrese el numero de entrada a chequear: ")
         estatus=(f'No hay entrada numero: {entrada_revisando}')
         for entrada in self.ticket_list:
              if int(entrada_revisando) == entrada.numero:
                if entrada.chequeado==False:
                   entrada.chequeado=True
                   estatus='Bienvenido a su partido, que disfrute!'
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

    def venta_productos(self):
        """Gestiona la venta de productos para usuarios con tickets VIP.

    La función permite a un usuario con un ticket VIP seleccionar un restaurante y productos disponibles en un estadio,
    agregar productos a su carrito y proceder a la compra. También valida la cédula del usuario, verifica si el usuario es mayor
    de edad para la compra de productos alcohólicos, y aplica un descuento si la cédula es un número perfecto.

    Si no hay entradas registradas, la función devuelve un mensaje indicando que no hay entradas. Si el usuario no tiene un
    ticket VIP, o la cédula no está asociada a ninguna entrada, la función devuelve mensajes correspondientes.

    La función realiza las siguientes acciones:
    1. Solicita la cédula del usuario y la valida.
    2. Verifica si el usuario tiene un ticket VIP.
    3. Muestra los restaurantes disponibles en el estadio.
    4. Permite al usuario seleccionar un restaurante y productos para agregar al carrito.
    5. Verifica la disponibilidad de stock y la edad del usuario para productos alcohólicos.
    6. Calcula el subtotal y aplica un descuento si la cédula es un número perfecto.
    7. Solicita la confirmación de la compra y actualiza el stock si la compra se realiza.

    Devuelve:
        str: Mensaje indicando el estado del proceso de compra o validación.

    Ejemplo de uso:
        sistema.venta_productos()

    Notas:
        - La cédula debe ser un número entero válido entre 5 y 8 dígitos.
        - Solo usuarios con ticket VIP pueden realizar compras.
        - Productos alcohólicos no pueden ser comprados por menores de edad.
        - Se aplica un descuento del 15% si la cédula es un número perfecto."""
        if self.ticket_list==[]:
                return('No hay entradas registradas')
        else:
            carrito=[]
            print('Bienvenido al sistema de compra de productos')
            cedula=input('Ingresa tu cedula: ')
            while not cedula.isdigit() or len(cedula)>8 or len(cedula)<5:
                print('Por favor ingrese una cedula valida')
                cedula=input('Ingresa tu cedula: ')
            for entrada in self.ticket_list:
                if cedula == entrada.cedula:
                    if entrada.tipo == 'V':
                        nombre=entrada.nombre
                        estadio= entrada.partido.stadium
                        
                        print(f'Bienvenido, {nombre} los restaurantes en {estadio.name} son:')
                        for i, restaurantes in enumerate(estadio.restaurants, start=1):
                            print(f"{i}. {restaurantes.name}")
                        restaurante_idx = (input("Ingrese el número del restaurante: "))
                        while not restaurante_idx.isnumeric() or int(restaurante_idx) not in range(len(estadio.restaurants)+1) or restaurante_idx=='0':
                                print('por favor ingrese un numero valido')
                                restaurante_idx = (input("Ingrese el número del restaurante: "))
                        restaurante = estadio.restaurants[int(restaurante_idx) - 1]
                        for i, product in enumerate(restaurante.products, start=1):
                                print('---------------------------')
                                print(f"{i}. {product.show()}")
                        print('---------------------------')
                        while True:
                            producto_idx = (input("Ingrese el número del producto: "))
                            while not producto_idx.isnumeric() or int(producto_idx) not in range(len(restaurante.products)+1) or producto_idx=='0':
                                print('por favor ingrese un numero valido')
                                producto_idx = (input("Ingrese el número del producto: "))
                            producto = restaurante.products[int(producto_idx) - 1]
                            if int(entrada.edad)<18:
                                if producto.adicional == 'alcoholic':
                                    print('No puedes comprar este producto')
                                    continue
                            cantidad = int(input("Ingrese la cantidad del producto: "))
                            while cantidad > producto.stock:
                                print(f"No hay suficiente stock del producto {producto.nombre}. Stock disponible: {producto.stock}")
                                cantidad = int(input("Ingrese la cantidad del producto: "))                           
                            while cantidad <= 0:
                                print('por favor ingrese una cantidad valida')
                                cantidad = int(input("Ingrese la cantidad del producto: "))
                            carrito.append((producto, cantidad))
                            print('---------------------------')
                            print(f"Se ha agregado {cantidad} {producto.nombre} al carrito, desea agregar algo mas?")
                            respuesta = input("S/N: ").upper()
                            while respuesta not in ['S', 'N']:
                                print('por favor ingrese una respuesta valida')
                                respuesta = input("S/N: ").upper()
                            if respuesta == 'N':
                                subtotal=sum(float(producto.precio) * cantidad for producto, cantidad in carrito)
                                descuento=0
                                if es_perfecto(int(cedula)):
                                    subtotal*0.15
                                
                                print('---------------------------')
                                print("Carrito:")
                                for i, (producto, cantidad) in enumerate(carrito, start=1):
                                    print(f"{i}. {producto.nombre} x{cantidad}")
                                print('---------------------------')
                                print(f"Subtotal: ${subtotal}")
                                print(f"Descuento: ${descuento}")
                                print(f"Total: ${subtotal-descuento}")
                                print('---------------------------')
                                print("¿Desea realizar la compra?")
                                respuesta = input("S/N: ").upper()
                                while respuesta not in ['S', 'N']:
                                    print('por favor ingrese una respuesta valida')
                                    respuesta = input("S/N: ").upper()
                                if respuesta == 'S':
                                    for producto, cantidad in carrito:
                                            producto.stock -= cantidad
                                    print("Gracias por su compra!")
                                    print('---------------------------')
                                    return
                                else:
                                    print("Gracias por visitarnos")
                                    return
                                    
                            else:pass
                    else:
                        print('Necesitas un ticket VIP para comprar productos')
                        return
                else:
                    print(f'No tienes un ticket asociado a tu cedula')
                    return