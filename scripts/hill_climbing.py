from base import Base
import time

'''
    This hill climbing is specifically for the travelling salesman

    Hill Climbing (HC) has 2 parameters (all csv) when instantiating
        file_problem    : str (csv)
            the problem to solve
        file_result     : str (csv)
            csv for result

    Run the function `execute` to perform HC, execute has 3 parameters
        iterations      : int
            --//--
        hc_type         : 'randomized', 'stochastic'
            selection between the 2 variations
        random_type     : str (optional) [default is None]
            'fixed' to have fixed start and end position

    Example code
    `
    hc = HillClimbing('problem.csv', 'random.csv', 'stochastic.csv')
    hc.execute(500000, 'randomized')
    `
'''


class HillClimbing(Base):
    dist_history = []

    def execute(self, iterations, hc_type, random_type=None):
        begin = time.perf_counter()
        self.open_csv(self.file_problem)
        curr_dist = self.get_distance()
        best_dist = curr_dist
        self.dist_history.append(curr_dist)
        self.running_update()

        # selection between random-restart or stochastic variation
        if hc_type == 'randomized':
            for i in range(iterations):
                self.full_random(random_type)
                new_dist = self.get_distance()

                # saves the best
                if new_dist < best_dist:
                    best_dist = new_dist
                    self.dist_history.append(best_dist)

        elif hc_type == 'stochastic':
            for i in range(iterations):
                self.generate_random(random_type)
                self.swap()
                new_dist = self.get_distance()

                # saves the best.25
                if new_dist < best_dist:
                    best_dist = new_dist
                    self.dist_history.append(best_dist)

                # reverts position
                else:
                    self.swap()

        self.t_stop = True
        self.update_csv(self.file_result)

        print('HILL CLIMBING', hc_type)
        print('total improvements:', len(self.dist_history))
        print('best distance:', min(self.dist_history))
        stop = time.perf_counter()
        print(f'Finished in {round(stop - begin, 4)} seconds')
        print('---------------------------------------------------------')
