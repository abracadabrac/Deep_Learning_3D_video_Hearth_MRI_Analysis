import dicom
import os
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt

    # image adress only
def compute_inpute_dir(Path):
    dictPatients = {}  # create an empty dictonary
    num_patient=0   # numero courant du patient
    for dirName, subdirList, fileList in os.walk(Path):
        if(len(subdirList) == 1):   # true <=> dirName = dossier racine d'un patient       
            lstCoupes = []  # La liste des coupes contients les image, elle est contenue par la liste des patients
            indice_str = dirName.find('/',len(dirName)-5)       #indice du numero du patient dans le nom du dossier
            num_patient = int(dirName[indice_str+1:indice_str+5])
        if(len(subdirList) == 0):   # true <=> dirName = dossier d'une coupe contenant les images 
            lstimage = []
            for filname in fileList:
                lstimage.append([dirName+'/'+filname])  
            lstCoupes.append(lstimage)
            dictPatients[num_patient] = lstCoupes   #mise a jour du dico           
    return dictPatients
    
    
def compute_inpute_list(Path):
    lstPatients = np.zeros(compute_nb_patients(Path), dtype = object)  # create np.array of size nb_patients
    num_patient=1   # numero courant du patient
    lstCoupes = []
    for dirName, subdirList, fileList in os.walk(Path):
        if(len(subdirList) == 1):   # true <=> dirName = dossier racine d'un patient
            lstPatients[num_patient-1] = lstCoupes
            lstCoupes = []  # La liste des coupes contients les image, elle est contenue par la liste des patients
            indice_str = dirName.find('/',len(dirName)-5)       #indice du numero du patient dans le nom du dossier
            num_patient = int(dirName[indice_str+1:indice_str+5])
        if(len(subdirList) == 0):   # true <=> dirName = dossier d'une coupe contenant les images 
            lstimage = []
            for filname in fileList:
                file_name = dirName+'/'+filname
                img = dicom.read_file(file_name).pixel_array 
                lstimage.append( img )  
            lstCoupes.append(lstimage) # mise a jour de la list   
    return lstPatients

    # compute a rectangular input
def compute_inpute_list_rect(Path, nb_fix_coupes):
    # on restreint aux patients eyant plus que nb_fix_coupes coupes
    nb_patient_selected = compute_nb_patient_selected(Path, nb_fix_coupes)
    x_input = np.zeros([nb_patient_selected, nb_fix_coupes, 30, 512, 512] )  # create an empty dictonary
    list_index = []
    id_input = -1
    list_dir_patient = os.listdir(Path)[1:]
    for dir_patient in list_dir_patient:
        dir_patient_path = Path + '/' + dir_patient + '/study'
        lst_dir_coupe = os.listdir(dir_patient_path)
        if '.DS_Store' in lst_dir_coupe:
            lst_dir_coupe.remove('.DS_Store')   # on enleve le dossier .DS_Store
        if len(lst_dir_coupe) > nb_fix_coupes-1:
            print(' ')
            print('         ___### patient ###___ : ' + dir_patient)
            id_ = int(dir_patient)
            list_index.append(id_)
            id_input = id_input + 1
            for dir_coupe in lst_dir_coupe:
                z = lst_dir_coupe.index(dir_coupe)
                if z < nb_fix_coupes:           # !! how z cuts are selected
                    print('coupe : ' + str(z+1))
                    dir_coupe_path = dir_patient_path + '/' + dir_coupe
                    lst_file_DCM = os.listdir(dir_coupe_path)
                    for file_DCM in lst_file_DCM:
                        t = lst_file_DCM.index(file_DCM)
                        #print('temps : ' + str(t))
                        file_DCM_path = dir_coupe_path + '/' + file_DCM
                        img = dicom.read_file(file_DCM_path).pixel_array 
                        #print( 'patient : ' + dir_patient +  '           |           coupe : ' + dir_coupe )
                        #plt.pcolormesh(img)
                        #plt.show()
                        for x in np.arange(img.shape[0]):
                            for y in np.arange(img.shape[1]):
                                x_input[id_input, z, t, x, y] = img[x, y] 
    print(list_index)
    return x_input, list_index

def Analysis_inpute_list_rect(x_input):
    shape_ = x_input.shape
    for id_ in shape_[0]:
        for z in shape_[1]:
            for t in shape_[2]:
                print( 'patient : ' + str(id_) +  '           |           coupe : ' + str(z) )
                plt.pcolormesh(x_input[id_, z, t, :, :])
                plt.show()

    
def compute_nb_patient_selected(Path, nb_fix_coupes):
    nb_patient_selected = 0
    nb_coupes = compute_nb_coupes(Path)
    for nb in nb_coupes:
        if nb > nb_fix_coupes-1:
            nb_patient_selected = nb_patient_selected + 1
    return nb_patient_selected
             
            
def compute_nb_patients(Path):
    nb_patients=0   # nombre de patients
    for dirName, subdirList, fileList in os.walk(Path):
        if(len(subdirList) == 1):   # true <=> dirName = dossier racine d'un patient
            nb_patients = nb_patients+1
    return nb_patients
    # type( nb_patient ) = int
    
def compute_nb_trams(Path):
    nb_trams = []
    for dirName, subdirList, fileList in os.walk(Path):
        if(len(subdirList) == 0):   # true <=> dirName = dossier d'une coupe contenant les images 
            nb_trams.append(len(fileList))
    return nb_trams
    # nb_trams[num_patient]
    
def compute_nb_coupes(Path):
    nb_coupes = []   
    for dirName, subdirList, fileList in os.walk(Path):
        if(len(dirName[dirName.find('/study'):100]) == 6):   # true <=> dirName = dossier study 
            nb_coupes.append(len(subdirList))         
    return nb_coupes  
    # nb_coupes[num_patient]
    
def compute_size_images(Path):
    imageSize = {}  # create an empty dictonary
    num_patient=0   # numero courant du patient
    for dirName, subdirList, fileList in os.walk(Path):
        if(len(subdirList) == 1):   # true <=> dirName = dossier racine d'un patient
            lstCoupes = []  # La liste des coupes contients les image, elle est contenue par la liste des patients
            indice_str = dirName.find('/',len(dirName)-5)        #indice du numero du patient dans le nom du dossier
            num_patient = int(dirName[indice_str+1:indice_str+5])
        if(len(subdirList) == 0):   # true <=> dirName = dossier d'une coupe contenant les images 
            print(num_patient)
            lstimage = []
            filname = fileList[1]
            Path_image = dirName+'/'+filname
            image = dicom.read_file(Path_image)
            lstimage = [int(image.Rows), int(image.Columns)]
            lstCoupes.append(lstimage)
            imageSize[num_patient] = lstCoupes   #mise a jour du dico            
    return imageSize
    
    # convert every values of x_size and y_size of images in sigles vectors for ploting
def analyse_size_images(imageSize):
    vect_x_size = []
    vect_y_size = []
    for _, size_patient in imageSize.items():
        for size_coupe in size_patient:
            vect_x_size.append(size_coupe[0])
            vect_y_size.append(size_coupe[1])
    return vect_x_size, vect_y_size
    
'''
imageSize = compute_size_images(Path)
vect_x_size, vect_y_size = analyse_size_images(imageSize)
plt.plot(vect_x_size)
plt.plot(vect_y_size)
'''
            
    
# Path = "/Volumes/LaCie/PFE_INSERM_IRM_Data/train"  
Path = "/Users/charles/Workspace/Sample_TrainSet_IRM_images"
nb_fix_coupes = 12

x_input = compute_inpute_list_rect(Path, nb_fix_coupes)





