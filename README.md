# Opinions and Gaze: Code for Paxton, Richardson, & Dale (*submitted*)

This repo contains code for the analyses presented in our article, "Seeing the
other side: Conflict and controversy increase gaze coordination" (Paxton, Dale,
& Richardson, *submitted*).

## Overview

The repo contains separate directories for analysis files, figures, and
supplementary code.

* `analyses`: Directory of Jupyter notebooks:
    * `oag-data_cleaning.ipynb`: Notebook with Python kernel. Converts raw
      output files into more manageable formats.
    * `oag-data_preparation.ipynb`: Notebook with R kernel. Cleans the data
      and outputs analysis-ready files.
    * `oag-data_analysis.ipynb`: Notebook with R kernel. Performs analysis over
      processed and cleaned data. Includes aggregated code output to show
      work for those who cannot access the raw data from ICPSR.
* `supplementary-code`: Directory of R and Python scripts called by the
  notebooks.
* `figures`: Directory of figures produced by `oag-data_analysis.ipynb`.

## Related materials

Data for the project are available to verified researchers through ICPSR. The
determination to make these data openly available only to researchers was made
by the original ethical governing body for the study (the [Institutional
Review Board](http://rci.ucmerced.edu/irb) at the [University of California,
Merced](https://www.ucmerced.edu/)), in keeping with the approved IRB protocol
and the informed consent signed by participants. A link to the data deposit
will be made available once the deposit is accepted by ICSPR. You can find more
about ICSPR's restricted-use data policies on
[their website](https://www.icpsr.umich.edu/icpsrweb/content/ICPSR/access/restricted/).

## Notes on running and viewing

Static notebooks may be viewed in your browser. In order to interact with the
notebooks, you will need to download them to your computer; in order to execute
them, you will need to download the data from ICPSR (again, in accordance with
their restricted-use data policies) as well.

For those unfamiliar with Jupyter notebooks, we recommend taking a look at
[Project Jupyter's documentation and FAQ](https://jupyter.readthedocs.io/en/latest/running.html#running)
before getting started. (Be sure to have [Jupyter](http://jupyter.org/install)
installed first.)
