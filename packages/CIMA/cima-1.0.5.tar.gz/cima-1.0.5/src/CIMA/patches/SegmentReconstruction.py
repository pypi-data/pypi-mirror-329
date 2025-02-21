#===============================================================================
#     This file is part of CIMA.
#     
#     CIMA is a software designed to help the user in the manipulation 
#     and analyses of genomic super resolution localisation data. 
#     
#      Copyright  2019-2023 
#
#                Authors: Irene Farabella, Ivan Piacere
# 
#     This file contains code to reconstruct a segment from multiple information sources.
#     If you have a localization file from a multi-walk experiment and you already have run clustering on all the timepoints,
#     you can use getLociMapsFromFullWalkSegment to obtain a density map for each locus in the experiment.
#     If you have SMLM localization for a whole segment and Diffraction Limited patches of it, you can use getLociMapsFromLocalizationsVsDL.
#     If you have density maps about the same segment from two different sources and want cross those informations to locate your loci,
#     you can use the more general getClusterMatches.
#     
#===============================================================================

import pandas as pd
import numpy as np
from CIMA.maps.ScoringFunctions import ScoringFunctions
from CIMA.maps.MapFeatures import _match_grid
from CIMA.segments.SegmentGaussian import TransformBlurrer
from CIMA.segments.SegmentInfo import Segment
from CIMA.segments.SegmentInfoXYZ import SegmentXYZ
from CIMA.detection import clusters as CL
from CIMA.maps.MapFeatures import *
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns
import sys
import time
from scipy.stats import entropy



class Decoder():
    '''
    Decodes a hierarchical barcoding experiment by following the provided patching scheme.
    To obtain the decoded segment (with loci ids in the clusterID column) first create a Decoder object (decoder = Decoder()),
    then call fit() with the appropriate parameters and finally get the segment from the object's loci_segment attribute.
    '''

    def __init__(self):
        self.fitted = False

    def fit(self, phase1_segments, phase2_segments, walk_loci_matrix, comparison_measure='overlap_iofirst', n_jobs=4, verbose=1):
        '''
        Arguments:
        * full_segment: segment obtained from the localizations file of a walk
        * phase1_tpoints: list of int, the timepoints of the phase1
        * phase2_tpoints: list of int, the timepoints of the phase2
        * clustering_labels: list of numpy arrays identifying the clusters and the noise among the localizations of each timepoint
        * walk_loci_matrix: numpy array of shape (len(phase1_tpoints), len(phase2_tpoints)) of type 'int'.
            Defines at the intersection of which phase1 and phase2 timepoints each genomic locus lies.
            Values inside the matrix are considered as loci ids. Values 0 indicate absence of loci at that intersection.
        * comparison_threshold: float, the comparison score value above which a cluster is considered to match the patch
        * comparison_measure: function accepting two maps and returning a float. The measure to use to compare maps
        * comparison_matrix_save_folder: where to save matrices with comparison results. If None they are not saved.
        * maps_save_folder: where to save maps with comparison results. If None they are not saved.
        * chr_id: which of the chromosomes (possibly homologs) to consider. If None it is assumed that just one element is present.

            
        Attributes:
        * loci_segment: the decoded segment
        * comparison_mats: matrices representing comparisons between cluster maps and macropatches maps
        * localizations_classification: DataFrame representing the estimated probability of a localization to come from each of the loci, or neither of them
        '''

        self.walk_loci_matrix = walk_loci_matrix
        self.fitted = True
        
        assert(self.walk_loci_matrix.shape[0] == len(phase1_segments))
        assert(self.walk_loci_matrix.shape[1] == len(phase2_segments))
        
        if verbose: print('Removing noise')
        phase1_segments = [seg.removeNoise() for seg in phase1_segments]
        phase2_segments = [seg.removeNoise() for seg in phase2_segments]
        self.phase1_segments = phase1_segments
        self.phase2_segments = phase2_segments


        if verbose: print('Splitting by clusterIds and computing single cluster maps')
        phase1_sub_segments = [[] for t in phase1_segments]
        phase1_maps = [[] for t in phase1_segments]
        jobs = [[] for t in phase1_segments]

        import multiprocessing as mp
        pool = mp.Pool(n_jobs)
        for itpoint, _ in enumerate(phase1_segments):
            jobs[itpoint] = pool.apply_async(Decoder._getSegsAndMapsForTimepoint, [phase1_segments[itpoint]])
        for itpoint, _ in enumerate(phase1_segments):
            res = jobs[itpoint].get()
            phase1_sub_segments[itpoint] = res[0]
            phase1_maps[itpoint] = res[1]

        
        phase2_maps = []
        for itpoint, _ in enumerate(phase2_segments):
            if(not phase2_segments[itpoint] is None):
                current_map = TransformBlurrer().SR_gaussian_blur(phase2_segments[itpoint], 50, 1)
                phase2_maps.append(current_map)
            else:
                phase2_maps.append(None)
            

        # matching_clusters_ids = getClusterMatches(phase1_maps, phase2_maps, walk_loci_matrix>0, comparison_measure, comparison_threshold, comparison_matrix_save_folder, n_jobs, verbose>0)
        if verbose: print('Computing comparisons')
        self.comparison_mats_overlap = Decoder._computeComparisonsForAllTimepointsParallel(phase1_maps, phase2_maps, self.walk_loci_matrix>0, comparison_measure='overlap_iofirst', n_jobs=n_jobs, verbose=verbose)
        # self.comparison_mats_ccc = Decoder.computeComparisonsForAllTimepointsParallel(phase1_maps, phase2_maps, self.walk_loci_matrix>0, comparison_measure='ccc', n_jobs=n_jobs, verbose=verbose)
        if(comparison_measure=='overlap_iofirst'):
            # TODO: move this to parameter of this function
            comparison_score_minimum = 0.0
            comparison_mats = self.comparison_mats_overlap
        elif(comparison_measure=='ccc'):
            comparison_score_minimum = -1.0
            comparison_mats = self.comparison_mats_ccc
        else:
            raise ValueError('Comparison measure not supported')
        
        self.comparison_mats = self.comparison_mats_overlap

        if verbose: print('Finding matching clusters')

        self.walk_loci_segs = {i:None for i in set(self.walk_loci_matrix.flatten()) - set([0])}
        full_cleaned_seg = phase1_segments[0]._combine_segments(phase1_segments[1:])
        self.reconstruction_segment = full_cleaned_seg
        self.localizations_classification = pd.DataFrame(np.zeros((len(full_cleaned_seg), len(self.walk_loci_segs))), columns=['locus_%i'%l for l in list(self.walk_loci_segs.keys())])
        self.localizations_classification[['timepoint','clusterID']] = full_cleaned_seg.atomList[['timepoint', 'clusterID']].values

        for t in range(len(comparison_mats)):
            for ci, c in enumerate(np.unique(phase1_segments[t].atomList['clusterID'])):
                for wi, w in enumerate(np.arange(self.walk_loci_matrix.shape[1])[self.walk_loci_matrix[t]!=0]):
                    self.localizations_classification.loc[
                        ((self.localizations_classification['timepoint']==t+1) * (self.localizations_classification['clusterID']==c)).astype('bool'),
                        'locus_%i'%self.walk_loci_matrix[t,w]] = \
                            comparison_mats[t][ci,wi]
        
        selected_cols_just_loci = ['locus_%i'%l for l in list(self.walk_loci_segs.keys())]
        selected_cols_all = selected_cols_just_loci + ['locus_none']
        summa = self.localizations_classification[selected_cols_just_loci].sum(axis=1)
        self.localizations_classification['locus_none'] = (summa==0.0).astype('float')
        self.localizations_classification[selected_cols_all] = self.localizations_classification[selected_cols_all]/self.localizations_classification[selected_cols_all].values.sum(axis=1).reshape(-1,1)
        self.localizations_classification['entropy'] = entropy(self.localizations_classification[selected_cols_all], axis=1)
        self.localizations_classification['normalized_entropy'] = self.localizations_classification['entropy']/np.log(len(selected_cols_all))
                        

        self.matching_clusters_ids = [[[] for _ in range(len(phase2_maps))] for _ in range(len(phase1_maps))]
        self.avg_comparison_score = np.zeros((len(phase1_maps), len(phase2_maps)))
        self.just_peaks_comparison_matrices = []
        for t1i, _ in enumerate(phase1_maps):
            just_peaks_comparison_matrix = Decoder._getMatrixWithJustRowsPeaks(comparison_mats[t1i], fill_value=comparison_score_minimum - 1.0)
            self.just_peaks_comparison_matrices.append(just_peaks_comparison_matrix)
            interested_phase2_tpoints = np.where((self.walk_loci_matrix>0)[t1i])[0]
            for t2i, t2 in enumerate(interested_phase2_tpoints):
                matching_clusters_ids_list = [i for i,_ in enumerate(phase1_maps[t1i]) if just_peaks_comparison_matrix[i,t2i]>comparison_score_minimum]
                self.matching_clusters_ids[t1i][t2] = matching_clusters_ids_list
                if len(just_peaks_comparison_matrix)>0 and np.any(just_peaks_comparison_matrix[:,t2i]>comparison_score_minimum):
                    self.avg_comparison_score[t1i][t2] = just_peaks_comparison_matrix[just_peaks_comparison_matrix[:,t2i]>comparison_score_minimum, t2i].mean() 
                else:
                    self.avg_comparison_score[t1i][t2] = 0.0


        if verbose: print('Extracting matching segments')


        for locus_ind in set(self.walk_loci_matrix.flatten()) - set([0]):
            where_inds = np.where(self.walk_loci_matrix == locus_ind)
            t1, t2 = where_inds[0][0], where_inds[1][0]
            clusters_ids = self.matching_clusters_ids[t1][t2]
            segments = [phase1_sub_segments[t1][c] for c in clusters_ids]
            
            if(len(segments)>0):
                joint_seg = segments[0]._combine_segments(segments[1:])
                self.walk_loci_segs[locus_ind] = joint_seg
        
        tempseg = Decoder()._getLociSegment(self.walk_loci_segs)
        # Create a decoding segment of the same class as the input segments
        self.loci_segment = phase1_segments[0].copyWithNewContent(tempseg.atomList)

        

        return self
    
    def load(self, loci_segment, walk_loci_matrix, localizations_classification):
        '''
        Fill the Decoder with precomputed data.
        This is useful for diplaying decoding results for a decoding performed in the past.
        '''
        if(self.fitted):
            raise ValueError('Decoder object already fitted, create and use a new one')
        self.loci_segment = loci_segment
        self.walk_loci_matrix = walk_loci_matrix
        self.localizations_classification = localizations_classification


    @staticmethod
    def _getLociSegment(locus_to_seg_dict):
        coords_list = []
        for lid, lseg in locus_to_seg_dict.items():
            if(not lseg is None):
                s2 = lseg.copy()
                # s2.set_cluster_ids(lid)
                s2.atomList['locusID'] = lid
                coords_list.append(s2)
        return coords_list[0]._combine_segments(coords_list[1:])
    
    def plotEfficacyTable(self):
        '''
        Plot the efficacy table coloring the found loci according to their relative position on the chromosome
        '''
        eff_mat = Decoder._getEfficacyTableFromFoundLoci(self.loci_segment['locusID'].unique(), walk_loci_matrix=self.walk_loci_matrix)
        Decoder._showEfficacyMat(eff_mat, self.walk_loci_matrix, cmap_on_found='bwr')
    
    def plotEfficacyTableWithUncertainty(self):
        '''
        Plot the efficacy table coloring the found loci according to the average uncertainty of the assignment of localizations to the locus.
        '''
        uncertainty_mat = Decoder._getUncertaintyMatFromLocalizationClassificationDf(self.walk_loci_matrix, self.localizations_classification)
        # uncertainty_mat = uncertainty_mat/_getMaxEntropy(np.sum(self.walk_loci_matrix!=0)+1)
        eff_mat = Decoder._getEfficacyTableFromFoundLoci(self.loci_segment['locusID'].unique(), walk_loci_matrix=self.walk_loci_matrix)
        Decoder._showEfficacyMat(eff_mat, self.walk_loci_matrix, custom_coloring_matrix=uncertainty_mat, cmap_on_found='bwr')
    
    def plotEfficacyTableWithVolume(self, max_expected_vol=None, verbose=False, precomputed_vols=None):
        '''
        Plot the efficacy table coloring the found loci according to its volume.
        '''
        vols_mat = np.zeros(self.walk_loci_matrix.shape)
        if(precomputed_vols is None):
            precomputed_vols = {}
            i = -1
            for lid, s in self.loci_segment.split_into_Clusters().items():
                i+=1
                if(verbose):
                    print('%i/%i'%(i, len(list(self.loci_segment.split_into_Clusters().values()))))
                m = TransformBlurrer().SR_gaussian_blur(s, 50, 1)
                precomputed_vols[lid] = GetVolume_abovecontour(m, 0.5)
        for lid, s in self.loci_segment.split_into_Clusters().items():
            vols_mat[self.walk_loci_matrix==lid] = precomputed_vols[lid]
        if(max_expected_vol == None):
            max_expected_vol = max(list(precomputed_vols.values()))
        vols_mat = vols_mat/max_expected_vol
        eff_mat = Decoder._getEfficacyTableFromFoundLoci(self.loci_segment['locusID'].unique(), walk_loci_matrix=self.walk_loci_matrix)
        Decoder._showEfficacyMat(eff_mat, self.walk_loci_matrix, custom_coloring_matrix=vols_mat, cmap_on_found='bwr', found_min_val=0.0, found_max_val='%.2g'%max_expected_vol)

    @staticmethod
    def _getUncertaintyMatFromLocalizationClassificationDf(walk_loci_matrix, localizations_classification):
        uncertainty_mat = np.zeros(walk_loci_matrix.shape)
        for lid in set(np.unique(walk_loci_matrix.flatten())) - set([0]):
            if(np.any(localizations_classification['locusID']==lid)):
                mentropy = localizations_classification.loc[localizations_classification['locusID']==lid,'normalized_entropy'].mean()
                uncertainty_mat[walk_loci_matrix==lid] = mentropy
            else:
                uncertainty_mat[walk_loci_matrix==lid] = 0.0
        
        return uncertainty_mat
    
    
    def getEfficacy(self):
        '''
        Returns the efficacy (float) of the decoding
        '''
        effmat = Decoder._getEfficacyTableFromFoundLoci(self.loci_segment['locusID'].unique(), self.walk_loci_matrix)
        _, _, eff = Decoder._getEfficacyValuesFromMat(effmat)
        return eff

    @staticmethod
    def _getEfficacyTableFromFoundLoci(loci_list, walk_loci_matrix):
        efficacy_mat = np.ones(walk_loci_matrix.shape, dtype='int')*0.5
        efficacy_mat[walk_loci_matrix==0] = 0
        for l in loci_list:
            efficacy_mat[walk_loci_matrix==l] = 1
        return efficacy_mat


    @staticmethod
    def _showEfficacyMat(efficacy_mat, walk_loci_matrix, custom_coloring_matrix=None, cmap_on_found='bwr', found_min_val=None, found_max_val=None):
        '''
        Arguments:
        * custom_coloring_matrix: matrix of same shape as walk_loci_matrix containing custom values (between 0.0 and 1.0) to be used for coloring the loci
        '''
        cell_side = 1
        fig = plt.figure(figsize=(efficacy_mat.shape[1]*cell_side,efficacy_mat.shape[0]*cell_side))
        colors = np.vstack((
            (np.array([171, 164, 164, 256])/256).reshape((1,-1)).repeat(85,axis=0),
            # (np.array([219, 123, 123, 256])/256).reshape((1,-1)).repeat(84,axis=0),
            (np.array([0, 0, 0, 256])/256).reshape((1,-1)).repeat(84,axis=0),
            (np.array([157, 230, 145, 256])/256).reshape((1,-1)).repeat(86,axis=0) if (cmap_on_found is None) else plt.get_cmap(cmap_on_found)(np.linspace(0, 1, 86)),
                            ))
        
        newcmp = mcolors.LinearSegmentedColormap.from_list('my_colormap', colors)
        
        if(cmap_on_found is None):
            temp_mat = efficacy_mat.copy()
        else:
            temp_mat = efficacy_mat.copy()
            if(not custom_coloring_matrix is None):
                assert type(custom_coloring_matrix) == type(np.array(10)) and custom_coloring_matrix.shape == walk_loci_matrix.shape
                minim = 0.0
                maxim = 1.0
                temp_mat[efficacy_mat==1] = ((custom_coloring_matrix[efficacy_mat==1]-minim)/(maxim-minim))*(1/3) + (2/3)
                temp_mat[efficacy_mat==1] = np.clip(temp_mat[efficacy_mat==1], 0.0, 1.0)
            else:
                minim = 1.0
                maxim = walk_loci_matrix.max()
                temp_mat[efficacy_mat==1] = ((walk_loci_matrix[efficacy_mat==1]-minim)/(maxim-minim))*(1/3) + (2/3)
        temp_mat = pd.DataFrame(temp_mat, index=np.arange(1,temp_mat.shape[0]+1).astype('int'), columns=np.arange(1,temp_mat.shape[1]+1).astype('int'))
        if(found_min_val is None): found_min_val=minim
        if(found_max_val is None): found_max_val=maxim
            
        sns.heatmap(temp_mat, annot=Decoder._stringZeroToEmpty(walk_loci_matrix.astype('int').astype('str')), cmap=newcmp, vmin=0.0, vmax=1.0, fmt='')
        plt.gca().collections[0].colorbar.set_ticks(ticks=[1/6,3/6,5/6,2/3,3/3], labels=['non existent','missed','found', str(found_min_val), str(found_max_val)], rotation=90)
        fig.suptitle('Efficacy %i/%i = %.2f'%(Decoder._getEfficacyValuesFromMat(efficacy_mat)))
        return fig
    
    @staticmethod
    def _stringZeroToEmpty(arr):
        arrc = arr.copy()
        arrc[arrc=='0'] = ''
        return arrc
    
    @staticmethod
    def _getEfficacyValuesFromMat(efficacy_mat):
        '''
        Returns:
            . num of found items
            . num of searched items
            . percentage of found among searched
        '''
        sum2 = (efficacy_mat==1).sum()
        sum1 = (efficacy_mat==0.5).sum()
        sum0 = (efficacy_mat==0).sum()
        return sum2, sum2+sum1, sum2/(sum2+sum1)

        


    @staticmethod
    def _computeComparisonsForAllTimepointsParallel(phase1_maps, phase2_maps, comparison_matrix, comparison_measure='overlap', n_jobs=4, verbose=False):
        '''
        Arguments:
            *phase1_maps*: is a list of lists of maps. Each nested list represents a timepoint.
                Each map represents a cluster detected in that timepoint.
            *phase2_maps*: is a list of maps. Each map represents a macro patch
            *comparison_matrix*: is a boolean matrix in which the True cells represent the comparisons that should be performed
            *comparison_measure*: function accepting two maps and returning a float. The measure to use to compare maps

        Return:
            a list with a numpy array for each timepoint, representing the comparison results
            between all the clusters (phase1) detected in that timepoint
            and all the required patches (phase2). The requirement of a patch is codified in comparison_matrix
        '''

        from multiprocessing import Pool
        import multiprocessing as mp
        pool = Pool(processes=n_jobs)
        comparison_mats = [None for _ in range(len(phase1_maps))]
        results = [None for _ in range(len(phase1_maps))]

        for tpoint in range(len(phase1_maps)):
            if verbose: print('started tpoint: %i with size %i'%(tpoint, len(phase1_maps[tpoint])))
            interested_phase2_tpoints = np.where(comparison_matrix[tpoint]==True)[0]
            selected_phase2_maps = [m for i,m in enumerate(phase2_maps) if i in interested_phase2_tpoints]
            
            results[tpoint] = pool.apply_async(Decoder._getMapsVsMapsComparisonMatrix,
                                            (phase1_maps[tpoint],selected_phase2_maps, comparison_measure, verbose, 'Timepoint '+str(tpoint)))
        for tpoint in range(len(phase1_maps)):
            comparison_mats[tpoint] = results[tpoint].get()
        return comparison_mats
    
    @staticmethod
    def _getMapsVsMapsComparisonMatrix(maps1, maps2, comparison_measure='overlap_ios', verbose=False, job_identifier=''):
        """
        Arguments:
            *comparison_measure*: function accepting two maps and returning a float. The measure to use to compare maps.
                It can also be a string, specifying which of the predefined functions to use.
        Return:
            a numpy array of shape (len(maps1),len(maps2)) containing the comparison score between each combination of the two lists of maps.

        This is useful for example when comparing a timepoint's clusters with a macro patch.
        """
        if(comparison_measure == 'overlap_ios' or comparison_measure == 'overlap'):
            # comparison_measure = lambda map1, map2: ScoringFunctions().CCC_map(map1,map2, mode=2, map_target_threshold=0.001,map_probe_threshold=0.001, overlap_type='ios')[1]
            comparison_measure = lambda map1, map2: ScoringFunctions.getMapsOverlap(map1,map2, map_target_threshold=0.001,map_probe_threshold=0.001, overlap_type='ios')
        elif(comparison_measure == 'overlap_iou'):
            comparison_measure = lambda map1, map2: ScoringFunctions().getMapsOverlap(map1,map2, map_target_threshold=0.001,map_probe_threshold=0.001, overlap_type='iou')
        elif(comparison_measure == 'overlap_iob'):
            comparison_measure = lambda map1, map2: ScoringFunctions().getMapsOverlap(map1,map2, map_target_threshold=0.001,map_probe_threshold=0.001, overlap_type='iob')
        elif(comparison_measure == 'overlap_iofirst'):
            comparison_measure = lambda map1, map2: ScoringFunctions().getMapsOverlap(map1,map2, map_target_threshold=0.001,map_probe_threshold=0.001, overlap_type='iofirst')
        elif(comparison_measure == 'overlap_iosecond'):
            comparison_measure = lambda map1, map2: ScoringFunctions().getMapsOverlap(map1,map2, map_target_threshold=0.001,map_probe_threshold=0.001, overlap_type='iosecond')
        elif(comparison_measure == 'ccc'):
            comparison_measure = lambda map1, map2: ScoringFunctions().CCC_map(map1,map2, mode=2, map_target_threshold=0.001,map_probe_threshold=0.001, meanDist=True)[0]
        score_matrix = np.zeros((len(maps1), len(maps2)))
        for ci, c in enumerate(maps1):
            for pi, p in enumerate(maps2):
                if((c is None) or (p is None)):
                    score_matrix[ci,pi] = 0.0
                else:
                    start_time = time.time()
                    m1, m2 = _match_grid(c,p)
                    start_time = time.time()
                    score_matrix[ci,pi] = comparison_measure(m1,m2)
            if(verbose):
                print('%s: Completed map: %i/%i'%(job_identifier, ci, len(maps1)))
        return score_matrix
    
    @staticmethod
    def _getSegsAndMapsForTimepoint(tpoint_segment):
        clusters_segments = list(tpoint_segment.split_into_Clusters().values()) if not tpoint_segment is None else []
        segs = []
        maps = []
        for ci, cluster_segment in enumerate(clusters_segments):
            segs.append(cluster_segment)
            current_map = TransformBlurrer().SR_gaussian_blur(cluster_segment, 50, 1)
            # if(not maps_save_folder is None): current_map.write_to_MRC_file(maps_save_folder + '/tphase1(%i)_c(%i).mrc'%(itpoint, ci))
            maps.append(current_map)
        
        return (segs, maps)
    
    @staticmethod
    def _getMatrixWithJustRowsPeaks(matrix, fill_value=0.0):
        '''
            Arguments:
                *matrix*: a 2-d numpy array
            Return:
                a copy of matrix with all the cells that are not a row-max substituted by fill_value.
                In case of multiple maximums just the first is selected.
        '''
        just_peaks_matrix = np.full(matrix.shape, fill_value, dtype='float')
        where_max = matrix.argmax(axis=1)
        just_peaks_matrix[np.arange(just_peaks_matrix.shape[0]), where_max] = matrix[np.arange(just_peaks_matrix.shape[0]), where_max]
        return just_peaks_matrix

        


def _getMaxEntropy(length):
    return entropy(np.full(length, 1.0/length))