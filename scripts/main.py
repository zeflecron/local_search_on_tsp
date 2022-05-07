from hill_climbing import HillClimbing
from beam_search import BeamSearch
from simulated_annealing import SimulatedAnnealing
from genetic_algorithm import GeneticAlgorithm
import time

# SECTION: INITIALIZATION
problem_file = '../csvs/problem1.csv'
# change the 'fixed' into anything else to have a non-fixed start and end
random_type = 'fixed'

hc1 = HillClimbing(problem_file, '../csvs/hc_result_rand.csv')
hc2 = HillClimbing(problem_file, '../csvs/hc_result_stoch.csv')
bs = BeamSearch(problem_file, '../csvs/bs_result.csv')
sa = SimulatedAnnealing(problem_file, '../csvs/sa_result.csv')
ga = GeneticAlgorithm(problem_file, '../csvs/ga_result.csv')

# SECTION: EXECUTE
begin_all = time.perf_counter()

# parameter explanations are in each individual files
hc1.execute(100000, 'randomized', random_type)
hc2.execute(100000, 'stochastic', random_type)
bs.execute(100000, 5, 2, random_type)
sa.execute(10, 0.0001, 0.01, random_type)
ga.execute(100, 1000, 0.05, random_type)

stop_all = time.perf_counter()
print('---------------------------------------------------------')
print(f'All finished in {round(stop_all - begin_all, 4)} seconds')
