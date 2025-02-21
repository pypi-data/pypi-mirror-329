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

from CIMA.segments.SegmentGaussian import TransformBlurrer
from CIMA.segments.SegmentInfo import Segment
from CIMA.maps import MapFeatures as MF
from CIMA.maps import MapSpatialFeatures as MSF
from CIMA.segments import SegmentFeatures as SF
from CIMA.parsers import ParserCSV as Parser
from CIMA.maps import DensityProprieties as DS
import os
import numpy as np
import pandas as pd
#from tqdm import tqdm
TB=TransformBlurrer()


def _read3DF(pathin="",chr_list=[]):
	f_list=[]
	f_list_volumes=[]
	chrmlist=[]
	seg_pass=[]
	for f in os.listdir(pathin):
		if f.startswith("3Dsegments_") and f.endswith("IMGRanalysis.txt"):#3Dsegments_Chr82018-09-04_L03_A_IMGRanalysis.txt
			locflag=f.split("_")[1]
			nuclei=f.split("_")[2]
			chrom=locflag.split('2')[0].replace('b','').replace('chr','Chr')
			if chrom in chr_list:
				hom=f.split("_")[3]
				fop=open(pathin+f,"r")
				lines=fop.readlines()
				plist=[]
				for i in lines[1:]:
					ll=[i for i in i.strip().split(",")]
					ll.append(hom)
					ll.append(locflag)
					ll.append(chrom)
					ll[0]=nuclei
					f_list.append(ll)
	return [f_list_volumes,f_list]

def getSegmentMetadata(seg):
    '''
    Arguments:
    * seg: Segment

    Return:
    * a dictionary with all the metadata of seg
    '''
    d1 = seg.metadata
    d2 = {s: seg.atomList[s].unique()[0] for s in ['chromosome','homolog','timepoint','clusterID']\
           if (s in seg.atomList.columns and len(seg.atomList[s].unique())==1)}
    return {**d1,**d2}

def getSegmentsMetadata(segs):
    '''
    Arguments:
    * segs: a list of Segments objects


    Return:
    * a DataFrame with each row containing metadata for a segment.
    If a metadata is =None for all the segments, the correspnding column will not be present in the DataFrame
    
    '''
    metadataDf = pd.DataFrame([getSegmentMetadata(s) for s in segs]).dropna(axis=1, how='all')
    metadataDf.index += 1
    return metadataDf

def getSegmentFeatures(seg, map, features='all', threshold=0.5, verbose=False):
    '''
    Returns a dictionary with the specified features computed on seg or map at the specified threshold

    Arguments:
    * seg: Segment on which to compute features
    * map: Map that is expected to be computed from seg
    * features: which features to compute. Use string 'all' to compute all the available ones
    * threshold: used to specify the threshold
    '''
    if(features == 'all'):
        features = ['volume', 'area', 'sphericity_bribiesca', 'sphericity',
                    'radius_of_gyration', 'point_cloud_ellipticity', 'point_cloud_eccentricity',
                    'mvee_ellipticity', 'mvee_eccentricity',
					'solidity', 'holeless_solidity','numerosity']
    f_dict = {}
    f_dict['timepoint'] = seg.atomList['timepoint'].values[0]
    if('volume' in features):
        if(verbose): print('computing volume')
        f_dict['volume'] = MF.GetVolume_abovecontour(map, threshold)
    if('area' in features):
        if(verbose): print('computing area')
        f_dict['area'] = MF.GetArea_abovecontour(map, threshold)
    if('sphericity_bribiesca' in features):
        if(verbose): print('computing sphericity_bribiesca')
        f_dict['sphericity_bribiesca'] = MF.GetSphericity_bribiesca(map, threshold)
    if('sphericity' in features):
        if(verbose): print('computing sphericity')
        f_dict['sphericity'] = MF.GetSphericity(map, threshold)
    if('radius_of_gyration' in features):
        if(verbose): print('computing radius_of_gyration')
        f_dict['radius_of_gyration'] = SF.get_rgyration(seg)
    if('point_cloud_ellipticity' in features):
        if(verbose): print('computing point_cloud_ellipticity')
        f_dict['point_cloud_ellipticity'] = SF.GetEllipticity(seg, verbose=False)
    if('point_cloud_eccentricity' in features):
        if(verbose): print('computing point_cloud_eccentricity')
        f_dict['point_cloud_eccentricity'] = SF.GetEccentricity(seg, verbose=False)
    if('mvee_ellipticity' in features):
        if(verbose): print('computing mvee_ellipticity')
        f_dict['mvee_ellipticity'] = SF.getMVEEEllipticity(seg)
    if('mvee_eccentricity' in features):
        if(verbose): print('computing mvee_eccentricity')
        f_dict['mvee_eccentricity'] = SF.getMVEEEccentricity(seg)
    if('solidity' in features):
        if(verbose): print('computing solidity')
        f_dict['solidity'] = MF.getSolidity(map, threshold)
    if('holeless_solidity' in features):
        if(verbose): print('computing holeless_solidity')
        f_dict['holeless_solidity'] = MF.getHolelessSolidity(map, threshold)
    if('numerosity' in features):
        if(verbose): print('computing numerosity')
        f_dict['numerosity'] = len(seg)

    return f_dict


def getSegmentsFeatures(segments, features='all', prec_mean=45, factor=1.0, threshold=0.5, verbose=False, n_jobs=1):
    '''
    Returns a DataFrame with the specified features computed on segments at the specified threshold

    Arguments:
    * segments: list of Segment objects on which to compute features
    * features: which features to compute. Use string 'all' to compute all the available ones
	* prec_mean: resolution of the maps that are built from segments to compute features
    * factor: used to specity the threshold. For each map the threshold is computed using DensityProprieties.calculate_map_threshold_SR with this factor
    * threshold: used to specity the threshold. If factor is None, this is used for all the maps
	* n_jobs: number of cpus to use for the processing
    '''
    if(type(segments)!=list): raise ValueError('segments must be a list')
    features_df = pd.DataFrame()
    if(verbose): print('getSegmentsFeatures: computing maps')
    maps = {}
    for i,s in enumerate(segments):
        if(verbose): print(f'getSegmentsFeatures: computing map {i}')
        maps[i] = TransformBlurrer().SR_gaussian_blur(s, prec_mean, sigma_coeff=1.,mode="unit")
    # maps = {i:TransformBlurrer().SR_gaussian_blur(s, prec_mean, sigma_coeff=1.,mode="unit") for i,s in enumerate(tqdm(segments, disable=not verbose))}
    thrs = [threshold]*len(segments) if factor is None else [DS.calculate_map_threshold_SR(maps[i], factor=factor) for i in range(len(maps))]
    if(n_jobs==1):
        for iseg, seg in enumerate(segments):
            if(verbose): print('Waiting for %i out of %i'%(iseg, len(segments)-1))
            d = getSegmentFeatures(seg, maps[iseg], features, thrs[iseg])
            features_df.loc[iseg, list(d.keys())] = d
            if(verbose): print('Segment %i out of %i completed'%(iseg, len(segments)-1))
    else:
        import multiprocessing as mp
        mp.set_start_method('spawn', force=True)
        pool = mp.Pool(n_jobs)
        
        jobs = {}
        for iseg, seg in enumerate(segments):
            jobs[iseg] = pool.apply_async(getSegmentFeatures, (seg, maps[iseg], features, thrs[iseg]))
        if(verbose):
            print('Started all jobs')
        
        for iseg, seg in enumerate(segments):
            if(verbose): print('Waiting for %i out of %i'%(iseg, len(segments)-1))
            d = jobs[iseg].get()
            features_df.loc[iseg, list(d.keys())] = d
            if(verbose): print('Segment %i out of %i completed'%(iseg, len(segments)-1))
    
    features_df.index +=1
    return features_df


def getSegmentsPairFeatures(maps, features='all', threshold1=0.5, threshold2=0.5):
    '''
    Returns a dictionary with the specified features computed on maps at the specified threshold	

    Arguments:
    * maps: list of two maps on which to compute features
    * features: which features to compute. Use string 'all' to compute all the available ones
    * threshold1, threshold2: the threshold to use on the maps for the computation
    '''
    if(features == 'all'):
        features = ['coms_distance', 'surface_distance', 'entanglement']
    assert(len(maps)==2)
    f_dict = {}
    if('coms_distance' in features):
        f_dict['coms_distance'] = MSF.DistanceBetweenSegments(maps[0],maps[1],threshold1=threshold1,threshold2=threshold2)
    if('surface_distance' in features):
        f_dict['surface_distance'] = MSF.getSurfaceDistance(maps[0],maps[1],threshold1=threshold1,threshold2=threshold2)
    if('entanglement' in features):
        f_dict['entanglement'] = MSF.EntanglementBetweenSegments(maps[0],maps[1],threshold1=threshold1,threshold2=threshold2)
    return f_dict


def getSpatialFeaturesIntraWalk(segments, features='all', prec_mean=45, factor=1.0, threshold=0.5, n_jobs=1, verbose=False, fill_missing_timepoints=False, max_timepoint=None):
    '''
    Returns a DataFrame with the specified features computed on pairs of segments at the specified threshold

    Arguments:
    * segments: list of Segment objects on which to compute features
    * features: which features to compute. Use string 'all' to compute all the available ones
	* prec_mean: resolution of the maps that are built from segments to compute features
    * factor: used to specity the threshold. For each map the threshold is computed using DensityProprieties.calculate_map_threshold_SR with this factor
	* threshold: used to specity the threshold. If factor is None, this is used for all the maps
	* n_jobs: number of cpus to use for the processing
    * fill_missing_timepoints: whether to add rows, with Nan values, representing comparisongs between missing timepoints
    * max_timepoint: if fill_missing_timepoints is True, this is used to determine the missing timepoints
    '''
    if(type(segments)!=list): raise ValueError('segments must be a list')
    features_df = pd.DataFrame()
    maps = {i:TransformBlurrer().SR_gaussian_blur(s, prec_mean, sigma_coeff=1.,mode="unit") for i,s in enumerate(segments)}
    thrs = [threshold]*len(segments) if factor is None else [DS.calculate_map_threshold_SR(maps[i], factor=factor) for i in range(len(maps))]
    import multiprocessing as mp
    pool = mp.Pool(n_jobs)
    
    jobs = {}
    for iseg1, seg1 in enumerate(segments):
        for iseg2, seg2 in enumerate(segments[iseg1:], iseg1):
            jobs[(iseg1, iseg2)] = pool.apply_async(getSegmentsPairFeatures,
                                                    ([maps[iseg1], maps[iseg2]],
                                                     features,
													 thrs[iseg1], thrs[iseg2]))
    if(verbose):
        print('Started all jobs')
    
    for i, (k,v) in enumerate(jobs.items()):
        tempdict = jobs[k].get()
        tempdict['segment1'] = k[0]
        tempdict['segment1_timepoint'] = segments[k[0]].atomList['timepoint'].values[0]
        tempdict['segment2'] = k[1]
        tempdict['segment2_timepoint'] = segments[k[1]].atomList['timepoint'].values[0]
        features_df.loc[i, list(tempdict.keys())] = tempdict
        if(verbose): print('Pair %i out of %i completed'%(i, len(jobs.items())-1))
    
    features_df['segment1'] +=1
    features_df['segment2'] +=1

    features_df['segment1'] = features_df['segment1'].astype('int')
    features_df['segment2'] = features_df['segment2'].astype('int')

    if(max_timepoint is None):
        max_timepoint = int(features_df['segment1_timepoint'].max())
    if(fill_missing_timepoints):
        missing_tpoints = list(set(list(range(1,max_timepoint+1))) \
                            - set(features_df['segment1_timepoint'].unique().astype('int')) \
                            - set(features_df['segment2_timepoint'].unique().astype('int')))
        for itpoint1, tpoint1 in enumerate(missing_tpoints):
            for tpoint2 in missing_tpoints[itpoint1:]:
                d1 = {c:None for c in features_df.columns}
                d1['segment1_timepoint'] = tpoint1
                d1['segment2_timepoint'] = tpoint2
                features_df.loc[len(features_df)] = d1

    return features_df

def getSpatialFeaturesInterWalk(segments1, segments2, features='all', prec_mean=45, factor=1.0, threshold=0.5, n_jobs=1, verbose=False, fill_missing_timepoints=False, max_timepoint1=None, max_timepoint2=None):
    '''
    Returns a DataFrame with the specified features computed on pairs of segments at the specified threshold

    Arguments:
    * segments1: list of Segment objects coming from the first walk
    * segments2: list of Segment objects coming from the second walk
    * features: which features to compute. Use string 'all' to compute all the available ones
	* prec_mean: resolution of the maps that are built from segments to compute features
    * factor: used to specity the threshold. For each map the threshold is computed using DensityProprieties.calculate_map_threshold_SR with this factor
	* threshold: used to specity the threshold. If factor is None, this is used for all the maps
	* n_jobs: number of cpus to use for the processing
    * fill_missing_timepoints: whether to add rows, with Nan values, representing comparisongs between missing timepoints
    * max_timepoint1: if fill_missing_timepoints is True, this is used to determine the missing timepoints
    * max_timepoint2 if fill_missing_timepoints is True, this is used to determine the missing timepoints
    '''
    if(type(segments1)!=list): raise ValueError('segments1 must be a list')
    if(type(segments2)!=list): raise ValueError('segments2 must be a list')
    features_df = pd.DataFrame()
    maps1 = {i:TransformBlurrer().SR_gaussian_blur(s, prec_mean, sigma_coeff=1.,mode="unit") for i,s in enumerate(segments1)}
    maps2 = {i:TransformBlurrer().SR_gaussian_blur(s, prec_mean, sigma_coeff=1.,mode="unit") for i,s in enumerate(segments2)}
    thrs1 = [threshold]*len(segments1) if factor is None else [DS.calculate_map_threshold_SR(maps1[i], factor=factor) for i in range(len(maps1))]
    thrs2 = [threshold]*len(segments2) if factor is None else [DS.calculate_map_threshold_SR(maps2[i], factor=factor) for i in range(len(maps2))]
    import multiprocessing as mp
    pool = mp.Pool(n_jobs)
    
    jobs = {}
    for iseg1, seg1 in enumerate(segments1):
        for iseg2, seg2 in enumerate(segments2):
            jobs[(iseg1, iseg2)] = pool.apply_async(getSegmentsPairFeatures,
                                                    ([maps1[iseg1], maps2[iseg2]],
                                                     features,
													 thrs1[iseg1], thrs2[iseg2]))
    if(verbose):
        print('Started all jobs')
    
    for i, (k,v) in enumerate(jobs.items()):
        tempdict = jobs[k].get()
        tempdict['segment1'] = k[0]
        tempdict['segment1_timepoint'] = segments1[k[0]].atomList['timepoint'].values[0]
        tempdict['segment2'] = k[1]
        tempdict['segment2_timepoint'] = segments2[k[1]].atomList['timepoint'].values[0]
        features_df.loc[i, list(tempdict.keys())] = tempdict
        if(verbose): print('Pair %i out of %i completed'%(i, len(jobs.items())-1))
    
    features_df['segment1'] +=1
    features_df['segment2'] +=1

    features_df['segment1'] = features_df['segment1'].astype('int')
    features_df['segment2'] = features_df['segment2'].astype('int')

    if(max_timepoint1 is None):
        max_timepoint1 = int(features_df['segment1_timepoint'].max())
    if(max_timepoint2 is None):
        max_timepoint2 = int(features_df['segment2_timepoint'].max())
    if(fill_missing_timepoints):
        missing_tpoints1 = list(set(list(range(1,max_timepoint1+1))) - set(features_df['segment1_timepoint'].unique().astype('int')))
        missing_tpoints2 = list(set(list(range(1,max_timepoint2+1))) - set(features_df['segment2_timepoint'].unique().astype('int')))
        for tpoint1 in missing_tpoints1:
            for tpoint2 in missing_tpoints2:
                d1 = {c:None for c in features_df.columns}
                d1['segment1_timepoint'] = tpoint1
                d1['segment2_timepoint'] = tpoint2
                features_df.loc[len(features_df)] = d1

    return features_df

def _getListsDifference(factor1, factor2):
    return [it for it in factor1 if not it in factor2]

def _convertSpatialFeaturesToMatrixFormat(pairs_features_df, type_cols = ['coms_distance','surface_distance','entanglement'], seg2_values=np.arange(1,60).astype('int')):
    '''
    Converts from long to wide format. Moreover it fills missing pairs with Nans and copies relation values for mirrored loci pairs.
    Pivots on columns 'segment1' and 'segment2'.

    Arguments:
    * pairs_features_df: DataFrame in long format to be converted
    * type_cols: which columns contain the spatial data
    * seg2_values: all the indices of the segments in the chromosome

    Return:
    * a DataFrame
    '''
    tempdf = pairs_features_df.copy()
    tempdf = pd.concat([tempdf, tempdf.assign(segment1 = tempdf['segment2'], segment2 = tempdf['segment1'])]).drop_duplicates()
    tempdf = tempdf.melt(value_vars=type_cols, var_name='type', ignore_index=False, id_vars=_getListsDifference(pairs_features_df.columns,type_cols))
    tempdf = tempdf.pivot(index='segment1',columns=['type','segment2'], values='value')
    tempdf = tempdf.reindex(pd.MultiIndex.from_product([type_cols, seg2_values], names=tempdf.columns.names), axis=1)
    return tempdf

def getMergedMorphologicalAndSpatialSegmentsFeatures(single_features_df, pairs_features_df, metadata=None):
    '''
    Merges single segment features with features computed on pairs of segments.
    The dataframes this function requires can be obtained by using functions
    getSegmentsFeatures, getSpatialFeaturesIntraWalk and getSegmentsMetadata, respectively.
    
    Arguments:
    * single_features_df: DataFrame with columns indicating feature values and index indicating identifiers of segments
    * pairs_features_df: DataFrame with columns 'segment1' and 'segment2' indicating the pair of segment and the rest of columns indicating feature values
    * metadata: DataFrame with columns indicating metadata of segments and index indicating identifiers of segments
    
    
    Returns:
    * DataFrame with segment identifiers on the index and all the columns indicating a morphological or spatial feature.
    Moreover if metadata is provied its columns are appended at the beginning of the DataFrame
    '''
    final_df = single_features_df.copy()
    num_segs = single_features_df.shape[0]
    for f in [c for c in pairs_features_df.columns if not c in set(['segment1','segment2','segment1_timepoint','segment2_timepoint'])]:
        tempdf = pairs_features_df.pivot(index='segment1',columns='segment2', values=f)
        # Complete the missing lower triangle by copying there the transpose of the upper triangle
        tempdf[tempdf.isna()] = 0.0
        tempdf.iloc[:,:] = tempdf.values + np.triu(tempdf.values, 1).T
        tempdf.columns = [str(f)+'_%i'%i for i in range(num_segs)]
        final_df = pd.merge(final_df, tempdf, left_index=True, right_index=True)
    if(not metadata is None):
         final_df = metadata.merge(final_df, left_index=True, right_index=True)
    return final_df




def _getDiagonalOperationMatrix(arr, value_where_nan=0.0, op=np.nanmean):
    '''
    Returns a matrix of the same shape as arr with each element replaced by the result of op on the corresponding diagonal.
    Requires a symmetric square matrix


    Arguments:
    * arr: symmetric square matrix
    '''

    assert arr.shape[0]==arr.shape[1]
    normalizing_arr = []
    for di in range(arr.shape[0]):
        diag = np.diag(arr, k=di)
        m = op(diag)
        if(m==np.nan):
            m=value_where_nan
        normalizing_arr.append(m)
    normalizing_arr = np.array(normalizing_arr)
    # print(normalizing_arr)
    # print('---')
    normalizing_mat=[]
    for ri in range(arr.shape[0]):
        if(ri==0):
            part = normalizing_arr
        else:
            part = np.concatenate([normalizing_arr[1:ri+1][::-1], normalizing_arr[:-ri]])
        # print(part)
        normalizing_mat.append(part)
    normalizing_mat = np.array(normalizing_mat)
    return normalizing_mat


def _divideByDiagonalMeans(arr):
    '''
    Given a square symmetric matrix, this function returns the same matrix with each entry divided by the mean on the corresponding diagonal
    '''
    normalizing_mat = _getDiagonalOperationMatrix(arr, value_where_nan=0.0, op=np.nanmean)
    return arr/normalizing_mat



def getEigenvecsFromContactMat(mat, num_corr=1, show=False, eigenvector_number=0):
    '''
    Arguments:
    * mat: square matrix to apply the procedure to (contact frequency matrix). All values in it must be finite
    * num_corr: number of times the correlation matrix is built from mat or from the previous correlation matrix
    * show: whether to show the matrix from which the eigenvector is extracted
    * eigenvector_number: which eigenvector to take return (0: first, 1: second, 2: third, ...)
    '''
    norm1 = _divideByDiagonalMeans(mat)
    ccm = norm1
    for i in range(num_corr):
        ccm = np.corrcoef(ccm)
    if(show):
        plt.matshow(ccm)
        plt.colorbar()
        plt.show()
    evals, evecs = np.linalg.eig(np.where(np.isnan(ccm), 0, ccm))
    order = np.argsort(evals)[::-1]
    evals = evals[order]
    evecs = evecs[:,order]
    return evecs[:,eigenvector_number]
