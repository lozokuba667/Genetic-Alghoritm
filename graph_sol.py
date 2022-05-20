import random

def reverseContent(txt):
    return txt[::-1]

def createGraph(matrice, width):
    graph = {}
    scissors = -1
    for singleEntry in matrice:
        for anotherAntry in matrice:
            if anotherAntry == singleEntry:
                continue
            for i in range(len(anotherAntry)):
                contemp = anotherAntry[:(-scissors)]
                if singleEntry[scissors:] == contemp:
                    wage = width - (-scissors)
                    if wage not in graph:
                        graph[wage] = []
                    graph[wage].append([singleEntry, anotherAntry])
                scissors -= 1
            scissors = -1
        scissors = -1

    return graph


def getNumberOfPositive(percentage,matrice):
    amount = (percentage / 100) * len(matrice)
    amount = int(amount)
    return amount
    
def selectRandomPositive(empty,stats,matrice,percentage):
    amount = getNumberOfPositive(percentage,matrice)
    windows = list(stats.keys())
    for i in range(amount):
        current = random.choice(windows)
        while current in empty or stats[current] !=1:
            current = random.choice(windows)
        empty.append(current)
    
    return empty

def selectFirstMember(matrice, forbid, stats):
    first = random.choice(list(matrice))
    while first in forbid:
        first = random.choice(list(matrice))
    
    return first
    
def searchNeighbourhood(vert,all_routes):
    route_choice = []
    for single_con in all_routes:
        if single_con[0] == vert:
            route_choice.append(single_con)
    return route_choice

def getAllRoutes(graph):
    lst = list(graph.values())
    all_routes = [item for sublist in lst for item in sublist]
    return all_routes
      
def pickNeighbour(moves, forbid, stats,sol,graph):
    not_possible_moves = 0
    # unable_to_find = 0
    # best_option = pickPossibleBestNeighbour(moves, forbid, stats,sol,graph)
    # if best_option == 1:
    #     unable_to_find = 1
    # else:
    #     if isSingleGood(best_option,forbid,stats,sol):
    #         return best_option
    #     elif isDoubleGood(best_option,stats,sol):
    #         return best_option
    #     elif isMultiGood(best_option,stats,sol):
    #         return best_option
    #     else:
    #         not_possible_moves+=1
    
    
    while not_possible_moves < len(moves):
        rand_move = random.choice(moves)
        rand_neigh = rand_move[1]
        if isSingleGood(rand_neigh,forbid,stats,sol):
            return rand_neigh
        elif isDoubleGood(rand_neigh,stats,sol):
            return rand_neigh
        elif isMultiGood(rand_neigh,stats,sol):
            return rand_neigh
        else:
            not_possible_moves+=1
        
    return -1
 
def validateNeighbourhood(moves,forbid,stats,sol):
    somsiedzi = []
    cannot_move = 0
    for move in moves:
        somsiedzi.append(move[1])
    
    for somsiad in somsiedzi:
        if isSingleGood(somsiad,forbid,stats,sol):
            return True
        elif isDoubleGood(somsiad,stats,sol):
            return True
        elif isMultiGood(somsiad,stats,sol):
            return True
        else:
            cannot_move+=1
    
    return False
        
# def pickPossibleBestNeighbour(moves,forbid,stats,sol,graph):
#     pick_val = {}
#     value = 0
#     for elem in moves:
#         val = getMaximumConvergance(elem[0],elem[1])
#         if val not in pick_val:
#             pick_val[val] = list()
#         pick_val[val].append(elem[1])
#         value = val
        
#     my_conv = list(pick_val.keys())
#     if len(my_conv) >= 1:
#         best_max = max(my_conv)
#     else:
#         return 1
    
#     area_of_choice = pick_val[best_max]
    
#     return area_of_choice[0]



def prepareGraphSolution(sol,stats):
    temp = sol[:]
    if -1 in temp:
        temp.remove(-1)
    
    for single in temp:
        if stats[single] == 2 and temp.count(single) == 1:
            temp.append(single)
        elif stats[single] == 'wiele' and temp.count(single) < 3:
                randflag = random.randint(1,3)
                for i in range(randflag):
                    temp.append(single)
                    

        
    # sol = sol + rest_of_array
    return temp
                
def isSingleGood (vert, forbid, stats, sol):
    if stats[vert] == 1:
        if vert not in forbid:
            if vert not in sol:
                return True

    
    return False
 
def isDoubleGood (vert, stats,sol):
    if stats[vert] == 2:
        if sol.count(vert) < 2:
            return True 
        
    return False

def isMultiGood(vert,stats,sol):
    if stats[vert] != 1 and stats[vert] != 2:
        if sol.count(vert) < random.randint(3,4):
            return True
    
    return False


def getMaximumConvergance(one, two):
    scissors = -1
    convergance = 0
    for i in range(len(one)):
        contep = two[:(-scissors)]
        if one[scissors:] == contep:
            convergance = -scissors
        scissors -= 1
    return convergance