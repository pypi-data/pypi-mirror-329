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
import CIMA.maps.MapFeatures as MF
import numpy as np
import pandas as pd
from scipy.stats import kurtosis, skew
from scipy.spatial.distance import cdist
import CIMA.utils.Vector  as Vector
from CIMA.maps import  DensityProprieties as DS
from CIMA.segments import SegmentConvex as SC
from CIMA.segments.SegmentInfoXYZ import SegmentXYZ
from CIMA.segments.SegmentGaussian import TransformBlurrer
from CIMA.segments import SegmentFeatures as SF
from CIMA.segments import SegmentSpatialFeatures as SSF
TConv=SC.TransformConvex()
from math import pi

def DistanceBetweenSegments(map_s1,map_s2,threshold1=0.5,threshold2=0.5):
    """
    Calculate the distance between the centers of mass of two map instances.

    This function computes the distance between the centers of mass of two density map objects, 
    considering only the regions above specified threshold values.

    Args:
    * map_s1: Density Map Object The first density map object.
    * map_s2: Density Map Object The second density map object.
    * threshold1 (float, optional):  The threshold value for the first map above which to compute the center of mass. Default is 0.5.
    * threshold2 (float, optional):  The threshold value for the second map above which to compute the center of mass. Default is 0.5.

    Returns:
    *  float: The distance between the centers of mass of the two map instances.
    """

    COM1=map_s1._get_com_threshold(threshold1)
    COM2=map_s2._get_com_threshold(threshold2)
    return _calc_distcom(COM1,COM2)

def _calc_distcom(com1,com2):
    com1x=float(com1[0])
    com1y=float(com1[1])
    com1z=float(com1[2])

    com2x=float(com2[0])
    com2y=float(com2[1])
    com2z=float(com2[2])

    return ((com1x - com2x)**2 + (com1y - com2y)**2 + (com1z - com2z)**2)**0.5


def getSurfaceDistance(map_s1, map_s2, threshold1=0.5, threshold2=0.5):
    """
    Calculate the distance between the surfaces of two map instances.

    This function computes the distance between the surfaces of two density map objects,
    considering only the regions above specified threshold values. If the two maps intersect,
    the distance is 0.0.

   Args:
    * map_s1: Density Map Object The first density map object.
    * map_s2: Density Map Object The second density map object.
    * threshold1 (float, optional):  The threshold value for the first map above which to define the surface. Default is 0.5.
    * threshold2 (float, optional):  The threshold value for the second map above which to define the surface. Default is 0.5.

  
    Returns:
    * float: The distance between the surfaces of the two map instances. If the maps intersect, returns 0.0.
    """
    ps1 = MF.getPointsFromMap(map_s1, threshold1)
    ps2 = MF.getPointsFromMap(map_s2, threshold2)
    s1 = SegmentXYZ(ps1)
    s2 = SegmentXYZ(ps2)
    return SSF.getMinDistance(s1, s2)


def EntanglementBetweenSegments(map_s1,map_s2,threshold1=0.5,threshold2=0.5):
    """
    Calculate Entanglement of two map instance (within the optimal contour) as define in Nir et al. PlosGen 2018.
    (Intersection over minor)

    Args:
    * map_s1: Density Map Object The first density map object.
    * map_s2: Density Map Object The second density map object.
    * threshold1 (float, optional):  The threshold value for the first map above which to define the surface. Default is 0.5.
    * threshold2 (float, optional):  The threshold value for the second map above which to define the surface. Default is 0.5.

    Returns:
    * float:  Entanglement
    """

    scorer = ScoringFunctions()


    map_s1g,map_s2g=MF._match_grid(map_s1,map_s2)


    perov = scorer._percent_overlap(map_s1g,map_s2g,threshold1,threshold2,flagsize=0)
    return  perov