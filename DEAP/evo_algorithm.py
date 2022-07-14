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

creator.create("FitnessMax", base.Fitness, weights=(1.0,-.001))
creator.create("Individual", list, fitness=creator.FitnessMax)

def load_individuals(creator, n):
    individuals = []
    for i in range(n):
        individual = [9, 3, 2, 1, 10]
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
    pt = individual[0][4]/10.

    log.write("Nhit: %s \n" % nhit)
    log.write("Nhit1: %s \n" % nhit1)
    log.write("Nhit2: %s \n" % nhit2)
    log.write("Nhit3: %s \n" % nhit3)
    log.write("MinPt: %s \n" % pt)

    subprocess.run(["Marlin", "example/actsseedckf_steer_hists.xml", 
                    "--global.LCIOInputFiles=/global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_0_0.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_100_3.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_101_4.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_102_5.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_103_6.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_104_7.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_105_8.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_106_9.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_107_10.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_108_11.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_109_12.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_10_2.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_110_14.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_111_15.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_112_16.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_113_17.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_114_18.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_115_19.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_116_20.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_117_21.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_118_22.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_119_23.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_11_13.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_120_25.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_121_26.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_122_27.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_123_28.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_124_29.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_125_30.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_126_31.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_127_32.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_128_33.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_129_34.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_12_24.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_130_36.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_131_37.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_132_38.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_133_39.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_134_40.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_135_41.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_136_42.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_137_43.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_138_44.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_139_45.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_13_35.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_140_47.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_141_48.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_142_49.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_143_50.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_144_51.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_145_52.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_146_53.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_147_54.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_148_55.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_149_56.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_14_46.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_150_58.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_15_57.slcio \
                    /global/cfs/cdirs/atlas/natalieb/test_me_BIB_partial_insideout/output_muonGun_sim_MuColl_v1_1_1.slcio",
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

    f.Close()

    return efficiency, number_fakes

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

    # List of maximum scores to plot later on
    max_eff = []
    min_fake = []

    # Variable keeping track of the number of generations
    g = 0

    hof = tools.HallOfFame(1)

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
                toolbox.mutate(mutant, [0,0,0,0,5], [7,7,7,7,20])
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        outputfile.write("Invalid ind: %s \n" % invalid_ind)
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
        outputfile.write("Fits: %s \n" % fits)

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
        outputfile.write("  Std fake %s \n" % std_fake)
        for item in hof:
            outputfile.write("  Hall of fame %s" % item)

        max_eff.append(max(efficiencies))
        min_fake.append(min(fake_numbers))
    
        x = list(range(1,len(max_eff)+1))
        outputfile.write("Max eff: %s \n" % max_eff)
        outputfile.write("Min fake: %s \n" % min_fake)
        plt.figure()
        plt.plot(x,max_eff)
        plt.xlabel("Generation")
        plt.ylabel("Max efficiency")
        plt.show()
        plt.savefig("eff.png")
        plt.figure()
        plt.plot(x,min_fake)
        plt.xlabel("Generation")
        plt.ylabel("Min number of fakes")
        plt.show()
        plt.savefig("fake.png")

        subprocess.run(["rm", "actsseedckf_*.root"])
        
        

main()