import os
import sys
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
    file_dict = {"train" : "Output_Train.csv", "test" : "Output_Test.csv", "validate" : "Output_Validate.csv"}
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
        y_true[int(patient[id_patient])] = {'dia_volum' : dia_volume, 'sys_volum' : sys_volume}
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
    lst_patient = []
    regected_index_patient = []

    list_dir_patient = os.listdir(Path)
    if '.DS_Store' in list_dir_patient:
        list_dir_patient.remove('.DS_Store')
        
    for dir_patient in list_dir_patient:
        id_ = int(dir_patient)
        print('id patient    ', id_)
        dir_patient_path = dir_patient + '/study'
        lst_dir_coupe = os.listdir(Path + dir_patient_path)
        lst_coupe = []
        if '.DS_Store' in lst_dir_coupe:
            lst_dir_coupe.remove('.DS_Store')
            
        num_coupe = 0

        for dir_coupe in lst_dir_coupe:

            z = lst_dir_coupe.index(dir_coupe)
            lst_path = []
            dir_coupe_path = dir_patient_path + '/' + dir_coupe
            lst_file_DCM = os.listdir(Path + '/' + dir_coupe_path)

            if (len(lst_file_DCM) != 30) & (z == 0):
                regected_index_patient.append(id_)

            if len(lst_file_DCM) == 30:

                for file_DCM in lst_file_DCM:
                    file_DCM_path = dir_coupe_path + '/' + file_DCM
                    lst_path.append(file_DCM_path) # ON charge le chemin de l'image 

                lst_coupe.append({'type' : 'coupe',
                    'num' : num_coupe,
                    'lst_path' : lst_path,
                    'nom' : dir_coupe,
                    'desactivate' : True})

                num_coupe = num_coupe + 1
            
            del lst_path
            
        if len(lst_coupe) != 0:
            print('           *')
            lst_patient.append({'type' : 'patient',
            'id' : id_,
            'lst_coupe' : lst_coupe,
            'volume diastolique' : -1,
            'volume systolique' : -1,
            'nombre de coupes' : num_coupe})
        else:
            print(' ')
        
        del lst_coupe
        
    print('patients regete par ou exce manque de frame : ')
    print(regected_index_patient)
    return lst_patient
    
    

    
def merge_images_volumes(x_images, y_true):
    for patient in x_images:
        id_ = patient['id']
        index_ = x_images.index(patient)
        #print(' ')
        #print('merge id     ', str(id_))
        #print('merge index  ',str(index_))
        x_images[index_]['volume diastolique'] = y_true[id_]['dia_volum']
        x_images[index_]['volume systolique']  = y_true[id_]['sys_volum']
        
    return x_images

    
    
    ##print
def summarize_patient(x_input, id_):    
    for patient in x_input:
        if patient['id'] == id_:
            index_patient = x_input.index(patient)
            print('index du patient     ', str(index_patient))
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
    print(' pateint 1138 : ')
    summarize_patient(x_images_train_test, 1138)
    print(' ')
    print(' pateint 1001 : ')
    summarize_patient(x_images_train_test, 1001)
    print(' ')
    print(' pateint 50 : ')
    summarize_patient(x_images_train_test, 50)
    print(' ')
    print(' pateint 200 : ')
    summarize_patient(x_images_train_test, 200)
    print(' ')
    print(' pateint 506 : ')
    summarize_patient(x_images_train_test, 506)
    print(' ')
    print(' pateint 1065 : ')
    summarize_patient(x_images_train_test, 1065)     
    print(' ')

if __name__ == '__main__':

    #Path = '/usr/users/promo2017/englebert_cha/Workspace/data'
    Path = sys.argv[1]                      # commande : ipython3 InputComputing.py votre_path
                                            # avec votre path la racine du dossier contenant vos dossier parient
                                            # patient et volumes
    Path_Images = Path + '/Images/'     # c est a dire train test ou validate
    Path_Volumes = Path + '/Volumes/'       # le dossier des csv des volumes

    x_images = compute_images_rect_coupe(Path_Images)               #les images
    y_true = compute_volume_true_train_test_validate(Path_Volumes)  # les volumes

    merge_images_volumes(x_images, y_true)                          # fusion des deux
    
    
        
    np.save('x_input.npy', x_images)                    # sauvegarde des donnees

    # np.save('x_input_train.npy', x_images)        #si doc de train
    # np.save('x_input_test.npy', x_images)         #si doc de test ...








