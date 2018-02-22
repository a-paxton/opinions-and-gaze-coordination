def clean_gaze_data(in_file_path):
    
    """
    Read in raw SMI gaze data and write
    out a clean file.
    
    Parameters
    ----------
    
    in_file_path : str
        Path to raw data file
    
    """
    
    import re
    from StringIO import StringIO
    import pandas as pd
    
    # read in the file from path
    data_read = open(in_file_path,'r')
    datafile = data_read.read()
    data_read.close()
    
    # strip out the header information
    datafile = re.sub('##.*Time',"Time",datafile)
    datafile = re.sub('\#\#.*(\r|\n){1,3}','',datafile)
    datafile = re.sub('\#\#.*(\r|\n){1,3}','',datafile)

    # clean up delimeter and quotes
    datafile = re.sub('\"','',datafile)
    datafile = re.sub('\t',',',datafile)
    
    # convert to a pandas dataframe and strip out MSG lines
    datafile = pd.read_table(StringIO(datafile),
                             sep=',')
    datafile = datafile[datafile['Type']!='MSG'].reset_index(drop=True)
    
    # drop unneeded variables
    keep_columns = ['Time',
                    'L Pupil Diameter [mm]',
                    'R Pupil Diameter [mm]',
                    'Pupil Confidence',
                    'L AOI Hit',
                    'R AOI Hit',
                    'L Event Info',
                    'R Event Info',
                    'Stimulus']
    datafile = datafile.filter(keep_columns)
    
    # convert types as needed
    datafile = datafile.astype(dtype={'Time': int,
                                     'L Pupil Diameter [mm]': float,
                                     'R Pupil Diameter [mm]': float,
                                     'Pupil Confidence': int,
                                     'L AOI Hit': str,
                                     'R AOI Hit': str,
                                     'L Event Info': str,
                                     'R Event Info': str,
                                     'Stimulus': str
                                     }, copy=False)

    # rename the file
    cleanname = re.sub('\_\d{3} Samples','-smi-data',in_file_path)
    cleanname = re.sub('--','-',cleanname)
    cleanname = re.sub('opin\-gaze\-LISTENER\-salvaged\_','',cleanname) 
    cleanname = re.sub('opinions\-and\-gaze\_','',cleanname) 
    cleanname = re.sub('gaze-raw','gaze-prepped',cleanname)
    cleanname = re.sub('.txt','.csv',cleanname)
    
    # let us know what you're up to...
    print('Processed SMI Data File: '+cleanname)

    # save as a new file in another location
    datafile.to_csv(cleanname, sep=',', header=True, index=False)
    