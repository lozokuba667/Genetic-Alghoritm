import random


def createSeq(len, alph):
    seq = ""
    for i in range(len):
        seq += random.choice(alph)

    return seq

def validateSeq(seq, width):
    new_seq = seq
    windows = [new_seq[x : width + x] for x in range((len(new_seq) - width) + 1)]
    occurences = {}
    for singleWindow in windows:
        if singleWindow not in occurences:
            occurences[singleWindow] = 0
        occurences[singleWindow] += 1

    repeated_windows = []

    for window_occurence in occurences.keys():
        if occurences[window_occurence] > 1:
            repeated_windows.append(window_occurence)

    if len(repeated_windows) == 0:
        return False
    else:
        return True

def makeSequenceNegative(seq, width, neg,ihave):
    amount_of_negative = (neg / 100) * ((len(seq) - width) + 1)
    amount_of_negative = round(amount_of_negative)
    amount_of_negative -= ihave
    negative_made = 0
    windows_testes = 0
    temp = 0
    print(f"I should make {amount_of_negative} mistakes in code")
    if amount_of_negative < 1:
        return seq
    windows = [seq[x : width + x] for x in range((len(seq) - width) + 1)]
    addon = seq
    while negative_made < amount_of_negative:
        replacement = random.choice(windows)
        current_seq = addon + replacement
        current_win = [
            current_seq[x : width + x] for x in range((len(current_seq) - width) + 1)
        ]
        occurences = {}
        for singleWindow in current_win:
            if singleWindow not in occurences:
                occurences[singleWindow] = 0
            occurences[singleWindow] += 1

        for eh in occurences.keys():
            if occurences[eh] > 1:
                temp += occurences[eh] - 1

        windows_testes += 1
        negative_made = temp
        if windows_testes > int(len(windows) / 4):
            addon = current_seq
        temp = 0

    print(f"I made {negative_made} mistakes in code")
    return current_seq

def createComplementary(seq):
    complementar = {"A": "T", "C": "G", "T": "A", "G": "C"}
    new_seq = ""
    for char in seq:
        new_seq += complementar[char]

    return new_seq

def createMatriceAsList(seq, comb, width):
    originalWindows = [seq[i : width + i] for i in range((len(seq) - width) + 1)]
    complementWindows = [createComplementary(window) for window in originalWindows]
    basic_matrice = [matching for matching in complementWindows if matching in comb]
    return basic_matrice

def convertMatrice(matrice):
    random.shuffle(matrice)
    normalized_matrice = set(matrice)
    return normalized_matrice

def createStatistics(matrice):
    stat = {}
    for singleEntry in matrice:
        if singleEntry not in stat:
            stat[singleEntry] = 0
        stat[singleEntry] += 1

    for oneStat in stat.keys():
        if stat[oneStat] > 2:
            stat[oneStat] = "wiele"

    return stat

def makeMatricePositive(matrice, comb, positive_count):
    changes = 0
    positive_amount = (positive_count / 100) * len(matrice)
    positive_amount = round(positive_amount)
    while changes != positive_amount:
        impostorEntry = random.choice(comb)
        if impostorEntry not in matrice:
            matrice.add(impostorEntry)
            changes += 1

    impostorMatrice = matrice
    return impostorMatrice

def updateGraph(graph):
    for key in graph.keys():
        for singlelists in graph[key]:
            lst_rev = singlelists[::-1]
            if lst_rev in graph[key]:
                graph[key].remove(lst_rev)

    return graph

def reverseContent(txt):
    return txt[::-1]

def updateStatsAfterPositive(matriceDNA, stats):
    for single in matriceDNA:
        if single not in stats:
            stats[single] = 1

    return stats

def countNegative(seq,width):
    windows = [seq[x : width + x] for x in range((len(seq) - width) + 1)]
    occurences = {}
    repeat = 0
    for singleWindow in windows:
        if singleWindow not in occurences:
            occurences[singleWindow] = 0
        occurences[singleWindow] += 1
    
    for inp in occurences:
        if occurences[inp] > 1:
            repeat += occurences[inp]-1
    return repeat