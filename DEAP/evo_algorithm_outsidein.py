import random
import subprocess
import ROOT
import numpy
import multiprocessing
import matplotlib.pyplot as plt

from deap import base
from deap import creator
from deap import tools
from deap import algorithms

creator.create("FitnessMax", base.Fitness, weights=(1.0,1.0))
creator.create("Individual", list, fitness=creator.FitnessMax)

def load_individuals(creator, n):
    individuals = []
    for i in range(n):
        #parameters: [collision region, trackerror_relp, trackerror_phi, trackerror_lambda, trackerror_pos, chi2cutoff, nummeasurementscutoff]
        individual = [5, 2, 2, 2, 1, 1, 1]
        individual = creator(individual)
        individuals.append(individual)
    return individuals

toolbox = base.Toolbox()
# Structure initializers
toolbox.register("population", load_individuals, creator.Individual)


def evalOneMax(individual):
    log = open("marlin_log_%s" % individual[1], 'w')
    min_efficiency = 0.75

    collisionregion = individual[0][0] * 10
    trackerror_relp = individual[0][1] / 10
    trackerror_phi = individual[0][2] / 100
    trackerror_lambda = individual[0][3] /100
    trackerror_pos = individual[0][4] / 10
    chi2cutoff = individual[0][5] * 10
    nummeasurementscutoff = individual[0][6]

    subprocess.run(["Marlin", "example/actsseedckf_steer_out.xml", 
                    "--global.LCIOInputFiles=/global/cfs/cdirs/atlas/kkrizka/MCC/tracking/muonGun_sim_MuColl_v1.slcio",
                    "--MyAIDAProcessor.FileName=actsseedckf_%s" % individual[1],
                    "--MyCKFTracking.SeedFinding_CollisionRegion=%s" % collisionregion, 
                    "--MyCKFTracking.InitialTrackError_RelP=%s" % trackerror_relp, 
                    "--MyCKFTracking.InitialTrackError_Phi=%s" % trackerror_phi, 
                    "--MyCKFTracking.InitialTrackError_Lambda=%s" % trackerror_lambda, 
                    "--MyCKFTracking.InitialTrackError_Pos=%s" % trackerror_pos, 
                    "--MyCKFTracking.CKF_Chi2CutOff=%s" % chi2cutoff, 
                    "--MyCKFTracking.CKF_NumMeasurementsCutOff=%s" % nummeasurementscutoff], 
                    stdout = log)

    #get efficiency and fake rate to calculate score
    f = ROOT.TFile.Open("actsseedckf_%s.root" % individual[1])

    dir1 = f.Get("MyTrackPerf")
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
    k = 1000

    return 100*efficiency, -.001*number_fakes

pool = multiprocessing.Pool()
toolbox.register("map", pool.map)

toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutUniformInt, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)

def main():
    # Create output file
    outputfile = open('outputfile_outsidein_noBIB.txt', 'w')

    pop = toolbox.population(50)
    pop_index = []
    for i in range(len(pop)):
        pop_index.append(tuple([pop[i], i]))

    print(type(pop_index))
    print(pop_index)

    # Evaluate the entire population
    fitnesses = list(toolbox.map(toolbox.evaluate, pop_index))
    for ind, (fit1,fit2) in zip(pop, fitnesses):
        ind.fitness.values = (fit1,fit2)

    # MUTPB is the probability for mutating an individual
    MUTPB = 0.3

    # Extracting all the fitnesses of individuals
    fits = [ind.fitness.values for ind in pop]
    outputfile.write("Fits: %s \n" % fits)

    # List of scores to plot later on
    max_eff = []
    max_eff_fake = []

    # Variable keeping track of the number of generations
    g = 0

    hof = tools.HallOfFame(10)

    # Begin the evolution
    while g < 16:
        # A new generation
        g = g + 1
        print("-- Generation %i --" % g)
        outputfile.write("\n\n-- Generation %i -- \n\n" % g)

        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(toolbox.map(toolbox.clone, offspring))
        outputfile.write("Offspring: %s \n\n" % offspring)

        #Apply mutation on the offspring
        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant, [1,0,0,0,0,0,1], [15,10,20,20,10,10,5])
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        outputfile.write("Invalid ind: %s \n\n" % invalid_ind)
        invalid_ind_index = []
        for i in range(len(invalid_ind)):
            invalid_ind_index.append(tuple([invalid_ind[i], i]))
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind_index)
        for ind, (fit1,fit2) in zip(invalid_ind, fitnesses):
            ind.fitness.values = (fit1,fit2)

        pop[:] = offspring

        hof.update(pop)

        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values for ind in pop]
        outputfile.write("Fits: %s \n\n" % fits)

        efficiencies = []
        fake_numbers = []
        for item in fits:
            efficiencies.append(item[0])
            fake_numbers.append(item[1])

        length = len(pop)
        mean_eff = sum(efficiencies) / length
        sum2_eff = sum(x*x for x in efficiencies)
        std_eff = abs(sum2_eff / length - mean_eff**2)**0.5
        mean_fake = sum(fake_numbers) / length
        sum2_fake = sum(x*x for x in fake_numbers)
        std_fake = abs(sum2_fake / length - mean_fake**2)**0.5

        outputfile.write("Population: %s\n" % pop)
        outputfile.write("\n  Min eff %s \n" % min(efficiencies))
        outputfile.write("  Max eff %s \n" % max(efficiencies))
        outputfile.write("  Avg eff %s \n" % mean_eff)
        outputfile.write("  Std eff %s \n" % std_eff)
        outputfile.write("\n  Min fake %s \n" % min(fake_numbers))
        outputfile.write("  Max fake %s \n" % max(fake_numbers))
        outputfile.write("  Avg fake %s \n" % mean_fake)
        outputfile.write("  Std fake %s \n\n" % std_fake)
        for item in hof:
            outputfile.write("  Hall of fame %s \n" % item)

        max_eff.append(max(efficiencies))
        max_eff_fake.append(fake_numbers[efficiencies.index(max(efficiencies))])
    
        x = list(range(1,len(max_eff)+1))

        outputfile.write("\nMax eff: %s \n" % max_eff)

        plt.figure()
        plt.plot(x,max_eff)
        plt.title("Max efficiency")
        plt.xlabel("Generation")
        plt.ylabel("Max efficiency")
        plt.show()
        plt.savefig("max_eff.png")

        plt.figure()
        plt.plot(x,max_eff_fake)
        plt.title("Corresponding number of fakes")
        plt.xlabel("Generation")
        plt.ylabel("Number of fakes")
        plt.show()
        plt.savefig("max_eff_fake.png")

        subprocess.run(["rm", "actsseedckf_*.root"])
        
        

main()