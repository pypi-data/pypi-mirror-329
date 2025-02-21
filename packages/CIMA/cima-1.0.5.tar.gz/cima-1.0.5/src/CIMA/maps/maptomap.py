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

from CIMA.maps.EMMap import Map
import os
import re
import subprocess

def Map2Map(m1, m2, c1, c2, dirin, precision=45, number_alternative_fits=100, chimerapath='', runchimera='Mac', writemx=False, listfit=False):
	"""
	Map to Map comparison based on Rigid Body fitting.

	Arguments:
    * m1, m2 : Denisty Map Objects Density map objects to be compared.
    * c1, c2 : float Optimal contours for the density maps.
    * dirin : str Working directory.
    * precision : int, optional Precision to use for the fitting (default is 45).
    * number_alternative_fits : int, optional Number of fits to perform (default is 100).
    * chimerapath : str, optional Path to Chimera executable (default is '').
    * runchimera : str, optional Platform-specific Chimera run command (default is 'Mac').
    * writemx : bool, optional If True, write the rotation matrix (default is False).
    * listfit : bool, optional If True, return the CCC score for each fit (default is False).

	Returns:
    * list or float: If listfit is True, returns a list of CCC scores for each fit. Otherwise, returns the top scoring fit's CCC score.
	"""

	curdir = dirin
	if not os.path.isdir(curdir + 'tmp/'):
		os.mkdir(curdir + 'tmp/')
	else:
		print("overwrite dir tmp")
	
	m1.write_to_MRC_file(curdir + 'tmp/m1.mrc')
	m2 = m2.origin_change_maps(m1)
	m2.write_to_MRC_file(curdir + 'tmp/m2.mrc')
	
	_writecmdchimerafit(dirin, c1, c2, res=precision, number_alternative_fits=number_alternative_fits)
	
	if runchimera == 'Mac':
		_runcmdchimera_mac(chimerapath, dirin)
		cccfit = _getccfit(dirin)
		
		if listfit:
			if writemx:
				_writecmdchimeramx(dirin, chimerapath)
			_cleandir(dirin)
			return cccfit
		else:
			if writemx:
				_writecmdchimeramx(dirin, chimerapath)
			return cccfit[0]

def _cleandir(dirin):
	os.remove(dirin+'tmp/fitmap.cmd')
	os.remove(dirin+'tmp/fitmap.log')

def _writecmdchimerafit(dirin,c1,c2,res,number_alternative_fits):

	fout=open(dirin+'tmp/fitmap.cmd',"w")
	fout.write("open %s\n"%(dirin+'tmp/m1.mrc'))
	fout.write("open 1 %s\n"%(dirin+'tmp/m2.mrc'))
	fout.write("volume #0 level %s\n"%c1)
	fout.write("volume #1 level %s\n"%c2)
	fout.write("fitmap #1 #0 metric correlation resolution %s search %s listFits False\n"%(res,number_alternative_fits))
	fout.write("close all\n")

def _writecmdchimeramx(dirin,chimerapath):
	fmx=dirin+'tmp/fitmap.mx'
	fout=open(dirin+'tmp/mx_transform.cmd',"w")
	fout.write("open %s\n"%(dirin+'tmp/m2.mrc'))
	fout.write("matrixset %s\n"%fmx)
	fout.write("write #0 %s\n"%(dirin+'tmp/m2_t.mrc'))
	fout.write("close all\n")
	fout.flush()
	#fcmd=dirin+'tmp/mx_transform.cmd'
  	#subprocess.call("%s --nostatus --nogui %s"%(chimerapath,fcmd),shell=True)

#RB run command
def _runcmdchimera_mac(chimerapath,dirin):

	fcmd=dirin+'tmp/fitmap.cmd'
	subprocess.call("%s --nostatus --nogui %s > %s"%(chimerapath,fcmd,fcmd.replace('cmd','log')),shell=True)


def _getccfit(dirin):
	print('get mx')
	listccc=[]
	flog=dirin+'tmp/fitmap.log'
	linein=open(flog,'r')
	linein=linein.readlines()
	for i,l in enumerate(linein):
		if 'Correlations and times found:' in l:

			listccc=[x for x in linein[i+1].split()]
			listccc=[float(x) for x in listccc[0::2]]

		elif l == '  Matrix rotation and translation\n':
			l1='Model 0.0\n'
			l1+=linein[i+1]
			l1+=linein[i+2]
			l1+=linein[i+3]
			print("Matrix rotation and translation write")
			fmx=open(flog.replace(".log",".mx"),"w")
			fmx.write(l1)
			fmx.flush()
			#_writecmdchimeramx(dirin)
	return listccc
#def _runcmdchimera_mac2(chimerapath,dirin):

#	fcmd=dirin+'tmp/fitnogui.py'
#	print 'subprocess.call'
#	#subprocess.call("%s --nogui %s > %s"%(chimerapath,fcmd,fcmd.replace('cmd','log')),shell=True)


#	m1=dirin+'tmp/m1.mrc'
#	m2=dirin+'tmp/m2.mrc'
#	os.system("%s --nogui --nostatus --script %s  %s %s"%(chimerapath,fcmd,m1,m2))
