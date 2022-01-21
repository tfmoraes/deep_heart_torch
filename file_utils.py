import pathlib
import sys
import typing


def get_trachea_files(
    base_folder: pathlib.Path,
) -> typing.List[typing.Tuple[pathlib.Path, pathlib.Path]]:
    files = []
    for nii_folder in base_folder.iterdir():
        image_filename = nii_folder.joinpath("image.nii.gz")
        mask_filename = nii_folder.joinpath("mask.nii.gz")
        if image_filename.exists() and mask_filename.exists():
            files.append((image_filename, mask_filename))
    return files


def main():
    base_folder = pathlib.Path(sys.argv[1]).resolve()
    trachea_files = get_trachea_files(base_folder)
    print(len(trachea_files))


if __name__ == "__main__":
    main()
