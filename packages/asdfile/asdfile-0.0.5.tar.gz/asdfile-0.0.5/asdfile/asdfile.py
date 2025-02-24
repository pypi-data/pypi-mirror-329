import asdfile.ASCIIConstants as ASCIIConstants
import itertools 
from io import StringIO  
import pandas as pd
import csv


# this code allows to process default and readable format where headers are treated as text only

# multiple files with filegroup header, file headers and group/table headers
# get all tables/groups in 2 dimensional dataframe list
# get all table/group headers in 2 dimensional dataframe list
# get all file headers in 1 dimensional list
# get filegroup header in a list with single element (because it can be df or just a string)

# list of Encodings: https://docs.python.org/3/library/codecs.html#standard-encodings
# In file open modes rt and wt: t refers to the text mode. There is no difference between r and rt or w and wt since text mode is the default.
# Refer: https://docs.python.org/3/library/functions.html#open
# Character   Meaning
# 'r'     open for reading (default)
# 'w'     open for writing, truncating the file first
# 'x'     open for exclusive creation, failing if the file already exists
# 'a'     open for writing, appending to the end of the file if it exists
# 'b'     binary mode
# 't'     text mode (default)
# '+'     open a disk file for updating (reading and writing)
# 'U'     universal newlines mode (deprecated)

# Function to write data to a CSV file with a specified separator
def write_asd_single_from_listoflist(file_path, data_listoflist, separator='', lineterminator=''):
    with open(file_path, mode='w', newline='') as file:
        csv_writer = csv.writer(file, delimiter=separator, lineterminator=lineterminator)  # Specify the delimiter
        csv_writer.writerows(data_listoflist)  # Write the data

def write_asd_single_from_df(file_path, data_df, separator='', lineterminator=''):
    data_df.to_csv(file_path, sep=separator, lineterminator=lineterminator)

def read_asd_single_to_df(file_path, separator='', lineterminator=''):
    return pd.read_csv(file_path, sep=separator, lineterminator=lineterminator)

def read_asd_single_to_listoflist(file_path, separator='', lineterminator=''):
    asd_data = []
    with open(file_path, mode='r', newline='') as file:
        csv_reader = csv.reader(file, delimiter=separator, lineterminator=lineterminator)  # Specify the delimiter
        # header = next(csv_reader)  # Read the header
        # print("Header:", header)        
        # Read and print each row
        for row in csv_reader:
            # print(row)
            asd_data.append(row)

        return asd_data


def read_asd(file_path, encoding=None, Textstream = False): # path is actual data string if Textstream == True
    dft_2d_list = [] # tables/groups
    dfth_2d_list = [] # table/group headers
    dffh_list = [] # file headers
    dffgh_list = [] # filegroup headers
    r = False # readable/viewable format flag

    mode = 'rt'
    fileinput = open(file_path, mode=mode, encoding=encoding) if Textstream == False else StringIO(file_path)
    
    f = fileinput.read();
    filegrouptext = ""
    
    filegroupheadertext = ""
    filegroupwheader =  f.split(ASCIIConstants._ETXFG)
    # print(filewheader)
    if(len(filegroupwheader) > 1): # if filegroup header exists
        filegrouptext = filegroupwheader[1] # remaining part if actual filegroup contents
        temp = filegroupwheader[0].split(ASCIIConstants._STXFG)
        filegroupwheader = temp[0]
        # print(filegroupwheader)
        filegroupheadertext = temp[1] # Text after STXFG is Filegroup header text
        # print(filegroupheadertext)
        # if the text between SOHFG and STXFG is "readable" then set readable flag as true
        r = True if (filegroupwheader.lower().find("readable")>=0) else False
    else:
        filegrouptext = filegroupwheader[0]
        filegroupheadertext = None
    filegroupwheader = None # free the variable
    dffgh_list.append(filegroupheadertext)
    # print(filewheader)  
    # print('fh' ,filewheader)
    # print('g', file)

    RS =ASCIIConstants.F_RS(r)
    US =ASCIIConstants.F_US(r)

    FS =ASCIIConstants.F_FS (r)
    GS =ASCIIConstants.F_GS (r)

    SOHG =ASCIIConstants.F_SOHG(r)
    STXG =ASCIIConstants.F_STXG(r)
    ETXG =ASCIIConstants.F_ETXG(r)

    SOHF =ASCIIConstants.F_SOHF(r)
    STXF =ASCIIConstants.F_STXF(r)
    ETXF =ASCIIConstants.F_ETXF(r)

    SOHFG =ASCIIConstants.F_SOHFG(r)
    STXFG =ASCIIConstants.F_STXFG(r)
    ETXFG =ASCIIConstants.F_ETXFG(r)

    # print(r, US)


    filecount = 0
    # dfgh_list = []
    
    for file in filegrouptext.split(FS):
        filewheader =  file.split(ETXF)
        # print(filewheader)
        if(len(filewheader) >1):
            filetext = filewheader[1]
            filewheader = filewheader[0].split(STXF)[1]
        else:
            filetext = filewheader[0]
            filewheader = None
        # print('fh' ,filewheader)

        # print('fh' ,("NO HEADER - Group" if (filewheader==None) else filewheader + " - File") + str(filecount))
        
        dffh_list.append(filewheader)
        filecount+=1

        # print('g', group)
        df_list = []
        dfth_list = []
        tablecount = 0
        for table in filetext.split(GS):
            tablewheader = table.split(ETXG)
            # print(len(tablewheader))
            # print(tablewheader)
            if(len(tablewheader) >1):
                table = tablewheader[1]
                tablewheader = tablewheader[0].split(STXG)[1]
            else:
                table = tablewheader[0]
                tablewheader = None
            
            # print('th' ,("NO HEADER - Table" if (tablewheader==None) else tablewheader + " - Table") + str(tablecount))
            dfth_list.append(tablewheader)
            tablecount+=1    

            # TODO: header=0 means first row is header, we can also send header=None so there are no headers but then optional names have to be passed
            # engine= "python" to use multiple characters as separator
            df = pd.read_csv(StringIO(table), sep=US, lineterminator=RS, encoding=encoding, header=0)
            # df = pd.read_csv(StringIO(table), sep=US, lineterminator=RS, encoding=encoding, header=0, engine= "python")
            # print(df.columns)
            df_list.append(df)

        dft_2d_list.append(df_list)
        dfth_2d_list.append(dfth_list)

    return [dft_2d_list, dfth_2d_list, dffh_list, dffgh_list, r]


def write_asd(path, asd_data, encoding=None):
    dft_2d_list = asd_data[0] # tables/groups
    dfth_2d_list = asd_data[1] # table/group headers
    dffh_list = asd_data[2] # file headers
    dffgh_list = asd_data[3] # filegroup headers
    r = asd_data[4] # readable/viewable format flag

    # df_2d_list = asd_data[0]
    # dfth_2d_list = asd_data[1]
    # dfgh_list = asd_data[2]
    # dffh_list = asd_data[3]

    RS =ASCIIConstants.F_RS(r)
    US =ASCIIConstants.F_US(r)

    FS =ASCIIConstants.F_FS(r)
    GS =ASCIIConstants.F_GS(r)

    SOHG =ASCIIConstants.F_SOHG(r)
    STXG =ASCIIConstants.F_STXG(r)
    ETXG =ASCIIConstants.F_ETXG(r)

    SOHF =ASCIIConstants.F_SOHF(r)
    STXF =ASCIIConstants.F_STXF(r)
    ETXF =ASCIIConstants.F_ETXF(r)

    SOHFG =ASCIIConstants.F_SOHFG(r)
    STXFG =ASCIIConstants.F_STXFG(r)
    ETXFG =ASCIIConstants.F_ETXFG(r)


    firstFSflag = False
    firstGSflag = False
    tabletext = ""
    tableheadertext = ""
    groupheadertext = ""
    filegroupheadertext = ""
    
    mode = 'wt'
    with open(path, mode=mode, encoding=encoding) as fileoutput:
        # pd.DataFrame(dffh_list[0])
        if(len(dffgh_list) > 0):
            filegroupheadertext = '' if dffgh_list[0] is None else dffgh_list[0]
            if r == True:
                filegroupheadertext = SOHFG + "READABLE" + STXFG + filegroupheadertext + ETXFG
            # print(filegroupheadertext)
            fileoutput.write(filegroupheadertext)

        for (file, tableheaders, fileheaders) in itertools.zip_longest(dft_2d_list, dfth_2d_list, dffh_list):             
            fileheaders = '' if fileheaders is None else fileheaders
            if(len(fileheaders) > 0):
                fileheadertext = (FS if(firstFSflag == True) else '') + SOHF + STXF + fileheaders + ETXF
            else:
                fileheadertext = (FS if(firstFSflag == True) else '')
            # print(fileheadertext)
            fileoutput.write(fileheadertext)
            
            firstFSflag = True
            firstGSflag = False
            for (table, tableheader) in itertools.zip_longest(file, tableheaders):         
                tableheader = '' if tableheader is None else tableheader
                if(len(tableheader) > 0):
                    tableheadertext = (GS if(firstGSflag == True) else '') + SOHG + STXG + tableheader + ETXG
                else:
                    tableheadertext = (GS if(firstGSflag == True) else '')
                # print(tableheadertext)
                fileoutput.write(tableheadertext)

                firstGSflag = True
                
                df = table #pd.DataFrame(table)
                tabletext = df.to_csv(sep=ASCIIConstants._US, lineterminator=ASCIIConstants._RS, index=False, encoding=encoding)
                if r == True:
                    tabletext = tabletext.replace(ASCIIConstants._RS, RS).replace(ASCIIConstants._US, US)
                # print(tabletext)
                fileoutput.write(tabletext)
    fileoutput.close()



# # Chunk By Chunk
# https://stackoverflow.com/questions/47927039/reading-a-file-until-a-specific-character-in-python
# def each_chunk(stream, separator):
#   buffer = ''
#   while True:  # until EOF
#     chunk = stream.read(CHUNK_SIZE)  # I propose 4096 or so
#     if not chunk:  # EOF?
#       yield buffer
#       break
#     buffer += chunk
#     while True:  # until no separator is found
#       try:
#         part, buffer = buffer.split(separator, 1)
#       except ValueError:
#         break
#       else:
#         yield part

# with open('myFileName') as myFile:
#   for chunk in each_chunk(myFile, separator='\\-1\n'):
#     print(chunk)  # not holding in memory, but printing chunk by chunk