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

from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import scipy
from tqdm import tqdm


class HomologSeparator():

    def __init__(self):
        pass

    def fit(self, seg, randseed = 0, algorithm='kmeans', dbscan_config={'min_samples':1, 'eps':250}):
        '''
        Separates a segment into two different homologs using KMeans algorithm

        Arguments:
        * seg: Segment to separate
        * randseed: random seed to use when applying the separation algorithm
        * algorithm: kmeans, linkage, dbscan

        Returns:
        * None

        Attributes:
        * labels_: np array of same length as seg indicating with 0 and 1 the two homologs.
            No inference is made on the paternal/maternal nature of them.
        * seg1, seg2: the two segments representing the separated homologs

        '''

        if(algorithm=='kmeans'):
            kmeans = KMeans(n_clusters=2, random_state=randseed).fit(seg.Getcoord())
            self.labels_ = kmeans.labels_
        
        elif(algorithm=='linkage'):
            df1 = seg.atomList.copy()
            dict1 = {}
            for i, ((l,c), subdf) in enumerate(df1[['x','y','z','locusID','clusterID']].groupby(['locusID','clusterID'])):
                dict1[i] = subdf
            # df1[['x','y','z','locusID','clusterID']].groupby(['locusID','clusterID']).mean().reset_index(drop=True)
            dist_dict = {}
            for i in tqdm(range(len(dict1))):
                dist_dict[i] = {}
                for j in range(i,len(dict1)):
                    dist_dict[i][j] = scipy.spatial.distance.cdist(dict1[i][['x','y','z']].values,dict1[j][['x','y','z']].values).min()
            arr1 = pd.DataFrame(dist_dict).T.values
            arr1[np.diag_indices(arr1.shape[0])] = np.nan
            arr1 = arr1.flatten()
            arr1 = arr1[np.isfinite(arr1)]
            # arr1
            lm = scipy.cluster.hierarchy.linkage(arr1)
            # plt.figure()
            # scipy.cluster.hierarchy.dendrogram(lm, ax=plt.gca())
            # plt.show()
            labels1 = scipy.cluster.hierarchy.fcluster(lm, t=2, criterion='maxclust')
            labels1 = labels1-labels1.min()

            labels2 = np.repeat(labels1, [len(dftemp) for n,dftemp in df1[['x','y','z','locusID','clusterID']].groupby(['locusID','clusterID'])])
            
            self.labels_ = labels2
        
        elif(algorithm=='dbscan'):
            from sklearn.cluster import DBSCAN  
            config = dbscan_config
            hc= DBSCAN(min_samples=config['min_samples'], eps=config['eps'])
            labels= hc.fit_predict(seg.Getcoord())

            if(len(np.unique(labels[labels!=-1])) != 2):
                raise ValueError('More or less than two clusters identified. Stopping operation')
            elif((labels==-1).sum()>0):
                raise ValueError('Some localizations classified as noise: situation not supported')
            else:
                self.labels_ = labels
        else:
            raise ValueError('Algorithm not implemented')


        
        self.seg1 = seg.copyWithNewContent(seg.atomList[self.labels_==0])
        self.seg2 = seg.copyWithNewContent(seg.atomList[self.labels_==1])