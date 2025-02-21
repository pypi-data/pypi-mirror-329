#===============================================================================
#     This file is part of CIMA.
#
#     CIMA is a software designed to help the user in the manipulation
#     and analyses of genomic super resolution localisation data.
#
#      Copyright  2019-2024
#
#                Authors: Irene Farabella
#
#
#
#===============================================================================

__docformat__ = "markdown"

from CIMA.segments.SegmentInfo import Segment
from CIMA.segments.SegmentInfoXYZ import SegmentXYZ
from CIMA.segments import SegmentGaussian as SG
TB=SG.TransformBlurrer()
from CIMA.maps import MapFeatures as MF
from CIMA.segments import SegmentFeatures as SF
import CIMA.utils.WalkFeatures as WF
from CIMA.utils import Visualization

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#from sklearn.metrics import adjusted_rand_score
from sklearn.cluster import KMeans,DBSCAN
from sklearn.neighbors import NearestNeighbors
from sklearn import metrics
from sklearn.metrics import adjusted_rand_score
from scipy.stats import multivariate_normal
from scipy.ndimage import convolve
import seaborn as sns
import matplotlib.pyplot as plt
from CIMA.segments.SegmentInfoXYZ import SegmentXYZ
#from decimal import  Decimal






def _elbow_point(data):
    """This is a private function to detect the "elbow point" in the data.
    Input:
    * one-dimensional array data, sorted in ascending order


    Return:
    integer
    """

    # The elbow point is selected as the data point which is farthest from the line
    # that connects the leftmost to the rightmost data points in an ascending-order plot.
    from numpy import matlib as mb
    curve = data
    nPoints = len(curve)
    allCoord = np.vstack((range(nPoints), curve)).T
    np.array([range(nPoints), curve])

    firstPoint = allCoord[0]
    lineVec = allCoord[-1] - allCoord[0]
    lineVecNorm = lineVec / np.sqrt(np.sum(lineVec**2))
    vecFromFirst = allCoord - firstPoint
    scalarProduct = np.sum(vecFromFirst * mb.repmat(lineVecNorm, nPoints, 1), axis=1)
    vecFromFirstParallel = np.outer(scalarProduct, lineVecNorm)
    vecToLine = vecFromFirst - vecFromFirstParallel
    distToLine = np.sqrt(np.sum(vecToLine ** 2, axis=1))
    idxOfBestPoint = np.argmax(distToLine)

    return idxOfBestPoint


def searchepsilon(xyz,n_neighbors="", show=True,preclimit=50., n_jobs=None):
    """
    This function estimate the optimal value of the epsilon parameter for the DBSCAN clustering algorithm, given a dataset xyz.


    Arguments:
    * *xyz*: array of Localisation coordinates
    * *n_neighbors*: integer, number of neighbors to consider in the nearest neighbors algorithm (if not specified, it is set to 2 * len(xyz[0]) - 1)
    * *show*: show is set to True, the function plots a graph of the sorted distances and the estimated elbow point
    * *preclimit*: precision to use for rapresentation (see Nir et al., PloS Gen 2018)
    
    
    Return:
    integer, optimal epsilon value
    """
    #https://stackoverflow.com/questions/15050389/estimating-choosing-optimal-hyperparameters-for-dbscan?rq=1
    if n_neighbors=="":
        n_neighbors = 2 * len(xyz[1]) - 1

    neigh = NearestNeighbors(n_neighbors=n_neighbors+1,algorithm='ball_tree', n_jobs=n_jobs)
    nbrs = neigh.fit(xyz)
    distances, indices = nbrs.kneighbors(xyz)
    distances = distances[:,n_neighbors].flatten()
    distances = np.sort(distances, axis=0)
    dict_tm=dict (list(enumerate(distances)))
    k = _elbow_point(distances)
    if show:
        plt.plot(distances)
        plt.axhline(y=dict_tm[k], color='.3', linestyle='--')
        #plt.axhline(y=dict_tm[k]+preclimit, color='.8', linestyle='-')
    return dict_tm[k]
# run for varied NN negihbour and get the median across NN

def _gKernel(side):
    '''
    Return a square np array with the specified side. The values follow the density of a normal distribution centered in the center of the np array,
    and with std equal to 1/3 of the side
    '''
    grid0, grid1 = np.meshgrid(np.arange(side), np.arange(side))
    grid = np.dstack((grid0,grid1))
    
    rv = multivariate_normal(mean=np.ones(2)*(side-1)/2, cov=np.eye(2)*side/3)
    # rv = multivariate_normal([(side-1)/2, (side-1)/2], [[side/3, 0.], [0., side/3]])
    vals = rv.pdf(grid)
    return vals/vals.sum()


def _radiusToVolume(x):
    '''
    Returns volume of the sphere with radius x
    '''
    return (4/3)*3.1415*(x**3)

def _volumeToRadius(vol):
    '''
    Returns radius of the sphere with volume x
    '''
    return np.cbrt(vol*(3/4)*(1/3.1415))

def getPointwiseDensity(coords, radius, n_jobs=1, verbose=False):
    '''
    Arguments:
    * coords: 2-dimensional numpy array with each row representing the location of a point
    * radius: radius inside of which count neighbord
    * n_jobs: how many cpus have to be used for the computation


    Returns:
    * a numpy array representing density of each point in coords, estimated as the count of neighbors inide the specified radius divided by the volume of the corresponding volume
    '''
    nn = NearestNeighbors(n_jobs=n_jobs)
    nn.fit(coords)
    if(verbose): print('finding neighbors')
    neigh_inds = nn.radius_neighbors(radius=radius,
                                     return_distance=False)
    if(verbose): print('counting')
    area = _radiusToVolume(radius)
    if(verbose):
        from tqdm import tqdm
        counts = np.array([len(inds) for inds in tqdm(neigh_inds)])
    else:
        counts = np.array([len(inds) for inds in neigh_inds])
    return counts/area

class DBscan_grid_search_stable():
    '''
        Selects the pair of min_points and eps parameters which give the clustering with the highest stability,
        meaning that it changes less when changing the parameters.
        In the process computes DBSCAN labels for all the combinations of specified parameters.
        Also computes the grids of ari scores among neighborhood of labels, and the variation of those ari scores.
    '''
    def __init__(self):        
        self.neighborhood_ari = None
        self.neighborhood_ari_var = None
        self.labs = None
        self.downsampling_rate = 1.0
    
    def copy(self):
        '''
        Return an identical copy
        '''
        newone = DBscan_grid_search_stable()
        newone.neighborhood_ari = self.neighborhood_ari.copy()
        newone.neighborhood_ari_var = self.neighborhood_ari_var.copy()
        newone.labs = self.labs.copy()
        newone.downsampling_rate = self.downsampling_rate
        newone.min_pts_range = self.min_pts_range
        newone.eps_range = self.eps_range
        newone.downsampled_min_pts_range = self.downsampled_min_pts_range
        newone.segment = self.segment
        newone.ordered_params_df = self.ordered_params_df
        newone.best_min_pts = self.best_min_pts
        newone.best_eps = self.best_eps
        newone.best_inds = self.best_inds.copy()
        newone.labels_ = self.labels_
        newone.optimal_segment = self.optimal_segment
        return newone

    def fit(self, segment: SegmentXYZ, min_pts_range=None, eps_range = None, consider_noise=True, n_neighbors=2,
            conv=False, verbose=0, n_jobs=8, downsampling_rate=1., limit_density=False, random_seed=0):
        '''
        Computes labels, ari and ari_var grids.
        Computes the rank of parameter combinations according to stability.
        Saves best labels and a copy of segment with them as clusterIDs.


        Arguments:
        * segment: SegmentXYZ containing the coodinates on which to run the clustering
        * min_pts_range: list of min_samples values to provide to DBSCAN
        * eps_range: list of eps values to provide to DBSCAN
        * consider_noise: if False compute the ari just on the points which are not noise in at least one of the two clusterings.
            This may be useful when the majority of points are classified as noise, because it concentrates the comparison on the signal part.
        * n_neighbors: how far a parameter combination in the grid should be to be considered in the stability computations
        * conv: wheter to apply a blurring on the grid before computing the rank of stability
        * n_jobs: how many cpus to use
        * downsampling_rate: rate of subselection of points on which to run DBSCAN. Allows to decrease computation time.
            When the rate is <1 the min_pts_range is adjusted so that the pattern on the grid is very similar to that that would be obtained with rate=1.
            The results is less comparable as the rate is decreased towards 0. 
        * limit_density: limit the search for stability among those parameters defining a density threshold between the 25th and 75th density percentile of coordinates
        * random_seed: used in the random selection of downsampled coords
        
        '''

        assert(downsampling_rate>=0.0 and downsampling_rate<=1.0)
        if(min_pts_range is None):
            min_pts_range = [10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,220,230,240,250,260,270,300,350,400]
            # min_pts_range = [20,40,50,60,70,80,90,100,120,150,170,200]
        min_pts_range = np.array(min_pts_range)
        if(eps_range is None):
            if(verbose>1):
                print('searching epsilon')
            optimal_eps = searchepsilon(segment.Getcoord(), show=False, n_jobs=n_jobs)
            eps_range = np.linspace(50,optimal_eps+50,20).astype('int') # [self.optimal_eps+200]
        eps_range = np.array(eps_range)

        assert len(min_pts_range)>0, 'At least one min_pts needed'
        assert len(eps_range)>0, 'At least one eps needed'
        assert len(min_pts_range) + len(eps_range)>2, 'At least one of min_pts_range and eps_range should be contain more than one element'
        assert n_neighbors>0, 'Number of neighbors should be greater than 0'

        self.min_pts_range = min_pts_range
        self.downsampled_min_pts_range = (min_pts_range*downsampling_rate).astype('int')
        self.eps_range = eps_range
        self.downsampling_rate = downsampling_rate
        self.segment = segment
        self.n_jobs = n_jobs
        
        if(verbose>1):
            print('self.min_pts_range: ', self.min_pts_range)
            print('self.eps_range: ', self.eps_range)
        
        np.random.seed(random_seed)
        selection_array = np.random.choice([True, False], len(segment), replace=True, p=[self.downsampling_rate, 1-self.downsampling_rate])
        downsampled_coords = segment.Getcoord()[selection_array]
        denss = getPointwiseDensity(downsampled_coords, radius=np.median(self.eps_range))
        if(limit_density):
            min_dens = np.sort(denss)[int(len(denss)*0.25)]
            max_dens = np.sort(denss)[int(len(denss)*0.75)]
            self.min_dens = min_dens
            self.max_dens = max_dens
        else:
            min_dens = None
            max_dens = None
        self.labs = DBscan_grid_search_stable._getLabelsGrid(downsampled_coords,
                                                             self.downsampled_min_pts_range, self.eps_range, verbose, n_jobs)

        self._computeAllFromLabelsGrid(conv, consider_noise, n_neighbors, verbose, min_dens, max_dens)

        return self
    
    def _computeAllFromLabelsGrid(self, conv=False, consider_noise=True, n_neighbors=2, verbose=0, min_dens=None, max_dens=None):
        self.neighborhood_ari, self.neighborhood_ari_var = DBscan_grid_search_stable._getGridNeighborhoodAriAndAriVariance(self.labs, consider_noise, n_neighbors, verbose)

        if(conv):
            processed_ari_mat = convolve(self.neighborhood_ari, _gKernel(max(self.neighborhood_ari.shape)/3), mode='nearest') # , cval=0.0
            self.processed_ari_mat = processed_ari_mat
            processed_ari_var_mat = convolve(self.neighborhood_ari_var, _gKernel(max(self.neighborhood_ari_var.shape)/3), mode='nearest') # , cval=1.0
            self.processed_ari_var_mat = processed_ari_var_mat
        else:
            processed_ari_mat = self.neighborhood_ari
            processed_ari_var_mat = self.neighborhood_ari_var
        self.ordered_params_df = DBscan_grid_search_stable._getOrderedParametersDf(processed_ari_mat, processed_ari_var_mat,
                                                              self.min_pts_range, self.eps_range)
        if(not min_dens is None and not max_dens is None):
            self.ordered_params_df['dens'] = self.ordered_params_df['min_pts']/_radiusToVolume(self.ordered_params_df['eps'])
            self.ordered_params_df['inside_dens_range'] = ((self.ordered_params_df['dens']>=min_dens/self.downsampling_rate) * (self.ordered_params_df['dens']<=max_dens/self.downsampling_rate)).astype('bool')
            self.ordered_params_df = self.ordered_params_df.sort_values('inside_dens_range', ascending=False, kind='mergesort').reset_index(drop=True)
        self.best_min_pts = self.ordered_params_df.loc[0,'min_pts']
        self.best_eps = self.ordered_params_df.loc[0,'eps']
        self.best_inds = self.ordered_params_df.loc[0,['min_pts_ind','eps_ind']].tolist()
        if(self.labs.shape[-1] == len(self.segment)):
            self.labels_ = self.labs[self.best_inds[0], self.best_inds[1]]
        else:
            self.labels_ = DBSCAN(eps=self.best_eps, min_samples=self.best_min_pts, n_jobs=self.n_jobs).fit(self.segment.Getcoord()).labels_
        
        self.optimal_segment = self.segment.copy()
        self.optimal_segment.set_cluster_ids(self.labels_)
    
    @staticmethod
    def _getNeighborhoodAris(i1, i2, labels_arr, n_neighbors = 2, consider_noise=True):
        '''
        Returns the aris of the clustering (defined by the corresponding labels) located at indices i1,i2
        with all the clusterings in an n-radius square neighborhood
        '''
        square_neighborhood = labels_arr[max(0,i1-n_neighbors):min(labels_arr.shape[0]-1,i1+n_neighbors)+1, \
                                        max(0,i2-n_neighbors):min(labels_arr.shape[1]-1,i2+n_neighbors)+1, \
                                        :]
        c1 = min(i1,n_neighbors)
        c2 = min(i2,n_neighbors)
        # Now c1 and c2 are the indexes of the central cell in square_neighborhood (relative to the square neighborhood).
        # Central in the sense that it represents the currently considered combination of parameters.
        s = 0
        aris = []

        central_labels = square_neighborhood[c1,c2,:]
        for i in range(square_neighborhood.shape[0]):
            for j in range(square_neighborhood.shape[1]):
                if(i == c1 and j == c2):
                    continue
                current_neighbor_labels = square_neighborhood[i,j,:]
                if(consider_noise):
                    ari = adjusted_rand_score(central_labels, current_neighbor_labels)
                else:
                    where_no_noise = ((central_labels != -1) + (current_neighbor_labels != -1)).astype('bool')
                    ari = adjusted_rand_score(central_labels[where_no_noise], current_neighbor_labels[where_no_noise])
                aris.append(ari)
        return aris
    
    @staticmethod
    def _getLabelsGrid(coords, min_pts_range=[10,20,30], eps_range=[10,20,30], verbose=0, n_jobs=8):
        assert not (coords is None)
        labs = np.zeros((len(min_pts_range), len(eps_range), len(coords)), dtype='int')
        for mi, m in enumerate(min_pts_range):
            for ei, e in enumerate(eps_range):
                if(verbose>1): print(m,' - ', e)
                labs[mi, ei] = DBSCAN(eps=e, min_samples=m, n_jobs=n_jobs, metric='euclidean').fit(coords).labels_
            if(verbose>0):
                if(mi==len(min_pts_range)-1):
                    print('dbscan computation: ', np.round((mi+1)*100/len(min_pts_range),1), '%')
                else:
                    print('dbscan computation: ', np.round((mi+1)*100/len(min_pts_range),1), '%', end='\r')
        return labs
    
    @staticmethod
    def _getGridNeighborhoodAriAndAriVariance(labels_grid, consider_noise=True, n_neighbors=2, verbose=0):
        neighborhood_ari = np.zeros(shape=labels_grid.shape[:2])
        neighborhood_ari_var = np.zeros(shape=labels_grid.shape[:2])
        for mi, m in enumerate(range(labels_grid.shape[0])):
            if(verbose>=1):
                if(mi==len(range(labels_grid.shape[0]))-1):
                    print('Starting min_points: %i out of %i'%(mi, labels_grid.shape[0]))
                else:
                    print('Starting min_points: %i out of %i'%(mi, labels_grid.shape[0]), end='\r')
            for ei, e in enumerate(range(labels_grid.shape[1])):
                neigh_aris = DBscan_grid_search_stable._getNeighborhoodAris(mi, ei, labels_grid, n_neighbors = n_neighbors, consider_noise=consider_noise)
                neighborhood_ari[mi,ei] = np.round(np.nanmedian(np.array(neigh_aris)),3)
                neighborhood_ari_var[mi,ei] = np.round(np.nanmedian(np.absolute(neighborhood_ari[mi,ei] - np.array(neigh_aris))),3)
        return neighborhood_ari, neighborhood_ari_var
    
    def mergeOtherDBSCANGrid(self, other_scanner,
                            conv=False, consider_noise=True, n_neighbors=2, verbose=0):
        '''
        Integrates the grid of precomputed labels contained in other_scanner into this object.
        Then computes everything else from them.
        Useful when you want to extend the grid without having to recompute the labels that you already have.


        Arguments:
        * *other_scanner*: the scanner (already fitted) to integrate into this one
        * *conv*: see fit()
        * *consider_noise*: see fit()
        * *n_neighbors*: see fit()
        '''
        if(self.labs is None):
            raise ValueError('This object was not fitted')
        if(other_scanner.labs is None or
           other_scanner.labs.shape[0] == 0 or other_scanner.labs.shape[1] ==0):
            raise ValueError('Nothing to merge')
        if(not self.segment[['x','y','z']].equals(other_scanner.segment[['x','y','z']])):
            raise ValueError('The two segments\' coordinates don\'t correspond')

        df_labs_other = pd.DataFrame({i:other_scanner.labs[:,i].tolist() for i in range(other_scanner.labs.shape[1])}) \
            .set_axis(other_scanner.min_pts_range, axis=0).set_axis(other_scanner.eps_range, axis=1)

        df_labs = pd.DataFrame({i:self.labs[:,i].tolist() for i in range(self.labs.shape[1])}) \
            .set_axis(self.min_pts_range, axis=0).set_axis(self.eps_range, axis=1)

        write_mps = other_scanner.min_pts_range
        write_eps = other_scanner.eps_range
        
        for e in write_eps:
            df_labs.loc[write_mps, e] = df_labs_other.loc[write_mps, e]

        # df_labs[df_labs.isna()] = np.random.choice(np.arange(0,10), self.labs[0].shape[0])
        where_na = np.where(df_labs.isna())
        for i in range(len(where_na[0])):
            df_labs.iloc[:,where_na[1][i]].iloc[where_na[0][i]] = np.random.choice(np.arange(0,10), self.labs.shape[-1])

        self.min_pts_range = np.array(sorted(list(set(self.min_pts_range).union(set(other_scanner.min_pts_range)))))
        self.eps_range = np.array(sorted(list(set(self.eps_range).union(set(other_scanner.eps_range)))))

        self.labs = np.stack(df_labs.loc[self.min_pts_range, self.eps_range].values.flatten().tolist()).reshape(len(self.min_pts_range), len(self.eps_range), len(self.labs[0,0]))

        self._computeAllFromLabelsGrid(conv, consider_noise, n_neighbors, verbose)

        return self
    
    @staticmethod
    def _getOrderedParametersDf(neighborhood_ari, neighborhood_ari_var, min_pts_range, eps_range):
        '''
        Builds a DF of parameters, ari and ari variation values, in decreasing order of stability
        '''
        flat_order = np.lexsort((-1*neighborhood_ari_var.flatten(), neighborhood_ari.flatten())) # the best is at the end
        # Transpose is used because the melt function flattens the array in a transpose way wrt the usual numpy flattening
        flat_order_transpose = np.lexsort((-1*neighborhood_ari_var.T.flatten(), neighborhood_ari.T.flatten())) # the best is at the end
        df1 = pd.DataFrame(neighborhood_ari, index=min_pts_range, columns = eps_range) \
            .reset_index().rename({'index':'min_pts_range'}, axis=1).melt(id_vars='min_pts_range', value_vars=eps_range)
        df2 = pd.DataFrame(neighborhood_ari_var, index=min_pts_range, columns = eps_range) \
            .reset_index().rename({'index':'min_pts_range'}, axis=1).melt(id_vars='min_pts_range', value_vars=eps_range)
        df1['ari_var'] = df2['value']
        df1 = df1.rename({'min_pts_range':'min_pts', 'value':'ari','variable':'eps'}, axis=1).iloc[flat_order_transpose[::-1],:].reset_index(drop=True)
        df1['min_pts_ind'] = df1['min_pts'].apply(lambda x: np.where(min_pts_range==x)[0][0])
        df1['eps_ind'] = df1['eps'].apply(lambda x: np.where(eps_range==x)[0][0])
        return df1

    
    def saveLog(self, outfile):
        '''
        Saves the ari and ari variation values in a single csv file, in decreasing order of stability
        '''
        assert not self.ordered_params_df is None
        self.ordered_params_df.to_csv(outfile, index=False) # [['min_pts','eps','ari','ari_var']]
    
    def plotAriGrid(self):
        '''
        Plots the grid of ari values
        '''
        sns.heatmap(pd.DataFrame(self.neighborhood_ari, index=self.min_pts_range, columns=self.eps_range), cmap='Greens', annot=False)
        plt.scatter([self.best_inds[1]+0.5],[self.best_inds[0]+0.5], c='#d95f02')
        print('scattering at: ', str([self.best_inds[1]+0.5,self.best_inds[0]+0.5]))
        plt.xlabel('eps')
        plt.ylabel('min_pts')
        plt.title('neighborhood ari')
    
    def plotAriVarGrid(self):
        '''
        Plots the grid of ari variation values
        '''
        sns.heatmap(pd.DataFrame(self.neighborhood_ari_var, index=self.min_pts_range, columns=self.eps_range), cmap='Greens', annot=False)
        plt.scatter([self.best_inds[1]+0.5],[self.best_inds[0]+0.5], c='#d95f02')
        print('scattering at: ', str([self.best_inds[1]+0.5,self.best_inds[0]+0.5]))
        plt.xlabel('eps')
        plt.ylabel('min_pts')
        plt.title('neighborhood ari variation')

def _kernel1d(side):
    grid = np.arange(side)
    rv = multivariate_normal(mean=(side-1)/2, cov=side/3)
    # rv = multivariate_normal([(side-1)/2, (side-1)/2], [[side/3, 0.], [0., side/3]])
    vals = rv.pdf(grid)
    return vals/vals.sum()

class HDBSCAN_stable():
    '''
        Selects the value of min_cluster_size which gives the clustering with the highest stability,
        meaning that it changes less when changing the parameter.
        In the process computes HDBSCAN labels for all the specified parameters.
        Also computes the grids of ari scores among neighborhood of labels, and the variation of those ari scores.
    '''
    def __init__(self):
        pass

    def copy(self):
        '''
        Returns a copy of this object
        '''
        newone = HDBSCAN_stable()
        newone.ari_median = self.ari_median.copy()
        newone.ari_var = self.ari_var.copy()
        newone.all_labels = self.all_labels.copy()
        newone.min_cluster_size_range = self.min_cluster_size_range
        newone.segment = self.segment
        newone.ordered_params_df = self.ordered_params_df
        newone.best_mcs = self.best_mcs
        newone.best_ind = self.best_ind
        newone.labels_ = self.labels_
        newone.optimal_segment = self.optimal_segment
        return newone
    
    def fit(self, segment: SegmentXYZ, min_cluster_size_range=[10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,220,230,240,250,260,270,300,350,400],
                 n_neighbors=2, n_jobs=8, conv=False, verbose=False, consider_noise=True):
        '''
        Computes labels, ari and ari_var grids.
        Computes the rank of parameter combinations according to stability.
        Saves best labels and a copy of segment with them as clusterIDs.

        Arguments:
        * segment
            SegmentXYZ containing the coodinates on which to run the clustering
        * min_cluster_size_range
            list of min_samples values to provide to HDBSCAN
        * consider_noise
            if False compute the ari just on the points which are not noise in at least one of the two clusterings.
            This may be useful when the majority of points are classified as noise, because it concentrates the comparison on the signal part.
        * n_neighbors
            how far a parameter combination in the grid should be to be considered in the stability computations
        * n_jobs
            how many cpus to use
        * conv
            wheter to apply a blurring on the grid before computing the rank of stability
        
        '''
        
        self.segment = segment
        self.n_jobs = n_jobs

        if(min_cluster_size_range is None):
            self.min_cluster_size_range = [10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,220,230,240,250,260,270,300,350,400]
        else:
            self.min_cluster_size_range = min_cluster_size_range
        
        self.all_labels = HDBSCAN_stable._getLabelsGrid(segment.Getcoord(), self.min_cluster_size_range, verbose, n_jobs)
        self._computeAllFromLabelsGrid(conv, consider_noise, n_neighbors, verbose)
        return self
    
    def _computeAllFromLabelsGrid(self, conv=False, consider_noise=True, n_neighbors=2, verbose=False):
        import hdbscan
        self.ari_median, self.ari_var = HDBSCAN_stable._getGridNeighborhoodAriAndAriVariance(self.all_labels, n_neighbors, verbose, consider_noise)
        
        if(conv):
            processed_ari_median = convolve(self.ari_median, _kernel1d(self.ari_median.shape[0]/3), mode='constant', cval=0.0)
            processed_ari_var = convolve(self.ari_var, _kernel1d(self.ari_var.shape[0]/3), mode='constant', cval=0.0)
        else:
            processed_ari_median = self.ari_median
            processed_ari_var = self.ari_var
        
        self.ordered_params_df = HDBSCAN_stable._getOrderedParametersDf(processed_ari_median, processed_ari_var, self.min_cluster_size_range)
        self.best_ind = int(self.ordered_params_df.iloc[0,:]['min_cluster_size_ind'])
        self.best_mcs = self.min_cluster_size_range[self.best_ind]
        if(self.all_labels.shape[-1] == len(self.segment)):
            self.labels_ = self.all_labels[self.best_ind]
        else:
            self.labels_ = hdbscan.HDBSCAN(min_cluster_size=self.best_mcs, core_dist_n_jobs=self.n_jobs).fit(self.segment.Getcoord()).labels_

        self.optimal_segment = self.segment.copy()
        self.optimal_segment.set_cluster_ids(self.labels_)
    
    def mergeOtherHDBSCANGrid(self, other_scanner,
                            conv=False, consider_noise=True, n_neighbors=2, verbose=0):
        '''
        Integrates the grid of precomputed labels contained in other_scanner into this object.
        Then computes everything else from them.
        Useful when you want to extend the grid without having to recompute the labels that you already have.


        Arguments:
        * *other_scanner*: the scanner (already fitted) to integrate into this one
        * *conv*: see fit()
        * *consider_noise*: see fit()
        * *n_neighbors*: see fit()
        '''
        if(self.all_labels is None):
            raise ValueError('This object was not fitted')
        if(other_scanner.all_labels is None or
           other_scanner.all_labels.shape[0] == 0):
            raise ValueError('Nothing to merge')
        if(not self.segment[['x','y','z']].equals(other_scanner.segment[['x','y','z']])):
            raise ValueError('The two segments\' coordinates don\'t correspond')

        # df_labs_other = pd.DataFrame(other_scanner.all_labels.reshape(1,-1), columns=other_scanner.min_cluster_size_range)
        # df_labs = pd.DataFrame(self.all_labels, columns=self.min_cluster_size_range)

        df_labs_other = pd.DataFrame({i:other_scanner.all_labels.reshape(1,other_scanner.all_labels.shape[0],-1)[:,i].tolist() for i in range(other_scanner.all_labels.shape[0])}) \
            .set_axis(other_scanner.min_cluster_size_range, axis=1)
        df_labs = pd.DataFrame({i:self.all_labels.reshape(1,self.all_labels.shape[0],-1)[:,i].tolist() for i in range(self.all_labels.shape[0])}) \
            .set_axis(self.min_cluster_size_range, axis=1)

        write_mcs = other_scanner.min_cluster_size_range
        
        for e in write_mcs:
            df_labs.loc[:, e] = df_labs_other.loc[:, e]

        # df_labs[df_labs.isna()] = np.random.choice(np.arange(0,10), self.all_labels[0].shape[0])

        where_na = np.where(df_labs.isna())
        for i in range(len(where_na[0])):
            print(where_na[0][i], where_na[1][i])
            df_labs.iloc[:,where_na[1][i]].iloc[where_na[0][i]] = np.random.choice(np.arange(0,10), self.all_labels.shape[-1])
        self.min_cluster_size_range = sorted(list(set(self.min_cluster_size_range).union(set(other_scanner.min_cluster_size_range))))
        self.all_labels = np.stack(df_labs.loc[:, self.min_cluster_size_range].values.flatten().tolist()).reshape(len(self.min_cluster_size_range), len(self.all_labels[0]))

        self._computeAllFromLabelsGrid(conv, consider_noise, n_neighbors, verbose)

        return self

    @staticmethod
    def _getGridNeighborhoodAriAndAriVariance(all_labels, n_neighbors=2, verbose=False, consider_noise=True):
        ari_median = np.zeros(all_labels.shape[0])
        ari_var = ari_median.copy()
        for current_value_ind in (range(all_labels.shape[0])):
            if(verbose):
                print('Working on %ith value of %i'%(current_value_ind, all_labels.shape[0]))
            list_pre = list(range(max(0,current_value_ind-n_neighbors), current_value_ind))
            list_post = list(range(current_value_ind+1, min(all_labels.shape[0], current_value_ind+n_neighbors+1)))
            neighbords_inds = list_pre + list_post
            aris = np.zeros((len(neighbords_inds)))
            for j, current_neigh_ind in enumerate(neighbords_inds):
                if(consider_noise):
                    ari = adjusted_rand_score(all_labels[current_value_ind,:], all_labels[current_neigh_ind,:])
                else:
                    where_no_noise = ((all_labels[current_value_ind,:] != -1) + (all_labels[current_neigh_ind, :] != -1)).astype('bool')
                    ari = adjusted_rand_score(all_labels[current_value_ind,where_no_noise], all_labels[current_neigh_ind,where_no_noise])
                # aris[j] = adjusted_rand_score(all_labels[current_value_ind], all_labels[current_neigh_ind])
                aris[j] = ari
            ari_median[current_value_ind] = np.nanmedian(aris)
            ari_var[current_value_ind] = np.nanmedian(np.absolute(aris - np.nanmedian(aris)))
        return ari_median, ari_var
    
    @staticmethod
    def _getLabelsGrid(coords, min_cluster_size_range=[10,20,30], verbose=False, n_jobs=8):
        import hdbscan
        assert not (coords is None)
        all_labels = np.zeros((len(min_cluster_size_range), coords.shape[0]), dtype='int')
        for current_value_ind, mcs in enumerate(min_cluster_size_range):
            if(verbose):
                print('Working on %ith value of %i'%(current_value_ind, len(min_cluster_size_range)))
            clusterer = hdbscan.HDBSCAN(min_cluster_size=mcs, core_dist_n_jobs=n_jobs)
            all_labels[current_value_ind] = clusterer.fit(coords).labels_
        return all_labels
    
    @staticmethod
    def _getOrderedParametersDf(neighborhood_ari, neighborhood_ari_var, min_cluster_size_range):
        df = pd.DataFrame({'min_cluster_size_ind': np.arange(len(min_cluster_size_range)).astype('int'),
        'min_cluster_size': min_cluster_size_range,
        'ari': neighborhood_ari,
        'ari_var': neighborhood_ari_var})
        order = np.lexsort((-neighborhood_ari_var, neighborhood_ari))[::-1]
        return df.iloc[order,:].reset_index(drop=True)
    
    def saveLog(self, outfile):
        '''
        Saves the ari and ari variation values in a single csv file, in decreasing order of stability
        '''
        assert not self.ordered_params_df is None
        self.ordered_params_df[['min_cluster_size','ari','ari_var']].to_csv(outfile, index=False)
    
    def plotAriGrid(self):
        '''
        Plots the grid of ari values
        '''
        sns.heatmap(pd.DataFrame(self.ari_median.reshape(1,-1), columns=self.min_cluster_size_range), cmap='Greens', annot=False)
        plt.scatter([self.best_ind+0.5],[0.5], c='#d95f02')
        print('scattering at: ', str([self.best_ind+0.5,0.5]))
        plt.xlabel('min_cluster_size')
        plt.title('neighborhood ari')
    
    def plotAriVarGrid(self):
        '''
        Plots the grid of ari var values
        '''
        sns.heatmap(pd.DataFrame(self.ari_var.reshape(1,-1), columns=self.min_cluster_size_range), cmap='Greens', annot=False)
        plt.scatter([self.best_ind+0.5],[0.5], c='#d95f02')
        print('scattering at: ', str([self.best_ind+0.5,0.5]))
        plt.xlabel('min_cluster_size')
        plt.title('neighborhood ari variation')

        

def DBscan(StructureObj,epsi=0,minpoints=100,n_jobs=8):
    """
    The function takes a StructureObj object and performs DBSCAN clustering with user-defined parameters.

    
    Arguments:
    * *StructureObj*: Structure Object to cluster
    * *eps*: integer, epsilons
    * *minpoints*: integer, minimum points
    * *n_jobs*: integer, number of parallel jobs to run during the DBSCAN computation

    
    Return:
        Clustered Structure Object with clusterID assigned.
    """

    xyz=StructureObj.Getcoord()

    clusterer = DBSCAN(eps=epsi, min_samples=minpoints,n_jobs=8).fit(xyz)
    labels=clusterer.labels_

    StructureObj_clusters=_assigneclusterid( labels, StructureObj,homolog="")

    return StructureObj_clusters

def _assigneclusterid( listcluster, segment,homolog=""):
    new_seg = segment.copy()
    new_seg.set_cluster_ids(np.array(listcluster))
    return new_seg
#
def _SelectTopClusters(StructureObj_clusters,timestep=0,pfind=75,plot=True,WriteMRC=False,pathtMRC=""):
    """
    This function takes a StructureObj_clusters object and performs a selection of clusters based on the radius of gyration, number of localizations, and volume.


    Arguments:
    * *StructureObj*: Structure Object to cluster
    * *timestep*: integer, time step to assess
    * *pfind*: integer, quantile to consider
    * *plot*: True, plots relationship betwen radius of gyration, number of localizations, and volume
    * *WriteMRC*: True, write of a MRC file per each cluster identified.
    * *pathtMRC*: directory to save the MRC files.

    
    Return:
         list of selected cluster IDs and a list of properties for all clusters.
    """
    countcl=0
    gyrlist=[]
    selected=[]
    for c,cl in enumerate(list(StructureObj_clusters.split_into_Clusters().values())):
        clusterID_cl=cl.atomList.iloc[0].clusterID
        if (len(cl))>=0:
            if clusterID_cl==-1:
                pass
            else:
                countcl+=1
                m=TB.SR_gaussian_blur(cl, 50., sigma_coeff=1.,mode="unit",filename='test')
                voldens=MF.GetVolume_abovecontour(m)
                gyrlist.append([clusterID_cl,SF.get_rgyration(cl),len(cl),voldens])
                if WriteMRC==True:
                    m.write_to_MRC_file(pathtMRC+"timestep%s_cl%s.mrc"%(timestep,clusterID_cl))
                    print ('write')
    gyr_all=[g[1] for g in gyrlist]
    nloc_all=[g[2] for g in gyrlist]
    voldens_all=[g[3] for g in gyrlist]
    #vol_over_loc=[g[3]/float(g[2]) for g in gyrlist]
    p25_dens = np.percentile(voldens_all, pfind)
    p25_gyr_all = np.percentile(gyr_all, pfind)
    p25_nloc_all = np.percentile(nloc_all, pfind)
    #p25_vol_over_loc = np.percentile(vol_over_loc, pfind)
    print ("tot clusters detected:",countcl)
    countcls=0
    for gi in gyrlist:
        if gi[3]>=p25_dens and gi[2]>=p25_nloc_all and gi[1]>=p25_gyr_all:
            countcls+=1
            print ("clusterID selected:",gi[0])
            selected.append(gi[0])
        #print (gi[4],gi[2])
    print ( "tot clusters detected after filter by Volume N_loc Rgyr:",countcls)
    #gyrlist_ranked=sorted(gyrlist, key=lambda x: (x[1], x[2],x[3]),reverse=True)
    #print ("clusterID gyration localisationLen Vol")
    #for i in gyrlist_ranked:
    #    print (i)

    if plot==True:
        plt.plot(nloc_all,gyr_all,'k.')
        plt.ylabel("Radius of gyration")
        plt.xlabel("Number of localizations")
        plt.axhline(y=p25_gyr_all)
        plt.axvline(x=p25_nloc_all)
        plt.show()
        plt.clf()

        plt.plot(gyr_all,voldens_all,'k.')
        plt.ylabel("Volume")
        plt.xlabel("Radius of gyration")
        plt.axvline(x=p25_gyr_all)
        plt.axhline(y=p25_dens)
        plt.show()
        plt.clf()

        plt.plot(nloc_all,voldens_all,'k.')
        plt.ylabel("Volume")
        plt.xlabel("Number of localizations")
        plt.axvline(x=p25_nloc_all)
        plt.axhline(y=p25_dens)
        plt.show()
        plt.clf()

    return selected,gyrlist


class ThresholdClusterFilter():
    '''
    Attributes:
    * transformed_segment: copy of the input segment from which discarded clusters have been removed
    * retined_cluster_ids: np array containing the retained clusters' ids
    * feats_df: DataFrame containing computed features for all clusters
    '''
    def __init__(self):
        pass

    def fit(self, segment, features_to_use = ['radius_of_gyration', 'volume','numerosity'], method='proportional', fraction=1/5, percentile=75, custom_limits = {}, n_jobs=1, verbose=False):
        '''
        Arguments:
        * segments: Segment to filter
        * features_to_use: which features to use. Any subset of ['radius_of_gyration', 'volume','numerosity']
        * method: 'proportional' or 'percentile' or 'custom'
        * fraction: in case of 'proportional' method, which fraction of the max feature value should be used as limit
        * percentile: in case of 'percentile' method, which percentile of the feature distribution should be used as limit
        * custom_limits: in case of 'custom' method, which limits should be used for the features. It is expected to be a dictionary with feature names as keys and floats as values
        * n_jobs: how many cpus to use for the computation

        
        Returns:
        * None

        
        '''
        if(verbose): print('ThresholdClusterFilter: starting')
        features_to_use = list(set(features_to_use).intersection(set(['volume','radius_of_gyration','numerosity'])))
        self.features_to_use = features_to_use
        seg = segment.removeNoise()
        if(seg is None):
            return seg
        labels = seg.atomList['clusterID'].values
        if(verbose): print('ThresholdClusterFilter: splitting clusters')
        dict1 = seg.split_into_Clusters(verbose=max(0,verbose-1))
        cl_ids = list(dict1.keys())
        cl_segs = list(dict1.values())
        if(verbose): print('ThresholdClusterFilter: computing features')
        feats_df = WF.getSegmentsFeatures(cl_segs,
                                            features=features_to_use,
                                            prec_mean=50,
                                            factor=None,
                                            threshold=0.5,
                                            verbose=True,
                                            n_jobs=n_jobs)
        if(verbose): print('ThresholdClusterFilter: computed features')
        feats_df = feats_df.assign(clusterID=cl_ids).set_index('clusterID', drop=True)
        self.feats_df = feats_df

        if(method == 'proportional'):
            limits = {
                f: feats_df[f].max()*fraction
                for f in features_to_use
            }
        elif(method == 'percentile'):
            limits = {
                f: np.percentile(feats_df[f].values, percentile)
                for f in features_to_use
            }
        elif(method == 'custom'):
            assert(set(custom_limits.keys()) == set(features_to_use))
            limits = custom_limits
        else:
            raise ValueError('Method not supported')
        
        self.limits = limits
        where_retain = np.stack([
                (feats_df[f].values>=limits[f]).astype('bool')
                for f in features_to_use
            ], axis=1)
        where_retain = np.all(where_retain, axis=1).flatten()
        self.where_retain = where_retain

        retained_clusters_ids = feats_df.index.values[where_retain]
        self.retained_clusters_ids = retained_clusters_ids

        self.transformed_segment = seg.getClusters(retained_clusters_ids)
        old_labels = segment.atomList.clusterID.values
        where_signal = np.vectorize(lambda c: c in self.retained_clusters_ids)(old_labels)
        self.new_labels = old_labels.copy()
        self.new_labels[np.invert(where_signal)] = -1

    def plot(self, label_clusters=False, show_all=False):
        '''
        Display plots representing the clusters features and which have been filtered out.

        Arguments:

        *
        '''
        plt.figure(figsize=(5*(3 if len(self.features_to_use)==3 else 1), 5))
        i=0

        where_to_show = self.where_retain.copy()
        if(show_all):
            where_to_show[:] = True


        if('numerosity' in self.features_to_use and 'radius_of_gyration' in self.features_to_use):
            i+=1
            plt.subplot(1,len(self.features_to_use),i)
            sns.scatterplot(data=self.feats_df, x='numerosity', y='radius_of_gyration')
            plt.axvline(x=self.limits['numerosity'], ls='--')
            plt.axhline(y=self.limits['radius_of_gyration'], ls='--')
            if(label_clusters):
                Visualization.addLabelsOnPlot(plt.gca(), self.feats_df['numerosity'][where_to_show], self.feats_df['radius_of_gyration'][where_to_show], self.feats_df.index.values[where_to_show])

        if('radius_of_gyration' in self.features_to_use and 'volume' in self.features_to_use):
            i+=1
            plt.subplot(1,len(self.features_to_use),i)
            sns.scatterplot(data=self.feats_df, x='radius_of_gyration', y='volume')
            plt.axvline(x=self.limits['radius_of_gyration'], ls='--')
            plt.axhline(y=self.limits['volume'], ls='--')
            if(label_clusters):
                Visualization.addLabelsOnPlot(plt.gca(), self.feats_df['radius_of_gyration'][where_to_show], self.feats_df['volume'][where_to_show], self.feats_df.index.values[where_to_show])

        if('numerosity' in self.features_to_use and 'volume' in self.features_to_use):
            i+=1
            plt.subplot(1,len(self.features_to_use),i)
            sns.scatterplot(data=self.feats_df, x='numerosity', y='volume')
            plt.axvline(x=self.limits['numerosity'], ls='--')
            plt.axhline(y=self.limits['volume'], ls='--')
            if(label_clusters):
                Visualization.addLabelsOnPlot(plt.gca(), self.feats_df['numerosity'][where_to_show], self.feats_df['volume'][where_to_show], self.feats_df.index.values[where_to_show])
                
        if(len(self.features_to_use) == 1):
            f= self.features_to_use[0]
            sns.scatterplot(data=self.feats_df, x=0, y=f)
            plt.axhline(self.limits[self.features_to_use[0]], ls='--', c='red')
            plt.gca().annotate('threshold', (-0.05, self.limits[self.features_to_use[0]]*1/5+50), color='red')
            plt.xticks([])
            np.random.seed(6)
            if(label_clusters):
                Visualization.addLabelsOnPlot(plt.gca(), [0]*where_to_show.sum(), self.feats_df[f][where_to_show], self.feats_df.index.values[where_to_show])
    
    def writeMRCs(self, path, filename_pattern='cluster{}', verbose=False):
        for c, s in self.transformed_segment.split_info_Clusters():
            if(verbose):
                print('Starting cluster', str(c))
            m = TB.SR_gaussian_blur(s, 50, 1)
            p = filename_pattern.replace('{}',str(c))
            m.write_to_MRC_file(path+'/'+p+'.mrc')


def _spreadLabels(coords, labels, radius=90, n_jobs=1):
    '''
    Spread labels==1 by connectivity
    
    Arguments:
    * coords: coordinated which the labels refer to
    * labels: labels to be spread. Should have just 0 and 1 values
    * radius: at which maximum distance a coordinate should be so that the spread reaches it
    * n_jobs: how many cpus are to be used for the computation

    
    Returns:
    * copy of labels in which the labels==1 have been spread
    '''
    graph = NearestNeighbors(radius=radius, n_jobs=n_jobs).fit(coords).radius_neighbors_graph(mode='connectivity').toarray()
    beaditude = graph.T @ labels
    beaditude = beaditude + labels
    beaditude = (beaditude>0).astype('int')
    return beaditude


def _buildAdjacencyMatrixFromPointCloud(coords, max_radius=25, weighted=False, verbose=False):
    '''
    Return:
        csr_matrix with connection weights (just 1,0 if weighted = false)
        on both upper and lower triangle.
    '''
    from sklearn.neighbors import BallTree
    from scipy import sparse

    tree = BallTree(coords, leaf_size=10)
    inds, dists = tree.query_radius(coords, max_radius, return_distance=True)
    if weighted: max_dist = np.concatenate(dists, axis=0).max()
    if(verbose): print('Completed Sklearn BallTree')
    mat = sparse.dok_matrix((len(coords), len(coords)))
    for i in range(len(coords)):
        if(verbose):
            if(i%1000==0): print(i)
        mat[i,inds[i]] = (1 - dists[i]/max_dist) if weighted else 1
    
    mat.setdiag(np.zeros(mat.shape[0]))
    mat2 = sparse.csr_matrix(mat)

    return mat2


class _Louvain_on_point_cloud():
    def __init__(self, resolution=1., modularity_function='newman',
            network_max_radius=25, weighted=False, verbose=False):
        self.resolution = resolution
        self.modularity_function = modularity_function
        self.network_max_radius = network_max_radius
        self.weighted = weighted
        self.verbose  = verbose
        pass

    def fit(self, coords=None, adj_mat=None):
        assert not ((coords is None) and (adj_mat is None))
        from sknetwork.clustering import Louvain
        
        if(not coords is None):
            adj_mat = _buildAdjacencyMatrixFromPointCloud(coords, max_radius=self.network_max_radius,
                                                         weighted=self.weighted, verbose=self.verbose)
            if(self.verbose): print('Built adjacency matrix')

        algorithm = Louvain(modularity=self.modularity_function,
                    resolution=self.resolution)

        self.labels_ = algorithm.fit_predict(adj_mat)
        return self