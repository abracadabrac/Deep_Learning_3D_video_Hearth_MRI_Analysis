import dicom
import scipy.interpolate as itp
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy import ndimage

# When applying "dilate", adjust the labels accordingly
# Look up scipy -> ndimage.interpolation.imrotate (!!! RESHAPE = FALSE)


def dilate(frame_in, factor):
    nrows, ncols = frame_in.shape
    x = np.arange(0, ncols)
    y = np.arange(0, nrows)
    xd = x / factor
    yd = y / factor
    interp_function = itp.RectBivariateSpline(y, x, frame_in)
    frame_out = interp_function(yd, xd)
    nrows_out, ncols_out = frame_out.shape
    r = round((nrows_out - nrows) / 2)
    c = round((ncols_out - ncols) / 2)

    return frame_out[r:(r + nrows), c:(c + ncols)]


def skew_x(frame_in, delta):
    m = np.array([[1, delta], [0, 1]])
    frame_out = ndimage.interpolation.affine_transform(frame_in, m)

    return frame_out


def skew_y(frame_in, delta):
    m = np.array([[1, 0], [delta, 1]])
    frame_out = ndimage.interpolation.affine_transform(frame_in, m)

    return frame_out


def adjust_intensity(frame_in, imin, imax):
    frame_out = frame_in
    frame_out[frame_out < imin] = imin
    frame_out[frame_out > imax] = imax
    norm_k = 256 / (imax - imin)

    return norm_k * (frame_out - imin)


def tensor_rolling(stack_in, n_roll):
    stack_out = np.concatenate(
        (stack_in[:, :, n_roll:], stack_in[0, n_roll - 1]), axis=2)

    return stack_out

def center_mark(nrows, ncols, center_r, center_c):
    res = np.zeros([nrows, ncols])
    res[center_r, center_c] = 1
    
    return res


def locate_mark(mark_in):
    center_r, center_c = np.unravel_index(mark_in.argmax(), mark_in.shape)

    return center_r, center_c
