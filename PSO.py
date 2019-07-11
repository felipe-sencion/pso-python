import copy
import numpy as np
import sphere
import rosenbrock

class Individuo:
    def __init__(self, solucion, velocidad):
        self.solucion = solucion
        self.velocidad = velocidad
        self.b = copy.deepcopy(solucion)

class PSO:
    def __init__(self,
    cantidad_individuos,
    dimensiones,
    ro, #Tamaño de vecindad
    phi1_max,
    phi2_max,
    v_max,
    problema,
    generaciones):
        self.cantidad_individuos = cantidad_individuos
        self.dimensiones = dimensiones
        self.ro = ro
        self.phi1_max = phi1_max
        self.phi2_max = phi2_max
        self.v_max = v_max
        self.problema = problema
        self.generaciones = generaciones
        self.individuos = []
        self.mejor_historico = 0
        self.rango = self.problema.MAX_VALUE - self.problema.MIN_VALUE
        self.mejor = np.inf

    def crearIndividuos(self):
        for i in range(self.cantidad_individuos):
            solucion = np.random.random(size = self.dimensiones) * self.rango + self.problema.MIN_VALUE
            velocidad = np.random.random(size = self.dimensiones) * self.v_max * 2 + self.v_max
            individuo = Individuo(solucion, velocidad)
            self.individuos.append(individuo)
    def imprimirIndividuos(self):
        for individuo in self.individuos:
            print(individuo.solucion, individuo.velocidad)

    def mejorIndividuo(self):
        for i in self.individuos:
            if self.problema.fitness(i.solucion) < self.mejor:
                self.mejor = self.problema.fitness(i.solucion)


    def run(self):
        self.crearIndividuos()
        generacion = 0
        while (generacion < self.generaciones):
            for idx in range(len(self.individuos)):
                h = 0
                for i in range(-self.ro // 2, self.ro // 2 + 1):
                    if i == 0:
                        continue
                    elif i == -self.ro // 2:
                        h = copy.deepcopy(self.individuos[(idx + i) % len(self.individuos)])
                    elif self.problema.fitness(self.individuos[(idx + i) % len(self.individuos)].solucion) < self.problema.fitness(h.solucion):
                        h = copy.deepcopy(self.individuos[(idx + i) % len(self.individuos)])
                phi1 = np.random.random(size = self.dimensiones) * self.phi1_max
                phi2 = np.random.random(size = self.dimensiones) * self.phi2_max
                self.individuos[idx].velocidad = (self.individuos[idx].velocidad +
                np.multiply(phi1, self.individuos[idx].b - self.individuos[idx].solucion) +
                np.multiply(phi2, h.solucion - self.individuos[idx].solucion))
                for i in range(self.dimensiones):
                    if abs(self.individuos[idx].velocidad[i]) > self.v_max:
                        self.individuos[idx].velocidad[i] = self.v_max / (self.individuos[idx].velocidad[i])
                self.individuos[idx].solucion = self.individuos[idx].solucion + self.individuos[idx].velocidad
                if (self.problema.fitness(self.individuos[idx].solucion) <
                self.problema.fitness(self.individuos[idx].b) ):
                    self.individuos[idx].b = copy.deepcopy(self.individuos[idx].solucion)
                #input()
            self.mejorIndividuo()
            print('Generación ', generacion, ':', self.mejor)
            generacion += 1



def main():
    rosen = rosenbrock.Rosenbrock()
    rango = rosen.MAX_VALUE - rosen.MIN_VALUE
	cantidad_individuos = 30
    dimensiones = 8
    ro = 8
    phi1_max = 1.7
    phi2_max = 2.0
    v_max = rango * 0.01
    generaciones = 2000
    pso = PSO(cantidad_individuos, dimensiones, ro, phi1_max, phi2_max, v_max, rosen, generaciones)
    pso.run()

if  __name__ == '__main__':
    main()
