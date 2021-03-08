def swap_ids_filename(in_file_path, swap_identifier_df):
    
    """
    Read in a file with 5-digit numeric identifier in the filename,
    change it for a new 5-digit numeric identifier, and save it
    to a new file.
    
    Parameters
    ----------
    
    in_file_path : str
        Path to raw data file
        
    swap_identifier_df : Pandas DataFrame
        Pandas DataFrame object with two variables:
            original_id : int, original 5-digit identifier
            new_id : int, new numeric 5-digit identifier 
    
    """
    
    # read in libraries
    import re
    import pandas as pd
    
    # read in the file from path
    data_read = open(in_file_path,'r')
    original_datafile = data_read.read()
    data_read.close()
    
    # grab file's identifier
    original_id = re.search('\d{5}',in_file_path).group()
    new_id = (swap_identifier_df['new_id']
              .loc[swap_identifier_df['original_id']==original_id]
              .values[0])
    
    # update the filename so that we can save it in a new directory
    out_file_name = re.sub('00-raw','01-input',in_file_path)
    out_file_name = re.sub(r"(?<!\d)%s(?!\d)" % original_id,
                           new_id,
                           out_file_name)
    
    # save the file 
    data_write = open(out_file_name, "w")
    data_write.write(original_datafile)
    data_write.close()