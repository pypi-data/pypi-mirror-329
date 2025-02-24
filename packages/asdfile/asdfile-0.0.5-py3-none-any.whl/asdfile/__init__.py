# ASD stands for ASCII separated Data.
# The project was initiated by Hemant Nikam as his Masters Research project.
# This is based on his research paper: Flat file format for multi-tabular data storage using ASCII separator characters.
# Note: This package is still a work in progress.
# Contributions are welcome.


from .asdfile import read_asd, write_asd, write_asd_single_from_listoflist, write_asd_single_from_df, read_asd_single_to_df, read_asd_single_to_listoflist

__author__ = 'Hemant Nikam'
__email__ = 'nikhemant@gmail.com'
__version__ = '0.0.5'

__all__ = ['read_asd', 'write_asd', 'write_asd_single_from_listoflist', 'write_asd_single_from_df', 'read_asd_single_to_df', 'read_asd_single_to_listoflist']
