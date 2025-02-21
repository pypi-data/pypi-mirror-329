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
from __future__ import absolute_import, division, print_function
import os
import numpy as np

# The code in the following section come from https://cci.lbl.gov/hybrid_36/ and is needed to encode residue ids higher than 9999,
# as explained in https://www.cgl.ucsf.edu/chimerax/docs/user/formats/pdbintro.html

#############################################
try:
  from six.moves import range
  from six.moves import zip
except ImportError:
  pass

digits_upper = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
digits_lower = digits_upper.lower()
digits_upper_values = dict([pair for pair in zip(digits_upper, range(36))])
digits_lower_values = dict([pair for pair in zip(digits_lower, range(36))])

def _encode_pure(digits, value):
  "encodes value using the given digits"
  assert value >= 0
  if (value == 0): return digits[0]
  n = len(digits)
  result = []
  while (value != 0):
    rest = value // n
    result.append(digits[value - rest * n])
    value = rest
  result.reverse()
  return "".join(result)

def _hy36encode(width, value):
  "encodes value as base-10/upper-case base-36/lower-case base-36 hybrid"
  i = value
  if (i >= 1-10**(width-1)):
    if (i < 10**width):
      return ("%%%dd" % width) % i
    i -= 10**width
    if (i < 26*36**(width-1)):
      i += 10*36**(width-1)
      return _encode_pure(digits_upper, i)
    i -= 26*36**(width-1)
    if (i < 26*36**(width-1)):
      i += 10*36**(width-1)
      return _encode_pure(digits_lower, i)
  raise ValueError("value out of range.")
##################################

def _write_to_PDB(num,x,y,z,factor=1., custom_residue_id=None):
	"""
	Writes a PDB ATOM record based in the atom attributes to a file.
	"""
	#ATOM   2350  CA  CYS   151      87.310  74.561 119.522  1.00  0.00           C
	#ATOM    293 1HG  GLU A   18    -14.861  -4.847   0.361  1.00  0.00           H
	#ATOM      2  CA  DUM A   2       4.000   5.000   6.000  1.00  1.00           C
	#	print l
	record_name='ATOM'
	atom_name='CA'
	chain='A'
	res='CA'
	line = ''
	line += record_name.ljust(6)
	line += str(num).rjust(5)+' '
	line += atom_name.center(4)+' '
	line += res.ljust(3)+' '
	line += chain.ljust(1)
	line += str(_hy36encode(4,num)).rjust(4) if custom_residue_id is None else str(_hy36encode(4,custom_residue_id)).rjust(4)
	line += '    '
	x = '%.3f' % float(x/factor)
	y = '%.3f' % float(y/factor)
	z = '%.3f' % float(z/factor)
	line += x.rjust(8)
	line += y.rjust(8)
	line += z.rjust(8)
	occ = '%.2f'% float(1)
	temp_fac = '%.2f'% float(0)
	line += occ.rjust(6)
	line += temp_fac.rjust(6)+'          '
	line += 'C'.strip().rjust(2)
	return line + '\n'

def _writeTerm(num):
	line = ''
	line += 'TER'.ljust(6)
	line += str(num).rjust(5)+' '
	line += ''.center(4)
	line += ' '
	line += 'DUM'.ljust(4)
	line += 'A'.ljust(1)
	line += str(0).rjust(4)
	line +='\n'
	return line



def writeCOM_toPDB(list_coord,writeout=True,filenameout='',factor=1., same_residue_id=False):
	"""
	Returns a PDB file for ball and stick rapresentation

	Arguments:

	   *list_coord*
		   list of COM coortinates
	   *writeout*
		   save the pdb file
        *filenameout*
			location and name of the output file
        *factor*
			divides coords by this number before writing. Necessary to avoid crossing width limits set by pdb format.
            If None a valid factor is automatically computed and used.
        *same_residue_id*
			whether to use 0 as the residue id for all the atoms, or to use instead the index included in list_coord

	Returns:
		pdb file format
	"""

	# PDB file format allows max 8 columns for each coordinate. 3 are occupied by decimals, one by the dot, and one by the possible sign, leaving 3 available.
	# Choose a factor that makes all numbers <=999
	if(factor==None):
		factor = np.array(list_coord)[:,1:].max()/999.0

	ll=''
	idxin=0
	for i in list_coord:
		#print i
		ll+= _write_to_PDB(i[0],i[1],i[2],i[3],factor=factor, custom_residue_id=None if not same_residue_id else 0)
	ll+= _writeTerm(list_coord[-1][0])
	ll += 'ENDMDL'.ljust(6)+'\n'
	#for idx in range(len(list_coord)-1):
		#num=list_coord[idx][3]
		#num2=list_coord[idx+1][3]
		#ll+= 'CONECT'.ljust(6)
		#ll += str(num).rjust(5)+' '
		#ll += str(num2).rjust(5)+'\n'

	if writeout==True:
		fout=open(filenameout,'w')
		fout.write(ll)
		fout.flush()

	return ll
