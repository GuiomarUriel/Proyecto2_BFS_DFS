class arista:
    def __init__(self,nodo1,nodo2):
        #self.nodo1=min(nodo1,nodo2)
        #self.nodo2=max(nodo1,nodo2)
        self.nodo1=nodo1
        self.nodo2=nodo2

    def nueva_arista(self):
        union_arista=tuple(sorted((self.nodo1,self.nodo2)))
        return union_arista
    
    def __eq__(self, other):
        if isinstance(other, arista):
            return self.nodo1 == other.nodo1 and self.nodo2 == other.nodo2
        return NotImplemented

    def __hash__(self):
        return hash((self.nodo1, self.nodo2))

    def __repr__(self):
        return f"Arista({self.nodo1} -- {self.nodo2})"