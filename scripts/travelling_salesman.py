import random
import csv
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

'''
    To generate and plot Travelling Salesman Problem (TSP)

    The function `generate_tsp` has 2 parameters
        filename : str
            creates a csv file
        type     : str (optional) [default is None]
            'unique' to have unique (no duplicate) plots

    The function `real_time` has 1 parameter
        arg      : str (csv)
            reads the csv file to plot

    Example code
    `
    tsp = TravellingSalesman()
    tsp.generate_tsp('unique')
    tsp.real_time('stochastic.csv')
    `
'''


class TravellingSalesman:
    fig, axs = plt.subplots(2, 3, figsize=(18, 10))
    points = {'x': [], 'y': []}
    last_points = {'x': [], 'y': []}
    total_points = 0
    min_points = 0
    checker = True

    def __init__(self):
        pass

    @staticmethod
    def generate_tsp(filename, total_points):
        x = []
        y = []
        coordinates = []
        for i in range(total_points):
            gen_x = random.randint(1, total_points)
            gen_y = random.randint(1, total_points)
            point = [list(z) for z in zip([gen_x, gen_y])]

            # prevents duplicates
            while point in coordinates:
                gen_x = random.randint(1, total_points)
                gen_y = random.randint(1, total_points)
                point = [list(z) for z in zip([gen_x, gen_y])]
            coordinates.append(point)
            x.append(gen_x)
            y.append(gen_y)

        with open(filename, 'w', newline='') as new_csv:
            fieldnames = ['x', 'y']
            csv_writer = csv.DictWriter(new_csv, fieldnames=fieldnames)
            csv_writer.writeheader()
            writer = csv.writer(new_csv)
            values = zip(x, y)
            for row in values:
                writer.writerow(row)

        print(x)
        print(y)
        print('complete')

    def plotting(self, prob_file, hc_file_rand, hc_file_stoch,
                 bs_file, sa_file, ga_file):
        self.fig.suptitle('Local Search on Travelling Salesman Problem')

        file_set = [
            prob_file,
            hc_file_rand,
            hc_file_stoch,
            bs_file,
            sa_file,
            ga_file
        ]

        for i in range(6):
            try:
                data = pd.read_csv(file_set[i])
                x = data['x']
                y = data['y']
            except:
                continue

            if i == 0:
                self.axs[0, 0].plot(x, y, '--ko')
                self.axs[0, 0].set_title('Initial problem')
            elif i == 1:
                self.axs[0, 1].plot(x, y, '--bo')
                self.axs[0, 1].set_title('Hill Climbing (random-restart)')
            elif i == 2:
                self.axs[0, 2].plot(x, y, '--co')
                self.axs[0, 2].set_title('Hill Climbing (stochastic)')
            elif i == 3:
                self.axs[1, 0].plot(x, y, '--ro')
                self.axs[1, 0].set_title('Beam Search')
            elif i == 4:
                self.axs[1, 1].plot(x, y, '--mo')
                self.axs[1, 1].set_title('Simulated Annealing')
            else:
                self.axs[1, 2].plot(x, y, '--go')
                self.axs[1, 2].set_title('Genetic Algorithm')

        for ax in self.axs.flat:
            ax.set(xlabel='x', ylabel='y')

        # hide labels that are shared across plots
        for ax in self.axs.flat:
            ax.label_outer()

        plt.show()

    def animate(self, i, prob_file, hc_file_rand,
                hc_file_stoch, bs_file, sa_file, ga_file):
        self.fig.suptitle('Local Search on Travelling Salesman Problem')

        file_set = [
            prob_file,
            hc_file_rand,
            hc_file_stoch,
            bs_file,
            sa_file,
            ga_file
        ]

        for i in range(6):
            try:
                data = pd.read_csv(file_set[i])
                x = data['x']
                y = data['y']
            except:
                continue

            if i == 0:
                self.axs[0, 0].clear()
                self.axs[0, 0].plot(x, y, '--ko')
                self.axs[0, 0].set_title('Initial problem')
            elif i == 1:
                self.axs[0, 1].clear()
                self.axs[0, 1].plot(x, y, '--bo')
                self.axs[0, 1].set_title('Hill Climbing (random-restart)')
            elif i == 2:
                self.axs[0, 2].clear()
                self.axs[0, 2].plot(x, y, '--co')
                self.axs[0, 2].set_title('Hill Climbing (stochastic)')
            elif i == 3:
                self.axs[1, 0].clear()
                self.axs[1, 0].plot(x, y, '--ro')
                self.axs[1, 0].set_title('Beam Search')
            elif i == 4:
                self.axs[1, 1].clear()
                self.axs[1, 1].plot(x, y, '--mo')
                self.axs[1, 1].set_title('Simulated Annealing')
            else:
                self.axs[1, 2].clear()
                self.axs[1, 2].plot(x, y, '--go')
                self.axs[1, 2].set_title('Genetic Algorithm')

        for ax in self.axs.flat:
            ax.set(xlabel='x', ylabel='y')

        # hide labels that are shared across plots
        for ax in self.axs.flat:
            ax.label_outer()

    # change interval or frames to set the plotting animation speed
    def real_time(self, *args):
        ani = FuncAnimation(self.fig, self.animate, fargs=(*args,),
                            interval=1000, frames=100)
        plt.show()
        return ani


tsp = TravellingSalesman()

# to generate a new tsp
# tsp.generate_tsp('../csvs/problem2.csv', 40)

# if real time crashes or just want to see end result
# tsp.plotting('problem1.csv', 'hc_result_rand.csv',
#              'hc_result_stoch.csv', 'bs_result.csv',
#              'sa_result.csv', 'ga_result.csv')

tsp.real_time('../csvs/problem1.csv',
              '../csvs/hc_result_rand.csv',
              '../csvs/hc_result_stoch.csv',
              '../csvs/bs_result.csv',
              '../csvs/sa_result.csv',
              '../csvs/ga_result.csv')
