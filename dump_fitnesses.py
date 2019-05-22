import pickle

with open("logs/fitnesses/2019-05-21 17-20-24.255472-population.txt", 'rb') as f:
    fitnesses = pickle.load(f)

print(fitnesses)