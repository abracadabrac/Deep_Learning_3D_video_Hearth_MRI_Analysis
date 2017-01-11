#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 10:45:11 2017

@author: charles
"""

import dicom
import os
import numpy as np
import matplotlib.pyplot as plt
import time

PathDicom = '/Users/charles/Workspace/Sample_TrainSet_IRM_images/1/study/2ch_21/IM-4572-0001.dcm'

img = dicom.read_file(PathDicom).pixel_array  
plt.figure(1)
plt.pcolormesh(img)


'''
import InputComputing as

Path = "/Volumes/LaCie/PFE_INSERM_IRM_Data/train"  
Path = "/Users/charles/Workspace/Sample_TrainSet_IRM_images"

input_dcm = inputComputing.compute_inpute_list(Path)
'''

plt.figure(2)
plt.pcolormesh(input_dcm[0][0][0])
plt.show()

# les images divraient identiques, on devrait observer une image uniforme :
plt.figure(3)
plt.pcolormesh(input_dcm[0][0][0]-img)
plt.show()