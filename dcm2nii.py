import argparse
import pathlib
import sys

import nibabel as nib
import numpy as np
import pydicom
import imageio

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    "-i",
    "--input",
    type=pathlib.Path,
    metavar="folder",
    help="Dicom input folder",
    dest="input_folder",
    required=True,
)
parser.add_argument(
    "-o",
    "--output",
    default="nii",
    type=pathlib.Path,
    metavar="folder",
    help="output folder",
    dest="output_folder",
    required=True,
)

ignore = ["ID00052637202186188008618"]


def read_dicom_to_ndarray(folder: pathlib.Path) -> np.ndarray:
    print(folder)
    dicom_arrs = []
    for dcm_file in sorted(folder.iterdir(), key=lambda x: int(x.name.split(".")[0])):
        dicom_arrs.append(pydicom.dcmread(dcm_file).pixel_array)
    return np.array(dicom_arrs)


def save_to_nii(data: np.ndarray, filename: str):
    img = nib.Nifti1Image(data, np.eye(4))
    nib.save(img, filename)


def create_screenshot(data: np.ndarray, filename: str):
    mip_image = data.max(0)
    imageio.imwrite(filename, mip_image)



def main():
    args, _ = parser.parse_known_args()
    input_folder = args.input_folder.absolute()
    output_folder = args.output_folder.absolute()

    for dicom_folder in input_folder.iterdir():
        if dicom_folder.name not in ignore:
            dcm_array = read_dicom_to_ndarray(dicom_folder)
            nii_filename = output_folder.joinpath(dicom_folder.name, "image.nii.gz")
            nii_filename.parent.mkdir(parents=True, exist_ok=True)
            save_to_nii(dcm_array, str(nii_filename))
            #create_screenshot(dcm_array, str(nii_filename).replace("nii.gz", "png"))


if __name__ == "__main__":
    main()
