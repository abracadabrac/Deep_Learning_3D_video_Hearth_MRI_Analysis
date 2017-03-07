import tensorflow as tf
import numpy as np
import networker as nw 
import Input__ as ip

print('_____________')
print(' ')

shape_input = (1, 256, 256, 30)
#            batch  z   x    y    t
batch = shape_input[0]
#zz_ = shape_input[1]
xx_ = shape_input[1]
yy_ = shape_input[2]
tt_ = shape_input[3]

import_data = 1
if import_data:  
    print('data importation') 
    print(' ')     
    x_input = np.load("x_input_train.npy").item()  
    y_true = np.load("y_true_train.npy").item()  

input_1 = ip.InputImages(x_input, y_true, xx_, yy_, tt_)

print('building network')
print(' ')

   # # # # # # # #
  # # # Input # # # 
   # # # # # # # #

input_layer = tf.placeholder(tf.float32, shape=[None, xx_, yy_, tt_])

   # # # # # # # # #
  # # # layer I # # #
   # # # # # # # # #

# conv 1-1
filter_size_1_1 = 32
nb_filters_1_1 = 64

layer_conv_1_1, kernel_1_1 = \
    nw.new_conv_layer(input=input_layer,
                   num_input_channels=tt_,
                   filter_size=filter_size_1_1,
                   num_filters=nb_filters_1_1,
                   use_pooling=False)

# conv 1-2
filter_size_1_2 = 32
nb_filters_1_2 = 64

layer_conv_1_2, kernel_1_2 = \
    nw.new_conv_layer(input=layer_conv_1_1,
                   num_input_channels=nb_filters_1_1,
                   filter_size=filter_size_1_2,
                   num_filters=nb_filters_1_2,
                   use_pooling=True)

   # # # # # # # # #
  # # # layer 2 # # #
   # # # # # # # # #
 
 # conv 2-1
filter_size_2_1 = 32
nb_filters_2_1 = 128

layer_conv_2_1, kernel_2_2 = \
  nw.new_conv_layer(input=layer_conv_1_2,
                 num_input_channels=nb_filters_1_2,
                 filter_size=filter_size_2_1,
                 num_filters=nb_filters_2_1,
                 use_pooling=False)

 # conv 2-2
filter_size_2_2 = 32
nb_filters_2_2 = 128

layer_conv_2_2, kernel_2_2 = \
  nw.new_conv_layer(input=layer_conv_2_1,
                 num_input_channels=nb_filters_2_1,
                 filter_size=filter_size_2_2,
                 num_filters=nb_filters_2_2,
                 use_pooling=True)

   # # # # # # # # #
  # # # layer 3 # # #
   # # # # # # # # #

# conv 3-1
filter_size_3_1 = 16
nb_filters_3_1 = 256

layer_conv_3_1, kernel_3_1 = \
  nw.new_conv_layer(input=layer_conv_2_2,
                 num_input_channels=nb_filters_2_2,
                 filter_size=filter_size_3_1,
                 num_filters=nb_filters_3_1,
                 use_pooling=False)

# conv 3-2
filter_size_3_2 = 16
nb_filters_3_2 = 256

layer_conv_3_2, kernel_3_2 = \
  nw.new_conv_layer(input=layer_conv_3_1,
                 num_input_channels=nb_filters_3_1,
                 filter_size=filter_size_3_2,
                 num_filters=nb_filters_3_2,
                 use_pooling=False)

# conv 3-3
filter_size_3_3 = 16
nb_filters_3_3 = 256

layer_conv_3_3, kernel_3_3 = \
  nw.new_conv_layer(input=layer_conv_3_2,
                 num_input_channels=nb_filters_3_2,
                 filter_size=filter_size_3_3,
                 num_filters=nb_filters_3_3,
                 use_pooling=True)

   # # # # # # # # #
  # # # layer 4 # # #
   # # # # # # # # #

# conv 4-1
filter_size_4_1 = 4
nb_filters_4_1 = 512

layer_conv_4_1, kernel_4_1 = \
  nw.new_conv_layer(input=layer_conv_3_3,
                 num_input_channels=nb_filters_3_3,
                 filter_size=filter_size_4_1,
                 num_filters=nb_filters_4_1,
                 use_pooling=False)

# conv 4-2
filter_size_4_2 = 4
nb_filters_4_2 = 512

layer_conv_4_2, kernel_4_2 = \
  nw.new_conv_layer(input=layer_conv_4_1,
                 num_input_channels=nb_filters_4_1,
                 filter_size=filter_size_4_2,
                 num_filters=nb_filters_4_2,
                 use_pooling=False)

# conv 4-3
filter_size_4_3 = 4
nb_filters_4_3 = 512

layer_conv_4_3, kernel_4_3 = \
  nw.new_conv_layer(input=layer_conv_4_2,
                 num_input_channels=nb_filters_4_2,
                 filter_size=filter_size_4_3,
                 num_filters=nb_filters_4_3,
                 use_pooling=True)

   # # # # # # # # #
  # # # layer 5 # # #
   # # # # # # # # #

# conv 5-1
filter_size_5_1 = 4
nb_filters_5_1 = 512

layer_conv_5_1, kernel_5_1 = \
  nw.new_conv_layer(input=layer_conv_4_3,
                 num_input_channels=nb_filters_4_3,
                 filter_size=filter_size_5_1,
                 num_filters=nb_filters_5_1,
                 use_pooling=False)

# conv 5-2
filter_size_5_2 = 4
nb_filters_5_2 = 512

layer_conv_5_2, kernel_5_2 = \
  nw.new_conv_layer(input=layer_conv_5_1,
                 num_input_channels=nb_filters_5_1,
                 filter_size=filter_size_5_2,
                 num_filters=nb_filters_5_2,
                 use_pooling=False)

# conv 5-3
filter_size_5_3 = 4
nb_filters_5_3 = 512

layer_conv_5_3, kernel_5_3 = \
  nw.new_conv_layer(input=layer_conv_5_2,
                 num_input_channels=nb_filters_5_2,
                 filter_size=filter_size_5_3,
                 num_filters=nb_filters_5_3,
                 use_pooling=True)

     # # # # # # # # # # # 
    # # # # connecte  # # # 
     # # # # # # # # # # # 

# atirement
layer_flat, num_features = nw.flatten_layer(layer_conv_5_3)

# fc_1
fc_size_1 = 4096
layer_fc1 = nw.new_fc_layer(input=layer_flat,
                         num_inputs=num_features,
                         num_outputs=fc_size_1,
                         use_relu=False)

# fc_2
fc_size_2 = 4096
layer_fc2 = nw.new_fc_layer(input=layer_fc1,
                         num_inputs=fc_size_1,
                         num_outputs=fc_size_2,
                         use_relu=False)

# fc_3
fc_size_3 = 1000
layer_fc_3 = nw.new_fc_layer(input=layer_fc2,
                         num_inputs=fc_size_2,
                         num_outputs=fc_size_3,
                         use_relu=True)

# fc_4
fc_size_4 = 1
volume_pred = nw.new_fc_layer(input=layer_fc_3,
                         num_inputs=fc_size_3,
                         num_outputs=fc_size_4,
                         use_relu=False)

# Volumes
volume_true = tf.placeholder(tf.float32, shape=None, name='volume_true')

# Optimizer
cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=volume_pred,
                                                        labels=volume_true)
optimizer = tf.train.AdamOptimizer(learning_rate=1e-4).minimize(cross_entropy)
 

     # # # # # # # # # # # # #
    # # # # Computation # # # #
     # # # # # # # # # # # # #

print(' ')
print('computation beguin')
with tf.Session() as sess:  
    print('initialization')
    print(' ')
    sess.run(tf.initialize_all_variables())
    i=1
    while input_1.uncomplete:
        print('batch numero ', str(i))
        dirin = input_1.nextBatch(batch)
        feed_dict_test = { input_layer: dirin[0], volume_true: dirin[1] }
        sess.run(optimizer, feed_dict=feed_dict_test )       
print(' ')
print('end ')









