def swap_ids(in_file_path, swap_identifier_df):
    
    """
    Read in a file with 5-digit numeric identifier in the file contents
    and filename, change all identifiers for a new 5-digit numeric 
    identifier, and save everything to a new file.
    
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
    
    # swap the new identifier for the old identifier
    swapped_datafile = re.sub(r"(?<!\d)%s(?!\d)" % original_id,
                           new_id,
                           original_datafile)
    
    # create a dataframe to report our counts of new and old IDs
    original_old_count = original_datafile.count(original_id)
    original_new_count = original_datafile.count(new_id)
    swapped_old_count = swapped_datafile.count(original_id)
    swapped_new_count = swapped_datafile.count(new_id)
    swap_report_df = pd.DataFrame({'new_id' : [new_id],
                                   'original_old_count' : [original_old_count],
                                   'original_new_count' : [original_new_count],
                                   'swapped_old_count' : [swapped_old_count],
                                   'swapped_new_count' : [swapped_new_count]})
    
    # update the name so that we can save it in a new directory
    out_file_name = re.sub('00-raw','01-input',in_file_path)
    out_file_name = re.sub(r"(?<!\d)%s(?!\d)" % original_id,
                           new_id,
                           out_file_name)
    
    # save the file 
    data_write = open(out_file_name, "w")
    data_write.write(swapped_datafile)
    data_write.close()
    
    return swap_report_df