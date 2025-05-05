import m_nodo
import m_arista
import random
import math
import numpy as np

class grafo:
    def __init__(self,N,M=None,p=None,r=None,d=None,m=None):
        self.N=N
        self.M=M
        self.p=p
        self.r=r
        self.d=d
        self.m=m
        self.nodos=[]
    
    def generar_grafo_graphviz(self,lista_aristas,grafo):
      archivo=f"{grafo}.dot"
      try:
        with open(archivo, "x") as archivo_graphviz:
            archivo_graphviz.write("graph {\n")
            for arista in lista_aristas:
                archivo_graphviz.write(f"  {arista.nodo1} -- {arista.nodo2};\n")
            archivo_graphviz.write("}\n")
      except FileExistsError:
        print( "Archivo ya existente") 


    def generar_nodos(self):
        self.nodos = [m_nodo.nodo(i) for i in range(self.N)]
    
    #___________________Modelo Erdos Renyi_______________ 
    def generar_aristas_er(self):
        if self.M is None:
            raise ValueError("Favor de Especificar Aristas de  Erdős-Rényi")
        max_aristas=(self.N*(self.N-1))//2
        numero_aritas=min(max_aristas,self.M)
        aristas_esperadas=set()#suconjunto de aristas a generar sin duplicados

        while len(aristas_esperadas) < numero_aritas:
            #nodo1_id=random.randint(0,self.N-1)
            #nodo2_id=random.randint(0,self.N-1)
            nodo1=random.choice(self.nodos)
            nodo2=random.choice(self.nodos)
            if nodo1 != nodo2:
                nueva_arista=m_arista.arista(nodo1.id,nodo2.id)
                aristas_esperadas.add(nueva_arista)
        
        self.aristas=list(aristas_esperadas)
        print("\n>>Aristas Erdos Rengy: ",len(self.aristas))
        return self.aristas
    
    #------------Modelo Gilbert---------------        
    def generar_aristas_gilbert(self):
        if self.p is None:
            raise ValueError("Favor de Especificar Probabilidad en Modelo Gilbert")
        aristas_esperadas=set()
        for i in range (self.N):
            for j in range(i+1 ,self.N):
                if random.random()<self.p:
                    nueva_arista=m_arista.arista(i,j)
                    aristas_esperadas.add(nueva_arista)
        self.aristas=list(aristas_esperadas)
        print("\n>>Aristas Gilbert: ",len(self.aristas))
        return self.aristas
    
    #----------Modelo Geografico Simple---------
    
    def asignacion_direcciones(self):
        self.direcciones={}
        for nodo in self.nodos:
            self.direcciones[nodo.id]=(random.random(),random.random())

    def calculo_distancia(self,nodo1,nodo2):
        x1,y1= self.direcciones[nodo1]
        x2,y2= self. direcciones [nodo2]
        distancia=math.sqrt(((x2-x1)**2)+((y2-y1)**2))
        return distancia


    def generar_arista_geografico(self):
        if self.r is None:
            raise ValueError("Favor de Ingresar Distancia 'r' en Modelo Geográfico ")
        self.asignacion_direcciones()
        aristas_genradas=set()
        
        for i in range(self.N):
            for j in range(i+1,self.N):
                nodo1=self.nodos[i].id
                nodo2=self.nodos[j].id
                distancia=self.calculo_distancia(nodo1,nodo2)
                if distancia>=self.r:
                    nueva_arista=m_arista.arista(nodo1,nodo2)
                    aristas_genradas.add(nueva_arista)
        self.aristas=list(aristas_genradas)
        print("\n>>Aristas Geograficas: ",len(self.aristas))
        return self.aristas
        
#___________________Modelo Barabasi-Albert________________
    def calculo_de_grado_nodo(self,aristas,nodo):
        grado=0
        for arista in aristas:
            if nodo == arista.nodo1 or nodo == arista.nodo2:
                grado += 1
        return grado

    def calculo_de_probabilidad(self,grado_nodo):
           grado_de_conexion_global=self.d
           probabilidad=1-(grado_nodo/grado_de_conexion_global)
           return probabilidad 

    #---Generar las aristas en Barabasi---
    def generar_aristas_Barabasi(self):

        if self.d is None:
            raise ValueError("Favor de Ingresar grado de nodos 'd' en Modelo Barabasi")
        
        # Crear m aristas a primeros m nodos
        aristas_generadas=set()
        for i in range (self.d):
            for j in range(i+1,self.d):
                nodo1=self.nodos[i].id
                nodo2=self.nodos[j].id
                grado=self.calculo_de_grado_nodo(aristas_generadas,nodo2)
                if grado<self.d:
                    nueva_arista=m_arista.arista(nodo1,nodo2)
                    aristas_generadas.add(nueva_arista)

        #Empezar a conectar nuevos nodos
        for i in range (self.d+1,self.N):
                for j in range(self.N):
                    nodo_origen=self.nodos[i].id
                    nodo_tarjet=self.nodos[j].id
                    probabilidad=self.calculo_de_probabilidad(self.calculo_de_grado_nodo(aristas_generadas, nodo_tarjet))
                    probabilidad_aleatoria=random.random()
                    if probabilidad_aleatoria<probabilidad:
                        grado_origen = self.calculo_de_grado_nodo(aristas_generadas, nodo_origen)
                        grado_tarjet = self.calculo_de_grado_nodo(aristas_generadas, nodo_tarjet)
                        if grado_origen < self.d and grado_tarjet < self.d:
                            nueva_arista=m_arista.arista(nodo_origen,nodo_tarjet)
                            aristas_generadas.add(nueva_arista)
                            #vuelvo a calcular el grado de mis nodos despues de añadir otro nodo
                            grado_origen = self.calculo_de_grado_nodo(aristas_generadas, nodo_origen)
                            grado_tarjet = self.calculo_de_grado_nodo(aristas_generadas, nodo_tarjet)
                            if grado_origen>self.d or grado_tarjet>self.d:
                                aristas_generadas.remove(nueva_arista)

        # for i in range(self.N):
        #     grado_nodos=self.calculo_de_grado_nodo(aristas_generadas,i)
        #     print("Nodo: ", i, " ", "Grado: ",grado_nodos)            

        self.aristas = list(aristas_generadas)
        print("\n>>Aristas Barabasi: ", len(self.aristas))
        return self.aristas


#___________________MOdelo Dorogovtsev-Mendes_________________  
    
    def generar_aristas_dorogovtset(self):
        aristas_generadas=set()

        #Generar triángulo
        arista1=aristas_generadas.add(m_arista.arista(0,1))
        arista2=aristas_generadas.add(m_arista.arista(1,2))
        arista3=aristas_generadas.add(m_arista.arista(2,0))

        #Agregar nodos adicionales
        for i in range(3,self.N):
            arista_aleatoria=random.choice(list(aristas_generadas))
            nodo_nuevo=i
            nodo1x, nodo2x=arista_aleatoria.nodo1,arista_aleatoria.nodo2
            nueva_arista1=m_arista.arista(nodo_nuevo,nodo1x)
            aristas_generadas.add(nueva_arista1)
            nueva_arista2=m_arista.arista(nodo_nuevo,nodo2x)
            aristas_generadas.add(nueva_arista2)
            #print("Arista: ",nodo1x, "-",nodo2x)
        self.aristas = list(aristas_generadas)
        print("\n>>Aristas Dorogovtset-Mendez: ", len(self.aristas))
        return self.aristas

#_______________________Modelo Malla______________

    def generar_aristas_malla(self):
        self.aristas=[]
        
        aristas_generadas=set()
        malla=np.zeros((self.N,self.m),dtype=int)
        valor_incial=0

        for i in range(self.N):
            for j in range(self.m):
                malla[i,j]=valor_incial
                valor_incial+=1
        #print(malla)

        #generar aristas en la malla
        for i in range(0,self.N):
            for j in range(0,self.m):
                if i + 1 < self.N:  # Verificar límite inferior
                    nodo1 = malla[i, j]
                    nodo2 = malla[i + 1, j]
                    nueva_arista1 = m_arista.arista(nodo1, nodo2)
                    aristas_generadas.add(nueva_arista1)
                if j + 1 < self.m:  # Verificar límite derecho
                    nodo1 = malla[i, j]
                    nodo3 = malla[i, j + 1]
                    nueva_arista2 = m_arista.arista(nodo1, nodo3)
                    aristas_generadas.add(nueva_arista2)
        
        self.aristas = list(aristas_generadas)
        print("\n>>Aristas Malla: ", len(self.aristas))
        return self.aristas
        

            





