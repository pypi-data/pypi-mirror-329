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
from CIMA.segments import SegmentFeatures as SF

import sys

class SegmentXYZ:
    """
    
    A class representing an object Segment
    
    """
    # required_columns = ['timepoint','x','y','z']
    # content_columns = required_columns + ['record_name', 'mass', 'clusterID']

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
        
        if(not 'timepoint' in self.atomList.columns):    
            self.atomList['timepoint'] = 0
        if(not 'clusterID' in self.atomList.columns):    
            self.atomList['clusterID'] = 0
        self.atomList['record_name'] = 'sLOC'
        self.atomList['mass'] = 10.

        #Centre of mass calculations
        self.CoM = self.calculate_centre_of_mass()
        ##self.initCoM = self.CoM.copy()

    
    def __getitem__(self, index):
        return self.atomList[index]

    def __len__(self):
        return len(self.atomList)
    
    @staticmethod
    def representSingleLocalization(loc):
        '''
        *Arguments*:
        * *loc*: Dict representing a localization
        
        *Return*: string representation
        '''
        return '(Time %s  : %s ,%s ,%s, ClusterID: %s)'%(loc.timepoint,loc.x,loc.y,loc.z, loc.clusterID)

    def __repr__(self):
        if 'filename' in self.metadata and not self.metadata['filename'] == 'Unknown':
            s =  'Filename: ' + str(self.metadata['filename']) + '\n'
        else: 
            s = ''
        s += 'No Of Localisation: ' + str(len(self))  + '\n'
        s += 'First Localisation:' + SegmentXYZ.representSingleLocalization(self.atomList.iloc[0])+ '\n'
        s += 'Last Localisation: ' + SegmentXYZ.representSingleLocalization(self.atomList.iloc[-1]) + '\n'
        return s

    def copy(self):
        """
        *Return*:
            Copy of Segment instance.
        """
        return SegmentXYZ(self.atomList,
                          metadata=self.metadata)
    
    def copyWithNewContent(self, content):
        '''
        *Return*:
            A new object of this class, which has the provided content (DataFrame) but the attributes of self.
        '''
        return SegmentXYZ(content,
                          metadata=self.metadata)

    def Getcoord(self):
        """
            *Return*:
                list of coordinates
        """
        return self.atomList[['x','y','z']].values

    def calculate_centre_of_mass(self):
        """
        *Return*:
            Center of mass of Segment as a Vector instance.
        """
        mean = self.atomList[['x','y','z']].mean(axis=0).values
        return Vector.Vector(mean[0], mean[1], mean[2])

    def splitByValue(self, values, verbose=False):
        """
        Arguments:
        * values: 1-Dimensional np.array


        Return:
        * a dictionary with the given values (uniqued) as keys and the corresponding subsegments as values

        
        Split a segment by arbitrary values. Useful for example to split by region of interest or homolog.
        """
        assert(len(values) == len(self.atomList))

        structDict = {i: [] for i in np.unique(values)}
        valvals = np.unique(values)
        for iv, v in enumerate(valvals):
            if(verbose): print(f'{iv}/{len(valvals)}')
            structDict[v] = self.copyWithNewContent(self.atomList.loc[values==v,:])
        return structDict
        
    
    def split_into_time(self, return_list=False):
        """
         Splits a walk into separate segments and returns a dictionary with timepoints as keys and Segment instances as values.
        """
        if(return_list):
            return list(self.splitByValue(self.atomList['timepoint']).values())
        else:
            return self.splitByValue(self.atomList['timepoint'])
    
    def getPortion(self, selection_array):
        assert selection_array.dtype == 'bool'
        if(selection_array.sum()>0):
            return self.copyWithNewContent(self.atomList.loc[selection_array])
        else:
            return None

    def getInRange(self, sel_range):
        selection = np.zeros(len(self.atomList), dtype=bool)
        selection[sel_range] = True
        return self.copyWithNewContent(self.atomList.loc[sel_range])

    def renumber_Time(self,newTime=""):
        """
        Returns a copy of this SegmentXYZ which has newTime as timepoint value for all localizations.
        If newTime is numpy array of same length as the number of localizations, they will be assigned the timepoints specified in it respectively.
        """
        newAtomList = self.atomList.copy()
        if len(newAtomList)!=0:
            newAtomList['timepoint'] = newTime
            return self.copyWithNewContent(newAtomList)
        else:
            print("Segment empty")
    
    def renumberTimeFromInt(self,start=1):
        """
        Returns a copy of this SegmentXYZ which has the timepoints renumbered in order from the specified start
        """
        newAtomList = self.atomList.copy()
        current_timepoints = sorted(newAtomList['timepoint'].unique())
        for i,t in enumerate(current_timepoints, start=start):
            newAtomList.loc[self.atomList['timepoint']==t,'timepoint'] = i
        return self.copyWithNewContent(newAtomList)
    
    def get_multiple_Time_segment(self,timepoints=[]):
        """
        *Return*:
            the a specific  time in the segment object
        """
        timepoints=[int(i) for i in timepoints]

        newAtomList = self.atomList.loc[self.atomList['timepoint'].apply(lambda t: t in timepoints)]
        if len(newAtomList)!=0:
            return self.copyWithNewContent(newAtomList)
        else:
            print("Warning no segment found in timepoints")
    
    def TimesIDs(self):
        """
        *Return*:
            the unique timepoints identifiers in the segment object
        """
        return self.atomList['timepoint'].unique()

    def no_of_Times(self):
        """
        *Return*:
            the number of time in the segment object
        """
        return len(self.TimesIDs())
    
    def get_Time_segment(self,timepoint=""):
        """
        *Return*:
            the a specific  time in the segment object
        """
        timepoint=int(timepoint)

        newAtomList = self.atomList.loc[self.atomList['timepoint']==timepoint]
        if len(newAtomList)!=0:
            return self.copyWithNewContent(newAtomList)
        else:
            print("Warning no segment %s found"%timepoint)
 
    def _combine_segments(self, SegmentList):# to do
        """

        Add a list of Segment instance to the existing structure.

        *Arguments*:
        * *SegmentList*: list of Segment instance

        
        *Return*:
            New Segment Instance.
        """
        new_atomList = pd.concat([self.atomList]+[s.atomList for s in SegmentList], axis=0)
        return self.copyWithNewContent(new_atomList)
    
    def get_extreme_values(self):

        """
        *Return*:
        A 6-tuple containing the minimum and maximum of x, y and z co-ordinates of the segment.
        Given in order (min_x, max_x, min_y, max_y, min_z, max_z).
        """
        mins = self.atomList[['x','y','z']].min(axis=0).values
        maxs = self.atomList[['x','y','z']].max(axis=0).values
        return (mins[0], maxs[0], mins[1], maxs[1], mins[2], maxs[2])

    def calculate_centroid(self):
        """Return centre of mass of structure as a Vector instance."""
        return self.calculate_centre_of_mass()


    def get_vector_list(self):
        """
        *Return*:
        Array containing 3D Vector instances of positions of all atoms.
        """
        return self.atomList.apply(lambda row: Vector.Vector(row['x'], row['y'], row['z']), axis=1).values

    def get_vector_list_threshold(self,c):
        """
        *Return*:
        Vector instance of positions of the map above c.
        """

        newmap = self.copy()
        binmap = self.fullMap > float(c)
        newmap.fullMap = binmap*self.fullMap

        #vectorMap = argwhere(newmap.fullMap)
        #for v in vectorMap:
        a = []
        for z in range(len(newmap.fullMap)):
            for y in range(len(newmap.fullMap[z])):
                for x in range(len(newmap.fullMap[z][y])):
                    if self.fullMap[z][y][x] != 0:
                        a.append((Vector.Vector((x*newmap.apix)+newmap.origin[0], (y*newmap.apix)+newmap.origin[1], (z*newmap.apix)+newmap.origin[2]),newmap.fullMap[z][y][x]))
        return array(a)
    
    def set_cluster_ids(self, cluster_ids):
        '''
        *cluster_ids*: np.array of ints and of length=len(self.atomList) or single number
        '''
        self.atomList['clusterID'] = cluster_ids
    
    def removeNoise(self):
        """
        Filters out noise by removing unclustered atoms from the segment.
        Note: The segment need to have a 'clusterID' column.

        This method removes atoms in `atomList` that have a `clusterID` of -1, which 
        typically represents noise or unclustered points. Only atoms with a valid 
        `clusterID` are retained in the new segment.

        Returns:
            A new segment object containing only the atoms with a `clusterID` not equal 
            to -1. If no such atoms are found, an empty segment is returned.
        """
        sub_df = self.atomList.loc[self.atomList['clusterID']!=-1,:]
        if(len(sub_df) > 0):
            return self.copyWithNewContent(sub_df)
        else:
            return self.copyWithNewContent(sub_df)
            # return None
    
    def getClusters(self,cluster_ids=[]):
        """
        Return:
            the a specific  time in the segment object
        """
        segs = [self.get_Cluster_segment(cid) for cid in cluster_ids]
        segs = [s for s in segs if not s is None]

        if(len(segs)==0):
            return None
        elif(len(segs)==1):
            return segs[0].copy()
        else:
            return segs[0]._combine_segments(segs[1:])
    
    def split_into_Clusters(self, return_list=False, verbose=False):
        """
         Splits the image into separate segments and returns a dictionay with clusterIDs as keys and Segment objects as values.
        """
        if(return_list):
            return list(self.splitByValue(self.atomList['clusterID'].values, verbose=verbose).values())
        else:
            return self.splitByValue(self.atomList['clusterID'].values, verbose=verbose)


    def no_of_Cluster(self):
        """
        Return:
            the number of time in the segment object
        """
        return len(self.atomList['clusterID']).unique()

    def get_Cluster_segment(self,ClusterID=""):
        """
        Return:
            the a specific  time in the segment object
        """
        c_df = self.atomList.loc[self.atomList['clusterID']==ClusterID]
        if(len(c_df)>0):
            return self.copyWithNewContent(c_df)
        else:
            print("Warning no segment %s found"%ClusterID)