import random
import re
import math

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

#produces a random tour of the required size.
def random_tour():
    simple_tour = list(range(1, size+1))
    random.shuffle(simple_tour)
    return simple_tour


def neighbour(current_tour):
    tour_copy = current_tour.copy()
    #take two random indexes
    rand_val1 = random.randint(0, size - 1)
    rand_val2 = random.randint(0, size - 1)
    min_val = min(rand_val1, rand_val2)
    max_val = max(rand_val1, rand_val2)
    #reverse the elements in the current tour between these two indexes and set the result equal to the adjacent tour.
    adjacent_tour = tour_copy[0:min_val] + list(reversed(tour_copy[min_val:max_val + 1])) + tour_copy[max_val + 1:size + 1]
    return adjacent_tour


def distance(tour):
    #calculates the length of the tour passed in.
    distance_current = 0
    for d in range(len(tour)-1):
        source = min(int(tour[d]), int(tour[d+1])) - 1
        dest = max(int(tour[d]), int(tour[d+1])) - (source + 2)
        distance_current += content[source][dest]
    source = min(int(tour[0]), int(tour[size - 1])) - 1
    dest = max(int(tour[0]), int(tour[size - 1])) - (source + 2)
    distance_current += content[source][dest]
    return distance_current


if __name__ == "__main__":
    # open file and separate values by commas
    with open('AISearchfile535.txt.txt') as file:
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
    tourDistArray = []
    shortestTour = []
    #sets initial temperature to 100
    initial_temperature = 10 * size
    #sets the current temperature to the intiial temperature
    temperature = initial_temperature
    #initially set the current tour to a random tour
    current_tour = random_tour()
    #find the current length
    current_distance = distance(current_tour)
    k = 0
    if size > 300:
        limit = size + 120
    elif size > 100:
        limit = size + 10
    else:
        limit = size

    #if the temperature is less than the limit plus 1, were limit depends on size
    while temperature > limit + 1 | k > 1000:
        #find the length of the current tour
        current_distance = distance(current_tour)
        tourDistArray.append(current_distance)
        if (current_distance == min(tourDistArray)):
            shortestTour = current_tour
        #find an adjacent tour
        adjacent_tour = neighbour(current_tour)
        #find the length of the adjacent tour
        adjacent_distance = distance(adjacent_tour)
        #if the length of the adjacent tour is less than the length of the current tour then swap the two tours
        if adjacent_distance < current_distance:
            current_tour = list(adjacent_tour)
        else:
            #otherwise swap the two tours with the probability stated.
            swappingprob = math.exp((current_distance - adjacent_distance) / max(1, math.log(temperature)))
            prob = random.uniform(0, 1)
            if prob <= swappingprob:
                current_tour = list(adjacent_tour)
                #cool the temperature witht he following cooling schedule
                temperature = initial_temperature/(1+ math.log(1+k))
                k += 1
    else:
        #otherwise finish the process.
        finish(shortestTour, current_distance)
