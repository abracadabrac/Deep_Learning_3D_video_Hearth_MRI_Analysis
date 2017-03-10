import dicom_geometry as dgeom
import numpy as np
import matplotlib.pyplot as plt
import os

# dx0, dy0, nx0, ny0
# separate center localization from cropping


def sax_to_ndarray(dx0, dy0, nx0, ny0, four_ch, two_ch, sax):
    frame_in, x, y = dgeom.dicom_to_arrays(sax)
    p1 = dgeom.locate_plane(four_ch)
    p2 = dgeom.locate_plane(two_ch)
    p3 = dgeom.locate_plane(sax)
    itsc = dgeom.three_plane_intersect(p1, p2, p3)
    lv_center_x, lv_center_y = dgeom.xyz_to_pixels(itsc, sax)
    frame_out = dgeom.normalize_frame(
        frame_in, dx0, dy0, nx0, ny0, x, y, lv_center_x, lv_center_y)

    return frame_out


def nch_to_ndarray(dx0, dy0, nx0, ny0, four_ch, two_ch, sax_slices):
    four_ch_in, x4, y4 = dgeom.dicom_to_arrays(four_ch)
    two_ch_in, x2, y2 = dgeom.dicom_to_arrays(two_ch)
    p1 = dgeom.locate_plane(four_ch)
    p2 = dgeom.locate_plane(two_ch)
    l = []
    for sax_slice in sax_slices:
        p_sax = dgeom.locate_plane(sax_slice)
        itsc = dgeom.three_plane_intersect(p1, p2, p_sax)
        l.append(itsc)
    center = np.sum(np.array(l))
    four_ch_x, four_ch_y =  dgeom.xyz_to_pixels(center, four_ch)
    two_ch_x, two_ch_y =  dgeom.xyz_to_pixels(center, two_ch)
    four_ch_out = dgeom.normalize_frame(four_ch_in, dx0, dy0, nx0, ny0, x4, y4, four_ch_x, four_ch_y)
    two_ch_out = dgeom.normalize_frame(two_ch_in, dx0, dy0, nx0, ny0, x4, y4, two_ch_x, two_ch_y)
    
    return four_ch_out, two_ch_out


def sax_center(dx0, dy0, nx0, ny0, four_ch, two_ch, sax):
    frame_in, x, y = dgeom.dicom_to_arrays(sax)
    p1 = dgeom.locate_plane(four_ch)
    p2 = dgeom.locate_plane(two_ch)
    p3 = dgeom.locate_plane(sax)
    itsc = dgeom.three_plane_intersect(p1, p2, p3)
    lv_center_x, lv_center_y = dgeom.xyz_to_pixels(itsc, sax)
    
    return lv_center_x, lv_center_y


def nch_centers(dx0, dy0, nx0, ny0, four_ch, two_ch, sax_slices):
    four_ch_in, x4, y4 = dgeom.dicom_to_arrays(four_ch)
    two_ch_in, x2, y2 = dgeom.dicom_to_arrays(two_ch)
    p1 = dgeom.locate_plane(four_ch)
    p2 = dgeom.locate_plane(two_ch)
    l = []
    for sax_slice in sax_slices:
        p_sax = dgeom.locate_plane(sax_slice)
        itsc = dgeom.three_plane_intersect(p1, p2, p_sax)
        l.append(itsc)
    center = np.sum(np.array(l))
    four_ch_x, four_ch_y =  dgeom.xyz_to_pixels(center, four_ch)
    two_ch_x, two_ch_y =  dgeom.xyz_to_pixels(center, two_ch)
    
    return (four_ch_x, four_ch_y), (two_ch_x, two_ch_y)

def apply_normalization(dx0, dy0, nx0, ny0, mri_slice, lv_center_x, lv_center_y):
    frame_in, x, y = dgeom.dicom_to_arrays(mri_slice)
    frame_out = dgeom.normalize_frame(frame_in, dx0, dy0, nx0, ny0, x, y, lv_center_x, lv_center_y)
    
    return frame_out