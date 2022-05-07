from base import Base
import math
import random
import time


'''
    This simulated annealing is specifically for the travelling salesman

    Simulated Annealing (SA) has 2 parameters (all csv) when instantiating
        file_problem : str (csv)
            the problem to solve
        file_result  : str (csv)
            csv for result

    Run the function `execute` to perform SA, execute has 4 parameters
        initial_temp : int, float
            (can also be how many iterations until final_temp)
        alpha        : int, float
            the cooling down of initial temperature
        final_temp   : int, float
            end point
        random_type  : str (optional) [default is None]
            'fixed' to have fixed start and end position

    Example code
    `
    sa = SimulatedAnnealing('problem.csv', 'result1.csv', 'result2.csv')
    sa.execute('fixed', 50, 0.001, 0.1)
    `
'''


class SimulatedAnnealing(Base):
    dist_history = {'normal': [], 'best': []}

    def execute(self, initial_temp, alpha, final_temp, random_type=None):
        begin = time.perf_counter()
        self.open_csv(self.file_problem)
        curr_temp = initial_temp
        curr_dist = self.get_distance()
        best_dist = curr_dist
        self.dist_history['normal'].append(curr_dist)
        self.dist_history['best'].append(curr_dist)
        self.running_update()

        while curr_temp > final_temp:
            self.generate_random(random_type)
            self.swap()
            new_dist = self.get_distance()
            dist_diff = new_dist - curr_dist
            metropolis = math.exp(-dist_diff/curr_temp)

            # saves the best
            if new_dist < best_dist:
                best_dist = new_dist
                self.dist_history['best'].append(best_dist)

            # saves better results from previous or based on metropolis
            if dist_diff < 0 or random.uniform(0, 1) < metropolis:
                curr_dist = new_dist
                self.dist_history['normal'].append(curr_dist)

            # reverts position
            else:
                self.swap()

            # reduce temperature as time goes
            # alternatively, can use iterations and temperature separately
            # instead of using temperature for the iteration as well
            curr_temp -= alpha

        self.t_stop = True
        self.update_csv(self.file_result)

        print('SIMULATED ANNEALING')
        print('total norm "improvements":', len(self.dist_history['normal']))
        print('total best improvements:', len(self.dist_history['best']))
        print('best distance:', min(self.dist_history['best']))
        stop = time.perf_counter()
        print(f'Finished in {round(stop - begin, 4)} seconds')
        print('---------------------------------------------------------')
