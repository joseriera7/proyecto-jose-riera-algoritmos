import requests
import random
from Country import*
from Stadium import*
from Restaurant import *
from Match import*
from Product import *
from Ticket import *



class Sistema:
    def __init__(self):
        self.country_list=[]
        self.stadium_list=[]
        self.match_list=[]
        self.ticket_list=[]
        self.products=[]
        self.food=[]
        self.drinks=[]
        self.cedulas={}


    def register_all(self,url1,url2,url3):
        """
    Registra todos los datos necesarios desde las URL proporcionadas.

    Este método registra equipos, estadios y partidos desde las URL proporcionadas.

    Parámetros:
    url1 (str): La URL para registrar equipos.
    url2 (str): La URL para registrar estadios.
    url3 (str): La URL para registrar partidos.

    Retorna:
    None
    """
        self.registrar_equipos(url1)
        self.registrar_estadios(url2)
        self.registrar_partidos(url3)


    def menu(self):
        """
    Muestra el menú principal del sistema de la Euro 2024.

    Este método muestra un menú interactivo que permite al usuario realizar diferentes acciones,
    como buscar partidos, realizar compras de entradas, buscar productos, chequear entradas,
    comprar productos, gestionar estadísticas y salir del sistema.

    Returns:
    None
    """
        print("Bienvenido al sistema de la Euro 2024")
        while True:
            opcion_menu = input('¿Que desea hacer?\n1- Busqueda de partidos \n2- Realizar compra de entradas \n3- Busqueda de productos \n4- Chequear entradas \n5- Comprar productos \n6- Gestion de estadisticas \n7- Salir \n====>')
            while opcion_menu not in ['1','2','3','4','5','6','7']:
                print("Opcion no valida")
                opcion_menu = input('¿Que desea hacer?\n1- Busqueda de partidos\n2- Realizar compra de entradas \n3- Busqueda de productos \n4- Chequear entradas \n5- Comprar productos \n6- Gestion de estadisticas \n7- Salir \n====>')
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

            elif opcion_menu=='6':
                opcion_estadistica=input('Que desea hacer? \n1-Ver gasto promedio de clientes \n2-Ver partidos con mas boletos vendidos \n3-Ver tabla de relacion asistencia/venta \n4-Ver partidos con mayor asistencia \n5-Ver top 3 de clientes con mas boletos \n6-Ver top 3 de productos mas vendidos: ')
                while opcion_estadistica not in ['1','2','3','4','5','6']:
                    print("Opcion no valida")
                    opcion_estadistica=input('Que desea hacer? \n1-Ver gasto promedio de clientes \n2 ver partidos con mas boletos vendidos \n3-Ver tabla de relacion asistencia/venta \n4-Ver partidos con mayor asistencia \n5-Ver top 3 de clientes con mas boletos \n6-Ver top 3 de productos mas vendidos: ')
                if opcion_estadistica=='1':
                    print(self.gasto_promedio())
                elif opcion_estadistica=='2':
                    print(self.boletos_vendidos())
                elif opcion_estadistica=='3':
                    self.tabla()
                elif opcion_estadistica=='4':
                    print(self.asistencia())
                elif opcion_estadistica=='5':
                    print(self.topclientes())
                else:
                    print(self.topproductos())


            else: 
                print('Vuelva pronto!')
                break 

    def registrar_equipos(self,url):
        """
    Registra equipos desde una URL proporcionada.

    Este método hace una solicitud GET a la URL proporcionada, y si la respuesta es exitosa (200),
    procesa los datos JSON devueltos y crea objetos `Country` para cada equipo, agregándolos a la lista `country_list`.

    Parámetros:
    url (str): La URL desde la que se obtendrán los datos de los equipos.

    Returns:
    None
    """
        response=requests.get(url)
        if response.status_code == 200:
            data=response.json()
            for team in data:
                team_obj=Country(team['id'], team['name'], team['code'],team['group'])
                self.country_list.append(team_obj)
        else:
             print("Error al obtener los datos de los equipos")
    

    def registrar_estadios(self,url):
        """
    Registra estadios y sus respectivos restaurantes y productos desde una URL proporcionada.

    Este método hace una solicitud GET a la URL proporcionada, y si la respuesta es exitosa (200),
    procesa los datos JSON devueltos y crea objetos `Stadium`, `Restaurant` y `Product` para cada estadio,
    restaurante y producto, respectivamente, agregándolos a las listas `stadium_list` y `products`.

    Parámetros:
    url (str): La URL desde la que se obtendrán los datos de los estadios.

    Returns:
    None
    """
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
                        price=float(product['price'])*1.16
                        adicional=product['adicional']
                        stock=product['stock']
                        if adicional in ['plate','package']:
                            tipo='food'
                            product_obj=Product(name_prod,round(price,2),tipo,adicional,stock,0)
                            product_list.append(product_obj)
                            self.products.append(product_obj)
                        else:
                            tipo='drink'
                            product_obj=Product(name_prod,round(price,2),tipo,adicional,stock,0)
                            product_list.append(product_obj)
                            self.products.append(product_obj)
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
        """
    Registra partidos desde una URL proporcionada.

    Este método hace una solicitud GET a la URL proporcionada, y si la respuesta es exitosa (200),
    procesa los datos JSON devueltos y crea objetos `Match` para cada partido, asociándolos con los estadios y países
    previamente registrados, y agregándolos a la lista `match_list`.

    Parámetros:
    url (str): La URL desde la que se obtendrán los datos de los partidos.

    Returns:
    None
    """
        response=requests.get(url)
        
        if response.status_code == 200:
            data=response.json()
            for match in data:
                for stadium in self.stadium_list:
                    if match['stadium_id']== stadium.id:
                        home= Country(match['home']['id'],match['home']['name'],match['home']['code'],match['home']['group'])
                        away= Country(match['away']['id'],match['away']['name'],match['away']['code'],match['away']['group'])
                        match_obj=Match(match['id'],match['number'],home,away,match['date'], stadium,0,0)
                        
                        self.match_list.append(match_obj)

        else:
             print('Error al obtener los partidos')
              

    def buscar_porpais(self):
        """
    Busca partidos por país.

    Pide al usuario que ingrese el nombre de un país, y luego busca en la lista de partidos
    aquellos en los que participa el equipo de ese país. Si se encuentran partidos, los muestra
    con detalles; de lo contrario, informa que no se encontraron partidos para ese equipo.

    Returns:
    None
    """
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
        """
    Busca partidos por estadio.

    Muestra una lista de estadios y pide al usuario que seleccione uno ingresando su número.
    Luego, busca en la lista de partidos aquellos que se juegan en el estadio seleccionado
    y los muestra con detalles; de lo contrario, informa que no se encontraron partidos en ese estadio.

    Returns:
    None
    """
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
        """
    Busca partidos por fecha.

    Pide al usuario que ingrese un día del mes (entre 1 y 30) y construye una fecha completa
    en el formato '2024-06-DD'. Luego, busca en la lista de partidos aquellos que se juegan
    en esa fecha y los muestra con detalles; de lo contrario, informa que no se encontraron
    partidos en esa fecha.

    Returns:
    None
    """
        date=input("Ingresa que dia deseas insertar en 2024-06-__: ").strip()
        while not date.isdigit or int(date) not in range(0,31):
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
            """
    Muestra el plano de asientos de la sección general del estadio para un partido dado.

    Utiliza un diccionario para representar las letras de las columnas y un ciclo for anidado
    para mostrar las filas y columnas de asientos. Si un asiento está ocupado, muestra 'X',
    de lo contrario, muestra '0'.

    Args:
    partido: Partido
        El objeto Partido para el que se mostrará el plano de asientos de la sección general.

    Returns:
    None
    """
            
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
            """
    Muestra el plano de asientos de la sección VIP del estadio para un partido dado.

    Utiliza un diccionario para representar las letras de las columnas y un ciclo for anidado
    para mostrar las filas y columnas de asientos. Si un asiento está ocupado, muestra 'X',
    de lo contrario, muestra '0'.

    Args:
    partido: Partido
        El objeto Partido para el que se mostrará el plano de asientos de la sección VIP.

    Returns:
    None
    """
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
        if cedula in self.cedulas and self.cedulas[cedula]!=[nombre_cliente,apellido_cliente,edad]:
                print("los datos del cliente no coinciden")
        else:
            print('Que partido desea comprar: ')
            for i, match in enumerate(self.match_list):
                print(f'{i+1}. {match.show()}')
            partido_idx = input("Ingrese el número del partido: ")
            while not partido_idx.isdigit() or int(partido_idx) not in range(1, len(self.match_list)+1):
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
                        while not asiento_fila.isdigit() or  int(asiento_fila) not in range(1,(partido.stadium.getCapacidadGeneral()//10)+2):
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
                    cliente_obj=Ticket(entradas[i],f'{nombre_cliente} {apellido_cliente}',cedula,edad,partido, False,tipo,total)
                    self.ticket_list.append(cliente_obj)
                    self.cedulas[cedula]=[nombre_cliente,apellido_cliente,edad]
                print('¡Entrada comprada con exito!')
                
                partido.boletos_vendidos += int(cantidad)

            else:
                for asiento in asientos:
                    if tipo.upper() == 'V':
                        partido.taken_v.pop(asiento)
                    else:
                        partido.taken_g.pop(asiento)
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
            if nombre.lower() in product.nombre.lower():
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
                   entrada.partido.asistencia+=1
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
                                total=subtotal-descuento
                                print('---------------------------')
                                print("Carrito:")
                                for i, (producto, cantidad) in enumerate(carrito, start=1):
                                    print(f"{i}. {producto.nombre} x{cantidad}")
                                print('---------------------------')
                                print(f"Subtotal: ${subtotal}")
                                print(f"Descuento: ${descuento}")
                                print(f"Total: ${total}")
                                print('---------------------------')
                                print("¿Desea realizar la compra?")
                                respuesta = input("S/N: ").upper()
                                while respuesta not in ['S', 'N']:
                                    print('por favor ingrese una respuesta valida')
                                    respuesta = input("S/N: ").upper()
                                if respuesta == 'S':
                                    for producto, cantidad in carrito:
                                            producto.stock -= cantidad
                                            producto.vendido+=cantidad

                                    entrada.gasto += total
                                    print("Gracias por su compra!")
                                    print('---------------------------')
                                    return
                                else:
                                    print("Gracias por visitarnos")
                                    return
                                    
                            else:pass
                    else:
                        print('Necesitas un ticket VIP para comprar productos')
                        pass
                else:
                    print(f'No tienes un ticket asociado a tu cedula')
                    continue
                
    def gasto_promedio(self):
        """
    Calcula y devuelve el gasto promedio de los tickets registrados.

    Itera sobre la lista de tickets, agrupa los gastos por cédula y calcula la suma total de gastos.
    Luego, divide la suma total entre el número de cédulas únicas para obtener el gasto promedio.

    Returns:
    str
        Un mensaje que indica el gasto promedio, o un mensaje de error si no hay gastos registrados.
    """
        lista_gastos = {}
        if self.ticket_list == []:
            return 'No hay gastos registrados todavía'
        else:
            for ticket in self.ticket_list:
                
                if ticket.cedula in lista_gastos:
                    continue
                else:
                    lista_gastos[ticket.cedula] = ticket.gasto
            
            total_gastos = sum(lista_gastos.values())
            promedio_gastos = total_gastos / len(lista_gastos)
            
            return f'El gasto promedio fue: {promedio_gastos}$'
            
        
    def tabla(self):
        """
        Muestra una tabla con la asistencia a los partidos de mejor a peor.

        La tabla incluye el nombre del partido, el estadio donde se juega, la cantidad de boletos vendidos,
        el número de personas que asistieron y la relación asistencia/venta. Los partidos se ordenan
        en orden descendente basado en la relación asistencia/venta.
        """
         # segun la documentacion de python: 
         # "Las expresiones lambda (a veces denominadas formas lambda) son usadas para crear funciones anónimas. La expresión lambda parameters: expression produce un objeto de función."
        
        partidos_ordenados = sorted(self.match_list, key=lambda x: x.asistencia / x.boletos_vendidos if x.boletos_vendidos else 0, reverse=True)

        
        print(f"{'Partido':<35} {'Estadio':<30} {'Boletos Vendidos':<20} {'Asistencia':<15} {'Relación Asistencia/Venta':<25}")
        print("="*135)
        for partido in partidos_ordenados:
            equipos=f'{partido.home.name} vs {partido.away.name}'
            relacion_asistencia_venta = partido.asistencia / partido.boletos_vendidos if partido.boletos_vendidos else 0
            print(f"{equipos:<35} {partido.stadium.name:<30} {partido.boletos_vendidos:<20} {partido.asistencia:<15} {relacion_asistencia_venta:<25.2f}")

    def boletos_vendidos(self):
            """
            Recorre la lista de partidos (`match_list`), recoge cada partido junto con la boletos_vendidos 
            (cantidad de boletos vendidos), y los almacena en una lista de tuplas. Luego, ordena 
            esta lista en orden descendente basado en la cantidad de boletos vendidos y muestra el partido con mas boletos
            vendidos primero.
            """
            boletos_vendidos = []
            for partido in self.match_list:
                boletos_vendidos.append((partido, partido.boletos_vendidos))
            
           
            boletos_vendidos.sort(key=lambda x: x[1], reverse=True)
            
            for (partido, cantidad) in (boletos_vendidos):
                return(f"El partido con mas boletos vendidos fue {partido.show_sinfecha()} con {cantidad} boletos")
    def asistencia(self):
            """

            Recorre la lista de partidos (`match_list`), recoge cada partido junto con la asistencia,
            y los almacena en una lista de tuplas. Luego, ordena esta lista en orden descendente basado en la cantidad de asistidores al partido
            y muestra los partidos con su numero total de asistencia.
            """
            asistencia = []
            for partido in self.match_list:
                asistencia.append((partido, partido.asistencia))
            
           
            asistencia.sort(key=lambda x: x[1], reverse=True)
            
            for (partido, cantidad) in (asistencia):
                return(f"El partido con mayor asistencia fue {partido.show_sinfecha()} con {cantidad} boletos")
    def topclientes(self):
        """
    Devuelve una lista de los top 3 clientes con más entradas compradas.

    Itera sobre la lista de tickets, cuenta la cantidad de entradas compradas por cada cliente
    y ordena la lista de clientes por la cantidad de entradas en orden descendente.
    Luego, devuelve un string que muestra los top 3 clientes con más entradas.

    Returns:
    str
        Un mensaje que lista los top 3 clientes con más entradas, o un mensaje de error si no hay clientes registrados.
    """
        clientes={}
        for ticket in self.ticket_list:
            if ticket.nombre in clientes:
                clientes[ticket.nombre]+=1
            else:
                clientes[ticket.nombre]=1
        
        clientes=sorted(clientes.items(), key=lambda x: x[1], reverse=True)
        top_clientes=''
        for idx,cliente in enumerate(clientes):
            top_clientes+=f'\n {idx+1} - {cliente[0]} con {cliente[1]} entradas '
            if idx==2:
                break
        if clientes==[]:
            return "No hay clientes todavia"
        else:
            return f'''Los clientes con mas entradas son: 
            {top_clientes}'''
        
    def topproductos(self):
        """
    Devuelve una lista de los top 3 productos más vendidos.

    Itera sobre la lista de productos, cuenta la cantidad de artículos vendidos por cada producto
    y ordena la lista de productos por la cantidad de artículos vendidos en orden descendente.
    Luego, devuelve un string que muestra los top 3 productos más vendidos.

    Returns:
    str
        Un mensaje que lista los top 3 productos más vendidos.
    """
        prod_porventas=[]
        for producto in self.products:
            nombre=producto.nombre
            ventas=producto.vendido
            
            prod_porventas.append((nombre,ventas))

        productos_ord=sorted(prod_porventas, key=lambda x: x[1], reverse=True)
        top_productos=''
        for idx,producto in enumerate(productos_ord):
            top_productos+=f'\n {idx+1} - {producto[0]} con {producto[1]} articulos vendidos '
            if idx==2:
                break
        return f'''Los productos mas vendidos son: 
            {top_productos}'''

def generar_permutaciones(arr):
        """
            Genera todas las permutaciones posibles de una lista de elementos.

            Utiliza un revursividad para generar todas las permutaciones de la lista.
            Primero, se verifica si la lista está vacía o tiene solo un elemento, en cuyo caso se devuelve una lista vacía o la lista original, respectivamente.
            Luego, se itera sobre cada elemento de la lista, se elimina temporalmente el elemento de la lista y se generan permutaciones de la lista restante.
            Finalmente, se devuelve una lista que contiene todas las permutaciones posibles de la lista original.

            Args:
            arr (list)
                La lista de elementos para generar permutaciones.

            Returns:
            list
                Una lista que contiene todas las permutaciones posibles de la lista original.
        """
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
        """
            Verifica si un número es un número vampiro.

            Un número vampiro es un número que puede ser expresado como el producto de dos números (llamados "colmillos") que contienen exactamente los mismos dígitos que el número original, pero en un orden diferente.
            La función genera todas las permutaciones posibles de los dígitos del número y verifica si alguna de ellas forma un par de colmillos válido.

            Args:
            num (int)
                El número a verificar si es un número vampiro.

            Returns:
            bool
                True si el número es un número vampiro, False en caso contrario.
            """
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
    """
    Verifica si un número es perfecto.

    Un número perfecto es un número que es igual a la suma de sus divisores propios (excluyendo al número mismo).
    La función itera sobre todos los números menores que el número dado y verifica si son divisores del número.
    Luego, suma todos los divisores encontrados y verifica si la suma es igual al número original.

    Args:
    num (int)
        El número a verificar si es perfecto.

    Returns:
    bool
        True si el número es perfecto, False en caso contrario.
    """
    suma = []
    for i in range(1, num):
        if num % i == 0:
            suma.append(i)
    return sum(suma) == num
