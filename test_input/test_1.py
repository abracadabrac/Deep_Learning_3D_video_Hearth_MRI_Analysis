#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 20:49:26 2017

@author: charles
"""

import tensorflow as tf
import numpy as np
import InputComputing as ipc

layer_input = tf.placeholder(tf.float32, [None, ipc.nb_fix_coupes, 30, 512, 512])