import tensorflow as tf
from scipy.stats import norm
import numpy as np

def new_weights(shape):
    return tf.Variable(tf.truncated_normal(shape, stddev=0.05))

def new_biases(length):
    return tf.Variable(tf.constant(0.05, shape=[length]))

def new_conv_layer(input,
                   num_input_channels,
                   filter_size, 
                   num_filters, 
                   use_pooling=True): 
    shape = [filter_size, filter_size, num_input_channels, num_filters]
    kernel = new_weights(shape=shape)
    biases = new_biases(length=num_filters)
    layer = tf.nn.conv2d(input=input,
                         filter=kernel,
                         strides=[1, 1, 1, 1],
                         padding='SAME')
    layer += biases
    if use_pooling:
        layer = tf.nn.max_pool(value=layer,
                               ksize=[1, 2, 2, 1],
                               strides=[1, 2, 2, 1],
                               padding='SAME')
    layer = tf.nn.relu(layer)
    return layer, kernel
    
def flatten_layer(layer):
    layer_shape = layer.get_shape()
    print('layer shape :')
    print(layer_shape)
    num_features = layer_shape[1:4].num_elements()
    print('num_features : %d' %num_features)
    layer_flat = tf.reshape(layer, [-1, num_features])
    return layer_flat, num_features

def new_fc_layer(input, 
                 num_inputs,
                 num_outputs,    
                 use_relu=True): 
    weights = new_weights(shape=[num_inputs, num_outputs])
    biases = new_biases(length=num_outputs)
    layer = tf.matmul(input, weights) + biases
    if use_relu:
        layer = tf.nn.relu(layer)
    return layer

def crps(true, pred):

    return np.sum(np.square(true - pred)) / true.size


def real_to_cdf(y, sigma=1e-10):

    cdf = np.zeros((y.shape[0], 600))
    for i in range(y.shape[0]):
        cdf[i] = norm.cdf(np.linspace(0, 599, 600), y[i], sigma)
    return cdf

