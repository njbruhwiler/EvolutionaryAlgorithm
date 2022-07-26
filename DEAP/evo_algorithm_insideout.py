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
        individual = [9, 3, 2, 1, 10]
        individual = creator(individual)
        individuals.append(individual)
    return individuals

toolbox = base.Toolbox()
# Structure initializers
toolbox.register("population", load_individuals, creator.Individual)


def evalOneMax(individual):
    log = open("marlin_log_%s" % individual[1], 'w')
    min_efficiency = 0.75

    nhitstotal = individual[0][0]
    nhitsvertex = individual[0][1]
    nhitsinner = individual[0][2]
    nhitsouter = individual[0][3]
    pt = individual[0][4]/10.

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
                    "--FilterTracks.NHitsTotal=%s" % nhitstotal, 
                    "--FilterTracks.NHitsVertex=%s" % nhitsvertex, 
                    "--FilterTracks.NHitsInner=%s" % nhitsinner, 
                    "--FilterTracks.NHitsOuter=%s" % nhitsouter, 
                    "--FilterTracks.MinPt=%s" % pt],
                    stdout = log)

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
    k = 1000

    #if efficiency < min_efficiency:
        #return 0, 1000000000

    return 100*efficiency, -number_fakes/1000

pool = multiprocessing.Pool()
toolbox.register("map", pool.map)

toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutUniformInt, indpb=0.2)
toolbox.register("select", tools.selRandom, k=3)

def main():
    # Create output file
    outputfile = open('outputfile_insideout_fixed_2.txt', 'w')

    pop = toolbox.population(50)
    pop_index = []
    for i in range(len(pop)):
        pop_index.append(tuple([pop[i], i]))

    # Evaluate the entire population
    fitnesses = list(toolbox.map(toolbox.evaluate, pop_index))
    for ind, (fit1,fit2) in zip(pop, fitnesses):
        ind.fitness.values = (fit1,fit2)

    # MUTPB is the probability for mutating an individual
    MUTPB = 0.5

    # Extracting all the fitnesses of individuals
    fits = [ind.fitness.values for ind in pop]
    outputfile.write("Fits: %s \n\n" % fits)

    # List of scores to plot later on
    max_score = []
    max_score_eff = []
    max_score_fake = []
    max_eff = []
    max_eff_fake = []
    min_fake = []
    min_fake_eff = []
    avg_eff = []
    avg_fake = []


    # Variable keeping track of the number of generations
    g = 0

    hof = tools.HallOfFame(10)

    # Begin the evolution
    while g < 20:
        # A new generation
        g = g + 1
        print("-- Generation %i --" % g)
        outputfile.write("\n\n-- Generation %i -- \n\n" % g)

        # Select the next generation individuals
        #offspring = toolbox.select(pop, len(pop))
        offspring = []
        for i in range(len(pop)):
            aspirants = toolbox.select(pop_index)
            aspirant_scores = []
            print("Aspirants: ",aspirants)
            for individual in aspirants:
                aspirant_fitness = fits[individual[1]]
                print("Aspirant fitness: ",aspirant_fitness)
                aspirant_scores.append(aspirant_fitness[0]+aspirant_fitness[1])
            print("Aspirant scores: ",aspirant_scores)
            winning_score = max(aspirant_scores)
            winning_individual = aspirants[aspirant_scores.index(winning_score)][0]
            offspring.append(winning_individual)
            print("Offspring:", offspring)

        # Clone the selected individuals
        offspring = list(toolbox.map(toolbox.clone, offspring))
        outputfile.write("Offspring: %s \n\n" % offspring)

        #Apply mutation on the offspring
        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant, [0,0,0,0,5], [7,7,7,7,20])
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
        pop_index = []
        for i in range(len(pop)):
            pop_index.append(tuple([pop[i], i]))

        hof.update(pop)

        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values for ind in pop]
        outputfile.write("Fits: %s \n\n" % fits)

        efficiencies = []
        fake_numbers = []
        scores = []
        for item in fits:
            efficiencies.append(item[0]/100)
            fake_numbers.append(-item[1]*1000)
            scores.append(item[0]+item[1])

        length = len(pop)
        mean_eff = sum(efficiencies) / length
        sum2_eff = sum(x*x for x in efficiencies)
        std_eff = abs(sum2_eff / length - mean_eff**2)**0.5
        mean_fake = sum(fake_numbers) / length
        sum2_fake = sum(x*x for x in fake_numbers)
        std_fake = abs(sum2_fake / length - mean_fake**2)**0.5

        outputfile.write("Population: %s\n" % pop)
        outputfile.write("\nScores: %s\n" % scores)
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

        max_score.append(max(scores))
        max_score_eff.append(efficiencies[scores.index(max(scores))])
        max_score_fake.append(fake_numbers[scores.index(max(scores))])
        max_eff.append(max(efficiencies))
        max_eff_fake.append(fake_numbers[efficiencies.index(max(efficiencies))])
        min_fake.append(min(fake_numbers))
        min_fake_eff.append(efficiencies[fake_numbers.index(min(fake_numbers))])
        avg_eff.append(mean_eff)
        avg_fake.append(mean_fake)
    
        x = list(range(1,len(max_eff)+1))

        outputfile.write("\nMax eff: %s \n" % max_eff)
        outputfile.write("Min fake: %s \n" % min_fake)
        outputfile.write("Max score: %s \n" % max_score)

        plt.figure()
        plt.plot(x,max_score)
        plt.title("Max scores")
        plt.xlabel("Generation")
        plt.ylabel("Max score")
        plt.show()
        plt.savefig("max_score.png")
        
        plt.figure()
        plt.plot(x,max_score_eff)
        plt.title("Corresponding efficiency")
        plt.xlabel("Generation")
        plt.ylabel("Efficiency")
        plt.show()
        plt.savefig("max_score_eff.png")
        
        plt.figure()
        plt.plot(x,max_score_fake)
        plt.title("Corresponding number of fakes")
        plt.xlabel("Generation")
        plt.ylabel("Number of fake tracks")
        plt.show()
        plt.savefig("max_score_fake.png")

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

        plt.figure()
        plt.plot(x,min_fake)
        plt.title("Minimum number of fakes")
        plt.xlabel("Generation")
        plt.ylabel("Min number of fakes")
        plt.show()
        plt.savefig("min_fake.png")

        plt.figure()
        plt.plot(x,min_fake_eff)
        plt.title("Corresponding efficiency")
        plt.xlabel("Generation")
        plt.ylabel("Efficiency")
        plt.show()
        plt.savefig("min_fake_eff.png")

        plt.figure()
        plt.plot(x,avg_eff)
        plt.title("Average efficiency")
        plt.xlabel("Generation")
        plt.ylabel("Average efficiency")
        plt.show()
        plt.savefig("avg_eff.png")

        plt.figure()
        plt.plot(x,avg_fake)
        plt.title("Average number of fakes")
        plt.xlabel("Generation")
        plt.ylabel("Average number of fakes")
        plt.show()
        plt.savefig("avg_fake.png")

        subprocess.run(["rm", "actsseedckf_*.root"])
        
        

main()