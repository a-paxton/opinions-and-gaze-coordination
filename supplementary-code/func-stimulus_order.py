def stimulus_order(xml_file):

    import re

    # only grab XML "Name" tags
    stimulus_order = re.findall('(?<=\" Name=\").*(?=\" Type=)',xml_file)

    # clean them all up
    stimulus_order = [stimulus for stimulus in stimulus_order if len(re.findall('.rtf',stimulus))>0]
    stimulus_order = [stimulus for stimulus in stimulus_order if len(re.findall('instructions',stimulus))==0]
    stimulus_order = [stimulus for stimulus in stimulus_order if len(re.findall('thank-you',stimulus))==0]

    # spit out the cleaned file
    return [re.sub('.rtf','',stimulus) for stimulus in stimulus_order]