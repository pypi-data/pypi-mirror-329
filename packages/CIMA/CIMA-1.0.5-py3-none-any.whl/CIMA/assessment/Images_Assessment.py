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

from math import pi
from random import randrange
import CIMA.utils.Vector as Vector
import numpy as np
from numpy import ndarray,array,append,matrix
import os
import sys
import pandas as pd
from CIMA.parsers import ParserCSV as Parser
from CIMA.segments import SegmentGaussian as SG
from CIMA.maps import  DensityProprieties as DS
from CIMA.maps import MapFeatures as MF
from CIMA.utils import WalkFeatures as WF
from CIMA.segments import SegmentInfo as SI

from CIMA.maps.ScoringFunctions import ScoringFunctions
from CIMA.segments.SegmentInfo import Segment


scorer = ScoringFunctions()

TB=SG.TransformBlurrer()

#saturation Plot
def Saturation_tofinal(endstructure: Segment,prec_mean=0.,mode="unit",maxframes=250,interval=5,ccc_mode=1.,getcom=False, selection_mode='frames', random_groups_num=50):
	"""
    Calculates the saturation plot by evaluating the cross-correlation coefficient (CCC) between a reference structure and 
    cumulative subsets of its frames or random groups, allowing the assessment of structural saturation over time or random groups.

    Args:
    * endstructure (Segment): The reference structure used for CCC calculations.
    * prec_mean (float, optional): Precision value used in Gaussian blurring. Defaults to 0.0.
    * mode (str, optional): Mode for Gaussian blurring ('unit' or other available modes). Defaults to "unit".
    * maxframes (int, optional): Maximum number of frames to process. Defaults to 250.
    * interval (int, optional): Number of frames in each chunk for CCC calculation. Defaults to 5.
    * ccc_mode (float, optional): Mode for calculating CCC between reference and partial structures. Defaults to 1.0.
    * getcom (bool, optional): If True, includes the center of mass (COM) of partial structures in the output. Defaults to False.
    * selection_mode (str, optional): Mode of selection for frames ('frames' or 'random'). Defaults to 'frames'.
    * random_groups_num (int, optional): Number of random groups used if `selection_mode` is 'random'. Defaults to 50.

    Returns:
    * list: A list of scores, where each score is a list containing:
              - Chunk ID (int)
              - CCC value (float)
              - Number of atoms in the partial structure (int)
              - (Optional) COM of the partial structure (if `getcom` is True)
	"""
	if(selection_mode == 'frames'):
		maxframes=int(maxframes)
		interval=int(interval)
		frames=list(range(0,int(maxframes)))
		frames_chucks = [frames[x:x+interval] for x in range(0, len(frames),interval)]
		#print (frames_chucks)
		#tmp=[]
		scores=[]
		tmp0=[]
		strcture_list_chucks=[endstructure.getFrames(fr) for C, fr in enumerate(frames_chucks) if endstructure.getFrames(fr)!= None ]
	elif(selection_mode == 'random'):
		labels = np.random.choice(np.arange(0,random_groups_num), len(endstructure), replace=True)
		strcture_list_chucks=[endstructure.copyWithNewContent(subdf) for n, subdf in endstructure.atomList.groupby(labels) if len(subdf)>0 ]
	else:
		raise ValueError('Selection mode not implemented')
	#print (strcture_list_chucks)
	C            = 0
	ncc          = []
	tmp          = []
	scores       = []
	#for fr in frames_chucks[0:1]:
	#	tmp0_s = endstructure.getFrames(fr)


    # Run per cicle and add them upon convergence
	for i in range(0,len(strcture_list_chucks)):
		cc = strcture_list_chucks[i]
		if cc:
			if (i==0):
				acc = strcture_list_chucks[0]
			else:
				acc.atomList = pd.concat([acc.atomList,cc.atomList])
				acc.copyWithNewContent(acc.atomList)
			C+=1
			tmp_map         = TB.SR_gaussian_blur(acc, prec_mean, sigma_coeff=1.,mode=mode)
			endstructuremap = TB.SR_gaussian_blur(endstructure, prec_mean, sigma_coeff=1.,mode=mode)
			cth             = 0.5
			cth2            = 0.5
			map_s1g,map_s2g = MF._match_grid(endstructuremap,tmp_map)
			ccctmp,ovtmp    = scorer.CCC_map(map_s1g,map_s2g,map_target_threshold=cth,map_probe_threshold=cth2,mode=ccc_mode)
			# ccctmp = scorer.CCC_simple(map_s1g, map_s2g, map1_thr=cth,map2_thr=cth2,mode=ccc_mode)
			if getcom==True:
				COM2=tmp_map._get_com_threshold(cth2)
				scores.append([C,ccctmp,len(acc.atomList),COM2])
			else:
				scores.append([C,ccctmp,len(acc.atomList)])
	return scores



def _Saturation_incremental(endstructure: Segment,prec_mean=0.,mode="unit",maxframes=250,interval=5,ccc_mode=1.):
	"""
	Arguments:

	*endstructure*
	 	an input structure that serves as the reference structure.
	*prec_mean*
		the precision value for the Gaussian blur function used in the function.
	*maxframes*
		the maximum number of frames to use for calculating the saturation.
	*interval*
		 the number of locations to use in each chunk  for calculating the saturation.
	*ccc_mode*
		the mode for calculating the cross-correlation coefficient (CCC) between the reference structure and the partial structures.
	*getcom*
		a Boolean parameter indicating whether to include the center of mass (COM) of the partial structures in the output.


	Return:

		An array of 3-list (Id, score, number of localisation)
		The function then returns a list of scores, where each score corresponds to a chunk of frames and includes the CCC value and the number of atoms in the partial structure.
		If getcom is True, the output also includes the COM of the partial structure.
	"""
	maxframes=int(maxframes)
	interval=int(interval)
	frames=list(range(0,int(maxframes)))
	frames_chucks = [frames[x:x+interval] for x in range(0, len(frames),interval)]
	tmp=[]
	scores=[]
	tmp_ref=[]
	for fr in frames_chucks[0:1]:
		tmp_ref = endstructure.getFrames(fr)

	if tmp_ref is None:
			tmp_ref=False
	else:
		tmp_ref=tmp_ref

	for C, fr in enumerate(frames_chucks):
		C+=1
		tmp = endstructure.getFrames(fr)
		if tmp is None:
			scores.append([C,0,0])
		else:
			tmp_str=tmp
			#print(tmp_ref)
			tmp_map=TB.SR_gaussian_blur(tmp_str, prec_mean, sigma_coeff=1.,mode=mode)
			if tmp_ref==False:
				scores.append([C,0,0])
			else:
				endstructuremap=TB.SR_gaussian_blur(tmp_ref, prec_mean, sigma_coeff=1.,mode=mode)
				#cth=DS.calculate_map_threshold_SR(endstructuremap)
				#cth2=DS.calculate_map_threshold_SR(tmp_map)
				cth=0.5
				cth2=0.5

				map_s1g,map_s2g=MF._match_grid(endstructuremap,tmp_map)
				ccctmp,ovtmp=scorer.CCC_map(map_s1g,map_s2g,map_target_threshold=cth,map_probe_threshold=cth2,mode=ccc_mode)
				scores.append([C,ccctmp,len(tmp_str.atomList)])
				tmp_ref=tmp_str


	return scores



def Assessment_Chrom_Precision(StructureObj,chrin,nuclei="",date="",hom="",pathin="",writeout=True):
    
	"""
    Assesses chromatin structure precision over time and outputs summary data.

    This function calculates the mean positional precision of chromatin data across timepoints 
    in a given structure. It then compiles this information into a summary table and optionally 
    writes the data to a file.

    Args:
    * StructureObj (Segment): The structure object containing chromatin data.
    * chrin (str): Identifier for the chromatin input structure.
    * nuclei (str, optional): Label for the output file. Defaults to an empty string.
    * date (str, optional): Identifier for the date of the experiment. Defaults to an empty string.
    * hom (str, optional): Identifier for homology data in the experiment. Defaults to an empty string.
    * pathin (str, optional): Directory path for saving the output file. Defaults to an empty string.
    * writeout (bool, optional): If True, writes the assessment data to a file. Defaults to True.

    Returns:
    * list: A list containing assessment data. Each entry includes:
              - Chromatin ID (`chrin`)
              - Timepoint label
              - Nuclei label
              - Date of experiment
              - Homology identifier
              - Mean precision values (x, y, z)
              - Number of localizations at the timepoint
              - Total number of timepoints
	"""
	
	table_out=""
	listout=[]
	timechrin=StructureObj.split_into_time()
	prec_mean_ch=StructureObj.GetMeanPrecision()
	nlocchrin=len(StructureObj.atomList)
	timepoint_list=[]
	for t1 in range(len(timechrin)):
		lab1=timechrin[t1].atomList.iloc[0].timepoint
		prec_mean_time=timechrin[t1].GetMeanPrecision()
		nloctime=len(timechrin[t1].atomList)
		listouttmp=[chrin,lab1,nuclei,date,hom,prec_mean_time[0],prec_mean_time[1],prec_mean_time[2],nloctime,0]
		listout.append(listouttmp)
		#timepoint_list.append(lab1)
		table_out+="%s,%s,%s,%s,%s,%s,%s,%s\n"%(date,hom,lab1,prec_mean_time[0],prec_mean_time[1],prec_mean_time[2],nloctime,0)

	table_out+="%s,%s,%s,%s,%s,%s,%s,%s\n"%(date,hom,0,prec_mean_ch[0],prec_mean_ch[1],prec_mean_ch[2],nlocchrin,len(timechrin))

	listout.append([chrin,0,nuclei,date,hom,prec_mean_ch[0],prec_mean_ch[1],prec_mean_ch[2],nlocchrin,len(timechrin)])

	if writeout==True:
		import os
		FOUT=pathin+"Assessment/"+"multi_assessment_precision_chr%s_%s_%s_%s.txt"%(chrin,date,nuclei,hom)
		if not os.path.isdir(pathin+"Assessment/"):
			os.mkdir(pathin+"Assessment/")
		fout=open(FOUT,"w")
		fout.write("Date,hom,Segment,pmeanx,pmeany,pmeanz,nloc,ntime\n")
		fout.write(table_out)
	return listout



def Saturation_tofinal_cycle_incremental(endstructure,prec_mean=0.,mode="unit",ccc_mode=1.,merge=1):#,getcom=False):
	"""
	Arguments:

	*endstructure*
	 	an input structure that serves as the reference structure.
	*prec_mean*
		the precision value for the Gaussian blur function used in the function.
	*mode*
		a string indicating the mode for the Gaussian blur function used in the function.
	*ccc_mode*
		the mode for calculating the cross-correlation coefficient (CCC) between the reference structure and the partial structures.
	*getcom*
		a Boolean parameter indicating whether to include the center of mass (COM) of the partial structures in the output.


	Return:
		An array of 3-list (Id, score, number of localisation)
		The list includes the cycle number, CCC score, number of atoms in the cycle, and optionally, the center of mass for the cycle.
	"""
	cicli        = endstructure.split_into_cycle()
	C            = 0
	ncc          = []
	tmp          = []
	scores       = []
    # Run per cicle and add them upon convergence
	for i in range(0,len(cicli)):
		cc = cicli[i]
		if (i==0):
			acc = cicli[0]
		else:
			acc.atomList = pd.concat([acc.atomList,cc.atomList])
			acc.copyWithNewContent(acc.atomList)
		C+=1
		tmp_map         = TB.SR_gaussian_blur(acc, prec_mean, sigma_coeff=1.,mode=mode)
		endstructuremap = TB.SR_gaussian_blur(endstructure, prec_mean, sigma_coeff=1.,mode=mode)
		#print (acc)
		#print (tmp_map)
		#print (endstructuremap)
		cth             = 0.5
		cth2            = 0.5
		map_s1g,map_s2g = MF._match_grid(endstructuremap,tmp_map)
		ccctmp,ovtmp    = scorer.CCC_map(map_s1g,map_s2g,map_target_threshold=cth,map_probe_threshold=cth2,mode=ccc_mode)
		scores.append([C,ccctmp,len(cc.atomList)])
	return scores

def Cycle_assessment(endstructure,prec_mean=0.,mode="unit",ccc_mode=1.,merge=1):#,getcom=False):
	"""
    Performs cycle-based assessment of a structure using cross-correlation coefficient (CCC) calculations.

    This function evaluates the similarity between each cycle in the input structure (`endstructure`) 
    and the overall structure by calculating the CCC. Each cycle is processed individually to compute 
    the CCC score relative to the full structure, allowing for an assessment of structural changes over cycles.

    Args:
    * endstructure (Segment): The reference structure used for CCC calculations.
    * prec_mean (float, optional): Precision value used in Gaussian blurring. Defaults to 0.0.
    * mode (str, optional): Mode for Gaussian blurring ('unit' or other available modes). Defaults to "unit".
    * ccc_mode (float, optional): Mode for calculating CCC between reference and cycle structures. Defaults to 1.0.
    * merge (int, optional): Reserved for future extensions to merge cycles, currently unused.

    Returns:
    * list: A list of lists, where each inner list contains:
            - Cycle number (int)
            - CCC score (float)
            - Number of atoms in the cycle (int)
	"""


	C=0
	tmp=[]
	scores=[]
	cycles=endstructure.split_into_cycle()
	#print (len(cicli))
	for cc in cycles:
		C+=1
		tmp_map=TB.SR_gaussian_blur(cc, prec_mean, sigma_coeff=1.,mode=mode)
		endstructuremap=TB.SR_gaussian_blur(endstructure, prec_mean, sigma_coeff=1.,mode=mode)
		#cth=DS.calculate_map_threshold_SR(endstructuremap)
		cth=0.5
		cth2=0.5
		#cth2=DS.calculate_map_threshold_SR(tmp_map)
		map_s1g,map_s2g=MF._match_grid(endstructuremap,tmp_map)
		ccctmp,ovtmp=scorer.CCC_map(map_s1g,map_s2g,map_target_threshold=cth,map_probe_threshold=cth2,mode=ccc_mode)
		scores.append([C,ccctmp,len(cc.atomList)])
	return scores

def _Halfdataset_ccc(endstructure,prec_mean=45.,mode="unit",ccc_mode=1.):
	"""
	Arguments:

		*endstructure*
			an input structure that serves as the reference structure.
		*prec_mean*
		 	the precision value for the Gaussian blur function used in the function.
		*maxframes*
		 	the maximum number of frames to use for calculating the saturation.
		*interval*
			the number of locations to use in each chunk  for calculating the saturation.
		*ccc_mode*
		 	the mode for calculating the cross-correlation coefficient (CCC) between the reference structure and the partial structures.
		*getcom*
			a Boolean parameter indicating whether to include the center of mass (COM) of the partial structures in the output.

	Return:

		list of scores, where each score corresponds to a chunk of frames and includes the CCC value and the number of atoms in the partial structure.
		If getcom is True, the output also includes the COM of the partial structure.

		Id, score, number of localisation
	"""
	df=endstructure.atomList
	shuffled_df = df.sample(frac=1)
	splitted_df = np.array_split(shuffled_df, 2) 
	#print (len(splitted_df))
	str1=endstructure.copy()
	str2=endstructure.copy()
	#print (str1,str2)
	str1=str1.copyWithNewContent(splitted_df[0])
	str2=str2.copyWithNewContent(splitted_df[1])
	#print (str1,str2)
	tmp_map1=TB.SR_gaussian_blur(str1, prec_mean, sigma_coeff=1.,mode=mode)
	tmp_map2=TB.SR_gaussian_blur(str2, prec_mean, sigma_coeff=1.,mode=mode)
	tmp_map1,tmp_map2=MF._match_grid(tmp_map1,tmp_map2)
	ccctmp,ovtmp=scorer.CCC_map(tmp_map1,tmp_map2,map_target_threshold=0.5,map_probe_threshold=0.5,mode=ccc_mode)
	return [ccctmp,str1.GetMeanPrecision()[2],str2.GetMeanPrecision()[2]]


def Saturation_experimentpseudotime(endstructure: Segment,numberoflocations=100,prec_mean=0.,mode="unit",ccc_mode=1.,getcom=False):
	"""
    Calculates saturation over experimental pseudotime by evaluating the cross-correlation coefficient (CCC) 
    between the reference structure and cumulative subsets of frames, allowing for an assessment of structural 
    stability over pseudotime.

    Args:
    * endstructure (Segment): The reference structure used for CCC calculations.
    *  numberoflocations (int, optional): The number of locations to use in each chunk for CCC calculation. Defaults to 100.
    * prec_mean (float, optional): Precision value used in Gaussian blurring. Defaults to 0.0.
    * mode (str, optional): Mode for Gaussian blurring ('unit' or other available modes). Defaults to "unit".
    *  ccc_mode (float, optional): Mode for calculating CCC between reference and partial structures. Defaults to 1.0.
    *  getcom (bool, optional): If True, includes the center of mass (COM) of partial structures in the output. Defaults to False.

    Returns:
    * list: A list of lists, where each inner list contains:
            - Pseudotime step (int)
            - CCC score (float)
            - Number of localizations in the chunk (int)
            - (Optional) COM of the partial structure (if `getcom` is True)
	"""

	StrObjOrdered=endstructure.OrderbyExperimenttime()
	#print (StrObjOrdered)
	maxframes=len(StrObjOrdered.atomList)
	maxframes=int(maxframes)
	interval=int(numberoflocations)
	frames=list(range(0,int(maxframes)))
	frames_chucks = [frames[x:x+interval] for x in range(0, len(frames),interval)]
	#print (frames_chucks)
	C=0
	tmp=[]
	scores=[]
	tmp_ref=[]
	for fr in frames_chucks[0:1]:
		countx=0
		tmp_ref = endstructure.getInRange([f-1 for f in fr])

	if tmp_ref is None:
		tmp_ref=False

	for C, fr in enumerate(frames_chucks):
		C+=1
		local_fr_parcial=[]
		countx=0
		tmp = endstructure.getInRange([f-1 for f in fr])
		if tmp is None:
			scores.append([C,0,0])
		else:
			tmp_str=tmp
			print(tmp_ref,tmp_str)
			tmp_map=TB.SR_gaussian_blur(tmp_str, prec_mean, sigma_coeff=1.,mode=mode)
			if tmp_ref==False:
				scores.append([C,0,0])
			else:
				endstructuremap=TB.SR_gaussian_blur(tmp_ref, prec_mean, sigma_coeff=1.,mode=mode)
				#cth=DS.calculate_map_threshold_SR(endstructuremap)
				#cth2=DS.calculate_map_threshold_SR(tmp_map)
				cth=0.5
				cth2=0.5

				map_s1g,map_s2g=MF._match_grid(endstructuremap,tmp_map)
				ccctmp,ovtmp=scorer.CCC_map(map_s1g,map_s2g,map_target_threshold=cth,map_probe_threshold=cth2,mode=ccc_mode)
				scores.append([C,ccctmp,len(tmp_str.atomList)])
				tmp_ref=tmp_str


	return scores


def _split(a, n):
	k, m = divmod(len(a), n)
	return list((a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n)))
