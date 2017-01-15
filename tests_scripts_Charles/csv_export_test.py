#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 17:20:17 2017

@author: charles
"""

import numpy
a = numpy.arange(10)
numpy.savetxt("input.csv", a, delimiter=",")