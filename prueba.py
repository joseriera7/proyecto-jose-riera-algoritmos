
def mostrarAsientosGeneral(self):
    for entrada in range(1,int(cantidad)+1):
        print("Entrada: ",entrada)
        
        diccionario = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8 : 'I', 9 : 'J'}
        
        total = self.estadio.getCapacidadGeneral()
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
                    if f'{diccionario[j]}{i+1}' not in self.asientos_tomados:
                        print(0, end='    ')
                    else: print('X', end='    ')
                print('\n')
            elif i < 9:
                print(i +1, end= ' | ')
                for j in range(10):
                    if f'{diccionario[j]}{i+1}' not in self.asientos_tomados:
                        print(0, end='    ')
                    else: print('X', end='    ')
                print('\n')
            
            else:
                print(i +1, end= '| ')
                for j in range(10):
                    if f'{diccionario[j]}{i+1}' not in self.asientos_tomados:
                        print(0, end='    ')
                    else: print('X', end='    ')
                print('\n')