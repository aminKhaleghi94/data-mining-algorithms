# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 21:22:59 2017

@author: rafael
"""

import pandas as pd
import plotly.plotly as py
import plotly as plotly
import plotly.graph_objs as go
import numpy as np
import csv
from preprocessing import loadDataResult

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

#df = pd.read_csv('/home/rafael/Documents/DataScience/FPGrowth/csvfile.csv')

dataset = loadDataResult()

supp = []
conf = []
lift = []

for i in dataset:
    supp.append(i[0])#supp
    conf.append(i[1])
    lift.append(i[2])


"""
matplotlib.rcParams['axes.unicode_minus'] = False
fig, ax = plt.subplots()
ax.plot(supp, conf, lift)
ax.set_title('Using hyphen instead of Unicode minus')
plt.show()
"""

fig, ax = plt.subplots()
ax.scatter(lift, conf)
ax.set_title('Support and Lift for 13448 rules')
plt.show()