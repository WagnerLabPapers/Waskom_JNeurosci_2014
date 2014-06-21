import sys
sys.path.insert(0, "nilearn/")

import os
import os.path as op
import argparse
import numpy as np
import pandas as pd
from scipy import ndimage
from scipy.stats import zscore
import nibabel as nib
import subprocess as sp
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import LeaveOneLabelOut
from nilearn.decoding import SearchLight

import lyman
project = lyman.gather_project_info()
data_dir = project["data_dir"]
analysis_dir = project["analysis_dir"]


def main(arglist):

    args = parse_args(arglist)

    if args.subjects is None:
        args.subjects = lyman.determine_subjects()

    for subj in args.subjects:

        print "Running subject", subj

        searchlight_dir = op.join(analysis_dir, "dksort", subj,
                                  "mvpa/searchlight")

        if not op.exists(searchlight_dir):
            os.mkdir(searchlight_dir)

        vol_fname = op.join(searchlight_dir, "dimension_dksort_pfc.nii.gz")

        if "fit" in args.do and (not op.exists(vol_fname) or args.overwrite):

            print " Doing searchlight" 

            mask_img, X, y, runs = load_data(subj)

            s = SearchLight(mask_img, radius=10, n_jobs=10,
                            estimator=LogisticRegression(),
                            cv=LeaveOneLabelOut(runs))
            s.fit(X, y)
            out_img = nib.Nifti1Image(s.scores_, s.mask_img.get_affine())
            out_img.to_filename(vol_fname)

        surf_fnames = [op.join(searchlight_dir, "lh.dimension_dksort_pfc.mgz"),
                       op.join(searchlight_dir, "rh.dimension_dksort_pfc.mgz")]

        if "surf" in args.do and (not all(map(op.exists, surf_fnames))
                                  or args.overwrite):

            print " Doing surfreg"

            reg_fname = op.join(analysis_dir, "dksort", subj,
                                "preproc/run_1/func2anat_tkreg.dat")

            for i, hemi in enumerate(["lh", "rh"]):

                cmdline = ["mri_vol2surf",
                           "--mov", vol_fname,
                           "--reg", reg_fname,
                           "--trgsubject", "fsaverage",
                           "--projfrac-avg", "0", "1", ".1",
                           "--surf-fwhm", "5",
                           "--hemi", hemi,
                           "--o", surf_fnames[i]]
                sp.check_output(" ".join(cmdline), shell=True)


def load_data(subj):

    design = pd.read_csv(op.join(data_dir, subj, "design/dimension.csv"))
    mask_img = nib.load(op.join(data_dir, subj, "masks/dksort_all_pfc.nii.gz"))
    mean_img = nib.load(op.join(analysis_dir, "dksort", subj, 
                                "preproc/run_1/mean_func.nii.gz"))

    orig_mask_data = mask_img.get_data()
    mask_data = ndimage.binary_dilation(orig_mask_data, iterations=2)
    mask_img = nib.Nifti1Image(mask_data.astype(int),
                               mask_img.get_affine(),
                               mask_img.get_header())

    mask_img.to_filename(op.join(analysis_dir, "dksort", subj,
                                 "mvpa/searchlight/dksort_pfc_mask.nii.gz"))

    X_data = []
    for run in range(1, 5):
        ts_img = nib.load(op.join(analysis_dir, "dksort", subj, "reg/epi",
                          "unsmoothed/run_%d" % run, "timeseries_xfm.nii.gz"))

        ts_data = ts_img.get_data()
        onsets = design.loc[design.run == run, "onset"].values
        indices = np.round(onsets / 2).astype(int)

        frame1 = ts_data[..., indices + 2]
        frame2 = ts_data[..., indices + 3]

        X_run = np.mean([frame1, frame2], axis=0)
        X_run = zscore(X_run, axis=-1)
        X_data.append(X_run)

    X = nib.Nifti1Image(np.concatenate(X_data, axis=-1),
                        mean_img.get_affine(), mean_img.get_header())
    y = design["condition"].values
    runs = design["run"].values

    return mask_img, X, y, runs

def parse_args(arglist):

    parser = argparse.ArgumentParser()
    parser.add_argument("-subjects", nargs="*")
    parser.add_argument("-do", nargs="*", default=[])
    parser.add_argument("-overwrite", action="store_true")
    args = parser.parse_args(arglist)
    return args


if __name__ == "__main__":
    main(sys.argv[1:])
