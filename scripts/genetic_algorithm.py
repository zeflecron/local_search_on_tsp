from base import Base
import random
import time

'''
    This genetic algorithm is specifically for the travelling salesman

    Genetic Algorithm (GA) has 2 parameters (all csv) when instantiating
        file_problem    : str (csv)
            the problem to solve
        file_result     : str (csv)
            csv for result

    Run the function `execute` to perform GA, execute has 4 parameters
        max_pop         : int
            how many population to perform GA
        iterations      : int
            --//--
        mutation_rate   : float
            chance of a point to be randomly swapped with another
        random_type     : str (optional) [default is None]
            'fixed' to have fixed start and end position

    Example code
    `
    ga = GeneticAlgorithm('problem.csv', 'result.csv')
    ga.execute(50, 100000, 0.01, 'fixed')
    `
'''


class GeneticAlgorithm(Base):
    pop = []
    temp_pop = []
    pop_content = {'dist': 0, 'x': [], 'y': []}
    pop_history = []
    ptr = 0
    good_fit = False
    start_val = 0
    end_val = 0

    def create_pop(self, max_pop, random_type):
        self.open_csv(self.file_problem)
        initial_dist = self.get_distance()
        while len(self.temp_pop) < max_pop:
            self.full_random(random_type)
            new_dist = self.get_distance()
            if new_dist < initial_dist:
                self.temp_update(new_dist)
        self.real_update()

    # check if data is better than previous one or not
    def fitness_check(self):
        new_dist = self.get_distance()
        if new_dist < self.pop[self.ptr][0]:
            self.temp_update(new_dist)
            self.good_fit = True
        else:
            self.good_fit = False

    # appends fitness checked population
    def temp_update(self, dist, x=None, y=None):
        if x is None and y is None:
            x = self.points['x']
            y = self.points['y']
        self.pop_content['dist'] = dist
        self.pop_content['x'] = x
        self.pop_content['y'] = y
        self.temp_pop.append(tuple(self.pop_content.values()))

    # updates a sorted list after appending to a temporary list
    def real_update(self):
        self.pop = sorted(self.temp_pop, key=lambda x: x[0])
        if self.pop[0] not in self.pop_history:
            self.pop_history.append(self.pop[0])
        self.temp_pop = []

    # swap some data between 2 populations based on fitness
    def crossover(self, max_pop, random_type):
        for i in range(0, max_pop, 2):
            full_x1 = self.pop[i][1]
            full_x2 = self.pop[i + 1][1]
            full_y1 = self.pop[i][2]
            full_y2 = self.pop[i + 1][2]

            # select middle part because points are fixed
            x1 = full_x1[self.start_val:self.end_val]
            x2 = full_x2[self.start_val:self.end_val]
            y1 = full_y1[self.start_val:self.end_val]
            y2 = full_y2[self.start_val:self.end_val]

            parent_1 = [list(x) for x in zip(*[x1, y1])]
            parent_2 = [list(x) for x in zip(*[x2, y2])]
            temp_1 = []
            temp_2 = []
            save_index_1 = []
            save_index_2 = []

            # select random index to read from parent_1
            if random_type == 'fixed':
                selection = random.randint(0, self.end_val - 2)
            else:
                selection = random.randint(0, self.end_val - 1)

            search_value = parent_1[selection]
            index_2 = None

            # do a loop between both parents
            # save both values and index that are in the loop
            while index_2 != selection:
                index_1 = parent_1.index(search_value)
                save_index_1.append(index_1)
                temp_1.append(parent_1[index_1])

                index_2 = parent_2.index(search_value)
                save_index_2.append(index_2)
                temp_2.append(parent_2[index_2])

                search_value = parent_1[index_2]

            # crossover data not in loop
            child_1 = [x for x in parent_2 if x not in temp_2]
            child_2 = [x for x in parent_1 if x not in temp_1]

            # reinsert the loop data in its position
            for j in range(len(temp_1)):
                min_1 = min(save_index_1)
                min_2 = min(save_index_2)
                child_1.insert(min_1, temp_1[save_index_1.index(min_1)])
                child_2.insert(min_2, temp_2[save_index_2.index(min_2)])
                del(temp_1[save_index_1.index(min_1)])
                del(temp_2[save_index_2.index(min_2)])
                save_index_1.remove(min_1)
                save_index_2.remove(min_2)

            # replace old data with child
            full_x1[self.start_val:self.end_val] = [x[0] for x in child_1]
            full_x2[self.start_val:self.end_val] = [x[0] for x in child_2]
            full_y1[self.start_val:self.end_val] = [x[1] for x in child_1]
            full_y2[self.start_val:self.end_val] = [x[1] for x in child_2]

            # do fitness check, if not fit, revert child with old data
            self.points['x'] = full_x1
            self.points['y'] = full_y1
            self.ptr = i
            self.fitness_check()
            if self.good_fit is False:
                full_x1[self.start_val:self.end_val] = x1
                full_y1[self.start_val:self.end_val] = y1
                self.temp_update(self.pop[i][0], full_x1, full_y1)
            self.points['x'] = full_x2
            self.points['y'] = full_y2
            self.ptr = i + 1
            self.fitness_check()
            if self.good_fit is False:
                full_x2[self.start_val:self.end_val] = x2
                full_y2[self.start_val:self.end_val] = y2
                self.temp_update(self.pop[i + 1][0], full_x2, full_y2)
        self.real_update()

    # chance of a random point being swapped with another
    def mutation(self, max_pop, mutation_rate, random_type):
        for i in range(max_pop):
            if mutation_rate > random.uniform(0, 1):
                self.points['x'] = self.pop[i][1]
                self.points['y'] = self.pop[i][2]
                self.generate_random(random_type)
                self.swap()
                self.fitness_check()
                if self.good_fit is False:
                    self.swap()
                    self.temp_update(self.pop[i][0])
            else:
                self.temp_update(self.pop[i][0])
        self.real_update()

    def execute(self, max_pop, iterations, mutation_rate, random_type=None):
        begin = time.perf_counter()
        self.open_csv(self.file_problem)
        if random_type == 'fixed':
            self.start_val = 1
            self.end_val = self.total_points - 1
        else:
            self.start_val = 0
            self.end_val = self.total_points
        self.create_pop(max_pop, random_type)
        self.running_update()
        for i in range(iterations):
            self.crossover(max_pop, random_type)
            self.mutation(max_pop, mutation_rate, random_type)

        self.t_stop = True
        self.points['y'] = self.pop[0][2]
        self.points['x'] = self.pop[0][1]
        self.update_csv(self.file_result)

        print('GENETIC ALGORITHM')
        print('times "improved":', len(self.pop_history))
        print('best distance:', self.pop[0][0])
        stop = time.perf_counter()
        print(f'Finished in {round(stop - begin, 4)} seconds')
        print('---------------------------------------------------------')
