#### libraries_and_functions-oag.r: Part of the "Opinions and Gaze" project ####
#
# This script loads libraries and creates a number of 
# additional functions to facilitate data prep and analysis.
#
# Written by: A. Paxton (University of California, Berkeley)
# Date last modified: 04 April 2018
#####################################################################################

#### Load necessary packages ####

# list of required packages
required_packages = c(
    'crqa',
    'lme4',
    'ggplot2',
    'gsubfn',
    'zoo',
    'dplyr',
    'data.table',
    'pander',
    'scales',
    'RCurl',
    'stringr',
    'LambertW'
)

# install missing packages (adapted from <http://stackoverflow.com/a/4090208>)
missing_packages = required_packages[!(required_packages %in% installed.packages()[,"Package"])]
if (length(missing_packages) > 0) {
  install.packages(missing_packages)
}

# load required packages
invisible(lapply(required_packages, require, character.only = TRUE))

#### Specify global variables ####

# prevent scientific notation
options(scipen=999)

# set which columns we'd like to keep for analysis later
speaker_keep_columns = c('r_aoi',
                         'r_event',
                         'time',
                         'speaker',
                         'side',
                         'topic')
listener_keep_columns = c('r_aoi',
                          'r_event',
                          'time')
old_rename_columns = c('R.AOI.Hit', 'R.Event.Info')
new_rename_columns = c('r_aoi', 'r_event')

# target the variables we want for CRQA calculations
crqa_compare_columns = c('r_aoi',
                         'time')
crqa_questionnaire_columns = c('agree',
                               'gender',
                               'listener',
                               'topic',
                               'side',
                               'native_lang',
                               'age')

# specify dominant-view topics
dominant_view_topics = c('abortion',
                         'gay-marriage',
                         'legal-marijuana',
                         'tax-rich')

# specify sampling rate
native_sampling_rate = 100
native_sampling_fraction = 1/native_sampling_rate
sampling_hz = 10
sampling_fraction = 1/sampling_hz

# create file paths for cleaned, processed, and analysis-ready data
input_data_path = file.path('../data/01-input')
cleaned_data_path = file.path('../data/02-data_cleaning')
processed_data_path = file.path('../data/03-data_processing')
analysis_data_path = file.path('../data/04-analysis_dataframes')

# identify which variables should be factors
factor_variables = c('speaker',
                     'listener',
                     'topic_and_side',
                     'agree',
                     'gender',
                     'native_lang',
                     'data',
                     'viewtype')

#### Specify CRQA variables ###

# specify window size (in samples) for DRPs
win_size = 30

#### Create functions ####
# function to return an opinion if we have it and an NA if we don't
set_opinion = function(opinion_df,
                       answer_variable,
                       source_variable,
                       match_answer){
    opinion = opinion_df[,answer_variable][opinion_df[,source_variable]==match_answer]
    if (length(opinion)==0){
        opinion = NA
    }
    return(opinion)
}

# function to return a concatenated string if an answer would be multiple strings
set_concat_opinion = function(opinion_df,
                              answer_variable,
                              source_variable,
                              match_answer){
    opinion = set_opinion(opinion_df,answer_variable,source_variable,match_answer)
    if (length(opinion) > 1){
        opinion = paste(opinion, collapse = '') 
    }
    return(opinion)
}

# function to ensure that specified sampling rate
# is compatible with code as written
create_downsampled_time = function(sampling_rate){
        
    if ((log10(sampling_rate) - as.integer(log10(sampling_rate))) > 0){
        # print an error if it won't work
        print("Specified sampling rate is not compatible with 
              code as written. Common logarithm of `sampling_hz` 
              must be a whole number. Please update and re-source 
              `libraries_and_functions-oag.r`.")
        return(NaN)
    } else {

        # otherwise, return new time variable
        return(ceiling(log10(sampling_rate)))
    }
}

# downsampling function
downsample_df = function(original_df,
                         time_variable,
                         start_time,
                         increment_time,
                         downsample_rate){
    
    # identify time variable
    original_times = original_df[,time_variable]
    
    # expand the time variable so we can account for missing slices
    new_times = as.data.frame(seq(start_time,max(original_times),increment_time))
    new_times$time = new_times[,1]
    
    # use our previously specified downsampling rate (in Hz) to identify slices to keep
    new_times = data.frame(new_times$time,(seq_along(new_times$time)-1),
                              ((seq_along(new_times$time)-1)%%(downsample_rate*increment_time)==0))
    
    # rename some variables and drop originals
    new_times$sample_num = new_times[,2]
    new_times$target_sample = new_times[,3]
    new_times[,2:3] <- list(NULL)
    new_times = plyr::rename(new_times,c("new_times.time"="time"))
    
    # spit back the new dataframe
    return(new_times)
}

# function to return p-values from t-values
pt = function(x) {return((1-pnorm(abs(x)))*2)}

#### Read in model output formatting functions from repo ####

# read in `pander_lme` at the correct commit
# thanks to https://github.com/opetchey/RREEBES/wiki/
pander_lme_url = "https://raw.githubusercontent.com/a-paxton/stats-tools/bee546f2c959cb6a5b9cad1f28d3afbae6e46c41/pander_lme.R"
pander_lme_file = getURL(pander_lme_url, ssl.verifypeer = FALSE)
eval(parse(text = pander_lme_file))
