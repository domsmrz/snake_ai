import glob
import os
import pickle
import matplotlib.pyplot as plt


list_of_files = glob.glob('logs/fitnesses/*') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)

with open(latest_file, "rb") as f:
    fitness_log = pickle.load(f)

list_of_maxs = []
for i, generation in enumerate(fitness_log):
    print(i, max(generation), min(generation))

    list_of_maxs.append(max(generation))
plt.plot(list_of_maxs)
plt.show()