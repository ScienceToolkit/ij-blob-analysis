#@ Dataset(label="Image:") image
#@ Dataset(label="Mask:") mask
#@ String(label="Smoothing:", choices={"None", "Mean 3x3", "Mean 5x5"}) smoothing
#@ String(label="Thresholding:", choices={"None", "ij1", "li", "otsu"}) thresholding
#@ String(label="Comment:", value="") comment
#@ ResultsTable results
#@ LogService logging
#@ OpService ops
#@ UIService ui

from ij import IJ
from ij.gui import ImageRoi
from ij.gui import Overlay

from net.imglib2.algorithm.labeling.ConnectedComponents import StructuringElement
from net.imglib2.algorithm.neighborhood import CenteredRectangleShape
from net.imglib2.img.display.imagej import ImageJFunctions
from net.imglib2.outofbounds import OutOfBoundsMirrorFactory
from net.imglib2.roi import Regions
from net.imglib2.roi.labeling import LabelRegions


# Smooth if desired
smoothed = mask.duplicate()
if smoothing == "None":
    pass
elif smoothing == "Mean 3x3":
    smooth_shape = CenteredRectangleShape([1,1], False)
    ops.run("filter.mean", smoothed, mask, smooth_shape)
elif smoothing == "Mean 5x5":
    smooth_shape = CenteredRectangleShape([2,2], False)
    ops.run("filter.mean", smoothed, mask, smooth_shape)

# Threshold if required
if thresholding == "None":
    binary = ops.run("threshold.mean", mask)
else:
    binary = ops.run("threshold.%s" % thresholding, smoothed)

# Create LabelRegions
img_labeling = ops.run("labeling.cca", binary, StructuringElement.EIGHT_CONNECTED)
regions = list(LabelRegions(img_labeling))

# Process each LabelRegion
for region in regions:
    # Get a sample view
    sample = Regions.sample(region, image)

    # Compute the stats
    area = ops.run("stats.size", sample)
    min = ops.run("stats.min", sample)
    max = ops.run("stats.max", sample)
    mean = ops.run("stats.mean", sample)
    median = ops.run("stats.median", sample)
    stdev = ops.run("stats.stdDev", sample)
    sum = ops.run("stats.sum", sample)

    # Increment the row and add everything to the table
    results.incrementCounter()
    results.addValue("area", area.getRealDouble())
    results.addValue("min", min.getRealDouble())
    results.addValue("max", max.getRealDouble())
    results.addValue("mean", mean.getRealDouble())
    results.addValue("median", median.getRealDouble())
    results.addValue("stdev", stdev.getRealDouble())
    results.addValue("sum", sum.getRealDouble())
    results.addValue("comment", comment)

# Display the table
results.show("Results")

# Outline and highlight the regions
outline = ops.run("morphology.outline", binary, False)
image_imp = ImageJFunctions.wrap(image, "Overlay Render")
binary_imp = ImageJFunctions.wrap(binary, "Binary")
outline_imp = ImageJFunctions.wrap(outline, "Outline")

IJ.run(binary_imp, "Green", "")
binary_ROI = ImageRoi(0, 0, binary_imp.getProcessor())
binary_ROI.setZeroTransparent(True)
binary_ROI.setOpacity(0.25)

IJ.run(outline_imp, "Green", "")
outline_ROI = ImageRoi(0, 0, outline_imp.getProcessor())
outline_ROI.setZeroTransparent(True)
outline_ROI.setOpacity(1.00)

overlay = Overlay()
overlay.add(binary_ROI)
overlay.add(outline_ROI)

image_imp.setOverlay(overlay)
image_imp.updateAndDraw()
image_imp.show()
