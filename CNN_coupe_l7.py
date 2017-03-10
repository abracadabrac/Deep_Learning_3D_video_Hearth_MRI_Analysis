'''
Version           Autor                  Descriptioin
1.0               Jean Bizot             Initiation        
1.1               Charles Englebert      minor changes


'''



import tensorflow as tf
import numpy as np
import networker as nw 
import hospital as hp
import csv

print('_____________')
print(' ')

shape_input = (20, 64, 64, 30)
#           batch  z   x   y   t
batch = shape_input[0]
xx_ = shape_input[1]
yy_ = shape_input[2]
tt_ = shape_input[3]

root_train = '/usr/users/promo2017/englebert_cha/Workspace/data/Images_train/'
root_test =  '/usr/users/promo2017/englebert_cha/Workspace/data/Images_test/'

import_data = 1
if import_data:  
    print('data importation') 
    print(' ')     
    x_input_train = list(np.load("x_input_train.npy"))  
    x_input_test = list(np.load("x_input_test.npy"))  


print('Data imported')
print('building network')
print(' ')

   # # # # # # # #
  # # # Input # # # 
   # # # # # # # #

images_layer = tf.placeholder(tf.float32, shape=[None, xx_, yy_, tt_])

   # # # # # # # # #
  # # # layer I # # #
   # # # # # # # # #

filter_size_1_1 = 32
nb_filters_1_1 = 64

layer_conv_1_1, kernel_1_1 = \
    nw.new_conv_layer(input=images_layer,
                   num_input_channels=tt_,
                   filter_size=filter_size_1_1,
                   num_filters=nb_filters_1_1,
                   use_pooling=True)


   # # # # # # # # #
  # # # layer 2 # # #
   # # # # # # # # #

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

layer_flat, num_features = nw.flatten_layer(layer_conv_5_3)

# fc_1
fc_size_1 = 700
layer_fc1 = nw.new_fc_layer(input=layer_flat,
                         num_inputs=num_features,
                         num_outputs=fc_size_1,
                         use_relu=False)

# fc_3
fc_size_3 = 350
layer_fc_3 = nw.new_fc_layer(input=layer_fc1,
                         num_inputs=fc_size_1,
                         num_outputs=fc_size_3,
                         use_relu=True)

# fc_4
fc_size_4 = 2
volume_pred_layer = nw.new_fc_layer(input=layer_fc_3,
                         num_inputs=fc_size_3,
                         num_outputs=fc_size_4,
                         use_relu=False)

# Volumes
volume_true_layer = tf.placeholder(tf.float32, shape=[None, 2])

# batch_size
batch_size_layer = tf.placeholder(tf.float32)

# Optimizer
cost = nw.crps(volume_true_layer, volume_pred_layer, batch_size_layer)
#optimizer = tf.train.AdamOptimizer(learning_rate=1e-4).minimize(cost)





with tf.Session() as sess: 

    hsp_train = hp.Hospital(root_train, x_input_train, xx_)

    sess.run(tf.global_variables_initializer())

    with open('pred_CNN_coupe_l7_Test.csv', 'w') as csvfile:
        fieldnames = ['id patient',
            'nom de la coupe',
            'index patient',
            'index coupe' ,
            'volume dia ',
            'volume sys',
            'volume dia *',
            'volume sys *',
            'volume dia pred',
            'volume sys pred',
            'cost',
            'batch']    

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


    for _ in range(2):
      images, volumes = hsp_train.nextBatch(12)
      batch_size = volumes.shape[0]


      y_pred_ = sess.run(volume_pred_layer, feed_dict = { images_layer: images })
      print(' ')
      print('y_pred')
      print(y_pred_)

      y_true_ = sess.run(volume_true_layer, feed_dict = { volume_true_layer : volumes })
      print('y_true')
      print(y_true_)
      
      cost_ = sess.run(cost, feed_dict = { volume_pred_layer : y_pred_, 
        volume_true_layer : y_true_,
        batch_size_layer : batch_size })
      print('cost')
      print(cost_)


      hsp_train.maj_info(y_pred_, y_true_, cost_)

'''
    with open('predictions_CNN_coupe_l7.csv', 'w') as csvfile:
        fieldnames = ['id patient', 'nom de la coupe', 
        'index patient', 'index coupe', 
        'volume true', 'volume pred', 'cost']

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'id patient' : 0 , 'nom de la coupe' : 0, 
        'index patient' : 0, 'index coupe' : 0, 
        'volume true' : y_true_, 'volume pred' : y_pred_, 'cost' : cost_})
'''





'''

print('optimizer')
# Optimizer
cost = nw.crps(volume_pred,volume_true)
optimizer = tf.train.AdamOptimizer(learning_rate=1e-4).minimize(cost)
'''

     # # # # # # # # # # # # #
    # # # # Computation # # # #
     # # # # # # # # # # # # #

'''
print(' ')
print('computation beguin')
with tf.Session() as sess:  
    print('initialization')
    print(' ')

    lst_ypred_test = np.empty(0)
    lst_ytrue_test = []
    lst_loss = []
    hsp_train = hp.Hospital(root_train, x_input_train, xx_)

    sess.run(tf.initialize_all_variables())

    while hsp_train.uncomplete():
        print('batch numero ', str(hsp_train.nb_element()))

        images, volumes_ture = hsp_train.nextBatch(batch)
        feed_dict_test = { input_layer: images, volume_true: volumes_ture }

        sess.run(optimizer, feed_dict=feed_dict_test )    

        if input_train.nb_elements() % 5 == 0:
            print('validation test')

            hsp_test = hp.Hospital(root_test, x_input_test, xx_)

         


            print( 'loss value on validation set : ', str(loss) )                   
print(' ')
print('end ')
'''








