import random
import decimal
import re
finisharray = []
tourDistArray = []

def finish(tour, distance):
    #finishes the algorithm and writes the data to the file.
    with open('tourAISearchfile535.txt.txt', 'w') as f:
        #writes the name string line.
        f.write(nameString + ',\n')
        #writes the tour size line.
        f.write('TOURSIZE = ' + str(size) + ',\n')
        #writes the tour length line.
        f.write('LENGTH = ' + str(distance) + ',\n')
        #writes each element of the array separated by commas, last element does not have a comma following it.
        for a in range(len(tour)-1):
            f.write(str(tour[a]) + ',')
        f.write(str(tour[len(tour)-1]))
    exit()


def summate(array, x):
    #calculates and returns the sum of all elements in the list.
    cumsum = 0
    for b in range(x):
        cumsum += array[b]
    return cumsum


def initial_generation(initial_population):
    generation0 = []
    # initial generation consists of population random tours.
    for c in range(initial_population):
        parent = list(range(1, size+1))
        random.shuffle(parent)
        generation0.append(parent)
    return generation0


def fitness(array):
    fitnessarray = []
    #for each tour
    for tour in array:
        distance = 0
        #calculates length of each tour
        for d in range(len(tour)-1):
            source = min(int(tour[d]), int(tour[d+1])) - 1
            dest = max(int(tour[d]), int(tour[d+1])) - (source + 2)
            distance += content[source][dest]
        source = min(int(tour[0]), int(tour[size - 1])) - 1
        dest = max(int(tour[0]), int(tour[size - 1])) - (source + 2)
        distance += content[source][dest]
        #append 1/distance^2 tot his fitness array
        fitnessarray.append(1/distance**2)
        tourDistArray.append(distance)
        #if distance is the minimum distance store the associated tour as finish tour.
        if distance <= min(tourDistArray) and tour != []:
            global finishtour
            finishtour = tour
    finisharray.append(min(tourDistArray))
    #if the minimum distance hasn't changed in 3*size generations then end the algorithm
    if size> 300:
        limit = int(0.75*size)
    elif size > 100:
        limit = int(1.5*size)
    elif size > 40:
        limit = 4*size
    else:
        limit = 6*size
    if w > limit | w>400:
        if finisharray[w-(limit)] == finisharray[w]:
            finish(finishtour, min(finisharray))
    return fitnessarray

def selection(array, fitnessarray):
    total_fitness = summate(fitnessarray, len(fitnessarray))
    select_array, chosen_parents = [], []
    #roulette wheel approach of selection
    for fitness_i in fitnessarray:
        selectionvar = (fitness_i * 360) / total_fitness
        select_array.append(selectionvar)
    e = 0
    while e < 2:
        rand_dec = decimal.Decimal(random.randrange(36000)) / 100
        for f in range(len(select_array)):
            if f != 0:
                lower_bound = summate(select_array, f)
            else:
                lower_bound = -1
            upper_bound = summate(select_array, f + 1)
            if lower_bound < rand_dec <= upper_bound:
                #randomly pick 2 parents
                if len(chosen_parents) > 0:
                    #if second parent is the same as the first parent pick the parents again
                    if array[f] != chosen_parents[0]:
                        chosen_parents.append(array[f])
                    else:
                        e = 0
                else:
                    chosen_parents.append(array[f])
        e += 1
    return chosen_parents


def form_child(array):
    #list of all numbers that should be in the tour
    not_found = list(range(1, size+1))
    not_found_copy = not_found.copy()

    #removes numbers that are in the tour so we have a list of all numbers in the tour that should be that aren't
    for number in not_found_copy:
        if number in array:
            not_found.remove(number)


    #adds these numbers to the tour, replacing numbers that are in the tour twice.
    for z in range(len(array)):
        if array.count(array[z]) > 1:
            array[z] = not_found[0]
            not_found.remove(not_found[0])

    return array


def crossover(array):
    index = random.randint(0, size-1)
    #sets child1 and child2 as parts a portion of each parent followed by a portion of the other parent
    child1 = array[0][0: index] + array[1][index:size]
    child2 = array[1][0: index] + array[0][index:size]
    #fixes these children so they represent valid tours
    child1 = form_child(child1)
    child2 = form_child(child2)
    # return the fitter of the two children.
    child_array = [child1, child2]
    child_fitness = fitness(child_array)
    if child_fitness[0] > child_fitness[1]:
        return child1
    else:
        return child2


def mutate(array):
    #mutate each child with prob 0.25, do this by reversing the order of a random portion of elements.
    next_gen = []
    for child in array:
        rand_dec = random.uniform(0, 1)
        #6th running with 0.25
        if (rand_dec <= 0.15):
            rand_val1 = random.randint(0, size - 1)
            rand_val2 = random.randint(0, size - 1)
            min_val = min(rand_val1, rand_val2)
            max_val = max(rand_val1, rand_val2)
            temp = child
            child = temp[0:min_val] + list(reversed(temp[min_val:max_val+1])) + temp[max_val+1:size+1]
        next_gen.append(child)
    return next_gen


def elitism(fitness_array, prev_gen):
    prev_gen_fitness = []
    fittest = []
    #sorts each tour by its fitness
    for n in range(len(prev_gen)):
        prev_gen_fitness.append((fitness_array[n], prev_gen[n]))
    prev_gen_fitness = sorted(prev_gen_fitness, key=lambda fitness: fitness[0])
    #append the fittest half of tours to from the previous generation to an array
    for o in range(population):
        if o >= int(population - int(0.2*population)):
            fittest.append(prev_gen_fitness[o][1])
        else:
            fittest.append(-1)
    return fittest


def crossoverelite(fittest_prev_gen, gen):
    #replace a random half of tours with the top half of fittest tours from the previous generation
    for p in range(population):
        if fittest_prev_gen[p] != -1:
            gen[p] = fittest_prev_gen[p]
    return gen


if __name__ == "__main__":
    # open file and separate values by commas
    with open('AISearchfile535.txt') as file:
        file_content = file.read().replace('\n', '')
        file_content = file_content.split(',')
    temp, content = [], []
    # set the first line to the name string, then remove it as its not needed.
    nameString = file_content[0]
    file_content.remove(file_content[0])
    # set size to the numbers in the new first line, then remove the first line as its not needed.
    size = int(re.sub('[^0-9]', '', file_content[0]))
    file_content.remove(file_content[0])
    # for each line get each element and make it numeric with no spaces.
    for element in file_content:
        if element and element != '' and element != 0:
            element = re.sub(' ', '', element)
            element = re.sub('[^0-9]', '', element)
            temp.append(int(element))
    sizecopy = size
    # set q to 0 and r to size-1
    q, r = 0, (size - 1)
    # set sum size to the number of elements.
    sum_size = (size - 1) * size / 2
    # while q is less than the number of elements
    while q < sum_size:
        # take a list from q to r
        subList = temp[q:r]
        q += (sizecopy - 1)
        r = q + sizecopy - 2
        sizecopy -= 1
        content.append(subList)
    w = 0
    #number of tours in each generation
    population = 100
    new_gen = []
    #makes previous generation an initial generation of 100 random tours
    prev_gen = initial_generation(population)
    s = 0
    #do the following forever (stop condition inside the while)
    while s==0:
        #get fitness of the previous generation
        generation_fitness = fitness(prev_gen)
        #do the next bit 100 times
        for t in range(population):
            #select parents
            genParents = selection(prev_gen, generation_fitness)
            #crossover parents and set the result as the child
            child = crossover(genParents)
            #add the child to the next generation
            new_gen.append(child)
        #mutate each child with prob 15%
        new_gen = mutate(new_gen)
        #put the fittest half of tours from the previous generation in this generation
        fit_prev_gen = elitism(generation_fitness, prev_gen)
        new_gen = crossoverelite(fit_prev_gen, new_gen)
        prev_gen = list(new_gen)
        new_gen = []
        w+=1
