def load_general(self,mapas,matriz):
        cont =0
        fila =mapas['general'][0]
        columns = mapas['general'][1]
                        
        for i in range(fila):
            matriz.append([])
            for j in range(columns):
                matriz[i].append(f"{cont}")
                cont+=1

load_general()

