def clean_responses(subject_ID, in_tsv, out_csv=None):

    """
    Clean participant questionnaire TSV files
    and save as CSV files.
    
    Parameters
    ----------
    
    subject_ID : str
        Unique participant identifier
        
    in_tsv : str
        Path to raw TSV file to be processed
    
    out_csv : None or str (optional)
        Path (CSV) to which cleaned dataframe
        file will be saved.
        
    Output
    ------
    
    datafile : pandas DataFrame
        Cleaned dataframe.
    
    """
    
    # preliminaries
    import re
    from StringIO import StringIO
    import pandas as pd

    # open up the TSV file
    tsv = open(in_tsv, 'r')
    file_data = tsv.read()

    # strip out what we don't need
    file_data = re.sub("Please write a brief summary "
                       "of your opinion in response to "
                       "the question below.",'',
                       file_data)
    file_data = re.sub("Please choose the number that "
                       "best describes how strongly you "
                       "feel about your opinion.",'',
                       file_data)
    file_data = re.sub("Please rate the following "
                       "question based on the opinion "
                       "you just heard.",'',
                       file_data)
    file_data = re.sub(subject_ID+'\t', "", file_data)
    file_data = re.sub(subject_ID, "", file_data)
 
    # remove grammatical commas and apostrophes,
    # convert from tabs to commas, and remove
    # multiple empty lines
    file_data = re.sub(',',' ',file_data)
    file_data = re.sub('\'','',file_data)
    file_data = re.sub("\t", ",", file_data)
    file_data = re.sub('\n+','\n',file_data)

    # convert to a dataframe to make processing easier
    datafile = pd.read_table(StringIO(file_data),
                             sep=',')
    
    # clean up column names
    datafile_colnames = datafile.columns.tolist()
    datafile_colnames.remove('Subject')
    
    # reset index and remove lines with NA
    datafile = datafile.reset_index(
                            drop=True
                        ).dropna(axis=0,
                                 subset=['Question']
                                ).dropna(axis=1)
    

    
    # rename columns
    datafile.columns = datafile_colnames
    datafile = datafile.reset_index(drop=True)
    
    # write out the new file
    if out_csv is not None:
        datafile.to_csv(out_csv, 
                        sep=',', 
                        header=True, 
                        index=False)
    
    # return the dataframe
    return datafile