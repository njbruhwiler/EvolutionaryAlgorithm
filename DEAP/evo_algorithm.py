import random
import subprocess
import ROOT
import numpy
import multiprocessing

from deap import base
from deap import creator
from deap import tools
from deap import algorithms

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

def load_individuals(creator, n):
    individuals = []
    for i in range(n):
        individual = [7, 3, 2, 1, 1.0]
        individual = creator(individual)
        individuals.append(individual)
    return individuals

toolbox = base.Toolbox()
# Structure initializers
toolbox.register("population", load_individuals, creator.Individual)


def evalOneMax(individual):
    log = open("log_%s" % individual[1], 'w')

    nhit = individual[0][0]
    nhit1 = individual[0][1]
    nhit2 = individual[0][2]
    nhit3 = individual[0][3]
    pt = individual[0][4]

    log.write("Nhit1: %s \n" % nhit1)
    log.write("Nhit2: %s \n" % nhit2)
    log.write("Nhit3: %s \n" % nhit3)

    subprocess.run(["Marlin", "example/actsseedckf_steer_hists.xml", 
                    "--global.LCIOInputFiles=/global/homes/n/natalieb/TrackPerfWorkspace/output_file.slcio",
                    "--MyAIDAProcessor.FileName=actsseedckf_%s" % individual[1],
                    "--FilterTracks.NHits=%s" % nhit, 
                    "--FilterTracks.NHits1=%s" % nhit1, 
                    "--FilterTracks.NHits2=%s" % nhit2, 
                    "--FilterTracks.NHits3=%s" % nhit3, 
                    "--FilterTracks.MinPt=%s" % pt])

    #get efficiency and fake rate to calculate score
    f = ROOT.TFile.Open("actsseedckf_%s.root" % individual[1])

    dir1 = f.Get("MyTrackPerf2")
    dir2 = dir1.Get("real")
    dir3 = dir1.Get("all")
    dir4 = dir1.Get("fake")

    real_truth = dir2.Get("truth_pt")
    all_truth = dir3.Get("truth_pt")
    fake_reco = dir4.Get("reco_nhit")

    entries_real = real_truth.GetEntries()
    entries_all = all_truth.GetEntries()
    number_fakes = fake_reco.GetEntries()

    efficiency = entries_real/entries_all
    print(efficiency)
    print(number_fakes)
    k = 1000

    log.write("Score: %s \n" % (efficiency - number_fakes/k))

    return efficiency - number_fakes/k

pool = multiprocessing.Pool()
toolbox.register("map", pool.map)

toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutUniformInt, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)

def main():
    # Create output file
    outputfile = open('outputfile.txt', 'w')

    pop = toolbox.population(50)
    hof = tools.HallOfFame(1)
    pop_index = []
    for i in range(len(pop)):
        pop_index.append(tuple([pop[i], i]))

    print(type(pop_index))
    print(pop_index)

    # Evaluate the entire population
    fitnesses = list(toolbox.map(toolbox.evaluate, pop_index))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = (fit,)

    # MUTPB is the probability for mutating an individual
    MUTPB = 0.3

    # Extracting all the fitnesses of individuals
    fits = [ind.fitness.values[0] for ind in pop]
    outputfile.write("Fits: %s \n" % fits)


    # Variable keeping track of the number of generations
    g = 0

    # Begin the evolution
    while g < 16:
        # A new generation
        g = g + 1
        print("-- Generation %i --" % g)
        outputfile.write("-- Generation %i -- \n" % g)

        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(toolbox.map(toolbox.clone, offspring))
        outputfile.write("Offspring: %s \n" % offspring)

        #Apply mutation on the offspring
        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant, 0, 7)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        outputfile.write("Invalid ind: %s \n" % invalid_ind)
        invalid_ind_index = []
        for i in range(len(invalid_ind)):
            invalid_ind_index.append(tuple([invalid_ind[i], i]))
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind_index)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = (fit,)

        pop[:] = offspring

        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]
        outputfile.write("Fits: %s \n" % fits)

        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5

        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
        print("  Avg %s" % mean)
        print("  Std %s" % std)
        print("  Hall of fame %s" % hof)
        outputfile.write("%s\n" % pop)
        outputfile.write("\n  Min %s \n" % min(fits))
        outputfile.write("  Max %s \n" % max(fits))
        outputfile.write("  Avg %s \n" % mean)
        outputfile.write("  Std %s \n" % std)
        outputfile.write("  Hall of fame %s \n" % hof)

        subprocess.run(["rm", "actsseedckf_*.root"])

main()