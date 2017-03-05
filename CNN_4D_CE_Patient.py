import tensorflow as tf
import numpy as np


shape_input = [1,12,30,512,512]
x_input = np.ones(shape_input)
zz_ = shape_input[1]
tt_ = shape_input[2]
xx_ = shape_input[3]
yy_ = shape_input[4]

filter_size_1_xy = 14
filter_size_1_t = 3
nb_filters1 = 16

x_input_layer = []
x_input_layer_reshape = []
layer1 = []

for z in np.arange(zz_):   
    placeholer_ = tf.placeholder(tf.float32, shape=[None, tt_, xx_, yy_])
    x_input_layer.append(placeholer_)
    placeholer_ = tf.reshape(placeholer_, [-1, tt_, xx_, yy_, 1])
    x_input_layer_reshape.append(placeholer_)
   
for z in np.arange(zz_): 
    shape = [filter_size_1_t, filter_size_1_xy, filter_size_1_xy, 1, nb_filters1]
    weights = tf.Variable(tf.truncated_normal(shape, stddev=0.05))
    layer1.append(tf.nn.conv3d(input=x_input_layer_reshape[z],
                             filter=weights,
                             strides=[1, 1, 1, 1, 1],
                             padding='VALID'))


    
feed_dict_test = {}
for z in np.arange(zz_):
    feed_dict_test[x_input_layer[z]] =  x_input[:,z,:,:,:]
 
#print(feed_dict_test)


with tf.Session() as sess:  
    print(sess.run(layer1[1], feed_dict=feed_dict_test ))
    #sess.run(layer1[1], feed_dict=feed_dict_test)

    
    