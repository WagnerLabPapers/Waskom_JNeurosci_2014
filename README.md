DKsort Manuscript Code
======================

This repository contains all of the code related to the DKsort project manuscript. The code is contained within several IPython notebooks that will perform the main analyses and generate all figures used in the manuscript.

Two processing steps were performed outside the scope of this code. First,
the anatomical image for each subject was processed using Freesurfer 5.1 to
generate the cortical surface models. Specifically, the following command line was used for each subject:

    recon-all -s $subject -all -nuintensitycor-3T

Additionally, the functional data were preproccesed with FSL 4.1 and Freesufer 5.1 tools using Lyman, which contains my fMRI workflows as implemented in Nipype. Specifically, [this commit](https://github.com/mwaskom/lyman/tree/dfe0512bda2098dc8aeb0cda3542ee6698e7df58) of the Lyman repository was used. The processing was performed with the following command line:

    run_fmri.py -s subjects.txt -w preproc reg -t -reg epi -unsmoothed

Once those commands have been executed, every analysis can be generated using these notebooks.
