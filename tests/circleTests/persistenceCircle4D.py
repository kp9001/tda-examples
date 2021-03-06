import random
import numpy as np
import math
import itertools
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime
from sklearn.cluster import KMeans
import re
import shutil
import os
import copy

start_time = datetime.now()

def randomCoordinates(num, dim, lower, upper, decimals):
    
    coordinates = []
    
    for i in range(num):
        coordinates.append([])
        
    for i in range(num):
        for j in range(dim):
            coordinates[i].append(random.randint(lower*(10**decimals), upper*(10**decimals))/(10**decimals))
            
    return coordinates

def removeRectangle(coordinates, size, lower1, upper1, lower2, upper2):

    count = 0
    j = 0 
    
    while count < size:
        if lower1 < coordinates[j][0] < upper1 and lower2 < coordinates[j][1] < upper2:
            coordinates.remove(coordinates[j])
            count += 1
        else:
            j += 1
            count += 1
                   
    return coordinates

def mergeSort(alist):
    
    if len(alist)>1:
        mid = len(alist)//2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]

        mergeSort(lefthalf)
        mergeSort(righthalf)

        i=0
        j=0
        k=0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i] <= righthalf[j]:
                alist[k]=lefthalf[i]
                i=i+1
            else:
                alist[k]=righthalf[j]
                j=j+1
            k=k+1

        while i < len(lefthalf):
            alist[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j < len(righthalf):
            alist[k]=righthalf[j]
            j=j+1
            k=k+1

def dist(x, y, dim):
    
    L = []
    
    for i in range(dim):
        L.append((y[i]-x[i])**2)
    
    d = math.sqrt(sum(L))
    
    return d

def mergeSortDist(alist, reference, dim):
    
    if len(alist)>1:
        mid = len(alist)//2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]

        mergeSortDist(lefthalf, reference, dim)
        mergeSortDist(righthalf, reference, dim)

        i=0
        j=0
        k=0
        
        while i < len(lefthalf) and j < len(righthalf):
            if dist(lefthalf[i], reference, dim) <= dist(righthalf[j], reference, dim):
                alist[k]=lefthalf[i]
                i=i+1
            else:
                alist[k]=righthalf[j]
                j=j+1
            k=k+1

        while i < len(lefthalf):
            alist[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j < len(righthalf):
            alist[k]=righthalf[j]
            j=j+1
            k=k+1

def VietorisRips(data, epsilon):
    
    C = []
    dim = len(data[0])
    
    for i in range(dim+1):
        C.append([])
        
    for i in range(len(data)):
        C[0].append([data[i]])
    
    while data != []:
        mergeSortDist(data, data[0], dim)
        L = len(data)
        j = 1
        while j < L:
            if dist(data[0], data[j], dim) >= epsilon:
                break
            else:
                C[1].append([data[0],data[j]])
                k = j+1
                while k < L:
                    if dist(data[0], data[k], dim) >= epsilon:
                        break
                    elif dist(data[j], data[k], dim) >= epsilon:
                        k += 1
                    else:
                        C[2].append([data[0],data[j],data[k]])
                        l = k+1
                        while l < L:
                            if dist(data[0], data[l], dim) >= epsilon:
                                break
                            elif dist(data[j], data[l], dim) >= epsilon:
                                break
                            elif dist(data[k], data[l], dim) >= epsilon:
                                l += 1
                            else:
                                C[3].append([data[0],data[j],data[k],data[l]])
                                l += 1
                        k += 1
                j += 1   
        data.remove(data[0])
    return C

def homology(complex):
    
    cLength = len(complex)
    lengths = []
    
    for i in range(cLength):
        lengths.append(len(complex[i]))
    
    if cLength == 0:
        return "Empty"
    
    elif cLength == 1:
        return len(complex[0])
    
    else:
        
        #sort complex elements

        for i in range(cLength):
            for j in range(lengths[i]):
                mergeSort(complex[i][j])
        
        #define sublist function
                
        def sublist(lst1, lst2):
            ls = [element for element in lst1 if element in lst2]
            return ls == lst1
        
        #create boundary operators

        boundary = []
        
        for i in range(1,cLength):
            b = np.zeros((lengths[i-1],lengths[i]))
            for j in range(lengths[i-1]):
                for k in range(lengths[i]):
                    if sublist(complex[i-1][j],complex[i][k]) == True:
                        l = 0
                        for v in complex[i-1][j]:
                            w = 0
                            while True:
                                if v == complex[i][k][w]:
                                    l += w
                                    break
                                else:
                                    w += 1
                        b[j][k] = (-1)**l
            boundary.append(b)
        
        #define rank formula
        
        bLength = len(boundary)
        ranks = []
  
        for i in range(bLength):
            if boundary[i].size > 0:
                ranks.append(np.linalg.matrix_rank(boundary[i]))
            else:
                ranks.append(0)

        BettiNumbers = [lengths[0]-ranks[0]]
        
        for i in range(bLength-1):
            BettiNumbers.append(lengths[i+1]-ranks[i]-ranks[i+1])
            
        for i in range(bLength):
            print(lengths[i])
            
        #BettiNumbers.append(lengths[-1]-ranks[-1])
        
    return BettiNumbers

coordinates = randomCoordinates(5000, 2, -1000, 1000, 2)
L1 = len(coordinates)

lower = 500
upper = 600

count = 0
j = 0

while count < L1:
    if upper**2 < (coordinates[j][0])**2 + (coordinates[j][1])**2 or (coordinates[j][0])**2 + (coordinates[j][1])**2 < lower**2:
        coordinates.remove(coordinates[j])
        count += 1
    else:
        j += 1
        count += 1

for i in range(len(coordinates)):
    X = coordinates[i][0]
    Y = coordinates[i][1]
    Z = round(np.arctan(Y/X),4)
    coordinates[i].append(1000*math.cos((3*Z)/2))
    coordinates[i].append(1000*math.sin((3*Z)/2))    
    coordinates.append([coordinates[i][0], coordinates[i][1], -1000*math.cos((3*Z)/2), -1000*math.sin((3*Z)/2)])
    
data = np.array(coordinates)

print("Number of points: " + str(len(data)))

end_time6 = datetime.now()
print('Duration: {}'.format(end_time6 - start_time))

#fig = plt.figure()
#ax = Axes3D(fig)

#plt.scatter(data[:,0], data[:,1], s = 10, alpha = 0.3)
#plt.show()

N = 50
print("N = " + str(N))
kmeans = KMeans(n_clusters = N)
kmeans.fit(data)
y_kmeans = kmeans.predict(data)

#plotting all data (takes a long time for large data)

centers = kmeans.cluster_centers_
centersList = []

for i in range(N):
    centersList.append([round(centers[i][0],2),round(centers[i][1],2),round(centers[i][2],2),round(centers[i][3],2)])
    
end_time5 = datetime.now()
print('Duration: {}'.format(end_time5 - start_time))

#plt.scatter(centers[:,0], centers[:,1], c = 'purple', s = 200, alpha = 0.7)
#plt.show()

ax = plt.axes(projection='3d')

for i in range(len(centersList)):
    x = centersList[i][0]
    y = centersList[i][1]
    z = centersList[i][2]
    ax.scatter(x,y,z)
plt.show()

L = [copy.deepcopy(centersList)]

epsilon = 100
i = 0

H1 = []
H2 = []

while epsilon < 950:

    L.append(copy.deepcopy(L[i]))
    VR = VietorisRips(L[i], epsilon)
    H = homology(VR)
    print("epsilon = " + str(epsilon) + ",  " + str(H))
    
    H1.append(H[1])
    H2.append(H[2])
    epsilon += 50
    i += 1
    
    end_time1 = datetime.now()
    print('Duration: {}'.format(end_time1 - start_time))  

for i in range(len(H1)):
    plt.scatter(100+50*i, H1[i], c = 'red')

plt.show()    

for i in range(len(H2)):
    plt.scatter(100+50*i, H2[i], c = 'black')
    
plt.show()

end_time2 = datetime.now()
print('Duration: {}'.format(end_time2 - start_time))



