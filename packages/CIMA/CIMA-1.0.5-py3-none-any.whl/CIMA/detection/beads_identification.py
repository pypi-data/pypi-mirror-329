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

__docformat__ = "markdown"

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.neighbors import NearestNeighbors


class BeadsFinder():
    def __init__(self):
        pass
 
    def fit(self, seg, n_jobs=1, radius=40, min_persistence=0.75):
        '''
        Arguments:
        * seg: Segment object with at least x,y,z,cycle,zstep,frame columns
        * n_jobs: number of cpus used to compute distances
        * radius: radius inside of which to search for neighbors
        * min_persistence: ratio of frames inside of which there should be
        a neighbor so that the localization be classified as bead-originated

        Attributes:
        * debeaded_segment: the segment cleaned of beads is saved here
        * labels_: 0/1 numpy array of same length as seg, where 0 indicates localizations coming from beads
        * graphs_df: contains the intermidiate data computed during fitting

        This class marks as beads those localizations which have a localization
        distant from them less than the specified radius in at least the specified
        percentage of frames of the current zstep and cycle.
        This approach works only if the localization have already been drift corrected.
        '''

        df = seg.atomList
        bead_labels = []
        
        self.graphs_df = pd.DataFrame(columns=['cycle', 'zstep', 'graph', 'shrinked_graph', 'coords', 'persistence'])
        for c in df['cycle'].unique():
            for z in df['zstep'].unique():
                subdf = df.loc[(df['cycle']==c) & (df['zstep']==z)]
                if(len(subdf)<2):
                    continue
                subdf = subdf.sort_values('frame', kind='mergesort')
                where_splits = np.where(np.diff(subdf.frame.values)>0)[0]+1
                coords = subdf[['x','y','z']].values
                graph = NearestNeighbors(radius=radius, n_jobs=n_jobs).fit(coords).radius_neighbors_graph(mode='connectivity').toarray()
                subgs = np.split(graph, where_splits, axis=1)
                shrinked_graph = np.column_stack([s.sum(axis=1)>0 for s in subgs]).astype('int')
                persistence = (shrinked_graph>0).sum(axis=1).flatten()/subdf['frame'].max()
                local_where_bead = persistence>min_persistence
                bead_labels.extend(subdf.index.values[local_where_bead])
                # bead_labels.extend(subdf.index.values[local_where_bead_extended])
                
                self.graphs_df.loc[len(self.graphs_df)] = {'cycle': c,
                                                         'zstep': z,
                                                         'graph': graph,
                                                         'shrinked_graph': shrinked_graph,
                                                         'coords': coords,
                                                         'persistence': persistence
                                                         }
                
        self.persistence = np.concatenate(self.graphs_df['persistence'].values)
                
        
        labs = np.ones(len(df), dtype='int')
        labs[bead_labels]=0
 
        self.labels_ = labs
 
        self.debeaded_segment = seg.copyWithNewContent(seg.atomList[self.labels_==1])

        return self
    
    def show(self):
        '''
        Displays a representation of the connection matrices,
        first by considering all localizations and then considering one localization per frame.
        Then it also displays the persistence of each localization.
        '''
        for i,row in self.graphs_df.iterrows():
            plt.imshow(row['graph'], cmap='gray')
            plt.title('Connections between localizations')
            plt.ylabel('All localizations')
            plt.xlabel('All localizations')
            plt.show()
            plt.imshow(row['shrinked_graph'], cmap='gray')
            plt.title('Connections between localizations considering one localization per frame')
            plt.ylabel('All localizations')
            plt.xlabel('Frames')
            plt.show()
            sns.scatterplot(x=row['coords'][:,0], y=row['persistence'], alpha=0.1)
            plt.axhline(0.75, ls='--')
            plt.title('cycle ' + str(row['cycle']) + ' zstep '+ str(row['zstep']))
            plt.show()