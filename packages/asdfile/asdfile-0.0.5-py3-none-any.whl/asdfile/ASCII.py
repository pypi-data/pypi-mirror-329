# RS = '' # &#x001e in HTML
# """The record separator."""
# US = '' # &#x001f in HTML
# """The unit separator."""

# FS = '' # &#x001c in HTML
# """The File separator."""
# GS = '' # &#x001d in HTML
# """The group separator."""


_RS = '' # &#x001e in HTML --Record separator
_US = '' # &#x001f in HTML --Unit separator

_FS = '' # &#x001c in HTML --File separator
_GS = '' # &#x001d in HTML --Group separator

_SOHG = '' # &#x0001 --Start of Header for table level
_STXG = '' # &#x0002 --Start of Text for table level
_ETXG = '' # &#x0003 --End of Text for table level

_SOHF = '' # &#x0001 --Start of Header for group level --Literal['\u0001\u0001']
_STXF = '' # &#x0002 --Start of Text for group level
_ETXF = '' # &#x0003 --End of Text for group level

_SOHFG = '' # &#x0001 --Start of Header for File level
_STXFG = '' # &#x0002 --Start of Text for File level
_ETXFG = '' # &#x0003 --End of Text for File level

_HTAB = "\t" # &#x0009 in HTML - Horizontal Tab
_NEWLINE = "\n" # &#x000A in HTML - Line Feed
_VTAB = "\v" # &#x000B in HTML - Vertical Tab  


#############################################
# define functions for readable file formats
F_RS = lambda r: _RS+_NEWLINE if r == True else _RS
F_US = lambda r: _US+_HTAB if r == True else _US

F_FS = lambda r: _FS+_NEWLINE if r == True else _FS
F_GS = lambda r: _GS+_NEWLINE if r == True else _GS

F_SOHG = lambda r: _SOHG+_NEWLINE if r == True else _SOHG
F_STXG = lambda r: _STXG+_NEWLINE if r == True else _STXG
F_ETXG = lambda r: _ETXG+_NEWLINE if r == True else _ETXG

F_SOHF = lambda r: _SOHF+_NEWLINE if r == True else _SOHF
F_STXF = lambda r: _STXF+_NEWLINE if r == True else _STXF
F_ETXF = lambda r: _ETXF+_NEWLINE if r == True else _ETXF

F_SOHFG = lambda r: _SOHFG+_NEWLINE if r == True else _SOHFG
F_STXFG = lambda r: _STXFG+_NEWLINE if r == True else _STXFG
F_ETXFG = lambda r: _ETXFG+_NEWLINE if r == True else _ETXFG


# ASCII = dict(
#     RS = '', # &#x001e in HTML
#     US = '', # &#x001f in HTML

#     FS = '', # &#x001c in HTML
#     GS = '', # &#x001d in HTML

#     SOH = '', # &#x0001
#     STX = '', # &#x0002
#     ETX = '' # &#x0003
# )
# ASCII['RS']
# check on:  https://www.w3schools.com/charsets/tryit.asp?deci=8251



# Following to be added in Readme.md file after paper is published
'''
# ASCII Separated Data
## Flat file format for multi-tabular data storage using ASCII separator characters

Flat/Text file (e.g. comma-separated, tab-separated, fixed-width, etc.) is by far the most common file format used for tabular data by data analysts in any industry. Flat files store structured data using specific column/row separator like comma, newline and data qualifier characters like double quotation.  
There are few major issues present in the existing flat file formats: The separator and qualifier characters are commonly present in the data itself which makes it difficult to parse the file. Also, multiple tables are not supported by most of the existing file formats.  
.asd flat file format/structure eliminates above listed and other issues in existing flat file formats. The presented file format uses existing ASCII separator characters (which are almost obsolete considering present day usage and may not appear in actual data) instead of common characters like comma, tab, pipe, etc.  
This improves the quality and efficiency of data processing and allows multi-tabular data in a single flat file. I have named it ASCII Separated Data (ASD) with .asd as file extension.

## Characters used

| DEC       | OCT       | HEX       | BIN             | Symbol     | Description               |
|-----------|-----------|-----------|-----------------|------------|---------------------------|
|     1     |     1     |     01    |     00000001    |     SOH    |     Start of   Heading    |
|     2     |     2     |     02    |     00000010    |     STX    |     Start of Text         |
|     3     |     3     |     03    |     00000011    |     ETX    |     End of Text           |
|     28    |     34    |     1C    |     00011100    |     FS     |     File   Separator      |
|     29    |     35    |     1D    |     00011101    |     GS     |     Group   Separator     |
|     30    |     36    |     1E    |     00011110    |     RS     |     Record   Separator    |
|     31    |     37    |     1F    |     00011111    |     US     |     Unit   Separator      |


## Basic Structure of .asd file
[FILE GROUP LEVEL METADATA (only one in a single .asd file)]

   [FILE LEVEL METADATA]
      [DATASET/TABLE LEVEL METADATA]
         [DATA TABLE SEPARATED BY (US) AND (RS)]
      [GROUP SEPARATOR CHARACTER (GS)]
      [DATASET/TABLE LEVEL METADATA]
         [DATA TABLE SEPARATED BY (US) AND (RS)]

   [FILE SEPARATOR CHARACTER (FS)]

   [FILE LEVEL METADATA]
      [DATASET/TABLE LEVEL METADATA]
         [DATA TABLE SEPARATED BY (US) AND (RS)]
      [GROUP SEPARATOR CHARACTER (GS)]
      [DATASET/TABLE LEVEL METADATA
         [DATA TABLE SEPARATED BY (US) AND (RS)]
      [GROUP SEPARATOR CHARACTER (GS)]
      [DATASET/TABLE LEVEL METADATA]
         [DATA TABLE SEPARATED BY (US) AND (RS)]

   [FILE SEPARATOR CHARACTER (FS)]

   [FILE LEVEL METADATA]
      [DATASET/TABLE LEVEL METADATA]
         [DATA TABLE SEPARATED BY (US) AND (RS)]
      [GROUP SEPARATOR CHARACTER (GS)]
      [DATASET/TABLE LEVEL METADATA]
         [DATA TABLE SEPARATED BY (US) AND (RS)]


- **Note**: newline characters are used for readability and will not appear in default .asd format
## Installation
pip install asdfile


## Usage
import asdfile as asd

### Functions
- read_asd()
- write_asd()
'''