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

from scipy.spatial import ConvexHull
import numpy as np

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
from CIMA.maps import  DensityProprieties as DS
from CIMA.segments import SegmentFeatures as SF
from CIMA.maps import MapSpatialFeatures as MSF
from math import pi
from scipy.spatial import cKDTree
from scipy.spatial.distance import cdist


def GetLocalisationOverlap(structure1,structure2, radius=200):
    """
    Calculates the overlap between two structures within a specified radius.

    This function computes the proportion of pairs of points, one from `structure1` 
    and the other from `structure2`, that lie within a given distance (`radius`). 
    The overlap is calculated using the `scipy.spatial.cKDTree` structure, which 
    efficiently finds neighboring points within the specified radius.

    Args:
    * structure1: The first structure, expected to have a `Getcoord` method 
                    that returns its coordinates as an array.
    * structure2: The second structure, expected to have a `Getcoord` method 
                    that returns its coordinates as an array.
    * radius (float, optional): The maximum distance within which pairs of points 
                                  are considered overlapping. Defaults to 200.

    Returns:
    * float: The proportion of point pairs, one from each structure, that lie within 
               the specified radius.

    """
    coord1= structure1.Getcoord()
    coord2= structure2.Getcoord()
    kd_tree1 = cKDTree(coord1)
    kd_tree2 = cKDTree(coord2)
    tot_len=len(coord1)*len(coord2)
    return float(kd_tree1.count_neighbors(kd_tree2, radius))/float(tot_len)
    	
def _GetLocOverlap_v2(structure1,structure2, radius=200):
    """
    Returns the proportion of pairs of points, one from structure 1 and the other from structure2,
    which lie at a distance lower than radius.
    scipy.spatial.distance.cdist function is used for the computation.
    """
    from scipy.spatial.distance import cdist
    coord1= structure1.Getcoord()
    coord2= structure2.Getcoord()
    distmx=cdist(coord1, coord2)
    #print distmx
    selected=distmx[distmx <= radius]
    tot_len=len(coord1)*len(coord2)
    #print len(distmx),len(selected),tot_len
    return len(selected)/float(tot_len)

def getMinDistance(s1, s2):
    '''
    Arguments:
    * points1, points2: two segments


    Returns:
    * the minimum distance between points from the two sets
    '''
    dists = cdist(s1.Getcoord(), s2.Getcoord(), 'euclidean')
    return dists.min()

def getMeanDistance(s1, s2):
    '''
    Arguments:
    * points1, points2: two segments


    Returns:
    * the mean distance between points from the two sets
    '''
    dists = cdist(s1.Getcoord(), s2.Getcoord(), 'euclidean')
    return dists.mean()


def getCOMDistance(s1, s2):
    '''
    Arguments:
    * points1, points2: two segments


    Returns:
    * the center of mass distance between the two sets
    '''
    dists = MSF._calc_distcom(s1.calculate_centre_of_mass(),s1.calculate_centre_of_mass())
    return dists


