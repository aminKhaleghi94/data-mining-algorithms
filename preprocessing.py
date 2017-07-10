# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 11:39:25 2017

@author: rafael
"""
import csv
from fpgrowth import *


#transactions = perftesting.get_default_transactions()
#transactions = (('a', 'b', 'c'), ('b'), ('a'), ('a', 'c', 'd'), ('b', 'c'), ('b', 'c'))


#transactions = loadData2()


   
def loadData1():
    
    f = open("/home/rafael/Documents/DataScience/votes_dataset.csv")
    #f = open("/home/rafael/Documents/DataScience/t25i10d10.txt")
    filecontent = csv.reader(f)
    dataset = []
    
    j = 0
    for i in filecontent:  
        if j > 450:
            break
        
        element = []
        
        element.append(i[0])
        element.append('handicapped-infants='+ i[1]) 
        element.append('water-project-cost-sharing='+ i[2]) 
        element.append('adoption-of-the-budget-resolution='+ i[3]) 
        element.append('physician-fee-freeze='+ i[4]) 
        element.append('el-salvador-aid='+ i[5]) 
        element.append('religious-groups-in-schools='+ i[6]) 
        element.append('anti-satellite-test-ban='+ i[7]) 
        element.append('aid-to-nicaraguan-contras='+ i[8]) 
        element.append('mx-missile='+ i[9]) 
        element.append('immigration='+ i[10]) 
        element.append('synfuels-corporation-cutback='+ i[11]) 
        element.append('education-spending='+ i[12]) 
        element.append('superfund-right-to-sue='+ i[13]) 
        element.append('crime='+ i[14]) 
        element.append('duty-free-exports='+ i[15]) 
        element.append('export-administration-act-south-africa=' + i[16])
        
        dataset.append(element)
        #dataset.append(i)
        j+=1
        
    return dataset

def loadData2(limitT=0):
    
    #f = open("/home/rafael/Documents/DataScience/t25i10d10.txt")
    f = open("/home/rafael/Documents/DataScience/FPGrowth/datasets/T10I4D100K.txt")
    filecontent = csv.reader(f, delimiter=' ')
    dataset = []
    j = 0
    for i in filecontent:  
        if limitT > 0:
            if j > limitT:
                break
        
        element = []
        
        for item in i:
            if item is None or item == "":
                continue
            element.append(item)

        #print(element)
        dataset.append(element)
        #dataset.append(i)
        j += 1
    return dataset
    
def loadDataResult():
    f = open('/home/rafael/Documents/DataScience/FPGrowth/csvfile.csv')
    filecontent = csv.reader(f, delimiter=';')
    j = []
    for i in filecontent:
        j.append([i[2],i[3],i[4]])
    
    
    return j

    
#print len(loadData1())
#loadDataResult()