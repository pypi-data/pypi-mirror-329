
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

from numpy import ndarray,array,append,matrix
from math import pi
from random import randrange
import CIMA.utils.Vector as Vector
import numpy as np
import pandas as pd
from CIMA.segments.SegmentInfoXYZ import SegmentXYZ


import sys



class SegmentH5(SegmentXYZ):
    """
    A class representing an object Segment
    """

    # the columns that are expected in the input dataframe
    # required_columns = ['frame',
    #                     'x','y','z',
    #                     'lpx','lpy','d_zcalib',
    #                     'photons',
    #                     'bg',
    #                     'len','n','photon_rate']
    # # the columns that should be in the class dataframe
    # content_columns = ['record_name', 'imageID','timepoint','cycle','zstep','frame',
    #                     'photoncount','photoncount11','photoncount12','photoncount21','photoncount22',
    #                     'psfx','psfy','psfz','psfphotoncount',
    #                     'x','y','z',
    #                     'background11','background12','background21','background22',
    #                     'maxResidualSlope',
    #                     'chi','loglike','llr','accuracy',
    #                     'mass',
    #                     'xprec','yprec','zprec',
    #                     'clusterID',
    #                     'chromosomes',
    #                     's11','s12','shiftz',
    #                     'lenon','nubon','photon_rate']
    
    def __init__(self, atomList, metadata={}, pxcamera=65.):
        """

        Initialise using a string of the relevant numpy array of Segment objects.

        *Arguments*:
        * *atomList*: DataFrame with required columns or np.ndarray with shape[1] = len(required_columns)

        """

        if(type(atomList) == pd.DataFrame):
            if (set(['x','y','z']) - set(atomList.columns) == set()):
                self.atomList = atomList.reset_index(drop=True)
            else:
                raise ValueError('Not all required columns found')
        if type(atomList) == list:
            atomList = array(atomList)
        if type(atomList) == ndarray:
            if(atomList.shape[1] == 3):
                self.atomList = pd.DataFrame(atomList.copy(), columns=['x','y','z'])
            else:
                raise ValueError('Just 3 columns supported when using array or list')

        self.metadata = dict(metadata)
        self.pxcamera = pxcamera
        

        if(not 'timepoint' in self.atomList.columns):
            self.atomList['timepoint'] = 1
        if(not 'clusterID' in self.atomList.columns):
            self.atomList['clusterID'] = 0
        self.atomList['record_name'] = 'sLOC'
        self.atomList['imageID'] = 0
        self.atomList['cycle'] = 0
        self.atomList['zstep'] = 0

        self.atomList['x'] = self.atomList['x']*pxcamera
        self.atomList['y'] = self.atomList['y']*pxcamera

        if('lpx' in self.atomList.columns):
            self.atomList['xprec'] = self.atomList['lpx']*pxcamera
        if('lpy' in self.atomList.columns):
            self.atomList['yprec'] = self.atomList['lpy']*pxcamera
        if('d_zcalib' in self.atomList.columns):
            self.atomList['zprec'] = self.atomList['d_zcalib']

        self.atomList['chromosomes'] = 0

        if('photons' in self.atomList.columns):
            self.atomList['photoncount'] = self.atomList['photons']
        self.atomList['photoncount11'] = 0.
        self.atomList['photoncount12'] = 0.
        self.atomList['photoncount21'] = 0.
        self.atomList['photoncount22'] = 0.
        self.atomList['psfx'] = 0.
        self.atomList['psfy'] = 0.
        self.atomList['psfz'] = 0.
        self.atomList['psfphotoncount'] = 0.

        if('bg' in self.atomList.columns):
            self.atomList['background11'] = self.atomList['bg']
        self.atomList['background12'] = 0.
        self.atomList['background21'] = 0.
        self.atomList['background22'] = 0.
        self.atomList['maxResidualSlope'] = 0.

        self.atomList['chi'] = None
        self.atomList['loglike'] = None
        self.atomList['llr'] = None
        self.atomList['accuracy'] = None

        self.atomList['s11'] = 0.
        self.atomList['s12'] = 0.
        self.atomList['shiftz'] = None
        self.atomList['mass'] = 10.

        if('len' in self.atomList.columns):
            self.atomList['lenon'] = self.atomList['len']
        if('n' in self.atomList.columns):
            self.atomList['nubon'] = self.atomList['n']

        #Centre of mass calculations
        self.CoM = self.calculate_centre_of_mass()


    def __getitem__(self, index):
        return self.atomList.iloc[index,:]

    def __len__(self):
        return len(self.atomList)
    
    @staticmethod
    def representSingleLocalization(loc):
        '''
        *Arguments*:
        * *loc*: Dict representing a localization

        
        *Return*: string representation
        '''
        return '(Time %s  ClusterID %s : %s ,%s ,%s)'%(loc.timepoint,loc.clusterID,loc.x,loc.y,loc.z)

    def __repr__(self):
        if 'filename' in self.metadata and not self.metadata['filename'] == 'Unknown':
            s =  'Filename: ' + str(self.metadata['filename']) + '\n'
        else:
            s = ''
        s += 'No Of Localisation: ' + str(len(self))  + '\n'
        s += 'First Localisation:' + SegmentH5.representSingleLocalization(self.atomList.iloc[0])+ '\n'
        s += 'Last Localisation: ' + SegmentH5.representSingleLocalization(self.atomList.iloc[-1]) + '\n'
        return s

    def copy(self):
        """
        *Return*:
            Copy of Segment instance.
        """
        return SegmentH5(self.atomList,
                         metadata=self.metadata)
    
    def copyWithNewContent(self, content):
        '''
        *Return*:
            A new object of this class, which has the provided content (DataFrame) but the attributes of self.
        '''
        return SegmentH5(content,
                         metadata=self.metadata)