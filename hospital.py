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
import pp_execution as pp
import matplotlib.pyplot as plt
import csv

def open_image(file_DCM_path, im_size):
    img = dicom.read_file(file_DCM_path).pixel_array
    im_shape = img.shape
    im_shape_max = np.max(im_shape)
    img_carre = np.zeros([im_shape_max,im_shape_max])
    img_carre[0:im_shape[0],0:im_shape[1]] = img
    img_carre_crop = cv2.resize(img_carre, (im_size,im_size))
    return img_carre_crop

class Hospital():

    
    root = ' '          # dir contenant les dossiers patients : 1, 2, 3 ...
    x_input_dir = []
        
    xx_ = -1
    yy_ = -1
    tt_ = 30
    
    index_last_patient = -1
    
    ## variables courantes : ##
    index_p = 0         # index du patient suivant, le patient 
                        # suivant est le meme que le patient courant si sa coupe n'est pas vide
    index_c = -1         # index de la coupe suivante
    nb_c = -1           # nombre de coupe du patient suivant
    id_patient = -1
  
    nb_element = 0      # nombre d'elements recuperes
    nb_batch = 0
    
    uncomplete = True   # tant que unnecomplete est vrai il reste des coupes a utiliser

    lst_info = []
    lst_lst_info = []

    
    
    
    def __init__(self, root, x_input_dir, xx_):
        
        self.root = root
        self.x_input_dir = x_input_dir
        self.xx_ = xx_
        self.yy_ = xx_

        self.nb_c = x_input_dir[0]['nombre de coupes']
        self.id_patient = x_input_dir[0]['id']  
        self.index_last_patient = len(x_input_dir)-1
        
        self.sax_only()         # ne selectionne que les saxs
        self.filterNoCh()       # inibe les patient auquel il manque un ch
        self.nextCoupe()        # initialise les variables d etat
              
    def describeYou(self):
        print(' ')
        print('description de l hospital')
        print(' id_patient         ', str(self.id_patient))
        print(' index_p            ', str(self.index_p), ' / ', str(self.index_last_patient))
        print(' index_c            ', str(self.index_c), ' / ', str(self.nb_c))
        print(' nb_batch           ', str(self.nb_batch))
        print(' nb_elements        ', str(self.nb_element))
        
        # ajoute un patient a l hospital
    def add_patient(self, new_patient):
        self.x_input_dir.append(new_patient)
        self.index_last_patient = len(self.x_input_dir)-1
        
        # ajoute une coupe a un patient
    def add_coupe(self, index_patient, lst_path, nom):
        patient = self.x_input_dir[index_patient]
        num = patient['nombre de coupes']
        lst_coupe = self.x_input_dir[index_patient]['lst_coupe'][:]
        
        self.x_input_dir[index_patient]['nombre de coupes'] = num +1
        
        coupe = { 'type' : 'coupe',
            'num' : num,
            'lst_path' : lst_path, 
            'nom' : nom }
            
        lst_coupe.append(coupe)
        
        self.x_input_dir[index_patient]['lst_coupe'] = lst_coupe       
        
    def info_patient(self, index_patient):
        patient = self.x_input_dir[index_patient]
        
        print( ' ' )
        print('description du patient indexe', str(index_patient))
        print(' id                     ', str(patient['id']))
        print(' nombre de coupes       ', str(patient['nombre de coupes']))
        print(' nombre de coupes *     ', str(len(patient['lst_coupe'])))
        print( ' ' )
            
    def info_coupe(self, index_patient, index_coupe, path):
        patient = self.x_input_dir[index_patient]
        coupe = patient['lst_coupe'][index_coupe]
        
        print( ' ' )
        print('description de la coupe ', str(index_coupe),
              ' du patient indexe ', str(index_patient))
        print(' id du patient          ', str(patient['id']))
        print(' nombre de coupes       ', str(patient['nombre de coupes']))
        print(' nom                    ', str(coupe['nom']))
        print(' num                    ', str(coupe['num']))
        print(' taille du path         ', str(len(coupe['lst_path'])))
        print(' desactivated           ', str(coupe['desactivate']))
        if path:
            print(' path   :')
            print(coupe['lst_path'])
        print( ' ' )


    def summarize_patient(self, id_):    
        for patient in self.x_input_dir:
            if patient['id'] == id_:
                print('descpition du patient id ', str(id_))
                index_patient = self.x_input_dir.index(patient)
                print(' index du patient     ', str(index_patient))
                print(' volume diastolique   ', patient['volume diastolique'])
                print(' volume systolique    ', patient['volume systolique'])
                print(' nombre de coupes     ', patient['nombre de coupes'])
                return              
        print('id not found')

        # retourne les indices des coupes de type demande du patient d indice delande
    def getCoupeIndex(self, index_patient, type):        
        patient = self.x_input_dir[index_patient]
        lst_coupe = patient['lst_coupe']
        lst_indexCoupe = []
        for coupe in lst_coupe :
            if coupe['nom'][0:3] == type:
                lst_indexCoupe.append(lst_coupe.index(coupe))   
        return lst_indexCoupe
            
    def nextCoupe(self):
        self.index_c = self.index_c + 1        

        if self.index_c == self.nb_c :      # vrai si derniere coupe du patient
            if self.index_p  != self.index_last_patient:   # faux si dernier patient
                self.index_p = self.index_p + 1
                self.index_c = 0
                self.nb_c = self.x_input_dir[self.index_p]['nombre de coupes']
                self.id_patient = self.x_input_dir[self.index_p]['id']  
            else:       # vrai si dernier patient de l hospital
                self.index_c = self.nb_c - 1
                self.uncomplete = False

        if self.x_input_dir[self.index_p]['lst_coupe'][self.index_c]['desactivate'] :  
        # vrai si l element est innactif
            if (self.index_c == self.nb_c-1) & (self.index_p  == self.index_last_patient):
                return
            else:
                self.nextCoupe()
        
    def nextElement(self):

        self.describeYou()

        # on teste si on a deja recupere tous les patients
        if [self.index_p, self.index_c]  == [self.index_last_patient, self.nb_c - 1] :
            self.uncomplete = False
            return {'lst_path' : [],            # ceci est un element vide
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
                  
        self.lst_info.append({'id patient' : self.id_patient,
            'nom de la coupe' : coupe['nom'],
            'index patient' : self.index_p,
            'index coupe' : self.index_c,
            'volume dia ' : dia_volume,
            'volume sys' : sys_volume,
            'volume dia *' : ' ',
            'volume sys *' : ' ',
            'volume dia pred' : ' ',
            'volume sys pred' : ' ',
            'cost' : ' ',
            'batch' : ' '})

        self.nb_element = self.nb_element + 1
        #print(' ')
        #self.describeYou()
        return element

    def nextBatch(self, batchSize):
        Images = np.zeros( [batchSize,  self.xx_, self.yy_, self.tt_] )
        Volumes = np.zeros([batchSize, 2])
        
        for batch in range(batchSize):
            
            element = self.nextElement()
            
            for frame_path in element['lst_path']:

                frame = self.processFrame(self.root + frame_path)

                # frame = open_image(self.root + frame_path, self.xx_)
                index_frame = element['lst_path'].index(frame_path)

                Images[batch, :, :, index_frame] = frame
                                
            dia_volume = element['volume diastolique']
            sys_volume = element['volume systolique']
            
            Volumes[batch,:] = [dia_volume, sys_volume]
            
            if dia_volume == 0:         # vrai si element vide, les elements suivant le seront aussi
                for _ in range(batch,batchSize):
                    Volumes = np.delete(Volumes, (batch), axis=0)
                    Images = np.delete(Images, (batch), axis=0)
                break

            # mise a jour des indices       
            self.nextCoupe()

        Images = Images.astype(np.float32)

        if len(Volumes) != 0:
            self.nb_batch = self.nb_batch + 1
        
        return Images, Volumes
            
    def data_augmentation(self, type_, val_):   # val est la proportion d'augmentation (dans ]0, 1])
        if type_ == 'temporal_translation':
            index_last = self.index_last_patient
            L = [x for x in range(index_last)]
            random.shuffle(L)       
            # L est un vecteur aléatoir avec une fois chaque nombre entre 0 et le dernier indice
            lst_index_patient = L[0:int(index_last*val_)]
            for index_patient in lst_index_patient:
                self.temporal_translation( index_patient )
                               
    def temporal_translation(self, index_patient):
        frame_0 = random.randrange(10, 21, 1)
        
        patient = self.x_input_dir[index_patient]        
        lst_coupe = patient['lst_coupe'][:]
        
        for coupe in lst_coupe:
            nom = coupe['nom']           
            lst_path = coupe['lst_path'][:]
            new_lst_path = sum([lst_path[frame_0:], lst_path[:frame_0]], [])
            
            self.add_coupe( index_patient, new_lst_path, nom)   

    def processFrame(self, frame_path):
        ch2_index = self.getCoupeIndex(self.index_p, '2ch')[0]
        ch4_index = self.getCoupeIndex(self.index_p, '4ch')[0]

        ch2_path = self.root + self.x_input_dir[self.index_p]['lst_coupe'][ch2_index]['lst_path'][0]
        ch4_path = self.root + self.x_input_dir[self.index_p]['lst_coupe'][ch4_index]['lst_path'][0]

        frame = pp.sax_to_ndarray(1.6, 1.6, self.xx_, self.yy_, ch4_path, ch2_path, frame_path)

        return frame

    def sax_only(self):
        for patient in self.x_input_dir:

            index_patient = self.x_input_dir.index(patient)

            lst_index_sax = self.getCoupeIndex( index_patient, 'sax')
            for index_sax in lst_index_sax:
                self.x_input_dir[index_patient]['lst_coupe'][index_sax]['desactivate'] = False

    def filterNoCh(self):
        for patient in self.x_input_dir:
            index_patient = self.x_input_dir.index(patient)
            lst_index_ch2 = self.getCoupeIndex( index_patient, '2ch')
            lst_index_ch4 = self.getCoupeIndex( index_patient, '4ch')

            if (len(lst_index_ch2) == 0 ) | (len(lst_index_ch4) == 0):
                for index_coupe in range(patient['nombre de coupes']):
                    self.x_input_dir[index_patient]['lst_coupe'][index_coupe]['desactivate'] = True


    def maj_info(self, y_pred, y_true, cost):
        new_lst_info = []
        for info in self.lst_info:
            index = self.lst_info.index(info)
            volume_pred = y_pred[index]
            volume_true = y_true[index]
            dia_pred = volume_pred[0]
            sys_pred = volume_pred[1]
            dia_true = volume_true[0]
            sys_true = volume_true[1]
            info['volume sys *'] = sys_true
            info['volume dia *'] = dia_true
            info['volume sys pred'] = sys_pred
            info['volume dia pred'] = dia_pred
            info['cost'] = cost
            info['batch'] = self.nb_batch
            new_lst_info.append(info)
            print(info)
            
        self.lst_info = []
        self.lst_lst_info.append(new_lst_info)

        print(self.lst_lst_info)


    def writte_csv(self, y_pred, y_true, cost, name):

        with open(name, 'w') as csvfile:
            fieldnames = list(self.sauv_infos[0].keys())
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            

                    
                
            writer.writerow(info)



        
def test(hosp):
    hosp.nextElement()
    print(' ')
    hosp.describeYou()
    print(' ')

def sumarization_1(hosp):
    print(' ')
    hosp.summarize_patient(721)
    print(' ')
    hosp.info_coupe(21,0, 0)
    print(' ')
    hosp.info_coupe(21,-1, 0)



if __name__ == '__main__':

    root = '/Users/charles/Workspace/PFE/data/IRM_images/'
    x_input_test = list(np.load("x_input_test.npy"))

    hosp = Hospital( root, x_input_test[0:10], xx_= 64 )

    while hosp.uncomplete:
        images, volumes = hosp.nextBatch(30)

    print(' ')
    print('fin')

    # hosp.describeYou()        # print des variables de l hosp
                                # c est la fonction qui est appelee a chaque NextElement()


    # hosp.info_coupe(index_patient, index_coupe, False) # print les info sur la coupe
    # hosp.getCoupeIndex(0, 'sax')      # list les index des coupes sax du patient d index 0








