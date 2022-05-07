import math
import random
import csv
from threading import Timer


class Base:
    points = {'x': [], 'y': []}
    total_points = 0
    nums = {'a': 0, 'b': 0}
    t = None
    t_stop = False

    def __init__(self, file_problem, file_result):
        self.file_problem = file_problem
        self.file_result = file_result

    # used for real time plotting (every 1 second)
    def running_update(self):
        if self.t_stop is False:
            self.update_csv(self.file_result)
            self.t = Timer(1, self.running_update)
            self.t.daemon = True
            self.t.start()

    def open_csv(self, filename):
        self.total_points = 0
        self.points['x'] = []
        self.points['y'] = []
        with open(filename, newline='') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                self.points['x'].append(int(row[0]))
                self.points['y'].append(int(row[1]))
                self.total_points += 1

    def update_csv(self, filename):
        with open(filename, 'w', newline='') as file:
            fieldnames = ['x', 'y']
            csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
            csv_writer.writeheader()

            writer = csv.writer(file)
            values = zip(self.points['x'], self.points['y'])
            for row in values:
                writer.writerow(row)

    def get_distance(self):
        total_dist = 0
        for i in range(self.total_points - 1):
            x_dist = self.points['x'][i] - self.points['x'][i+1]
            y_dist = self.points['y'][i] - self.points['y'][i+1]
            dist = math.sqrt((x_dist**2 + y_dist**2))
            total_dist += dist
        return total_dist

    # randomizes all the points
    def full_random(self, random_type):
        x = self.points['x']
        y = self.points['y']

        # use zip to randomize both list together
        combine = list(zip(x, y))

        if random_type == 'fixed':
            start = 1
            end = self.total_points - 1
        else:
            start = 0
            end = self.total_points

        segment = combine[start:end]
        random.shuffle(segment)
        combine[start:end] = segment

        # unzip and separate lists
        x, y = zip(*combine)
        self.points['x'] = list(x)
        self.points['y'] = list(y)

    # function to randomize the swapping points in the plot
    def generate_random(self, random_type):
        if random_type == 'fixed':
            start = 1
            end = self.total_points - 2
        else:
            start = 0
            end = self.total_points - 1

        self.nums['a'] = random.randint(start, end)
        self.nums['b'] = random.randint(start, end)

        # to ensure that it will not try to swap with itself
        while self.nums['a'] == self.nums['b']:
            self.nums['a'] = random.randint(start, end)
            self.nums['b'] = random.randint(start, end)

    # swaps 2 points in the plot
    def swap(self):
        a = self.nums['a']
        b = self.nums['b']
        x = self.points['x']
        y = self.points['y']
        x[a], x[b] = x[b], x[a]
        y[a], y[b] = y[b], y[a]
