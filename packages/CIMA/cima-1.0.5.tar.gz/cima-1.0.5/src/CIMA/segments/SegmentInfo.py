
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
from CIMA.segments.SegmentInfoXYZ import SegmentXYZ
import numpy as np
import pandas as pd


import sys



class Segment(SegmentXYZ):
    """
    A class representing an object Segment
    """

    # required_columns = ['imageID','timepoint','cycle','zstep','frame',
    #                     'photoncount','photoncount11','photoncount12','photoncount21','photoncount22',
    #                     'psfx','psfy','psfz','psfphotoncount',
    #                     'x','y','z',
    #                     'background11','background12','background21','background22',
    #                     'maxResidualSlope',
    #                     'chi','loglike','llr','accuracy',
    #                     'xprec','yprec','zprec']
    # 
    # content_columns = required_columns + ['record_name', 'clusterID', 'chromosomes',
    #                                               's11', 's12', 'shiftz', 'mass']

    def __init__(self, atomList, metadata={}):
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
        
        self.atomList['record_name'] = 'sLOC'
        if(not 'timepoint' in self.atomList.columns):    
            self.atomList['timepoint'] = 0
        if(not 'clusterID' in self.atomList.columns):    
            self.atomList['clusterID'] = 0
        if(not 'chromosomes' in self.atomList.columns):
            self.atomList['chromosomes'] = 0
        if('background' in self.atomList.columns):
            self.atomList.loc[self.atomList['background11']==0,'s11'] = 0.
            self.atomList.loc[self.atomList['background12']==0,'s12'] = 0.
        if('photoncount11' in self.atomList.columns and 'background11' in self.atomList.columns):
            self.atomList.loc[self.atomList['background11']!=0,'s11'] = self.atomList['photoncount11']/self.atomList['background11']
        if('photoncount12' in self.atomList.columns and 'background12' in self.atomList.columns):
            self.atomList.loc[self.atomList['background12']!=0,'s12'] = self.atomList['photoncount12']/self.atomList['background12']
        if('psfz' in self.atomList.columns):
            self.atomList['shiftz'] = np.abs(self.atomList['psfz'] - self.atomList['z'])
        self.atomList['mass'] = None
        if('accuracy' in self.atomList.columns):
            self.atomList.loc[pd.notna(self.atomList['accuracy']), 'mass'] = 10.

        #Centre of mass calculations
        self.CoM = self.calculate_centre_of_mass()
    
    @staticmethod
    def representSingleLocalization(loc):
        '''
        *Arguments*:
        * *loc*: Dict representing a localization

        
        *Return*: string representation
        '''
        return '(Time %s  ClusterID %s Chromosome %s: %s ,%s ,%s)'%(loc.timepoint,loc.clusterID,loc.chromosomes,loc.x,loc.y,loc.z)

    def __repr__(self):
        if 'filename' in self.metadata and not self.metadata['filename'] == 'Unknown':
            s =  'Filename: ' + str(self.metadata['filename']) + '\n'
        else:
            s = ''
        s += 'No Of Localisation: ' + str(len(self))  + '\n'
        s += 'First Localisation:' + Segment.representSingleLocalization(self.atomList.iloc[0])+ '\n'
        s += 'Last Localisation: ' + Segment.representSingleLocalization(self.atomList.iloc[-1]) + '\n'
        return s

    def copy(self):
        """
        *Return*:
            Copy of Segment instance.
        """
        return Segment(self.atomList,
                       metadata=self.metadata)
    
    def copyWithNewContent(self, content):
        '''
        *Return*:
            A new object of this class, which has the provided content (DataFrame) but the attributes of self.
        '''
        return Segment(content,
                       metadata=self.metadata)
    
    # CYCLE and ZSTEP
    

    def split_into_cycle(self):
        """
         Split a walk into separate segments and returns the list of Segment Instance for each cycle.
        """
        return list(self.splitByValue(self.atomList['cycle']).values())

    def OrderbyExperimenttime(self):
        """
        Orders the segment's  localisation list by experimental time.

        This method sorts the entries in `atomList` by experimental variables such as 
        cycle and z-step, which represent the order of data acquisition. Sorting by 
        these parameters allows for analysis in the sequence they were collected.

        Returns:
            A new segment object with `atomList` sorted by `cycle` and `zstep`.

        """
		#cyle farme dz add it
        return self.copyWithNewContent(self.atomList.sort_values(by=['cycle','zstep'], axis=0))


    # FRAME

    def split_into_frames_chunk(self,maxframes=250,interval=5):
        """
         Split a walk into separate segments and returns the list of Segment Instance for each chunk of frames.
        """
        structList = []
        maxframes=int(maxframes)
        interval=int(interval)
        frames=list(range(0,int(maxframes)))
        frames_chucks = [frames[x:x+interval] for x in range(0, len(frames),interval)]
        for fr in frames_chucks:
            seg = self.getFrames(self, fr)
            if(not seg is None):
                structList.append(seg)
        return structList
    
    def getFrames(self, frames):
        local_fr_parcial=self.atomList.loc[self.atomList['frame'].apply(lambda x: x in frames),:]
        if len(local_fr_parcial)>0:
            return self.copyWithNewContent(local_fr_parcial)
        else:
            return None
    
    # CHROMOSOMES

    def set_chromosomes(self, chromsomes_ids):
        '''
        *chromsomes_ids*: np.ndarray of ints and of length=len(self.atomList) or single number
        '''
        self.atomList['chromosomes'] = chromsomes_ids

    def split_into_Chromosomes(self):
        """
         Split the image into separate segments and returns the list of Segment Instance for each time point.
        """
        return list(self.splitByValue(self.atomList['chromosomes']).values())

    def ChromosomesIDs(self):
        """
        *Return*:
            the number of time in the segment object
        """
        return self.atomList['chromosomes'].unique()

    def no_of_Chromosomes(self):
        """
        *Return*:
            the number of time in the segment object
        """
        return len(self.atomList['chromosomes'].unique())

    def get_Chromosomes_segment(self,chromosome_id=""):
        """
        *Return*:
            the a specific  time in the segment object
        """
        chromosome_id=int(chromosome_id)+1
        c_df = self.atomList.loc[self.atomList['chromosomes']==chromosome_id]
        if(len(c_df)>0):
            return self.copyWithNewContent(c_df)
        else:
            print("Warning no segment %s found"%chromosome_id)

    # PRECISION

    def PrecisionFilter(self,factor=[100,100,100]):
        """
        Filters the segment's localisation list by precision.

        This method filters out entries in `atomList` where the positional precision 
        (for x, y, and z coordinates) exceeds the specified thresholds in `factor`. 
        Entries that meet the precision criteria are retained, allowing for analysis 
        with higher confidence in positional accuracy.

        Args:
            factor (list, optional): A list of precision thresholds for the x, y, and z coordinates.
                                    Defaults to [100, 100, 100].

        Returns:
            A new segment object with `atomList` filtered to include only entries with
            precision lower than the specified thresholds in x, y, and z. If no entries 
            meet the criteria, a warning message is printed, and nothing is returned.

        """
        factor = np.array(factor).astype('float')
        newAtomList = self.atomList.loc[((self.atomList['xprec']<factor[0])*
                                        (self.atomList['yprec']<factor[1])*
                                        (self.atomList['zprec']<factor[2])).astype('bool')]
        if len(newAtomList)!=0:
            return self.copyWithNewContent(newAtomList)
        else:
            print("Warning no localization with precision lower than that found")

    def GetMinPrecision(self):
        """return min precison in X,Y,Z"""
        return list(self.atomList[['xprec','yprec','zprec']].min(axis=0))

    def GetMaxPrecision(self):
        """return max precison in X,Y,Z"""
        return list(self.atomList[['xprec','yprec','zprec']].max(axis=0))

    def GetMeanPrecision(self):
        """return mean precison in X,Y,Z"""
        return list(self.atomList[['xprec','yprec','zprec']].mean(axis=0))

    # PSF
    def PSFz_shiftFilter(self,upperbound_factor=500,lowerbound_factor=0):
        newAtomList = []
        fupper=float(upperbound_factor)
        flower=float(lowerbound_factor)
        newAtomList = self.atomList.loc[((self.atomList['shiftz'].astype('float')<=fupper)*
                                        (self.atomList['shiftz'].astype('float')>=flower)).astype('bool')]
        if len(newAtomList)!=0:
            return self.copyWithNewContent(newAtomList)
        else:
            print("Warning no localization with precision in interval")


    def PhotonCount_Filter(self,upperbound_factor=500,lowerbound_factor=0):
        newAtomList = []
        fupper=float(upperbound_factor)
        flower=float(lowerbound_factor)
        newAtomList = self.atomList.loc[((self.atomList['psfphotoncount'].astype('float')<=fupper)*
                                        (self.atomList['psfphotoncount'].astype('float')>=flower)).astype('bool')]
        if len(newAtomList)!=0:
            return self.copyWithNewContent(newAtomList)
        else:
            print("Warning no localization with precision in interval")

    # ACCURACY

    def GetMaxAccuracy(self):
        """return min,max and mean precison in X,Y,Z"""
        return self.atomList['accuracy'].max()

    def GetMinAccuracy(self):
        """return min,max and mean precison in X,Y,Z"""
        return self.atomList['accuracy'].min()

    def GetMeanAccuracy(self):
        """return min,max and mean precison in X,Y,Z"""
        return self.atomList['accuracy'].mean()
    

