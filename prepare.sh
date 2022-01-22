#!/usr/bin/env bash

mkdir -p datasets
mkdir -p weights/
pushd datasets

# Downloading OSIC Pulmonary Fibrosis Progression
if [ ! -f osic-pulmonary-fibrosis-progression.zip ]; then
  echo "Downloading OSIC Pulmonary Fibrosis Progression"
  kaggle competitions download -c osic-pulmonary-fibrosis-progression
else
  echo "OSIC Pulmonary Fibrosis Progression already downloaded"
fi

# Downloading  CT Lung & Heart & Trachea segmentation"
if [ ! -f ct-lung-heart-trachea-segmentation.zip ]; then
  echo "Downloading CT Lung & Heart & Trachea segmentation"
  kaggle datasets download -d sandorkonya/ct-lung-heart-trachea-segmentation
else
  echo "CT Lung & Heart & Trachea segmentation already downloaded"
fi

####################### Extracting files ###################################
if [ ! -d "images/dicom" ]; then
  echo "Extracting osic-pulmonary-fibrosis-progression.zip"
  mkdir -p "images/dicom"
  unzip osic-pulmonary-fibrosis-progression.zip "train/*" -d "images/dicom/"
  mv images/dicom/train/* images/dicom/
  rm -r images/dicom/train
else
  echo "osic-pulmonary-fibrosis-progression.zip already extracted"
fi

if [ ! -d "masks/nrrd" ]; then
  echo "Extracting nrrd_heart"
  mkdir -p "masks/nrrd"
  unzip -j ct-lung-heart-trachea-segmentation.zip  "nrrd_heart/nrrd_heart/*" -d "masks/nrrd/"
else
  echo "nrrd_heart already extracted"
fi

popd

####################### Converting to nifti files ####################################

if [ ! -d "datasets/images/nii" ]; then
  echo "Converting images from dicom to nifti"
  mkdir -p datasets/images/nii
  python dcm2nii.py -i datasets/images/dicom -o datasets/images/nii
else
  echo "Images already converted to nifti"
fi

if [ ! -d "datasets/masks/nii" ]; then
  echo "Converting masks from nrrd to nifti"
  mkdir -p datasets/masks/nii
  python nrrd2nii.py -i datasets/masks/nrrd/ -o datasets/masks/nii
else
  echo "Masks already converted to nifti"
fi
