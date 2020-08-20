#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 21:18:25 2020

@author: oluwayemisirunsewe
"""
import matplotlib.pyplot as plt


#Function to load file and extract data from CSV file
def loadFile(file_name):
    file = open(file_name, "r")
    potential = []
    current = []
    #Reading lines from CSV file and transfeing data to a list
    for line in file:
        lin = line.strip()
        sline = lin.split(",")
        #Handling dataType error as i only want to work with dataType of float
        try:
            if type(float(sline[0])) is float:
                potential.append(float(sline[0]))
                current.append(float(sline[1]))
        except:
            continue
        #Returns a tuple containg the potential and current
    return (potential, current)


def normalize(potential, current, nml = 1000000):
    newCurrent = []
    for num in range(len(potential)):
       newCurrent.append(current[num] * nml)
    return newCurrent


#Identifying the last circle
    #Since its the last circle, we reverse the list and stat from the end of the circle till i identify the begining of the circle
def cropNumbers(potential, current):
    #Creating new list to put data into
    choosenCurrent = []
    choosenPotential = []
    done = 1
    #Using a for loop to walk through the numbers utill i identify the start of the circle
    for num in range(len(potential) - 1):
        if(potential[num] < potential[num +1] and (done == 1)):
            choosenPotential.append(potential[num])
            choosenCurrent.append(current[num])
            #The first time the condition turns false, it will add the data and change done
        elif(done == 1):
            choosenPotential.append(potential[num])
            choosenCurrent.append(current[num])
            done = 0
            #checking for the other half of the cycle
        elif(potential[num] > potential[num +1]):
            choosenPotential.append(potential[num])
            choosenCurrent.append(current[num])
        else:
            choosenPotential.append(potential[num])
            choosenCurrent.append(current[num])
            break    
    return (choosenPotential,choosenCurrent) 


def plotGraph(x, y):
    plt.style.use('default')
    plt.plot(x,y)
    plt.xlabel("potential(V)")
    plt.ylabel("current(mA)")
    plt.title("Cyclic Voltammetry")
    plt.show()
    
def EapEcp(curr,poten):
    Eap = poten[curr.index(max(curr))]
    Ecp = poten[curr.index(min(curr))]
    return (Eap, Ecp)


    
    
#MAIN
file_name = input("Please enter the name of the file You would like to analyse: ")
data = loadFile(file_name)
#Getting the data from tuple after extracting it from the file
left = data[0]
right = data[1]
#Reversing the list so as to make the process of readig efficient
left.reverse()
right.reverse()
#Calling function to Get the last circle
up_Data = cropNumbers(left, right)
potentialV = up_Data[0]
currentA = up_Data[1]
new_right = normalize(left, right)
plotGraph(left, new_right)
#normalizing the current so as to plot a graph
new_currentA = normalize(potentialV, currentA)
plotGraph(potentialV, new_currentA)
max_min = EapEcp(new_currentA, potentialV)
print("Ea,p =", str(max_min[0]) + " V\nEc,p =", str(max_min[1]) + " V")