#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 10:28:56 2017

@author: charles
"""
import dicom
import numpy as np
import time
import random

def open_image(file_DCM_path, im_size):
    img = dicom.read_file(file_DCM_path).pixel_array
    im_shape = img.shape
    im_shape_max = np.max(im_shape)
    img_carre = np.zeros([im_shape_max,im_shape_max])
    img_carre[0:im_shape[0],0:im_shape[1]] = img
    return img_carre

class InputImages():
   
    
    
    root = ' '          # dir contenant les dossiers patients : 1, 2, 3 ...
    x_input_dir = []
        
    xx_ = -1
    yy_ = -1
    tt_ = 30
    
    index_last_patient = -1
    
    ## variables courantes : ##
    index_p = 0         # index du patient suivant, le patient 
                        # suivant est le meme que le patient courant si sa coupe n'est pas vide
    index_c = 0         # index de la coupe suivante
    nb_c = -1           # nombre de coupe du patient suivant
    id_patient = -1
  
    nb_element = 0      # nombre d'elements recuperes
    
    uncomplete = True   # tant que unnecomplete est vrai il reste des coupes a utiliser
    
    
    
    def __init__(self, root, x_input_dir, xx_):
        self.root = root
        self.x_input_dir = x_input_dir
        self.xx_ = xx_
        self.yy_ = xx_
        self.nb_c = x_input_dir[0]['nombre de coupes']
        self.index_last_patient = len(x_input_dir)-1
        self.id_patient = x_input_dir[0]['id']         
             
        
        
    def describeYou(self):
        print('id_patient         ', str(self.id_patient))
        print('index_p            ', str(self.index_p))
        print('index_c            ', str(self.index_c))
        print('nb_c               ', str(self.nb_c))
        print('nb_batch           ', str(self.nb_batch))
        print('index_last_p       ', str(self.index_last_patient))
        
    def add_patient(self, new_patient):
        self.x_input_dir.append(new_patient)
        self.index_last_patient = len(self.x_input_dir)-1
        
    def nextElement(self):
        
        # on teste si on a deja recupere tous les patients
        if [self.index_p, self.index_c]  == [self.index_last_patient, self.nb_c - 1] :
            self.uncomplete = False
            return {'lst_path' : [],            # ceci est une coupe vide
                  'volume diastolique' : 0,
                  'volume systolique'  : 1 }
        
        # recuperation des volumes du patient
        patient= self.x_input_dir[self.index_p]
        dia_volume = patient['volume diastolique']
        sys_volume = patient['volume systolique' ]
        
        # recuperation de la liste des chemin de la coupe
        coupe = patient['lst_coupe'][self.index_c]        
        coupes_lst_path = coupe['lst_path']

        # creation de l'element
        element= {'lst_path' : coupes_lst_path,
                  'volume diastolique' : dia_volume,
                  'volume systolique'  : sys_volume }
                  
        # mise a jour des indices
        self.index_c = self.index_c + 1        
        if self.index_c == self.nb_c :
            if self.index_p  != self.index_last_patient:
                self.index_p = self.index_p + 1
                self.index_c = 0
                self.nb_c = x_input[self.index_p]['nombre de coupes']
                self.id_patient = x_input[self.index_p]['id']  
            else:       # vrai si dernier element
                self.index_c = self.nb_c - 1

        print(' ')
        self.describeYou()
        self.nb_element = self.nb_element + 1
        return element

    def nextBatch(self, batchSize):
        
        Images = np.zeros( [batchSize, self.tt_,  self.xx_, self.yy_] )
        Volumes = np.zeros([batchSize, 2])
        
        for batch in range(batchSize):
            
            element = self.nextElement()
            
            #for frame in range(len(element['lst_path'])):
                
                #open_image(self.root + element['lst_path'][frame],self.xx_)
                
                
            dia_volume = element['volume diastolique']
            sys_volume = element['volume systolique']
            
            Volumes[batch,:] = [dia_volume, sys_volume]
            
            if dia_volume == 0:         # vrai si element vide, les elements suivant le seront aussi
                for _ in range(batch,batchSize):
                    Volumes = np.delete(Volumes, (batch), axis=0)
                    Images = np.delete(Images, (batch), axis=0)
                break

        Images = Images.astype(np.float32)
        
        return [Images,Volumes]
            
    def data_augmentation(self, type_, val_):   # val est la proportion d'augmentation (dans ]0, 1])
        if type_ == 'temporal_translation':
            index_last = self.index_last_patient
            L = [x for x in range(index_last)]
            random.shuffle(L)       
            # L est un vecteur aléatoir avec une fois chaque nombre entre 0 et le dernier indice
            lst_index_patient = L[0:int(index_last*val_)]
            for index_patient in lst_index_patient:
                new_patient = self.temporal_translation( index_patient)
                self.add_patient(new_patient)
                               
    def temporal_translation(self, index_patient):
        frame_0 = random.randrange(10, 21, 1)
        
        patient = self.x_input_dir[index_patient]
        new_patient = patient
        
        lst_coupe = patient['lst_coupe']
        new_lst_coupe = []
        
        for coupe in lst_coupe:
            new_coupe = coupe
            
            lst_path = coupe['lst_path']
            new_lst_path = sum([lst_path[frame_0:], lst_path[:frame_0]], [])
            
            new_coupe['lst_path'] = new_lst_path
            new_lst_coupe.append(new_coupe)
            
        new_patient['lst_coupe'] = new_lst_coupe
        
        return new_patient
                   
def test(iip):
    iip.nextElement()
    print(' ')
    iip.describeYou()
    print(' ')



if __name__ == '__main__':

    root = '/Users/charles/Workspace/PFE/Sample_TrainSet_IRM_images_10/IRM_images/train_test/'
    x_input = list(np.load("x_input_train_test.npy"))

    xx_ = 256
    iip = InputImages( root, x_input[:3], xx_)
    
    debut = time.time()
    #Batch_ = iip.nextBatch(10)
    fin = time.time()
    
    print(' ')
    iip.describeYou()    
    iip.data_augmentation( 'temporal_translation', 0.5)
    print(' ')
    iip.describeYou()

    iip.x_input_dir
    # print(Batch_)    





















                               