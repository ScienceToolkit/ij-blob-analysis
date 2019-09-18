# Blob Analysis in ImageJ
## Overview
This repository hosts a Jython script for [Fiji](https://fiji.sc/), a distribution of ImageJ. The
script aims to recreate much of the functionality of IJ1's "Analyze Particles" plugin using mostly the ImageJ2 API.

## Installation :hammer:
1. Download the [latest release](https://github.com/ScienceToolkit/ij-blob-analysis/releases) and unzip the files archive.
2. Copy and paste the _blob-analysis.py_ file into the plugins/Scripts/Plugins folder of your Fiji installation (Fiji.app folder).
3. Rename _blob-analysis.py_ to _Blob_Analysis.py_ or whatever you would like it to show up as in the plugin's menu.
4. Restart Fiji.

## Usage :rocket:
1. Open the image with the blobs you want to extract some intensity information about. You can use different images for generating the mask and quantifying the intensity.
2. Run the script (_Plugins &rarr; Blob Analysis_) and fill out the options accordingly. The parameters are described in the table below.
3. Take a look at the overlay render and see if the selected regions were what you expected.

| Parameter | Description |
|-----------|-------------|
| Image | The image that the intensity quantification is to be done on. |
| Mask | The image that will be thresholded and used for finding independent regions. |
| Smoothing | You can smooth the mask image with one of the smoothing filters provided in the "Smoothing" drop down if you wish. Smoothing can help with generating better masks from noisy images sometimes. |
| Thresholding Method| The algorithm to be used for generating the binary. The _"None"_ option can be selected if your mask image is already a binary image.|
| Comment | Add some text to the comment column of the output so you can identify which analysis the dataset is associated with. |
