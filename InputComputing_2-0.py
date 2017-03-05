#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd


def reduce_lst(lst):
    new_lst = []

    a = int(len(lst)/30)
    for i in range(30):
        new_lst.append(lst[a*i])
    
    return new_lst
        


### Volumes ###
def compute_volume_true_train_test_validate(Path):
    file_dict = {"train" : "Output_Train.csv", "test" : "Output_Test.csv", "validate" : "validate.csv"}
    path_train = Path + file_dict["train"]
    path_test = Path + file_dict["test"]
    path_validate = Path + '/' + file_dict["validate"]
    train = pd.read_csv(path_train, sep = ',')
    test = pd.read_csv(path_test, sep = ';')
    validate = pd.read_csv(path_validate, sep = ',')
    for col in train.columns:
        train[col] = train[col].apply(lambda x: float(x))
        validate[col] = validate[col].apply(lambda x: float(x))
        test[col] = test[col].apply(lambda x: float(str(x).replace(',','.')))
    train = train.append(test)
    train = train.append(validate)
    train['Id'] = train['Id'].apply(lambda x: int(x))
    header = list(train)
    data = train.values.tolist()
    sys_index = header.index('Systole')
    dia_index = header.index('Diastole')
    id_patient = header.index('Id')
    y_true = {}
    for patient in data:
        sys_volume = float(patient[sys_index])
        dia_volume = float(patient[dia_index])
        y_true[int(patient[id_patient])] = {'dia_volum' : dia_volume, 'sys_volume' : sys_volume}
    return y_true # y_true est un DICT y_true[patient][sys, dias]
    # y_true_patient = y_true[num_patient]
    
def compute_volume_true_train_test(Path):
    file_dict = {"train" : "Output_Train.csv", "test" : "Output_Test.csv", "validate" : "validate.csv"}
    path = Path + file_dict['train']
    path2 = Path + file_dict["test"]
    train = pd.read_csv(path, sep = ',')
    test = pd.read_csv(path2, sep = ';')
    for col in train.columns:
        train[col] = train[col].apply(lambda x: float(x))
        test[col] = test[col].apply(lambda x: float(str(x).replace(',','.')))
    train = train.append(test)
    train['Id'] = train['Id'].apply(lambda x: int(x))
    header = list(train)
    data = train.values.tolist()
    sys_index = header.index('Systole')
    dia_index = header.index('Diastole')
    id_index = header.index('Id')
    y_true = {}
    for patient in data:
        sys_volume = float(patient[sys_index])
        dia_volume = float(patient[dia_index])
        y_true[int(patient[id_index])] = [dia_volume, sys_volume]
    return y_true # y_true est un DICT y_true[patient][sys, dias]
    # y_true_patient = y_true[num_patient]


## images ##
def compute_images_rect_coupe(Path):
    # on restreint aux patients eyant plus que nb_fix_coupes coupes
    lst_patient = []

    list_dir_patient = os.listdir(Path)
    if '.DS_Store' in list_dir_patient:
        list_dir_patient.remove('.DS_Store')
        
    for dir_patient in list_dir_patient:
        id_ = int(dir_patient)
        dir_patient_path = dir_patient + '/study'
        lst_dir_coupe = os.listdir(Path + dir_patient_path)
        lst_coupe = []
        if '.DS_Store' in lst_dir_coupe:
            lst_dir_coupe.remove('.DS_Store')
            
        nb_coupe = len(lst_dir_coupe)

            
        for dir_coupe in lst_dir_coupe:

            z = lst_dir_coupe.index(dir_coupe)
            lst_path = []
            dir_coupe_path = dir_patient_path + '/' + dir_coupe
            lst_file_DCM = os.listdir(Path + '/' + dir_coupe_path)
            
            if (len(lst_file_DCM) > 30) & (len(lst_file_DCM) % 30 == 0) :
                reduce_lst(lst_file_DCM)
                
            for file_DCM in lst_file_DCM:
                file_DCM_path = dir_coupe_path + '/' + file_DCM
                lst_path.append(file_DCM_path) # ON charge le chemin de l'image 
                
            lst_coupe.append({'type' : 'coupe',
            'num' : z,
            'lst_path' : lst_path, 
            'nom' : dir_coupe})
            
            del lst_path
            
        if len(lst_coupe) != 0:
            if len(lst_coupe):
      
                lst_patient.append({'type' : 'patient',
                'id' : id_,
                'lst_coupe' : lst_coupe,
                'volume diastolique' : -1,
                'volume systolique' : -1,
                'nombre de coupes' : nb_coupe})
        
        del lst_coupe
        
    return lst_patient
    
    

    
def merge_images_volumes(x_images, y_true):
    for patient in x_images:
        id_ = patient['id']
        index_ = x_images.index(patient)

        x_images[index_]['volume diastolique'] = y_true[id_][0]
        x_images[index_]['volume systolique']  = y_true[id_][1]
        
    return x_images

    
    
    ##print
def summarize_patient(x_input, id_):    
    for patient in x_input:
        if patient['id'] == id_:
            print('volume diastolique   ', patient['volume diastolique'])
            print('volume systolique    ', patient['volume systolique'])
            print('nombre de coupes     ', patient['nombre de coupes'])
            return
     
            
def A_1(x_input):
    for patient in x_input:
        id_ = patient['id']
        print(' ')
        print(' patient numero ', id_)
        dict_coupe = patient['lst_coupe']
        for coupe in dict_coupe:
            nom = coupe['nom']
            print(nom)
            
def A_2(x_images_train_test):
    print(' ')
    print(' pateint 1 : ')
    summarize_patient(x_images_train_test, 1)
    print(' ')
    print(' pateint 3 : ')
    summarize_patient(x_images_train_test, 3)
    print(' ')
    print(' pateint 50 : ')
    summarize_patient(x_images_train_test, 50)
    print(' ')
    print(' pateint 200 : ')
    summarize_patient(x_images_train_test, 200)
    print(' ')
    print(' pateint 1065 : ')
    summarize_patient(x_images_train_test, 1065)     


if __name__ == '__main__':

    Path = '/Users/charles/Workspace/PFE/data/'
    Path_Images = Path + 'IRM_images/'
    Path_Volumes = Path + 'Volumes/'

    x_images_train_test = compute_images_rect_coupe(Path_Images)
    y_true_train_test = compute_volume_true_train_test(Path_Volumes)
    merge_images_volumes(x_images_train_test, y_true_train_test)
    
    A_2(x_images_train_test)
    #A_2(x_images_train_test)
    
        
    np.save('x_input_train_test.npy', x_images_train_test)

