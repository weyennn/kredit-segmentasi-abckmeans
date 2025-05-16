import numpy as np
from sklearn.metrics import pairwise_distances_argmin_min

class ABCOptimizer:
    def __init__(self, data, num_clusters=3, max_iter=50, colony_size=20, seed=42):
        self.data = data
        self.k = num_clusters
        self.max_iter = max_iter
        self.colony_size = colony_size
        self.dim = data.shape[1]
        self.rng = np.random.RandomState(seed)

    def initialize_food_sources(self):
        return np.array([
            self.data[self.rng.choice(self.data.shape[0], self.k, replace=False)]
            for _ in range(self.colony_size)
        ])

    def evaluate(self, centroids):
        labels, dists = pairwise_distances_argmin_min(self.data, centroids)
        return np.sum(dists**2)

    def optimize(self):
        food_sources = self.initialize_food_sources()
        fitness = np.array([self.evaluate(source) for source in food_sources])
        best_idx = np.argmin(fitness)
        best_source = food_sources[best_idx]

        for _ in range(self.max_iter):
            for i in range(self.colony_size):
                phi = self.rng.uniform(-1, 1, size=(self.k, self.dim))
                partner = food_sources[self.rng.randint(0, self.colony_size)]
                candidate = food_sources[i] + phi * (food_sources[i] - partner)
                candidate_fitness = self.evaluate(candidate)
                if candidate_fitness < fitness[i]:
                    food_sources[i] = candidate
                    fitness[i] = candidate_fitness
                    if candidate_fitness < self.evaluate(best_source):
                        best_source = candidate

        return best_source
