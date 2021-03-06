import random
import math

def randomCoordinates(num, dim, lower, upper, decimals):
    
    coordinates = []
    
    for i in range(num):
        coordinates.append([])
        
    for i in range(num):
        for j in range(dim):
            coordinates[i].append(random.randint(lower*(10**decimals), upper*(10**decimals))/(10**decimals))
            
    return coordinates

def removeRectangle(coordinates, size, lower, upper):

    count = 0
    j = 0 
    
    while count < size:
        if lower < coordinates[j][0] < upper and lower < coordinates[j][1] < upper:
            coordinates.remove(coordinates[j])
            count += 1
        else:
            j += 1
            count += 1
                   
    return coordinates


