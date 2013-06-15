"""Experiment parameters for main dksort experiment."""

## Preprocessing parameters

# Basic information
source_template = "%s/nifti/scan0?.nii.gz"
n_runs = 4
TR = 2

# Equillibrium scans
frames_to_toss = 6

# Slice time correction
slice_time_correction = True
interleaved = False
slice_order = "up"

# Spatial smoothing
smooth_fwhm = 6

# High pass filter
hpf_sigma = 128

## Univariate model parameters

hrf_model = "dgamma"
hrf_derivs = False
parfile_base_dir = "/Users/mwaskom/Studies/DKsort/data"
parfile_template = "%(subject_id)s/parfiles/%(event)s_r%(run)1.txt"
units = "secs"
