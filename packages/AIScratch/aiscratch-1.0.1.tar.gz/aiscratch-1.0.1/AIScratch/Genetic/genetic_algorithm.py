import multiprocessing
import numpy as np
from abc import ABC, abstractmethod

class GeneticElement(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def __add__(self, other : "GeneticElement") -> "GeneticElement":
        pass

    @abstractmethod
    def __mul__(self, other) -> "GeneticElement":
        pass

class GeneticSolver(ABC):
    def __init__(self, population_size, number_of_generations, tol = 0.01, elite_rate = 0.2, exploration_rate = 0.2, mutation_rate = 0.2, core_number = 0):
        self.__population_size = population_size
        self.__number_of_generations = number_of_generations
        self.__tol = tol
        self.__elite_rate = elite_rate
        self.__exploration_rate = exploration_rate
        self.__mutation_rate = mutation_rate
        self.__core_number = core_number
        self.__last_fitness = None

    """
    #------- Abstract methods to implement
    """
    @abstractmethod
    def _init_elem(self) -> GeneticElement:
        pass

    @abstractmethod
    def _objective(self, elem : GeneticElement) -> float:
        pass

    @abstractmethod
    def _breeding(self, elm1 : GeneticElement, elm2 : GeneticElement) -> GeneticElement:
        pass

    @abstractmethod
    def _mutation(self, elem : GeneticElement) -> GeneticElement:
        pass
    
    @abstractmethod
    def _selection(self, population : list[GeneticElement], fitness : list[float], elite_rate : float) -> list[GeneticElement]:
        pass

    @abstractmethod
    def _debug(self) -> str:
        pass

    """
    #------- Main methods
    """
    def initialize_population(self, population_size) -> list[GeneticElement]:
        return [self._init_elem() for _ in range(population_size)]

    
    def evaluation(self, population : list[GeneticElement]) -> list[GeneticElement]:
        if self.__core_number == 0:
            return list(map(self._objective, population))
        with multiprocessing.Pool(processes=self.__core_number) as pool:
            ret = pool.map(self._objective, population)
        return ret
    
    def solve(self) -> tuple[GeneticElement, float]:
        population = self.initialize_population(self.__population_size)
        i = 0
        while (self.__last_fitness == None or self.__tol == None or min(self.__last_fitness) > self.__tol) and i < self.__number_of_generations:
            self.__last_fitness = self.evaluation(population)

            elites = self._selection(population, self.__last_fitness[::], self.__elite_rate)
            elites_indices = np.arange(len(elites))

            new_population : list = elites[::] + self.initialize_population(round(self.__population_size * self.__exploration_rate))

            for _ in range(int(self.__population_size * self.__mutation_rate)):
                element, = np.random.choice(elites_indices, 1, replace=False)
                new_population.append(self._mutation(elites[element]))

            while len(new_population) < self.__population_size:
                parent1, parent2 = np.random.choice(elites_indices, 2, replace=False)
                child = self._breeding(elites[parent1], elites[parent2])
                new_population.append(child)
            population = new_population
            print(f"Generation {i + 1} : " + self._debug())
            i += 1
        self.__last_fitness = self.evaluation(population)
        index = self.__last_fitness.index(min(self.__last_fitness))
        return population[index], min(self.__last_fitness)