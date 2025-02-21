
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
from numpy import array,  zeros, real,sqrt,exp, mgrid, transpose,median, mean as npmean
from scipy.fftpack import fftn, ifftn
from scipy.ndimage import fourier_gaussian,gaussian_filter,uniform_filter
from CIMA.maps.EMMap import Map
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from CIMA.segments.SegmentInfo import Segment

class TransformBlurrer:
    """ 
    
    A class to generate a density map from a Segment instance.
    Note that: segment classes represent coordinates as x,y,z.
    Map class instead represents them as z,y,x.
    
    """

    def __init__(self):
        pass
    
    @staticmethod
    def SR_gaussian_blur(segment, resolution , sigma_coeff=1., mode="unit",normalise=True,filename="None", verbose=False):
        
        """
        
        Returns a Map instance based on a Gaussian blurring of a segment.
        The convolution  is done in reciprocal space.
        
        Arguments:
        * *Segment*
                array of Localisation objects
        * *Mean precision*
            	integer
        * *Mode*
            	unit, in which each localisation as an arbitrary size of 1 as in Nir et al., PloS Gen 2018
        """

        fullMapempty=TransformBlurrer.SRMap(segment, resolution, resolution=resolution)
        if(verbose):
            sns.heatmap(fullMapempty[fullMapempty.fullMap.shape[0]//2,:,:])
            plt.show()
        newMap = TransformBlurrer.getMapWithAttributeOverlayed(fullMapempty, segment, attribute=mode)
        if(verbose):
            sns.heatmap(newMap.fullMap[newMap.fullMap.shape[0]//2,:,:])
            plt.show()
        fou_map = fourier_gaussian(fftn(newMap.fullMap), sigma_coeff)
        newMap.fullMap = real(ifftn(fou_map))
        if(verbose):
            sns.heatmap(newMap.fullMap[newMap.fullMap.shape[0]//2,:,:])
            plt.show()
        newMapB = newMap.resample_by_box_size(fullMapempty.box_size())
        if(verbose):
            sns.heatmap(newMapB.fullMap[newMapB.fullMap.shape[0]//2,:,:])
            plt.show()
        if normalise:
            newMapB = newMapB.normalise()
        if(verbose):
            sns.heatmap(newMapB.fullMap[newMapB.fullMap.shape[0]//2,:,:])
            plt.show()
        newMapB.filename=filename
        newMapB.update_header
        return newMapB

    @staticmethod
    def SRMap(struct, apix, resolution=None,filename="None"):
        
        """
        
        Returns an Map instance sized and centred based on the segment.
        
        Arguments:
        
        * *apix*
               Angstroms per pixel for the Map to be outputted.
        * *resolution*
                Target resolution of the outputted map.
        * *sigma_coeff*
               Sigma width of the Gaussian used to blur the atomic structure.
        * *filename* 
               output name of the map file.
               
           """

        # Build empty template map based on the size of the segmentein and the resolution.

        
        #edge = int(2*resolution/apix)+4
        if not resolution is None: edge = int(2*resolution/float(apix))+10
        else: edge = 10
        extr=struct.get_extreme_values()
        x_size = int((extr[1]-extr[0])/apix)+edge
        y_size = int((extr[3]-extr[2])/apix)+edge
        z_size = int((extr[5]-extr[4])/apix)+edge
        half_x = max(struct.CoM.x - extr[0],extr[1]-struct.CoM.x)
        if half_x < (apix*x_size/2.0): half_x = apix*x_size/2.0
        x_origin = struct.CoM.x - half_x - edge*apix
        x_size = int(half_x*2.0/apix + 2*edge)
        half_y = max(struct.CoM.y - extr[2],extr[3]-struct.CoM.y)
        if half_y < (apix*y_size/2.0): half_y = (apix*y_size/2.0)
        y_origin = struct.CoM.y - half_y - edge*apix
        y_size = int(half_y*2.0/apix+ 2*edge)
        half_z = max(struct.CoM.z - extr[4],extr[5]-struct.CoM.z)
        if half_z < (apix*z_size/2.0): half_z = apix*z_size/2.0
        z_origin = struct.CoM.z - half_z - edge*apix
        z_size = int(half_z*2.0/apix+ 2*edge)
 
        newMap = zeros((z_size, y_size, x_size))
        #print "map create"
        fullMap = Map(newMap, [x_origin, y_origin, z_origin], apix,"d")
        return fullMap
    
    @staticmethod
    def getCoordsRelativeToMap(densMap, coords) -> np.array:
        '''
        Returns coords converted to the densMap space.
        It scales and integerizes them appropriately.
        Moreover it rotates the axes, so that the final representation is z,y,x.
        '''
        origin = np.array(densMap.origin)
        apix = densMap.apix
        scaled_coords = np.round((coords-origin)/apix, 0).astype('int')
        rotated_coords = scaled_coords[:,[2,1,0]]
        return rotated_coords
    
    @staticmethod
    def getCoordsRelativeToMapWithOriginalAxesOrder(densMap, coords) -> np.array:
        '''
        Returns coords converted to the densMap space, but keepint the order of axes as x,y,z.
        It scales and integerizes them appropriately.
        Same as getCoordsRelativeToMap but without rotating axes.
        '''
        origin = np.array(densMap.origin)
        apix = densMap.apix
        scaled_coords = np.round((coords-origin)/apix, 0).astype('int')
        return scaled_coords
    
    @staticmethod
    def areCoordsInMapBox(densMap, map_relative_coords) -> np.array :
        '''
        Arguments:
        * *map_relative_coords*: np.array representing coords as z,y,x in the map space.
        
        Returns a np.array of booleans specifying whether map_relative_coords are inside densMap boundaries.
        '''
        box_size = densMap.box_size()
        return ( \
        (map_relative_coords[:,0] >=0)*(map_relative_coords[:,0] <box_size[0])* \
        (map_relative_coords[:,1] >=0)*(map_relative_coords[:,1] <box_size[1])* \
        (map_relative_coords[:,2] >=0)*(map_relative_coords[:,2] <box_size[2])).astype('bool')
    
    @staticmethod
    def getMapWithAttributeOverlayed(densMap, segment: Segment, attribute) -> Map :
        '''
        Arguments:
        * *densMap*: the map to overlay,
        * *segment*: the segment of which the localizations are used to overlay,
        * *attribute*: str, number or callable.
                If str must be one of the predefined, each of which will define a behaviour.
                If number it will be directly used as overlay value.
                If callable will be called on each row to produce the overlay value.
        Return:
        * a new densMap equal to the input one but with the overlay
        '''
        densMap = densMap.copy()

        # Assign to attribute the right value or callable
        if(type(attribute)==str):
            # TODO: define attribute='photon'
            if(attribute in ['acc','accuracy']):
                maxacc=segment.GetMaxAccuracy()
                attribute = lambda df: 10*(maxacc-df['accuracy'])
            elif(attribute == 'unit'):
                attribute = 1.
            elif(attribute == 'loglike'):
                attribute = lambda df: -1*df['loglike']
            elif(attribute in ['llr','llratio']):
                attribute = lambda df: df['llr']
            else:
                raise ValueError('No predefined behavior for this attribute string')
        
        seg_coords = segment.Getcoord()
        map_relative_coords = TransformBlurrer.getCoordsRelativeToMap(densMap, seg_coords)
        are_in_mapbox = TransformBlurrer.areCoordsInMapBox(densMap, map_relative_coords)
        if(are_in_mapbox.sum()>0):
            selected_coords = map_relative_coords[are_in_mapbox]

            # attribute is a number
            if(type(attribute)==int or type(attribute)==float):
                attribute_values = np.full(are_in_mapbox.sum(), attribute)
            
            # attribute is a function
            if(callable(attribute)):
                attribute_values = attribute(segment.atomList.loc[are_in_mapbox, :])
                assert attribute_values.shape == (are_in_mapbox.sum(),)
            
            selected_attributes = attribute_values
            df = pd.DataFrame(selected_coords, columns=['z','y','x'])
            df['attribute'] = selected_attributes
            # sum attributes when there are duplicate coordinates (because numpy batch increment skips duplicates)
            df = df.groupby(['z','y','x']).agg({'attribute':'sum'}).reset_index()
            densMap.fullMap[df['z'],df['y'],df['x']] += df['attribute']
        return densMap