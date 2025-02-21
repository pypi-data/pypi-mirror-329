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

#TO ADD FUNCTIONS

import numpy as np
from CIMA.maps.EMMap import Map
from CIMA.maps import  DensityProprieties as DS
from CIMA.segments.SegmentInfo import Segment
from CIMA.segments.SegmentGaussian import TransformBlurrer
from skimage.segmentation import random_walker
from skimage.measure import  regionprops
from sklearn.cluster import KMeans
from scipy.ndimage import gaussian_filter,label,generate_binary_structure
from skimage.filters import threshold_otsu
from scipy.ndimage.morphology import binary_dilation
import hdbscan

def _SegmentMarkers_randomwalker(mapin,markers):
	labels = random_walker(mapin.fullMap, markers, beta=10, mode='cg_mg')
	return labels

def _GetMaskedSegment( maskin, segment,homolog="",clusterIDupdated=0):
	'''
	Arguments:
		*maskin*: density map
		*segment*: Segment
		*clusterIDupdated*: number
	Return:
		A new segment containing just those localizations that lie in the area of the densitymap which has a value
		greater than 2.
	'''
	# idx_true=zip(*np.where(maskin.fullMap >= 2.))#z_size, y_size, x_size
	# Convert coords to density map space
	map_relative_coords = TransformBlurrer.getCoordsRelativeToMap(maskin, segment.Getcoord())
	# Select those that are inside
	are_in_map = TransformBlurrer.areCoordsInMapBox(maskin, map_relative_coords)
	mcoords_in = map_relative_coords[are_in_map==True]
	mcoords_in_zyx = mcoords_in[:,[2,1,0]]
	# Check which are in the map area above threshold
	threshold=2.
	is_above_threshold = maskin[mcoords_in_zyx.T] > threshold
	# Get segment with just atoms in area above threshold
	selection_array = np.zeros(len(segment), dtype='bool')
	selection_array[are_in_map] == is_above_threshold
	masked_seg = segment.getPortion(selection_array)
	masked_seg.set_cluster_ids(clusterIDupdated)
	if(masked_seg is None):
		raise ValueError('No localizations remaining')
	else:
		return masked_seg
