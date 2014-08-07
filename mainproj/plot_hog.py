"""
===============================
Histogram of Oriented Gradients
===============================

The `Histogram of Oriented Gradient
<http://en.wikipedia.org/wiki/Histogram_of_oriented_gradients>`__ (HOG) feature
descriptor [1]_ is popular for object detection.

In the following example, we compute the HOG descriptor and display
a visualisation.

Algorithm overview
------------------

Compute a Histogram of Oriented Gradients (HOG) by

    1. (optional) global image normalisation
    2. computing the gradient image in x and y
    3. computing gradient histograms
    4. normalising across blocks
    5. flattening into a feature vector

The first stage applies an optional global image normalisation
equalisation that is designed to reduce the influence of illumination
effects. In practice we use gamma (power law) compression, either
computing the square root or the log of each colour channel.
Image texture strength is typically proportional to the local surface
illumination so this compression helps to reduce the effects of local
shadowing and illumination variations.

The second stage computes first order image gradients. These capture
contour, silhouette and some texture information, while providing
further resistance to illumination variations. The locally dominant
colour channel is used, which provides colour invariance to a large
extent. Variant methods may also include second order image derivatives,
which act as primitive bar detectors - a useful feature for capturing,
e.g. bar like structures in bicycles and limbs in humans.

The third stage aims to produce an encoding that is sensitive to
local image content while remaining resistant to small changes in
pose or appearance. The adopted method pools gradient orientation
information locally in the same way as the SIFT [2]_
feature. The image window is divided into small spatial regions,
called "cells". For each cell we accumulate a local 1-D histogram
of gradient or edge orientations over all the pixels in the
cell. This combined cell-level 1-D histogram forms the basic
"orientation histogram" representation. Each orientation histogram
divides the gradient angle range into a fixed number of
predetermined bins. The gradient magnitudes of the pixels in the
cell are used to vote into the orientation histogram.

The fourth stage computes normalisation, which takes local groups of
cells and contrast normalises their overall responses before passing
to next stage. Normalisation introduces better invariance to illumination,
shadowing, and edge contrast. It is performed by accumulating a measure
of local histogram "energy" over local groups of cells that we call
"blocks". The result is used to normalise each cell in the block.
Typically each individual cell is shared between several blocks, but
its normalisations are block dependent and thus different. The cell
thus appears several times in the final output vector with different
normalisations. This may seem redundant but it improves the performance.
We refer to the normalised block descriptors as Histogram of Oriented
Gradient (HOG) descriptors.

The final step collects the HOG descriptors from all blocks of a dense
overlapping grid of blocks covering the detection window into a combined
feature vector for use in the window classifier.

References
----------

.. [1] Dalal, N. and Triggs, B., "Histograms of Oriented Gradients for
       Human Detection," IEEE Computer Society Conference on Computer
       Vision and Pattern Recognition, 2005, San Diego, CA, USA.

.. [2] David G. Lowe, "Distinctive image features from scale-invariant
       keypoints," International Journal of Computer Vision, 60, 2 (2004),
       pp. 91-110.

"""
import matplotlib.pyplot as plt1

#import skimage.feature
from skimage.feature import hog

from skimage import data, color, exposure
import os
import PIL.Image as Image
import sys


"""
fd, hog_image = hog(image, orientations=8, pixels_per_cell=(16, 16),
                    cells_per_block=(1, 1), visualise=True)

plt.figure(figsize=(8, 4))

plt.subplot(121).set_axis_off()
plt.imshow(image, cmap=plt.cm.gray)
plt.title('Input image')

# Rescale histogram for better display
hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 0.02))

plt.subplot(122).set_axis_off()
plt.imshow(hog_image_rescaled, cmap=plt.cm.gray)
#plt.title(fd)
plt.title('Histogram of Oriented Gradients')
plt.show()
"""

def plothog(k1):
    infile=os.path.join('C:\meenuneenu\project\libsvm-3.17\python\data',"IMG-%s.png" % k1)
    #infile="C:/Python27/Lib/site-packages/temp/svm/window/window4.jpg"
    #img = Image.open(infile)
    img = Image.open(infile)
    #image = color.rgb2gray(data.lena())
    """
    width = 50
    height = 50 
    # Resize it.
    img = img.resize((width, height), Image.BILINEAR)
    # Save it back to disk.
    img.save(os.path.join("C:/Python27/Lib/site-packages/temp/svm/", 'resized.png'))
    """
    img = img.convert('1')
    img.save("C:/Python27/Lib/site-packages/temp/IMG-4.png")

    fd = list(hog(img, orientations=8, pixels_per_cell=(16, 16),
                        cells_per_block=(1, 1), visualise=False))
#filepath=os.path.join('C:/Python27/Lib/site-packages/temp',"data%s.txt" % k1)
    filepath=os.path.join('C:\meenuneenu\project\libsvm-3.17\python\data',"data%s.txt" % k1)
    
    file = open(filepath, "w")
    for item in fd:
        file.write("%s " % item)
    file.close()
#delpath=os.path.join('rm C:/Python27/Lib/site-packages/temp/',"IMG-%s.png" % k)
    os.system('rm C:/Python27/Lib/site-packages/temp/IMG-4.png')
        