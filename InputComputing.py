import dicom
import os
import numpy
from matplotlib import pyplot, cm
import time

#Path = "./Sample_TrainSet_IRM_images/"
def compute_inpute(Path):
    dictPatients = {}  # create an empty dictonary
    num_patient=0   # numero courant du patient
    for dirName, subdirList, fileList in os.walk(Path):
        if(len(subdirList) == 1):   # true <=> dirName = dossier racine d'un patient
            lstCoupes = []  # La liste des coupes contients les image, elle est contenue par la liste des patients
            indice_str = dirName.find('/',10)       #indice du numero du patient dans le nom du dossier
            num_patient = int(dirName[indice_str+1:indice_str+5])
        if(len(subdirList) == 0):   # true <=> dirName = dossier d'une coupe contenant les images 
            lstimage = []
            for filname in fileList:
                lstimage.append([dirName+'/'+filname])  
            lstCoupes.append(lstimage)
            dictPatients[num_patient] = lstCoupes   #mise a jour du dico
            
    return dictPatients
            
            
def compute_nb_patients(Path):
    nb_patients=0   # nombre de patients
    for dirName, subdirList, fileList in os.walk(Path):
        if(len(subdirList) == 1):   # true <=> dirName = dossier racine d'un patient
            nb_patients = nb_patients+1
    return nb_patients
    
    
def compute_nb_trams(Path):
    nb_trams = []
    for dirName, subdirList, fileList in os.walk(Path):
        if(len(subdirList) == 0):   # true <=> dirName = dossier d'une coupe contenant les images 
            nb_trams.append(len(fileList))
    return nb_trams
    
    
def compute_nb_coupes(Path):
    nb_coupes = []   
    for dirName, subdirList, fileList in os.walk(Path):
        if(len(dirName[dirName.find('/study'):100]) == 6):   # true <=> dirName = dossier study 
            nb_coupes.append(len(subdirList))         
    return nb_coupes
    
    
Path = "/Volumes/LaCie/PFE_INSERM_IRM_Data/train"  
nb_coupes = compute_nb_coupes(Path)
nb_trams = compute_nb_trams(Path)
    
    