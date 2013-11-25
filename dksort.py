"""Preprocessing parameters for DKsort experiment."""
source_template = "{subject_id}/nifti/scan0?.nii.gz"
n_runs = 4
TR = 2
frames_to_toss = 6
temporal_interp = True
interleaved = False
slice_order = "up"
intensity_threshold = 3
motion_threshold = 0.5
hpf_cutoff = 128
