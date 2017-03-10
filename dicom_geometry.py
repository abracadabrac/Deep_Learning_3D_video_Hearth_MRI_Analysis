import dicom
import scipy.interpolate as itp
import matplotlib.pyplot as plt
import numpy as np
import os

# TODO:
#   - check for X/Y MIXUPS
#   - check heart alignment
#   - mass previewer
#   - use the .xls to adjust the new frame
#   - full run
#   - normalize_frame: cropping bug


def dicom_preview(filename):
    refd = dicom.read_file(filename)
    ny = int(refd.Rows)  # SWITCHED
    nx = int(refd.Columns)
    dy = float(refd.PixelSpacing[0])
    dx = float(refd.PixelSpacing[1])
    disp_x = np.arange(0, nx) * dx
    disp_y = np.arange(0, ny) * dy
    frame = refd.pixel_array
    plt.pcolormesh(disp_x, disp_y, frame,
                   cmap=plt.get_cmap('bone'))
    plt.show()

    return


def dicom_to_arrays(filename):
    refd = dicom.read_file(filename)
    ny = int(refd.Rows)
    nx = int(refd.Columns)
    dy = float(refd.PixelSpacing[0])
    dx = float(refd.PixelSpacing[1])
    x = np.arange(0, nx) * dx
    y = np.arange(0, ny) * dy
    frame = refd.pixel_array

    return frame, x, y


def dicom_to_3d(filename):
    refd = dicom.read_file(filename)
    origin = refd.ImagePositionPatient
    cosv = refd.ImageOrientationPatient
    cosvx = cosv[0:3]
    cosvy = cosv[3:6]
    dy, dx = refd.PixelSpacing
    ex = dx * np.array(cosvx)
    ey = dy * np.array(cosvy)
    Z3d = np.zeros([refd.Rows, refd.Columns])
    X3d = np.zeros([refd.Rows, refd.Columns])
    Y3d = np.zeros([refd.Rows, refd.Columns])
    for i in range(0, refd.Rows):
        for j in range(0, refd.Columns):
            Z3d[i, j] = origin[2] + i * ey[2] + j * ex[2]
            X3d[i, j] = origin[0] + i * ey[0] + j * ex[0]
            Y3d[i, j] = origin[1] + i * ey[1] + j * ex[1]

#    X3d = origin[0] + ex[0] * np.arange(0, refd.Columns)
#    Y3d = origin[1] + ey[1] * np.arange(0, refd.Rows)
#    X3d, Y3d = np.meshgrid(x3d, y3d)

    return Z3d, X3d, Y3d


def normalize_frame(frame, dx0, dy0, nx0, ny0, x, y, offx, offy):
    ny, nx = frame.shape  # SWITCHED
    dx, dy = (x[1], y[1])
    
    ox = int(np.round(offx * dx / dx0 - nx0 / 2))
    oy = int(np.round(offy * dy / dy0 - ny0 / 2))
    
    x0 = np.arange(0.0, x[-1], dx0)
    y0 = np.arange(0.0, y[-1], dy0)
    interp_function = itp.RectBivariateSpline(y, x, frame)
    z0 = interp_function(y0, x0)
    
    nl, nc = z0.shape
    
    if ox < 0:
        ox = 0
    
    if ox + nx0 > nc:
        ox = nc - nx0
        
    if oy < 0:
        oy = 0
    
    if oy + ny0 > nl:
        oy = nl - ny0 

    return z0[oy:(oy + ny0), ox:(ox + nx0)]


def locate_plane(filename):
    refd = dicom.read_file(filename)
    cos_v = refd.ImageOrientationPatient
    pos_v = refd.ImagePositionPatient
    norm_v = np.cross(cos_v[0:3], cos_v[3:6])
    bias = np.dot(norm_v, pos_v)

    return (norm_v, bias)


def three_plane_intersect(p1, p2, p3):
    n1, b1 = p1
    n2, b2 = p2
    n3, b3 = p3
    n4 = np.cross(n2, n3)
    res = b1 * n4 + b2 * (np.cross(n3, n1)) + b3 * (np.cross(n1, n2))
    res = res / np.dot(n1, n4)

    return res


def xyz_to_pixels(v, filename):
    refd = dicom.read_file(filename)
    cos_v = refd.ImageOrientationPatient
    pos_v = refd.ImagePositionPatient
    dx = float(refd.PixelSpacing[1])  # SWITCHED COLUMN AND LINE SPACING
    dy = float(refd.PixelSpacing[0])
    ux = cos_v[0:3]  # CHECK FOR X/Y MIXUPS
    uy = cos_v[3:6]
    idx = np.round(np.dot(ux, v - pos_v) / dx)
    idy = np.round(np.dot(uy, v - pos_v) / dy)

    return (int(idx), int(idy))
