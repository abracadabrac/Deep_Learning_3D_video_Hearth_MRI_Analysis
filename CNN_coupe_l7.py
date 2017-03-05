'''
Version           Autor                  Descriptioin
1.0               Jean Bizot             Initiation        
1.1               Charles Englebert      minor changes


'''



import tensorflow as tf
import numpy as np
import networker as nw 
import Input__ as ip

print('_____________')
print(' ')

shape_input = (1, 128, 128, 30)
#            batch  z   x    y    t
batch = shape_input[0]
xx_ = shape_input[1]
yy_ = shape_input[2]
tt_ = shape_input[3]

import_data = 1
if import_data:  
    print('data importation') 
    print(' ')     
    x_input_train = np.load("x_input_train.npy").item()  
    y_true_train = np.load("y_true_train.npy").item()  
    x_input_validate = np.load("x_input_validate.npy").item()  
    y_true_validate = np.load("y_true_validate.npy").item()


input_train = ip.InputImages(x_input_train, y_true_train, xx_, yy_, tt_)
input_validate = ip.InputImages(x_input_validate, y_true_validate, xx_, yy_, tt_)

print('Data imported')
print('building network')
print(' ')

   # # # # # # # #
  # # # Input # # # 
   # # # # # # # #

input_layer = tf.placeholder(tf.float16, shape=[None, xx_, yy_, tt_])

   # # # # # # # # #
  # # # layer I # # #
   # # # # # # # # #


print('layer 1')
filter_size_1_1 = 32
nb_filters_1_1 = 64

layer_conv_1_1, kernel_1_1 = \
    nw.new_conv_layer(input=input_layer,
                   num_input_channels=tt_,
                   filter_size=filter_size_1_1,
                   num_filters=nb_filters_1_1,
                   use_pooling=True)


   # # # # # # # # #
  # # # layer 2 # # #
   # # # # # # # # #
 

print('layer 2')
filter_size_2_2 = 32
nb_filters_2_2 = 128

layer_conv_2_2, kernel_2_2 = \
  nw.new_conv_layer(input=layer_conv_1_1,
                 num_input_channels=nb_filters_1_1,
                 filter_size=filter_size_2_2,
                 num_filters=nb_filters_2_2,
                 use_pooling=True)

   # # # # # # # # #
  # # # layer 3 # # #
   # # # # # # # # #

print('layer 3')
filter_size_3_3 = 16
nb_filters_3_3 = 256

layer_conv_3_3, kernel_3_3 = \
  nw.new_conv_layer(input=layer_conv_2_2,
                 num_input_channels=nb_filters_2_2,
                 filter_size=filter_size_3_3,
                 num_filters=nb_filters_3_3,
                 use_pooling=True)

   # # # # # # # # #
  # # # layer 4 # # #
   # # # # # # # # #

filter_size_4_3 = 4
nb_filters_4_3 = 512

layer_conv_4_3, kernel_4_3 = \
  nw.new_conv_layer(input=layer_conv_3_3,
                 num_input_channels=nb_filters_3_3,
                 filter_size=filter_size_4_3,
                 num_filters=nb_filters_4_3,
                 use_pooling=False)

   # # # # # # # # #
  # # # layer 5 # # #
   # # # # # # # # #

print('layer 5')
filter_size_5_3 = 4
nb_filters_5_3 = 512

layer_conv_5_3, kernel_5_3 = \
  nw.new_conv_layer(input=layer_conv_4_3,
                 num_input_channels=nb_filters_4_3,
                 filter_size=filter_size_5_3,
                 num_filters=nb_filters_5_3,
                 use_pooling=True)

     # # # # # # # # # # # 
    # # # # connecte  # # # 
     # # # # # # # # # # # 
print('flattening')
layer_flat, num_features = nw.flatten_layer(layer_conv_5_3)

print('fully connected 1')
# fc_1
fc_size_1 = 700
layer_fc1 = nw.new_fc_layer(input=layer_flat,
                         num_inputs=num_features,
                         num_outputs=fc_size_1,
                         use_relu=False)
print('fully connected 2')
# fc_3
fc_size_3 = 350
layer_fc_3 = nw.new_fc_layer(input=layer_fc1,
                         num_inputs=fc_size_1,
                         num_outputs=fc_size_3,
                         use_relu=True)

print('fully connected 3')
# fc_4
fc_size_4 = 2
volume_pred = nw.new_fc_layer(input=layer_fc_3,
                         num_inputs=fc_size_3,
                         num_outputs=fc_size_4,
                         use_relu=False)

# Volumes
volume_true = tf.placeholder(tf.float16, shape=None, name='volume_true')

print('optimizer')
# Optimizer
cost = nw.crps(logits=volume_pred,labels=volume_true)
optimizer = tf.train.AdamOptimizer(learning_rate=1e-4).minimize(cost)
 

     # # # # # # # # # # # # #
    # # # # Computation # # # #
     # # # # # # # # # # # # #

print(' ')
print('computation beguin')
with tf.Session() as sess:  
    print('initialization')
    print(' ')
    sess.run(tf.initialize_all_variables())
    while input_train.uncomplete:
        print('batch numero ', str(input_train.nb_batch()))
        dirin = input_train.nextBatch(batch)        
        feed_dict_test = { input_layer: dirin[0], volume_true: dirin[1] }
        sess.run(optimizer, feed_dict=feed_dict_test )    
        if input_train.nb_batch() % 20 == 0:
            print('validation test')
            dirin = input_validate.nextBatch(batch) 
            feed_dict_valide = { input_layer: dirin[0], volume_true: dirin[1] }
            loss = sess.run(cost, feed_dict=feed_dict_valide)
            print( 'loss value on validation set : ', str(loss) )                   
print(' ')
print('end ')









