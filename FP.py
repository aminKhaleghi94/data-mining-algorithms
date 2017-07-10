# -*- coding: utf-8 -*-
"""
Created on Sat Jun  10 11:44:01 2017

@author: rafael sandroni
"""

from time import time
from fpgrowth import _fpgrowth,get_fptree
from preprocessing import loadData1,loadData2
from fprules import mineAssocRules
import numpy
from operator import itemgetter
import matplotlib.pyplot as plt

def test_fpgrowth(T=None, support=2, pruning=False):
    if T is None:
        return T
        
    fptree = get_fptree(T, lambda e: e, support)
    fis = set()
    report = {}
    n = _fpgrowth(fptree, fis, report, support, pruning)
    
    return (n, report)

def writeFile(result):
    f = open('/home/rafael/Documents/DataScience/FPGrowth/csvfile.csv','w')
    for line in result:
        f.write(line+'\n')
    f.close()

#start testing fpgrowth

params = []
params.append([0.3,0.6])
params.append([0.4,0.6])
params.append([0.5,0.6])
params.append([0.6,0.6])


test_round = 1
for i in range(test_round):
    #transactions = loadData1()
    transactions = loadData2()
    
    numt = len(transactions)
    print("+------------------------------------------+")
    print('number of transactions {0}\n'.format(numt))
    
    #supp_freq = numt*0.30
    supp_freq = numt*0.010
    
    start = time()
    (n, report) = test_fpgrowth(transactions, supp_freq, pruning=True)
    end = time()
    
    print('FP-Growth time processing: {0}s {1}'.format(end - start,(end - start)/60))
    print('Computed {0} frequent item sets.'.format(n))
    print('Min Support {0}'.format(supp_freq))
    
    """
    supp_rules = supp_freq
    confidence = 0.5
    
    x = report.keys()
    
    rules = mineAssocRules(report, numt, supp_rules, confidence)
    print('Rules {0}, with supp {1}, confidence {2}'.format(len(rules), supp_rules, confidence))
    result = []
    result.append(len(rules))
    result.append(supp_rules)
    result.append(confidence)
    
    r = sorted(rules, key=lambda x: x[4])
    
    
    supp = []
    conf = []
    lift = []
    coss = []
    
    for i in range(len(r)):
        supp.append(r[i][2])#supp
        conf.append(r[i][3])
        lift.append(r[i][4])
        coss.append(r[i][5])

    fig, ax = plt.subplots()
    ax.scatter(supp, conf)
    ax.set_title('Support and Confidence')
    plt.show()
    
    fig, ax = plt.subplots()
    ax.scatter(supp, lift)
    ax.set_title('Support and Lift')
    plt.show()
    
    fig, ax = plt.subplots()
    ax.scatter(conf, lift)
    ax.set_title('Confidence and Lift')
    plt.show()
    
    
    fig, ax = plt.subplots()
    ax.scatter(supp, coss)
    ax.set_title('Support and Coss')
    plt.show()
    
    fig, ax = plt.subplots()
    ax.scatter(lift, coss)
    ax.set_title('Lift and Coss')
    plt.show()
    
    fig, ax = plt.subplots()
    ax.scatter(conf, coss)
    ax.set_title('Conf and Coss')
    plt.show()
    """