from base import Base
from itertools import islice
import time

'''
    This beam search is specifically for the travelling salesman

    Beam Search (BS) has 2 parameters (all csv) when instantiating
        file_problem    : str (csv)
            the problem to solve
        file_result     : str (csv)
            csv for result

    Run the function `execute` to perform BS, execute has 4 parameters
        iterations      : int
            --//--
        states          : int
            number of desired improvements for each successors
        k               : int
            number of selected successors after improvements
        random_type     : str (optional) [default is None]
            'fixed' to have fixed start and end position

    Example code
    `
    bs = BeamSearch('problem.csv', 'result.csv')
    bs.execute(1000, 3, 2)
    `
'''


class BeamSearch(Base):
    result = []
    temp_result = []
    content = {'name': '', 'dist': 0, 'x': [], 'y': []}
    result_history = []
    iter_ctr = 0

    @staticmethod
    def take(n, iterable):
        # returns first n items of the iterable as a list
        return list(islice(iterable, n))

    def temp_update(self, name, dist, x=None, y=None):
        if x is None and y is None:
            x = self.points['x']
            y = self.points['y']
        self.content['name'] = name
        self.content['dist'] = dist
        self.content['x'] = x
        self.content['y'] = y
        self.temp_result.append(tuple(self.content.values()))

    def real_update(self, k):
        temp = sorted(self.temp_result, key=lambda x: x[1])
        self.result = self.take(k, temp)
        if len(self.result) != 0:
            self.result_history.append(self.result)
        self.temp_result = []

    def execute(self, iterations, states, k, random_type=None):
        begin = time.perf_counter()
        self.open_csv(self.file_problem)
        curr_dist = self.get_distance()
        self.temp_update('root', curr_dist)
        self.real_update(k)
        self.running_update()

        while self.iter_ctr < iterations:

            # self.result is based on k (except the first which is only 1)
            for i in range(len(self.result)):
                ctr = 0
                best_dist = self.result[i][1]
                while ctr < states:
                    self.iter_ctr += 1

                    if self.iter_ctr > iterations:
                        break

                    self.generate_random(random_type)
                    self.swap()
                    new_dist = self.get_distance()

                    if new_dist < best_dist:
                        best_dist = new_dist
                        self.temp_update(f'successor_{i}_{ctr}', best_dist)
                        ctr += 1

                    # reverts position
                    else:
                        self.swap()

            self.real_update(k)

        self.t_stop = True
        self.update_csv(self.file_result)

        print('BEAM SEARCH')
        print('total "improvements":', len(self.result_history))
        print('best:', min(self.result_history[-1], key=lambda x: x[1])[1])
        stop = time.perf_counter()
        print(f'Finished in {round(stop - begin, 4)} seconds')
        print('---------------------------------------------------------')
