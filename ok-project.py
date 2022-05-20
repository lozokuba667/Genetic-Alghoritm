import numpy as np
import random
import generator as gen
import graph_sol as gs
from matplotlib import pyplot as plt
import time

# GENERATOR FUNCTIONS
def createCombinations(alph, width):
    length = len(alph)
    createAllCombinationsRecursivly(alph, "", length, width)

def createAllCombinationsRecursivly(alph, prefix, length, width):
    if width == 0:
        combinations.append(prefix)
        return
    for i in range(length):
        newPrefix = prefix + alph[i]
        createAllCombinationsRecursivly(alph, newPrefix, length, width - 1)

# VERIFYING FUNCTIONS
def reverseContent(txt):
    return txt[::-1]

def verifyData(data):
    reconstruction = ""
    conv = getMaximumConvergance(data[0], data[1])
    if conv == 0:
        reconstruction += data[0] + data[1]
    else:
        reconstruction += data[0] + data[1][conv:]

    for i in range(2, len(data)):
        clipping = reconstruction[(-width_of_window):]
        conv = getMaximumConvergance(clipping, data[i])
        if conv == 0:
            reconstruction += data[i]
        else:
            reconstruction += data[i][conv:]

    return reconstruction

def getMaximumConvergance(one, two):
    scissors = -1
    convergance = 0
    for i in range(len(one)):
        contep = two[:(-scissors)]
        if one[scissors:] == contep:
            convergance = -scissors
        scissors -= 1
    return convergance

def findNearest(array, value):
    arr = np.asarray(array)
    idx = (np.abs(arr - value)).argmin()
    return arr[idx]

def createComplementary(seq):
    complementar = {"A": "T", "C": "G", "T": "A", "G": "C"}
    new_seq = ""
    for char in seq:
        new_seq += complementar[char]

    return new_seq


# GRAPH_POPULATION FUNCTIONS
def getNumberOfPositive(percentage,matrice):
    amount = (percentage / 100) * len(matrice)
    amount = int(amount)
    return amount

def selectRandomPositive(empty,stats,matrice,percentage):
    amount = getNumberOfPositive(percentage,matrice)
    windows = list(stats.keys())
    for i in range(amount):
        current = random.choice(windows)
        while current in empty:
            current = random.choice(windows)
        empty.append(current)
    
    return empty

def createPopulationAsGraph(graph,stats,matrice,pop_size):
    population_graph = []
    for i in range(pop_size):
        # print(f'FAMILY {i}')
        forbidden = []
        forbidden = selectRandomPositive(forbidden,stats,matrice,positive_mistakes)
        solution = []
        all_routes = gs.getAllRoutes(graph)
        first_mem = gs.selectFirstMember(matrice, forbidden, stats)
        solution.append(first_mem)
        neighbourhood = gs.searchNeighbourhood(first_mem,all_routes)
        
        while gs.validateNeighbourhood(neighbourhood,forbidden,stats,solution): #Jeśli jest możliwość wybrać najlepsze to wtedy zawsze dobierze najlepsze, jeśli nie to i tak nie zalezy bo losowe
            vert = gs.pickNeighbour(neighbourhood,forbidden, stats,solution,graph)
            solution.append(vert)
            neighbourhood = gs.searchNeighbourhood(vert,all_routes)
        
        # print (f'This is my test solution {i} BEFORE prep: {solution}')
        # if 'wiele' in stats.values():
        #     print('I have multi windows')
        # print(f'Solution {i} has length {len(solution)} and i should have {testCount(stats,forbid)}')
        # print()
        solution = gs.prepareGraphSolution(solution,stats)
        # print (f'This is my test solution {i} AFTER prep: {solution}')
        # if 'wiele' in stats.values():
        #     print('I have multi windows')
        # print(f'Solution {i} has length {len(solution)} and i should have {testCount(stats,forbid)}')
        # print()
        population_graph.append(solution)
        print(f'I have added {i} solution out of {pop_size} TEST VAL')
    
    return population_graph

# METAHEURESTICS FUNCTIONS
def tournamentSelection(population, num_of_contest):

    parents = []
    for i in range(2):

        contestants = []
        for x in range(num_of_contest):
            single_one = random.choice(population)

            while single_one in contestants:
                single_one = random.choice(population)

            contestants.append(single_one)

        cont_stats = {}
        for every in contestants:
            cont_stats[len(verifyData(every))] = every

        lst = list(cont_stats.keys())
        the_nearest = findNearest(lst, length_of_seq)
        parent = cont_stats[the_nearest]
        parents.append(parent)

    return parents

def improvedTournament(population, num_of_contest):
    parents = []
    for i in range(2):

        contestants = []
        for x in range(num_of_contest):
            single_one = random.choice(population)

            while single_one in contestants:
                single_one = random.choice(population)

            contestants.append(single_one)

        cont_stats = {}
        for every in contestants:
            key = len(verifyData(every))
            if key not in cont_stats:
                cont_stats[key] = list()
            cont_stats[key].append(every)

        lst = list(cont_stats.keys())
        the_nearest = findNearest(lst,length_of_seq)
        if len(cont_stats[the_nearest]) > 1:
            sort_short = sorted(cont_stats[the_nearest], key=len)
            parent = sort_short[0]
        else:
            short = cont_stats[the_nearest]
            parent = short[0]
            
        parents.append(parent)

    return parents

def testCount(stats,forbid):
    sum = 0
    values = list(stats.values())
    for val in values:
        if val != 'wiele':
            sum+=val
    
    sum = sum - len(forbid)
    
    return sum

def crossLeftMiddle(left,mid,stats):
    temp_left = []
    for single in left:
        if stats[single] == 1:
            if single not in mid:
                temp_left.append(single)
        elif stats[single] == 2:
            if mid.count(single) < 2:
                if mid.count(single) == 1:
                    if temp_left.count(single) == 0:
                        temp_left.append(single)
                elif mid.count(single) == 0:
                    if temp_left.count(single) < 2:
                        temp_left.append(single)
        else:
            if mid.count(single) < 3:
                if mid.count(single) == 2:
                    if temp_left.count(single) == 0:
                        temp_left.append(single)
                elif mid.count(single) == 1:
                    if temp_left.count(single) < 2:
                        temp_left.append(single)
                else:
                    if temp_left.count(single) < 3:
                        temp_left.append(single)
    
    return temp_left
   
def crossRestRight(parent,rest,stats):
    temp_right = []
    for elem in parent:
        if stats[elem] == 1:
            if elem not in rest:
                temp_right.append(elem)
        elif stats[elem] == 2:
            if rest.count(elem) < 2:
                if rest.count(elem) == 1:
                    if temp_right.count(elem) == 0:
                        temp_right.append(elem)
                elif rest.count(elem) == 0:
                    if temp_right.count(elem) < 2:
                        temp_right.append(elem)
        else:
            if rest.count(elem) < 3:
                if rest.count(elem) == 2:
                    if temp_right.count(elem) == 0:
                        temp_right.append(elem)
                elif rest.count(elem) == 1:
                    if temp_right.count(elem) < 2:
                        temp_right.append(elem)
                else:
                    if temp_right.count(elem) < 3:
                        temp_right.append(elem)
    
    return temp_right

def createChild(left,mid,parent,stats):
    temp_left_child = crossLeftMiddle(left,mid,stats)
    temp_left_mid_child = temp_left_child + mid
    temp_right_child = crossRestRight(parent,temp_left_mid_child,stats)
    child = temp_left_child + mid + temp_right_child
    return child

def certainCrossover(one,two,stats):
    children = []
    
    if len(one) < len(two):
        point_to_cut_1 = random.randint(0,len(one)-1)
        point_to_cut_2 = random.randint(0,len(one)-1)
    elif len(two) < len(one):
        point_to_cut_1 = random.randint(0,len(two)-1)
        point_to_cut_2 = random.randint(0,len(two)-1)
    else:
        point_to_cut_1 = random.randint(0,len(one)-1)
        point_to_cut_2 = random.randint(0,len(two)-1)
    
    while point_to_cut_2 == point_to_cut_1:
        point_to_cut_2 = random.randint(0,len(two))
    
    if point_to_cut_1 < point_to_cut_2:
        point_to_cut_2 = point_to_cut_2 + 1
        
        middle_1 = one[point_to_cut_1:point_to_cut_2]
        middle_2 = two[point_to_cut_1:point_to_cut_2]
        
        left_1 = one[:point_to_cut_1]
        left_2 = two[:point_to_cut_1]
        
        child_1 = createChild(left_2, middle_1,two,stats)
        children.append(child_1)
        child_2 = createChild(left_1, middle_2,one,stats)
        children.append(child_2)
        
    else:
        point_to_cut_1 = point_to_cut_1+1
        
        middle_1 = one[point_to_cut_2:point_to_cut_1]
        middle_2 = two[point_to_cut_2:point_to_cut_1]
        
        left_1 = one[:point_to_cut_2]
        left_2 = two[:point_to_cut_2]
        
        child_1 = createChild(left_2, middle_1,two,stats)
        children.append(child_1)
        child_2 = createChild(left_1, middle_2,one,stats)
        children.append(child_2)
    
    
    return children
 
def certainMutation(one,two):
    mutants = []
    mutated_child_1 = mutateWithRandomPos(one)
    mutants.append(mutated_child_1)
    mutated_child_2 = mutateWithRandomPos(two)
    mutants.append(mutated_child_2)
    return mutants 
 
def mutateWithRandomPos(single):
    point_area_1 = random.randint(0,len(single)-1)
    point_area_2 = random.randint(0,len(single)-1)
    
    if point_area_1 == point_area_2:
        temp_mut = single[:]
        rem1 = single[point_area_1]
        rem2 = single[point_area_1 - 1]
        temp_mut[point_area_1] = rem2
        temp_mut[point_area_1-1] = rem1
        mutant = temp_mut
    
    elif point_area_1 < point_area_2:
        prob_of_micro_cross = 0.5
        point_area_2 = point_area_2+1
        rev_1 = single[:]
        rev_2 = list(reversed(single[point_area_1:point_area_2]))
        t=0
        for i in range(point_area_1,point_area_2):
            rev_1[i] = rev_2[t]
            t=t+1
        mutant = rev_1
    
    else:
        point_area_1 = point_area_1+1
        rev_1 = single[:]
        rev_2 = list(reversed(single[point_area_2:point_area_1]))
        t=0
        for i in range(point_area_2,point_area_1):
            rev_1[i] = rev_2[t]
            t=t+1
        mutant = rev_1
    
    return mutant
        
def elitistPopulation(population):
    temp = population[:]
    pop_stats = {}
    for every in temp:
        pop_stats[len(verifyData(every))] = every
    
    lst = list(pop_stats.keys())
    the_best = findNearest(lst, length_of_seq)
    the_worst = max(lst)
    
    for i in range(len(temp)):
        if temp[i] == pop_stats[the_worst]:
            remind = i
    
    temp[remind] = pop_stats[the_best]
    
    final_pop = temp
    return final_pop        

def improvedElitism(population,pop_stats,best_sol):
    temp = population[:]
    lst = list(pop_stats.keys())        
    max_elem = sorted(lst,reverse=True)[:3]
    for i in range(len(population)):
        if population[i] in pop_stats[max_elem[0]] or population[i] in pop_stats[max_elem[1]]:
            temp[i] = best_sol
    
    elitar_pop = temp
    return elitar_pop
        
def populationStats(population):
    temp = population[:]
    pop_stats = {}
    for every in temp:
        key = len(verifyData(every))
        if key not in pop_stats:
            pop_stats[key] = list()
        pop_stats[key].append(every)
    
    return pop_stats

def findBestInPop(pop_stats):    
    lst = list(pop_stats.keys())
    the_best = findNearest(lst, length_of_seq)
    if len(pop_stats[the_best]) > 1:
        sort_sol = sorted(pop_stats[the_best],key = len)
        best = sort_sol[0]
    else:
        sort_sol = pop_stats[the_best]
        best = sort_sol[0]
    return best

def findBestGeneration(population,best_one):
    for i in range(len(population)):
        if population[i] == best_one:
            return i


start_gen_and_fun = time.time()
print()
print('#############################################################################')
print('############### GENERATOR ###################################################')
print('#############################################################################')
print()
alphabet = list("ACTG")
combinations = []
validation = True
length_of_seq = int(input("Enter length of sequence: "))
width_of_window = int(input("Enter width of window: "))
negative_mistakes = int(input("Enter negative mistakes [%]: "))
positive_mistakes = int(input("Enter positive mistakes [%]: "))
createCombinations(alphabet, width_of_window)
if length_of_seq >= 100 or negative_mistakes > 10:
    sequence = gen.createSeq(length_of_seq,alphabet)
    rep = gen.countNegative(sequence,width_of_window)
else:
    while validation:
        sequence = gen.createSeq(length_of_seq, alphabet)
        validation = gen.validateSeq(sequence, width_of_window)
        rep = 0

print()
print(f"Sequence before interruption: {sequence} with length {length_of_seq}")
sequence = gen.makeSequenceNegative(sequence, width_of_window, negative_mistakes,rep)
length_of_seq = len(sequence)
print(f"Sequence after interruption: {sequence} with NEW length {length_of_seq}")
print()
matrice_as_list = gen.createMatriceAsList(sequence, combinations, width_of_window)
statistics = gen.createStatistics(matrice_as_list)
matriceDNA = gen.convertMatrice(matrice_as_list)
matriceDNA = gen.makeMatricePositive(matriceDNA, combinations, positive_mistakes)
statistics = gen.updateStatsAfterPositive(matriceDNA, statistics)
print(f'Current stats (before positive): {statistics}')
print()
print(f'DNA_MATRICE (after all errors): {matriceDNA}')
print()
print('####################################################################################')
print('############### END OF GENERATOR ###################################################')
print('####################################################################################')
end_gen = time.time()

start_fs = time.time()
probability_of_crossover = 1
probability_of_mutation = 0.4
population_size = 300
number_of_generations = 200
contestants_in_tournament = 6

graph = gs.createGraph(matriceDNA,width_of_window)
initial_population = createPopulationAsGraph(graph,statistics,matriceDNA,population_size)
print()
initial_parents = improvedTournament(initial_population, contestants_in_tournament)
initial_one = initial_parents[0]
initial_two = initial_parents[1]

# print(f'This is my example parent 1 in generation INITIAL: {initial_one}')
# print(f'This is my example parent 2 in generation INITIAL: {initial_two}')
# print()
# print(f'This is example value of parent 1 in generation INITIAL: {len(verifyData(initial_one))}')
# print(f'This is example value for parent 2 in generation INITIAL: {len(verifyData(initial_two))}')
# print()
# print(f'This is example seq 1 in generation INITIAL: {verifyData(initial_one)}')
# print(f'This is example seq 2 in generation INITIAL: {verifyData(initial_two)}')

populationX = initial_population
best_in_generation = []
for i in range(number_of_generations):
    temp_pop = []
    print(f'GENERATION {i}')
    for j in range (population_size//2):
        # print(f'FAMILY {j}')
        current_parents = improvedTournament(populationX, contestants_in_tournament)
        parent_1 = current_parents[0]
        parent_2 = current_parents[1]
        should_i_crossover = random.random()
        if should_i_crossover < probability_of_crossover:
            children = certainCrossover(parent_1,parent_2,statistics)
            child_1 = children[0]
            child_2 = children[1]
        else:
            child_1 = parent_1
            child_2 = parent_2
        
        should_i_muatate = random.random()
        if should_i_muatate < probability_of_mutation:
            mutants = certainMutation(child_1, child_2)
            mut_child_1 = mutants[0]
            mut_child_2 = mutants[1]
        else:
            mut_child_1 = child_1
            mut_child_2 = child_2
        
        temp_pop.append(mut_child_1)
        temp_pop.append(mut_child_2)
    
    generation_stat = populationStats(temp_pop)
    strongest_in_gen = findBestInPop(generation_stat)
    best_in_generation.append(strongest_in_gen)
    fixed_pop = improvedElitism(temp_pop,generation_stat,strongest_in_gen)
    populationX = fixed_pop
    print()
    print(f'This is the best solution in {i} generation: {strongest_in_gen}')
    print()
    print(f'This is the length of this sol in {i} generation: {len(verifyData(strongest_in_gen))}')
    print(f'This is starter length: {length_of_seq}')
    print(f'Diffrence is {len(verifyData(strongest_in_gen)) - length_of_seq}')
    print()
    
best_of_best_stat = populationStats(best_in_generation)
absolutely_the_best_sol = findBestInPop(best_of_best_stat)
length_of_the_best = len(verifyData(absolutely_the_best_sol))
best_seq = verifyData(absolutely_the_best_sol)
best_gen = findBestGeneration(best_in_generation,absolutely_the_best_sol)

meta_end_and_function = time.time()
print()
print(f'This is the best solution: {absolutely_the_best_sol}')
print()
print(f'Solution found in genertation: {best_gen}')
print(f'This is the length of this sol: {length_of_the_best}')
print(f'This is starter length: {length_of_seq}')
print(f'Diffrence is {length_of_the_best - length_of_seq}')
print()
print(f'New seq before comp: {best_seq}')
print()
print(f'New seq after comp (Final Solution): {createComplementary(best_seq)}')
print()
print(f'This is ORIGINAL seq: {sequence}')
print()
# initial_population = best_in_generation
    # print(f'This is time of generator execution {(end_gen - start_gen_and_fun):.2f} seconds')
    # print(f'This is time of first solution execution {(end_fs - start_fs):.2f} seconds')
    # print(f'This is time of metaheurestic execution {(meta_end_and_function - start_meta):.2f} seconds')
    # print(f'This is time of whole program execution {(meta_end_and_function - start_gen_and_fun):.2f} seconds')
    # print()
# populationX = best_in_generation
# population_size = len(best_in_generation)




    

