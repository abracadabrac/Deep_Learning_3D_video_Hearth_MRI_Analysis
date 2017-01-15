#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 17:20:17 2017

@author: charles
"""
import numpy as np
import pandas as pd 
data = pd.read_csv('./foo.csv',sep=';')
data = data.as_matrix(columns=None)
data = data.reshape(9)
print(data)
print(data.shape)