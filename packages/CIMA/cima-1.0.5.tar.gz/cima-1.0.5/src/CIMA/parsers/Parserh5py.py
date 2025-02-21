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
import h5py
from CIMA.segments.SegmentInfoH5 import SegmentH5
from CIMA.parsers import ParserCSV
import pandas as pd



class h5pyParser:
    """A class to read h5py localisation files"""
    def __init__(self):
        pass

    @staticmethod
    def readH5File(filename,pxcamera=65., metadata={}, content_type='free', verbose=False):
        """
        Reads an HDF5 file containing localization data and returns it as a `SegmentH5` object.

        This function reads data from an HDF5 file (`filename`) containing localization information. 
        It converts the data into real-world coordinates using the specified pixel size (`pxcamera`). 
        Based on the provided `content_type`, it renames columns and checks for required fields to 
        ensure compatibility with different data formats.

        Args:
        * filename (str): Path to the HDF5 file to read.
        * pxcamera (float, optional): Size of the pixel, used to convert microscope coordinates 
                                        to real-world coordinates. Defaults to 65.0.
        * metadata (dict, optional): Additional metadata to attach to the output SegmentH5 object. 
                                    Defaults to an empty dictionary.
        * content_type (str, optional): Specifies the expected content type in the file (e.g., 'srx', 
                                        'thunderstorm', 'xyztimepoint', 'free'). This affects required 
                                        columns and renaming rules. Defaults to 'free'.
        * verbose (bool, optional): If True, prints additional information for debugging. Defaults to False.

        Returns:
        * SegmentH5: A SegmentH5 object containing the localization data and metadata.

        Raises:
        * ValueError: If the content type is unsupported or if required columns are missing.
        """
        if(not content_type in ParserCSV.content_types_conversion_dicts.keys()):
            raise ValueError('Content type not supported')
        info_needed = ParserCSV.content_types_required_elements[content_type]
        with h5py.File(filename, 'r') as locs_file:
            locs = locs_file["locs"][...]
        locs = np.rec.array(locs, dtype=locs.dtype)  # Convert to rec array with fields as attributes
        df = pd.DataFrame(locs)
        conversion_dict = ParserCSV.content_types_conversion_dicts[content_type]
        if(content_type == 'free'):
            header_elements = ParserCSV._listCustomRename(df.columns, conversion_dict)
        else:
            header_elements = df.columns
        if(not ParserCSV._areAllRequiredColumnNamesProvided(info_needed, header_elements, verbose=verbose)):
            raise ValueError('Missing columns')
        df = ParserCSV._dfCustomRename(df, conversion_dict)
        metadata_copy = dict(metadata)
        if(not 'filename' in metadata_copy):
            metadata_copy['filename'] = filename
        return SegmentH5(df, metadata=metadata_copy, pxcamera=pxcamera)
    
        
    @staticmethod
    def writeToH5SingleDataset(structure_id, filename, pathout, content_type='srx'):
        """
        Writes a Segment object to a single-dataset HDF5 file.

        This function saves data from a Segment object (`structure_id`) to a single dataset in an 
        HDF5 file. It renames columns based on the specified `content_type`, scales `x` and `y` 
        coordinates by `pxcamera`, and removes columns with only null values. The output file is 
        saved at `pathout` + `filename` + ".h5".

        Args:
        * structure_id (Segment): The Segment object containing data to write to the HDF5 file.
        * filename (str): The name of the output file (without extension).
        * pathout (str): The directory path where the file will be saved.
        * content_type (str, optional): Specifies how columns are renamed based on content type. 
                                        Options are 'srx', 'thunderstorm', 'xyztimepoint', 'free', 
                                        and 'unchanged'. Defaults to 'srx'.

        Returns:
        * None

        Raises:
        * ValueError: If the content type is unsupported.
        """

        # info_needed=["image-ID","time-point","cycle","z-step","frame","photon-count","psfx","psfy","psfz","psf-photon-count","x","y","z","llr","accuracy","precisionx","precisiony","precisionz","cluster-ID"]
        if(not content_type in ParserCSV.content_types_conversion_dicts.keys()):
            raise ValueError('Content type not supported')
        conv_dict = ParserCSV._reverseConversionDict(ParserCSV.content_types_conversion_dicts[content_type])
        df = ParserCSV._dfCustomRename(structure_id.atomList, conv_dict)
        write_df = df.copy()
        write_df[['x','y']] /= structure_id.pxcamera
        for col in df.columns:
            if(df[col].isnull().all()):
                write_df = write_df.drop(col, axis=1)

        formats = [ write_df.dtypes[col] if write_df.dtypes[col] != 'object' else str(write_df[col].values.astype(str).dtype).replace('<U','S') for col in write_df.columns ] 
        with h5py.File(pathout+filename+'.h5','w') as h5f:
            # recarr = write_df.to_records()
            recarr = np.rec.fromarrays(write_df.values.T.tolist(), dtype={'names': write_df.columns, 'formats': formats})
            h5f.create_dataset('locs', data=recarr, compression='gzip', compression_opts=9)
        h5f.close()

    @staticmethod
    def _writeToH5MultiDataset(structure_id, filename, pathout, content_type='srx'):
        """
        Writes a Segment object to a multi-dataset HDF5 file.

        This function saves data from a Segment object (`structure_id`) to an HDF5 file, where each 
        column is stored as a separate dataset. Columns are renamed based on `content_type`, `x` and 
        `y` coordinates are scaled by `pxcamera`, and empty columns are skipped. The file is saved 
        at `pathout` + `filename` + ".h5".

        Args:
            structure_id (Segment): The Segment object containing data to write to the HDF5 file.
            filename (str): The name of the output file (without extension).
            pathout (str): The directory path where the file will be saved.
            content_type (str, optional): Specifies how columns are renamed based on content type.
                                        Options are 'srx', 'thunderstorm', 'xyztimepoint', 'free',
                                        and 'unchanged'. Defaults to 'srx'.

        Returns:
            None

        Raises:
            ValueError: If the content type is unsupported.
        """
        # info_needed=["image-ID","time-point","cycle","z-step","frame","photon-count","psfx","psfy","psfz","psf-photon-count","x","y","z","llr","accuracy","precisionx","precisiony","precisionz","cluster-ID"]
        if(not content_type in ParserCSV.content_types_conversion_dicts.keys()):
            raise ValueError('Content type not supported')
        conv_dict = ParserCSV._reverseConversionDict(ParserCSV.content_types_conversion_dicts[content_type])
        df = ParserCSV._dfCustomRename(structure_id.atomList, conv_dict)
        df[['x','y']] /= structure_id.pxcamera
        with h5py.File(pathout+filename+'.h5','w') as h5f:
            for i,col_name in enumerate(df.columns):
                if(df[col_name].isnull().all()): continue
                col_dtype = df.dtypes[col_name]
                if(df.dtypes[col_name]=='object'):
                    col_dtype = h5py.string_dtype(encoding='utf-8')
                h5f.create_dataset(col_name, data=df[col_name], dtype=col_dtype, compression="gzip", compression_opts=9)
        h5f.close()
