# Local Search on TSP
Local search algorithms solving the travelling salesman problem with matplotlib plotting

![v1.0/img_1.0_1.PNG](https://github.com/zeflecron/local_search_on_tsp/blob/main/changelog/v1.0/img_1.0_1.PNG)

# How to run it
1. Put all the folders and files into a directory
2. Create a virtual environment in that directory using cmd: `python -m venv venv`
3. Activate the virtual environment: `venv\Scripts\activate.bat`
4. Download the dependencies: `pip install -r requirements.txt`
5. Use an IDE (like PyCharm) and run `travelling_salesman.py`
6. Another window should appear with 6 subplots
7. Run `main.py` while the other is also running and see the plotting real-time

## The algorithms
There are 4 different local search types that are coded here:

### 1. Hill Climbing
It has 2 variations, random-restart and stochastic (both are shown in the plotting)

- Random-restart (sometimes also called shotgun mode) randomizes everything and take only if the result is better than the previous
- Stochastic is also random, but it only swaps points one by one and only accepts them if they improve the result. A worse result would be reverted back to the previous one

### 2. Beam Search
(I myself am not sure if the definition is correct but, it is basically multiple hill climbing rather than just 1)
It takes a certain number of improvements first before selecting another certain number of improved results and then the process repeats itself

Example: 
- Root generates 5 improvements
- From that 5, 2 is selected
- Then from those 2, each of them generate another 5 (total 10) 
- And from 10, 2 is selected, and so on

### 3. Simulated Annealing
Very similar to stochastic hill climbing but it has a random chance of taking a worse option in order to escape the local minima. Based on the name itself, it simulates the annealing process, start of with high temperature then it start to cool down slowly

- High initial temperature = More chaotic start
- Low alpha/cooling = Better chance to improve
- High end temperature = Might stop at local minimum

### 4. Genetic Algorithm
It is like partial DNA swapping with selective improvements (uses the cycle algorithm to retain the parts of DNA)

- DNA is first generated randomly with a certain number of population
- The population is then put into a fitness test (how well the result is or if it is even worse)
- Afterwards, each DNA will retain a random part of it and the rest will be swapped with another DNA (they come in pairs)
- Checked again whether it fits, if it does not, revert it back
- Finally, there is a small chance of mutation (random point swap) and it will once again be checked if it fits or not
- Process repeats until iteration is complete

## The plotting
Uses matplotlib (although PyQtGraph might be better for smoother experience)

- If plotting window is too big, it can be changed in the code
- If real-time is too slow/too fast, change the interval/frames
- If real-time does not work, switch to normal plotting (but it only shows the initial/final result)

