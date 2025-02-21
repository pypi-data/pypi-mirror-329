#===============================================================================
#     This file is part of CIMA.
#
#     CIMA is a software designed to help the user in the manipulation
#     and analyses of genomic super resolution localisation data.
#
#      Copyright  2019-2023
#
#                Authors: Irene Farabella
#
#
#
#===============================================================================

from numpy import  array, int32, float32, zeros, real, argwhere, diag, histogram, dot, matrix, amin, arange,\
                   indices, ravel, all as all_points, delete, transpose, searchsorted, newaxis, where, meshgrid,\
                   ma, sum as numsum,median,sqrt as srt, digitize, nonzero, floor, ceil, amax, mean as npmean,\
                   std as npstd, square as npsquare, tanh as np_tanh,set_printoptions

import glob
from CIMA.maps.MapParser import MapParser
from CIMA.maps.VQ import *
from CIMA.maps.ScoringFunctions import ScoringFunctions
import numpy as np
from scipy.stats import kurtosis, skew
import CIMA.utils.Vector  as Vector


def Hist_density(map_target):
    """
    Calculate various statistical properties of the density map.

    Args:
    * map_target: The target map object.

    Returns:
    * A tuple containing:
            - ave: The average density.
            - sigma: The standard deviation of the density.
            - kurt: The kurtosis of the density distribution.
            - sk: The skewness of the density distribution.
            - p25: The 25th percentile of the density.
            - p50: The 50th percentile (median) of the density.
            - p75: The 75th percentile of the density.
            - p90: The 90th percentile of the density.
    """
    ave = npmean(map_target.fullMap)
    sigma = npstd(map_target.fullMap)
    a = map_target.fullMap.flatten()
    kurt = kurtosis(a)
    sk = skew(a)
    p25 = np.percentile(map_target.fullMap, 25)
    p50 = np.percentile(map_target.fullMap, 50)
    p75 = np.percentile(map_target.fullMap, 75)
    p90 = np.percentile(map_target.fullMap, 90)

    return ave, sigma, kurt, sk, p25, p50, p75, p90


def calculate_map_threshold_SR(map_target, factor=1.5):
    """
    Calculate the threshold for the density map based on a noise factor.

    Args:
    * map_target: The target map object.
    * factor: The noise level in sigma (default is 1.5).

    Returns:
    * The calculated volume threshold.
    """
    try:
        peak, ave, sigma = map_target._peak_density()
        vol_threshold = float(ave) + (factor * float(sigma))
    except:
        amean = map_target.mean()
        rms = map_target.std()
        vol_threshold = float(amean) + (factor * float(rms))
    
    # Ensure the threshold is not below 0.5
    if vol_threshold < 0.5:
        vol_threshold = 0.5
    
    return vol_threshold



def CropBox(map_target, contour):
    """
    Crop the map to the bounding box of the region with density above the given contour level.

    Args:
    * map_target: The target map object.
    * contour: The density contour level.

    Returns:
    * The cropped map object.
    """
    level = contour
    sigma = map_target.fullMap.std()
    sigma = abs(sigma)
    try:
        map_target.fullMap = map_target._label_patches(level - 0.02 * sigma)[0]
    except:
        map_target._map_binary_opening(level - 0.02 * sigma)
    map_target._crop_box(level, 0.5)
    return map_target

def MaskCountour(map_target, contour):
    """
    Mask the map at the given contour level.

    Args:
    *  map_target: The target map object.
    * contour: The density contour level.

    Returns:
    * The masked map object.
    """
    level = contour
    map_target._mask_contour(level, 0.5)
    return map_target

def get_contour_points(map_target, contour):
    """
    Retrieve all points with a density greater than the given contour level.

    Args:
    * map_target: The target map object.
    * contour: The density contour level.

    Returns:
    * An array of 3-tuple (indices of the voxels in x, y, z format).
    """
    sig_points = []
    # Create a boolean mask where the density is greater than the contour level
    boo = map_target.fullMap > float(contour)
    
    # Iterate through the entire map to find points above the contour level
    for z in range(map_target.z_size()):
        for y in range(map_target.y_size()):
            for x in range(map_target.x_size()):
                if boo[z][y][x]:
                    # Append the coordinates of the point to the list
                    sig_points.append(array([z, y, x]))
    
    # Return the array of significant points
    return array([sig_points[0], sig_points[1], sig_points[2]])


def get_binarized_points(map_target, value):
    """
    Retrieve all points with a density greater than or equal to the specified value.

    Args:
    * map_target: The target map object.
    * value: The density threshold value.

    Returns:
    *  An array of 3-tuple (indices of the voxels in x, y, z format).
    """
    sig_points = []
    # Create a boolean mask where the density is greater than or equal to the specified value
    boo = map_target.fullMap >= int(value)
    
    # Iterate through the entire map to find points above the specified value
    for z in range(map_target.z_size()):
        for y in range(map_target.y_size()):
            for x in range(map_target.x_size()):
                if boo[z][y][x]:
                    # Append the coordinates of the point to the list
                    sig_points.append(array([z, y, x]))
    
    # Return the array of significant points
    return array(sig_points)


def get_index_points(map_target):
    """
    Retrieve all points with a density greater than zero.

    Args:
     * map_target: The target map object.

    Returns:
    * An array of 3-tuple (indices of the voxels in x, y, z format).
    """
    sig_points = []
    # Get the full density map
    boo = map_target.fullMap
    
    # Iterate through the entire map to find points with density greater than zero
    for z in range(map_target.z_size()):
        for y in range(map_target.y_size()):
            for x in range(map_target.x_size()):
                if boo[z][y][x]:
                    # Append the coordinates of the point to the list
                    sig_points.append(array([z, y, x]))
    
    # Return the array of significant points
    return array(sig_points)


def _get_vectors_binirized(map_target):
    """
    Retrieve all non-zero density points in the form of Vector instances.

    Args:
    * map_target: The target map object.

    Returns:
    * An array of 3-tuple (indices of the voxels in x, y, z format).
    """
    a = []
    # Create a boolean mask where the density is greater than or equal to 1
    boo = map_target.fullMap >= 1.0
    
    # Iterate through the entire map to find points with density greater than or equal to 1
    for z in range(len(map_target.fullMap)):
        for y in range(len(map_target.fullMap[z])):
            for x in range(len(map_target.fullMap[z][y])):
                if boo[z][y][x]:
                    # Append the coordinates of the point to the list as Vector instances
                    a.append((Vector.Vector((x * map_target.apix) + map_target.origin[0], 
                                            (y * map_target.apix) + map_target.origin[1], 
                                            (z * map_target.apix) + map_target.origin[2])))
    
    # Return the array of significant points
    return array(a)

def _get_vectors_below_contour(map_target, contour):
    """
    Retrieve all density points below the given contour level in the form of Vector instances.

    Args:
    * map_target: The target map object.
    * contour: The density contour level.

    Returns:
    *  An array of 4-tuple (Vector instance of the voxel coordinates in x, y, z format and the density value).
    """
    a = []
    # Create a boolean mask where the density is less than the specified contour level
    boo = map_target.fullMap < float(contour)
    
    # Iterate through the entire map to find points below the contour level
    for z in range(len(map_target.fullMap)):
        for y in range(len(map_target.fullMap[z])):
            for x in range(len(map_target.fullMap[z][y])):
                if boo[z][y][x]:
                    # Append the coordinates of the point as Vector instances and the density value to the list
                    a.append((Vector.Vector((x * map_target.apix) + map_target.origin[0], 
                                            (y * map_target.apix) + map_target.origin[1], 
                                            (z * map_target.apix) + map_target.origin[2]), 
                                map_target.fullMap[z][y][x]))
    
    # Return the array of significant points
    return array(a)
