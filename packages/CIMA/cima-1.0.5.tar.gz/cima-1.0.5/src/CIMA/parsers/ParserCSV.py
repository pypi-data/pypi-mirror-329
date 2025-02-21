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
import numpy as np
import sys, os
from CIMA.segments.SegmentInfo import Segment
from CIMA.segments.SegmentInfoXYZ import SegmentXYZ
import random
import pandas as pd
import re


_info_needed_srx = [['image-ID', 'imageID'],"time-point","cycle","z-step","frame","photon-count","photon-count11","photon-count12","photon-count21","photon-count22","psfx","psfy","psfz","psf-photon-count","x","y","z","background11","background12","background21","background22","maxResidualSlope","chisq","log-likelihood","llr","accuracy","precisionx","precisiony","precisionz"]
_info_needed_thunderstorm = ['id', 'frame', 'x [nm]', 'y [nm]', 'z [nm]', 'sigma1 [nm]', 'sigma2 [nm]', 'intensity [photon]', 'offset [photon]', 'bkgstd [photon]', 'uncertainty [nm]'] # 'uncertainty_xy [nm]', 'uncertainty_z [nm]'
_info_needed_xyztimepoint = ['x','y','z','timepoint']
_info_needed_free = ['x','y','z']

_content_types_required_elements = {'srx': _info_needed_srx,
                                   'thunderstorm': _info_needed_thunderstorm,
                                   'xyztimepoint': _info_needed_xyztimepoint,
                                   'free': _info_needed_free}
'''The previous lists specify which columns are required to be in the input file'''

_conversion_dict_srx = {
    'image-ID': 'imageID',
    'time-point': 'timepoint',
    'z-step': 'zstep',
    'photon-count': 'photoncount',
    'photon-count11': 'photoncount11',
    'photon-count12': 'photoncount12',
    'photon-count21': 'photoncount21',
    'photon-count22': 'photoncount22',
    'psf-photon-count': 'psfphotoncount',
    'chisq': 'chi',
    'log-likelihood': 'loglike',
    'precisionx': 'xprec',
    'precisiony': 'yprec',
    'precisionz': 'zprec',
    'cluster-ID': 'clusterID',
    'Chromosome': 'chromosomes'
    }

_conversion_dict_thunderstorm = {
    'id': 'imageID',
    'x [nm]': 'x',
    'y [nm]': 'y',
    'z [nm]': 'z',
    'sigma1 [nm]': 'psfx',
    'sigma2 [nm]': 'psfy',
    'intensity [photon]': 'photoncount',
    'offset [photon]': 'background',
    'bkgstd [photon]': 'background_std',
    'uncertainty [nm]': ['xprec', 'yprec'],
    'uncertainty_xy [nm]': ['xprec', 'yprec'],
    'uncertainty_z [nm]': 'zprec',
    }

_converted_dict_xyztimepoint = {
    'time-point': 'timepoint',
    'vis-probe': 'timepoint',
    'cluster-ID': 'clusterID',
}

_content_types_conversion_dicts = {'srx': _conversion_dict_srx,
                            'thunderstorm': _conversion_dict_thunderstorm,
                            'xyztimepoint': _converted_dict_xyztimepoint,
                            'free': {**_conversion_dict_srx, **_conversion_dict_thunderstorm, **_converted_dict_xyztimepoint},
                            'unchanged': {}}

'''Conversion dicts specifiy how to convert column names from file to Segment object. They don't specificy which columns are required'''


def _reverseConversionDict(c_dict):
        '''
        Returns a dict with reversed key-value pairs, using just the last value when there are multiple
        '''
        rev_dict = {}
        for k,v in c_dict.items():
            if(type(v) == type([])):
                rev_dict[v[-1]] = k
            else:
                rev_dict[v] = k
        return rev_dict


def _areAllRequiredColumnNamesProvided(required, provided, verbose=False):
    missing = []
    for req_el in required:
        if(type(req_el) == type([])):
            found = False
            for alt in req_el:
                if(alt in provided):
                    found=True
                    break
        else:
            found = req_el in provided
        if(not found):
            missing.append(req_el)
    if(len(missing)>0):
        if(verbose):
            print('Missing ', missing)
        return False
    else:
        return True

def _isThereHeaderInFirstLine(filename, req_elements=[], conversion_dict={}, verbose=True):
        '''
        Returns True if all the required items are in the header, False else
        If conversion_dict is not empty, it is used to convert header elements
        before checking for their presence
        '''
        header_elements = _getFirstLineAsList(filename)
        header_elements = _listCustomRename(header_elements, conversion_dict)
        # req_elements = _info_needed_srx if content_type=='srx' else info_needed_thunderstorm'
        return _areAllRequiredColumnNamesProvided(req_elements, header_elements, verbose)
        

def _getFirstLineAsList(filename):
        '''
        Return a list with the elements of the first line of the filename.
        Assumes comma as separator
        '''
        with open(filename,"r") as r:
            localisation_sing = r.readline()
            line_elements = localisation_sing.split(',')
            line_elements = [el.strip(' \'\"\n') for el in line_elements]
            return line_elements


def _getTextSubsample(filename, k=10000, verbose=False):
    """Returns k random lines from the file in the form of a string"""
    sample = []
    with open(filename, 'r') as f:
        # append the header line
        sample.append(f.readline())
        # find file size
        f.seek(0, 2)
        filesize = f.tell()
        # define a set of random positions in the file         
        random_set = sorted(random.sample(range(filesize), k))
        for i in range(k):
            if(verbose):
                print('%i/%i'%(i+1,k))
            f.seek(random_set[i])
            # Skip current line (because we might be in the middle of a line)
            f.readline()
            # Append the next line to the sample set
            sample.append(f.readline())
    return ''.join(sample)
	
def _dfCustomRename(df, dict):
    '''
    Renames the columns of df according to dict. If a value of dict is a list, it's elements all give name to new columns with the corresponing values
    '''
    
    df_cp = df.copy()
    for k,v in dict.items():
        if(k in df.columns):
            if(type(v) == type([])):
                for alt in v:
                    if(k!=alt):
                        # avoid duplicate columns
                        df_cp = df_cp.drop(alt, axis=1, errors='ignore')
                    df_cp[alt] = df_cp[k]
                df_cp = df_cp.drop(k, axis=1, errors='ignore')
            else:
                if(k!=v):
                    # avoid duplicate columns
                    df_cp = df_cp.drop(v, axis=1, errors='ignore')
                df_cp = df_cp.rename({k: v}, axis=1)
    return df_cp

def _listCustomRename(list1, dict):
    '''
    Renames the columns of df according to dict. If a value of dict is a list, it's elements all give name to new columns with the corresponing values
    '''
    df_cp = list1.copy()
    for k,v in dict.items():
        if(type(v) == type([])):
            if(k in list1):
                for alt in v:
                    df_cp.append(alt)
                df_cp.remove(k)
        else:
            df_cp = list(map(lambda x: v if x==k else x,df_cp))
        
    return df_cp


class CSVParser:
    """A class to read CSV localisation files"""
    def __init__(self):
        pass

    @staticmethod
    def read_CSV_file(filename, metadata={}, sep=",",chromosomes=False, subsample=False,ksub=10000, content_type='srx', verbose=False):
        """
        Reads a CSV file and returns its contents as a `Segment` object.

        This function reads a CSV file with specific formatting and optional metadata. The function
        can selectively rename columns based on the `content_type`, validate headers, and subsample
        data if requested. It supports various content types, each of which may have specific column
        requirements. Raises errors if the file format or headers do not match expectations.

        Args:
        * filename (str): Path to the CSV file to read.
        * metadata (dict, optional): Additional metadata to attach to the output Segment object.
                                    Defaults to an empty dictionary.
        * sep (str, optional): The separator used in the CSV file. Defaults to ",".
        * chromosomes (bool, optional): If True, includes chromosome identifiers in the output.
                                        Defaults to False.
        * subsample (bool, optional): If True, reads only a subset of the file. Defaults to False.
        * ksub (int, optional): Number of lines to read if `subsample` is True. Defaults to 10,000.
        * content_type (str, optional): Specifies the expected content type in the file. Options are
                                        'srx', 'thunderstorm', 'xyztimepoint', or 'free'. Determines
                                        required columns and renames. Defaults to 'srx'.
        * verbose (bool, optional): If True, prints additional information for debugging. Defaults to False.

        Returns:
        * Segment: A Segment object containing the parsed data.

        Raises:
        * ValueError: If the content type is not supported, or if required columns are missing.
        """

        if(not content_type in _content_types_conversion_dicts.keys()):
            raise ValueError('Content type not supported')
        req_elements = _content_types_required_elements[content_type]

        if(content_type == 'free' or content_type=='xyztimepoint'):
            if(not _isThereHeaderInFirstLine(filename, req_elements, _content_types_conversion_dicts[content_type], verbose=True)):
                raise ValueError('MISSING OR INCOMPLETE HEADER')
        elif(content_type == 'srx' or content_type == 'thunderstorm'):
            if(not _isThereHeaderInFirstLine(filename, req_elements, verbose=True)):
                raise ValueError('MISSING OR INCOMPLETE HEADER: maybe the file you are trying to read is not in %s format'%content_type)
        else:
            if(not _isThereHeaderInFirstLine(filename, req_elements, verbose=True)):
                raise ValueError('MISSING OR INCOMPLETE HEADER')
        
        if(subsample):
            string_subsample = _getTextSubsample(filename, ksub, verbose)
            from io import StringIO
            stringiotext = StringIO(string_subsample)
            df = pd.read_csv(stringiotext, sep=sep)
        else:
            df = pd.read_csv(filename, sep=sep)

        conversion_dict = _content_types_conversion_dicts[content_type]
        df = _dfCustomRename(df, conversion_dict)

        # missing_cols = set(Segment.required_columns) - set(df.columns)
        # df = df.assign(**{col: 0.0 for col in missing_cols}, axis=1)

        if(not chromosomes):
            df= df[[c for c in df.columns if not c=='chromosomes']]
        
        metadata_copy = dict(metadata)
        if(not 'filename' in metadata_copy):
            metadata_copy['filename'] = filename
        return Segment(df, metadata=metadata_copy)
    
    @staticmethod
    def read_step_from_CSV_file(filename, metadata={} ,sep=",",chromosomes=False,
                                timestep=0, chunk_size=1000, assume_sequentiality=False, content_type='free'):
        """
        Reads a specific time step from a CSV file in chunks and returns it as a `Segment` object.

        This function reads data from a CSV file containing time series data, filtering for a specific 
        time step. It processes the file in chunks to manage memory usage, especially useful for large files. 
        The function supports various content types, renames columns as specified, and includes optional 
        chromosome identifiers.

        Args:
      * filename (str): Path to the CSV file to read.
      * metadata (dict, optional): Additional metadata to attach to the output Segment object.
                                    Defaults to an empty dictionary.
      * sep (str, optional): Separator used in the CSV file. Defaults to ",".
      * chromosomes (bool, optional): If True, includes chromosome identifiers in the output.
                                        Defaults to False.
      * timestep (int, optional): The specific time step to read from the file.
                                    Defaults to 0.
      * chunk_size (int, optional): Number of lines to read at once. Defaults to 1000.
      * assume_sequentiality (bool, optional): If True, assumes time points are stored in ascending order 
                                                to improve efficiency. Defaults to False.
      * content_type (str, optional): Specifies the expected content type in the file (e.g., 'srx', 
                                        'thunderstorm', 'xyztimepoint', 'free'), which affects required 
                                        columns and renaming rules. Defaults to 'free'.

        Returns:
      * Segment or None: A Segment object containing data for the specified time step, or None if no 
                            data for the time step is found.

        Raises:
      * ValueError: If the content type is unsupported, or if required columns are missing in the header.
        """
        if(not content_type in _content_types_conversion_dicts.keys()):
            raise ValueError('Content type not supported')
        req_elements = _content_types_required_elements[content_type]
        req_elements.append(['time-point','timepoint'])
        
        if(content_type == 'free'):
            # Convert column names before checking for required ones,
            # in this way everything that maps to x,y,z (eg x [nm], y [nm], z [nm]) is sufficient.
            if(not _isThereHeaderInFirstLine(filename, req_elements, _content_types_conversion_dicts[content_type])):
                raise ValueError('MISSING OR INCOMPLETE HEADER')
        else:
            if(not _isThereHeaderInFirstLine(filename, req_elements)):
                raise ValueError('MISSING OR INCOMPLETE HEADER')


        clean_chunks = []
        inside_step = False
        # header=CSVParser._getFirstLineAsList(filename)
        # Reading a single timestep may be useful if there is not enough memory to read the whole file.
        # This advantage would be lost if the whole filename was read to a df and then filtered by timepoint.
        # To preserve the memory saving, df is read in chunks which are filtered one a time and then concatenated at the end.
        for ic, chunk in enumerate(pd.read_csv(filename, sep=sep, chunksize=chunk_size, header=0)):
            # c1 = chunk.set_axis(header, axis=1)
            c1 = chunk
            where_condition = c1['time-point'] == timestep
            # where_condition = np.full(len(c1), True)
            step_selected_df = c1.loc[where_condition]
            if(not chromosomes):
                step_selected_df= step_selected_df[[c for c in step_selected_df.columns if not c=='chromosomes']]
            if(len(step_selected_df)>0):
                clean_chunks.append(step_selected_df)
            if(inside_step and (where_condition==False).sum()>0 and assume_sequentiality):
                break
            if(inside_step==False and where_condition.sum()>0):
                inside_step=True
            
        if(len(clean_chunks)>0):
            df = pd.concat(clean_chunks, axis=0)
            # df = df.rename(dict(zip(info_needed_multi, converted_column_names)), axis=1)
            conversion_dict = _content_types_conversion_dicts[content_type]
            df = _dfCustomRename(df, conversion_dict)
            # missing_cols = set(Segment.required_columns) - set(df.columns)
            # df = df.assign(**{col: 0.0 for col in missing_cols}, axis=1)
            metadata_copy = dict(metadata)
            if(not 'filename' in metadata_copy):
                metadata_copy['filename'] = filename
            return Segment(df, metadata=metadata_copy)
        else:
            return None
    

    @staticmethod
    def write_CSV_file(structure, pathout,sep=",", content_type='srx'):
        """
        Writes a Segment object to a CSV file with optional column renaming based on content type.

        This function saves the data from a `Segment` object to a CSV file. Columns in the 
        data can be renamed based on the specified `content_type`, supporting various output 
        formats. If necessary, the function creates the output directory path before writing.

        Args:
      * structure (Segment): The Segment object containing data to write to the CSV file.
      * pathout (str): Path to the output CSV file.
      * sep (str, optional): Separator to use in the CSV file. Defaults to ",".
      * content_type (str, optional): Specifies the output format, which determines how 
                                        columns are renamed. Options are 'srx', 'thunderstorm', 
                                        'xyztimepoint', 'free', and 'unchanged'. Defaults to 'srx'.

        Returns:
      * None

        Raises:
      * ValueError: If the content type is unsupported.
        """

        if(not content_type in _content_types_conversion_dicts.keys()):
            raise ValueError('Content type not supported')
        conv_dict = _reverseConversionDict(_content_types_conversion_dicts[content_type])
        df1 = _dfCustomRename(structure.atomList, conv_dict)
        os.makedirs(re.sub('/[^/]+.csv','',pathout), exist_ok=True)
        df1.to_csv(pathout, sep=sep, index=False)