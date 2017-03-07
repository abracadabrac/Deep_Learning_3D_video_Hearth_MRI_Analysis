import dicom_geometry as dgeom
import numpy as np
import matplotlib.pyplot as plt
import os

# dx0, dy0, nx0, ny0

def sax_to_ndarray(dx0, dy0, nx0, ny0, four_ch, two_ch, sax_path):
    frame_in, x, y = dgeom.dicom_to_arrays(sax_path)
    p1 = dgeom.locate_plane(four_ch)
    p2 = dgeom.locate_plane(four_ch)
    p3 = dgeom.locate_plane(four_ch)
    itsc = dgeom.three_plane_intersect(p1, p2, p3)
    lv_center_x, lv_center_y = dgeom.xyz_to_pixels(itsc)
    frame_out = dgeom.normalize_frame(frame_in, dx0, dy0, nx0, ny0, x, y, lv_center_x, lv_center_y)
    
    return frame_out
