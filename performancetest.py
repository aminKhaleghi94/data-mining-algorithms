# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 11:44:01 2017

@author: rafael
"""

from time import time
import random
import string
from pymining.itemmining import _fpgrowth, get_fptree
from pymining.compat import range
from preprocessing import *
from fprules import *

def test_fpgrowth(should_print=False, T=None, support=2, pruning=False):
    if T is None:
        return T
        
    fptree = get_fptree(T, lambda e: e, support)
    fis = set()
    report = {}
    n = _fpgrowth(fptree, fis, report, support, pruning)
    if should_print:
        print(n)
        print(report)
    return (n, report)


#start testing fpgrowth
    
support = 10
"""
transactions = get_random_transactions(
        transaction_number=transaction_number,
        universe_size=universe_size,
        key_alphabet=None)
"""
        
transactions = loadData2()

print('number of transactions {0}\n'.format(len(transactions)))

start = time()
#for i in range(perf_round):
(n, report) = test_fpgrowth(False, transactions, support, pruning=True)
    
    
end = time()
print('FP-Growth time processing: {0}'.format(end - start))
print('Computed {0} frequent item sets.'.format(n))
print('Min Support {0}'.format(support))


rules = mineAssocRules(report, 2, 0.5)
