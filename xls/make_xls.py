import os
import dicom
from openpyxl import Workbook
import tkinter as tk
from tkinter import filedialog

# Collect dicoms
root = tk.Tk()
file_path = filedialog.askdirectory()
lstFilesDCM = []

for dirName, subdirList, fileList in os.walk(file_path):
    for filename in fileList:
        if ".dcm" in filename.lower():
            lstFilesDCM.append(os.path.join(dirName,filename))            
            
root.withdraw()

# Open Excel workbook
wb = Workbook()
ws = wb.active

# Write fields
metadata0 = dicom.read_file(lstFilesDCM[0])
line0_head = ['Patient','View','Frame No.']
line0 = line0_head + metadata0.dir()
ws.append(line0)

# Write data
for dicomFile in lstFilesDCM:
    metadata = dicom.read_file(dicomFile)
    
    (radix1,frame_name)     = os.path.split(dicomFile)
    (radix2,view_name)      = os.path.split(radix1)
    (radix3,dump)           = os.path.split(radix2)
    (radix4,patient_id)     = os.path.split(radix3)
    
    line_head = [patient_id,view_name,frame_name]
    full_line = line_head + metadata.dir()
    
    ws.append(full_line)

wb.save('summary.xlsx')
print('saved')