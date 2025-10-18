import random
import matplotlib.pyplot as plt


class Nodo:
    
    elementos: list
    valor: float
    hijos: list['Nodo']
    
    def __init__(self, elementos: list, valor: float, hijos: list['Nodo'] = []):
        self.elementos = elementos
        self.valor = valor
        self.hijos = hijos
        
    def label_name(self, indices : list):
        if self.valor == 0:
            return str(indices[self.elementos[0]])
        else:
            s = "["
            for h in self.hijos:
                s = s + h.label_name(indices) + ", "
            s = s[:-2] + "]"
            return s
        
    def get_position(self):
        if self.hijos == []:
            return (self.elementos[0], 0)
        else:
            return (self.hijos[0].elementos[0], self.valor) 
    
        
    def plot(self, indices: list, label_points: bool = False):
        plt.scatter(self.get_position()[0], self.get_position()[1])
        if (label_points):
            plt.annotate(self.label_name(indices), (self.get_position()[0], self.get_position()[1]), xytext=(5, 5), textcoords='offset points')
        
        for hijo in self.hijos:
            hijo.plot(indices, label_points)
            
        for j, hijo in enumerate(self.hijos):
            plt.plot([self.get_position()[0], hijo.get_position()[0]], [self.get_position()[1], hijo.get_position()[1]], color='b', linewidth=0.5)
