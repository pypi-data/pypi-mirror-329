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
import pandas as pd
from scipy.stats import kurtosis, skew
from scipy.spatial.distance import cdist
import CIMA.utils.Vector  as Vector
from CIMA.maps import  DensityProprieties as DS
from CIMA.segments import SegmentConvex as SC
from CIMA.segments.SegmentGaussian import TransformBlurrer
from CIMA.segments import SegmentFeatures as SF
TConv=SC.TransformConvex()
from math import pi


def GetVolume_abovecontour(map, threshold=0.5):
    """
    Calculate the volume of a map instance above a specified threshold.

    Arguments:
    * *map*: The density map object.
    * *threshold*: The threshold value above which to compute the volume.

    Return:
    *  float: Volume of the map instance above the specified threshold.
    """
    map_voxel_centers_above_threshold = getPointsFromMap(map, threshold)
    vol = float(len(map_voxel_centers_above_threshold)) * ((map.apix) ** 3)
    return vol


def GetArea_abovecontour(map, threshold=0.5):
    """
    Calculate the surface area of a map instance above a specified contour threshold.
   
    Arguments:
    * map (MapInstance): The map instance to analyze.
    * threshold (float, optional): The contour threshold value. Defaults to 0.5.
    
    Returns:
    * float: The surface area of the map instance above the specified contour threshold.
    """
    from skimage import measure

    masked=DS.MaskCountour(map.copy(),threshold)
    A=map.getMap()

	#verts, faces, normals, values = measure.marching_cubes_lewiner(A ,spacing=(map.apix,map.apix,map.apix),level= c,allow_degenerate=True)#,method='lewiner')
    verts, faces, normals, values=measure.marching_cubes(A, spacing=(map.apix,map.apix,map.apix),level= threshold,allow_degenerate=True,method='lewiner')
    area= measure.mesh_surface_area(verts, faces)
    return area


def GetVolume_equivalent_diameter(volume):
    """
    Calculate volume equivalent diameter.

    Arguments:
    * *Volume*

    Return:
    * float, Volume-equivalent diameter.
    """
    return np.cbrt(6 * volume/np.pi)

def GetArea_equivalent_diameter(surface_area):
    """
    Calculate surfacearea-equivalent diameter.

    Arguments:
    * surface_area

    Return:
    * float, Surface area-equivalent diameter.
    """
    return np.sqrt(surface_area/np.pi)



# volume sphere
#(4/3)*pi*(R^3)
#area sphere
#4*pi*(R^2)
#compactenss of a spehere
#C = (area3)/(volume2) =36pi

# discrete compactness Cd

#This descriptor takes into account the volume of the object (number of voxels) and the area of the enclosing surface, i.e. the number of voxel faces which are not directly in contact with another voxel
# (n-(a/6))/(n - n ** (2 / 3))
#where n is the total number of voxels and A is the area of the enclosing surface.

def GetSphericity(map, threshold=0.5):
    """
   Calculate the sphericity of a map instance above its optimal contour.

    Sphericity is a measure of the degree to which a particle approximates the shape of a sphere, and is independent of its size.
    Any particle which is not a sphere will have sphericity less than 1.

    Args:
    * map: The map instance to calculate sphericity for.
    * threshold (float, optional): The threshold value for the contour. Defaults to 0.5.

    Returns:
    * float: The sphericity of the map instance above its optimal contour.

    References:
        Wadell, H. (1935). Volume, Shape, and Roundness of Rock Particles. The Journal of Geology, 43(3), 250–280.
    """
    vol=GetVolume_abovecontour(map, threshold=threshold)
    area=GetArea_abovecontour(map, threshold=threshold)
    a=pi**(1/3)
    b=((6*vol)**(2/3))
    c=area
    #sphery=(pi**(1/3)*((6*vol)**(2/3)))/area
    sphery=(a*b)/c
    return sphery

def GetSphericity_bribiesca(map, threshold=0.5, verbose=False):
   """    
   Calculate the sphericity of a map instance above its optimal contour.

    It is a measure of discrete compactness for rigid solids composed of voxels. This 
    method requires more computation than the classical measure but has two 
    important advantages: it varies linearly, which may be useful in 3D shape 
    classification, and it depends significantly on the sum of the contact 
    surface areas of the face-connected voxels of solids, providing a more 
    robust measure for noisy enclosing surfaces.

    Args:
    * map (object): The map instance containing the fullMap attribute.
    *  threshold (float, optional): The threshold value to determine the contour. Defaults to 0.5.
    * verbose (bool, optional): If True, prints intermediate values for 
            debugging purposes. Defaults to False.

    Returns:
    * float: The sphericity value of the map instance.

    References:
        BRIBIESCA Computers and Mathematics with Applications 40 (2000)
  
    """
   X, Y, Z = np.where(map.fullMap > threshold)
   assert X.shape[0] == Y.shape[0]
   assert Y.shape[0] == Z.shape[0]
   n = float(X.shape[0])
   A = _findArea(X, Y, Z)
   num = (n - (A / 6.))
   den = (n - n ** (2. / 3.))
   if(verbose):
        print('A: ', A)
        print('shape prod: ', np.array(map.fullMap.shape).prod())
        print('n: ', n )
        print('num: ', num)
        print('den: ', den)
    # c = (n - (A / 6.)) / (n - n ** (2. / 3.))
   c = num/den
   return c

def _findArea(X, Y, Z):
    """
    Calculate the surface area of a 3D object represented by its voxel coordinates.

    This function computes the surface area of a 3D object by checking the presence of neighboring voxels.
    If a neighboring voxel is not present, it contributes to the surface area.

    Arguments:
    * X (numpy.ndarray): Array of x-coordinates of the voxels.
    * Y (numpy.ndarray): Array of y-coordinates of the voxels.
    * Z (numpy.ndarray): Array of z-coordinates of the voxels.

    Returns:
    * int: The surface area of the 3D object.
    """
    voxels = set()
    listXYZ = list(zip(X, Y, Z))
    for x, y, z in listXYZ:
        voxels.add((x, y, z))

    neighbours = [np.array([-1, 0, 0]), np.array([1, 0, 0]),
                  np.array([0, -1, 0]), np.array([0, 1, 0]),
                  np.array([0, 0, -1]), np.array([0, 0, 1])]
    A = 0
    # For each voxel
    for x, y, z in listXYZ:
        # Check its 6 possible neighbours
        vox = np.asarray([x, y, z], dtype=np.float32)
        for neigh in neighbours:
            vNeigh = vox + neigh
            # If neighbour is there, contribute 0 area
            # Otherwise, contribute 1
            A += 0 if tuple(vNeigh) in voxels else 1
    return A


def GetEllipticity_abovecontour(map,threshold=0.5,verbose=False,full=False):
    """
    Calculate Ellipticity of a map instance above its optimal contour.
    Both ellipticity and eccentricity are measures of how elongated an object is based on based on the semi-major axis and semi-minor axis.

    Arguments:
    * *map* Denisty Map Object
    * *threshold* value above which to compute ellipticity
    * *verbose* True, print out calculations
    * *full* integer, normalised scores

    Return:
    * values, Ellipticity of a map instance above its optimal contour.
    """
    	#coord= []
    coord2=getPointsFromMap(map,threshold)
    coord=[]
    for i in coord2:
        coord.append([i[0],i[1],i[2]])
    coord=np.array(coord)
    eval1, eval2, eval3,axis3, axis2, axis1=SF._principal_axes(coord)
    if verbose:
        if full:
            score= (eval1-eval2)/eval1
            return score, eval1, eval2, eval3,axis3, axis2, axis1
        else:
            return (eval1/eval2), eval1, eval2, eval3,axis3, axis2, axis1
    else:
        if full:
            score= (eval1-eval2)/eval1
            return score
        else:
            return (eval1/eval2)#, eval1, eval2, eval3,axis3, axis2, axis1
        
##https://astronomy.stackexchange.com/questions/43574/what-is-the-difference-between-the-two-terms-named-eccentricity-and-elliptici

def GetEccenticity_abovecontour(map,threshold=0.5,verbose=False,full=False):
    """
    Calculate Eccenticity of a map instance above its optimal contour.
    Both ellipticity and eccentricity are measures of how elongated an object is based on based on the semi-major axis and semi-minor axis.

    Arguments:
    * *map* Denisty Map Object
    * *threshold* value above which to compute ellipticity
    * *verbose* True, print out calculations
    * *full* integer, normalised scores
   
   Return:
   * values, Eccenticity of a map instance above its optimal contour.
    """
    coord = _GetCoordMap_abovecountour(map,threshold)
    eval1, eval2, eval3,axis3, axis2, axis1 =SF._principal_axes(coord)
    if verbose:
        if full:
            score=np.sqrt(1-((eval2**2)/(eval1**2)))
            return score, eval1, eval2, eval3,axis3, axis2, axis1
        else:
            return (eval2/eval1), eval1, eval2, eval3,axis3, axis2, axis1
    else:
        if full:
            score=np.sqrt(1-((eval2**2)/(eval1**2)))
            return score
        else:
            return (eval2/eval1)#, eval1, eval2, eval3,axis3, axis2, axis1


def _match_grid(map_s1,map_s2):
    """
    performs matching of two maps (map_s1 and map_s2) based on a common alignment box.
    The function takes two density maps (map_s1 and map_s2), as well as two intensity thresholds (c1 and c2) as input.

    Return
        map_s1,map_s2 with new grid matched
    """
  # DETERMINE A COMMON ALIGNMENT BOX : fill minvalue for extra voxel pads
    spacing = map_s2.apix
    if map_s2.apix < map_s1.apix: spacing = map_s1.apix
    grid_shape, new_ori = map_s1._alignment_box(map_s2,spacing)
    # INTERPOLATE TO NEW GRID
    try: emmap_1 = map_s1._interpolate_to_grid1(grid_shape,spacing,new_ori)
    except: emmap_1 = map_s1._interpolate_to_grid(grid_shape,spacing,new_ori)
    # try: c1 = emmap_1._find_level(np.sum(map_s1.fullMap>c1)*(map_s1.apix**3))
    # except: pass
    try: emmap_2 = map_s2._interpolate_to_grid1(grid_shape,spacing,new_ori)
    except: emmap_2 = map_s2._interpolate_to_grid(grid_shape,spacing,new_ori)
    # try: c2 = emmap_2._find_level(np.sum(map_s2.fullMap>c2)*(map_s2.apix**3))
    # except: pass
    return emmap_1, emmap_2



def GetSparseness(map,strobj,threshold=0.5):
    """
    The ratio between the ellipsoid volume and the object volume

    
    Arguments:
    * *map* Denisty Map Object
    * *strobj* Structure Object
    * *threshold* the threshold above which to compute sparseness

    Return:
    * values, Sparseness
    """
    centre, radii, ellipVol=strobj.GetMVEE()
    vol=GetVolume_abovecontour(map,threshold=threshold)
    spareness=ellipVol/vol
    return spareness

def getClassicalCompactness(segment_map, threshold=0.5):
    '''
    Returns Compactness defined as surface_area^3/volume^2

    BRIBIESCA Computers and Mathematics with Applications 40 (2000).
    '''
    area = GetArea_abovecontour(segment_map, threshold)
    vol = GetVolume_abovecontour(segment_map, threshold)
    return area**3/vol**2

def getDiscreteCompactness(segment_map, threshold=0.5):
    '''
    Paper: Bribiesca 2008, An easy measure of compactness for 2D and 3D shapes
    '''
    voxel_face_area = segment_map.apix**2
    voxel_vol =segment_map.apix**3
    area = GetArea_abovecontour(segment_map, threshold)
    n = (segment_map.fullMap>threshold).sum()
    num = (6*voxel_face_area*n - area)/2
    den = (6*voxel_face_area*n - 6*((n*voxel_vol)**(2/3)))/2
    # den = 3*(n-n**(2/3))
    # return (n-(area/6))/(n-n**(2/3))
    return num/den

def getPointsFromMap(map, threshold=0.0):
    '''
    Returns a numpy array with each row represening a cell of map with value > threshold
    '''
    wh = np.where(map.fullMap>threshold)
    return map.origin + np.stack(wh, axis=0).T[:,[2,1,0]]*map.apix + np.array([map.apix/2]*3)

def getMapRelativePointsFromMap(map, threshold=0.0):
    '''
    Returns a numpy array with each row represening a cell of map with value > threshold
    '''
    wh = np.where(map.fullMap>threshold)
    return np.stack(wh, axis=0).T[:,[2,1,0]]

def _arePointsInConvexHull(ch_points, query_points):
    '''
    Computes the convex hull of ch_points and return a boolean numpy array indicating which query_points are inside it
    '''
    from scipy.spatial import Delaunay
    dlny = Delaunay(ch_points)
    inside = dlny.find_simplex(query_points) > -1
    return inside

def getConvexMap(input_map, threshold):
    """
    Generate a convex hull map from the input map at a specified threshold.

    This function creates a new map representing the convex hull of the input map at the given threshold.
    The returned map has values 1.0 inside the convex hull and 0.0 everywhere else.

    Args:
    * input_map (MapInstance): The input density map object.
    *  threshold (float): The threshold value to determine the contour.

    Returns:
    * MapInstance: A new map instance representing the convex hull of the input map.
    """
    m2 = input_map.copy()
    m2.fullMap = np.zeros(m2.fullMap.shape)
    ps_signal = getPointsFromMap(input_map, threshold)
    ps_all = getPointsFromMap(m2, m2.fullMap.min() - 1)
    which_inside = _arePointsInConvexHull(ps_signal, ps_all)
    m2.fullMap[which_inside.reshape(m2.fullMap.shape)] = 1
    return m2

def getConvexHullVolume(coords):
    """
    Calculate the volume of the convex hull for a given set of coordinates.

    Arguments:
    * coords (numpy.ndarray): A 2D array of shape (n, 3) representing the coordinates of the points.

    Returns:
    * float: The volume of the convex hull enclosing the given points.
    """
    cv = ConvexHull(coords)
    return cv.volume

def getSolidity(segment_map, threshold=0.5):
    """
    Calculate the solidity of a map instance above a specified threshold.

    Solidity is defined as the ratio of the volume of the map instance to the volume of its convex hull.
    The value of this measure is between 0 and 1.

    Arguments:
    * segment_map (MapInstance): The map instance to analyze.
    * threshold (float, optional): The threshold value above which to compute the solidity. Defaults to 0.5.

    Returns:
    * float: The solidity of the map instance above the specified threshold.

    References:
        Liu, S., Cai, W., Song, Y., Pujol, S., Kikinis, R., Wen, L., & Feng, D. D. (2013, July). 
        Localized sparse code gradient in Alzheimer's disease staging. In 2013 35th Annual 
        International Conference of the IEEE Engineering in Medicine and Biology Society (EMBC) 
        (pp. 5398-5401). IEEE.
    """
    seg_vol = GetVolume_abovecontour(segment_map, threshold=threshold)
    points = getPointsFromMap(segment_map, threshold=threshold)
    ch_vol = getConvexHullVolume(points)
    return np.clip(seg_vol / ch_vol, 0.0, 1.0)

def getHolelessSolidity(segment_map, threshold=0.5):
    """
    Calculate the solidity of a map instance above a specified threshold, with holes filled.

    Solidity is defined as the ratio of the volume of the map instance (with holes filled) to the volume of its convex hull.
    The value of this measure is between 0 and 1.

    Arguments:
    * segment_map (MapInstance): The map instance to analyze.
    * threshold (float, optional): The threshold value above which to compute the solidity. Defaults to 0.5.

    Returns:
    * float: The solidity of the map instance above the specified threshold, with holes filled.
    """
    # Get the binary map at the specified threshold
    bin_map = segment_map.getBinaryMap(threshold)
    # Fill the holes in the binary map
    filled_binary_map = bin_map.getFilledMap()
    # Calculate the volume of the filled binary map above the threshold
    filled_seg_vol = GetVolume_abovecontour(filled_binary_map, threshold=0.5)
    # Get the points from the original segment map above the threshold
    points = getPointsFromMap(segment_map, threshold=threshold)
    # Calculate the volume of the convex hull enclosing the points
    ch_vol = getConvexHullVolume(points)
    # Return the ratio of the filled segment volume to the convex hull volume, clipped between 0 and 1
    return np.clip(filled_seg_vol / ch_vol, 0.0, 1.0)

def getConvexity(segment_map=None, threshold=0.5):
    """
    Calculate the convexity of a segment based on its density map.

    Convexity is computed as the ratio of the area above the threshold in the convex map 
    to the area above the threshold in the original segment map. This method is primarily 
    designed for 2D shapes and may not yield accurate results for 3D shapes.

    Args:
    * segment_map (numpy.ndarray, optional): The density map of the segment. Defaults to None.
    * threshold (float, optional): The density level at which the feature is computed. Defaults to 0.5.

    Returns:
    * float: The convexity value, which is the ratio of the convex hull area to the segment area.

    References:
        Liu, S., Cai, W., Song, Y., Pujol, S., Kikinis, R., Wen, L., & Feng, D. D. (2013, July). 
        Localized sparse code gradient in Alzheimer's disease staging. In 2013 35th Annual 
        International Conference of the IEEE Engineering in Medicine and Biology Society (EMBC) 
        (pp. 5398-5401). IEEE.
    """
    m_conv = getConvexMap(segment_map, threshold)
    seg_area = GetArea_abovecontour(segment_map, threshold=threshold)
    ch_area = GetArea_abovecontour(m_conv, threshold=0.5)
    return ch_area/seg_area



#ADD Aspect Ratio AR and Chunkiness Ch
# AR=lengh/with CH=with/lengh
#SIMILARITY:
# A 3D Discrete Fourier Transform (3D-DFT) as as a shape descriptor (Vranic and Saupe (2001)).the 3D-DFT was applied to a voxelized 3D model to produce feature vectors which were later used to search in a database for similar objects