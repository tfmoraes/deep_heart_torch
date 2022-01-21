import pathlib
import nibabel as nib
import numpy as np
import shutil

import sys

def read_nii(filename: pathlib.Path) -> np.ndarray:
    nii = nib.load(str(filename))
    return nii.get_fdata()

def main():
    folder = pathlib.Path(sys.argv[1]).absolute()
    output_folder = pathlib.Path(sys.argv[2]).absolute()
    for nii_folder in folder.iterdir():
        image_filename = nii_folder.joinpath("image.nii.gz")
        mask_filename = nii_folder.joinpath("mask.nii.gz")

        if image_filename.exists() and mask_filename.exists():
            image = read_nii(image_filename)
            mask = read_nii(mask_filename)
            if image.shape == mask.shape:
                shutil.copytree(image_filename.parent, output_folder.joinpath(image_filename.parent.name))



if __name__ == "__main__":
    main()
