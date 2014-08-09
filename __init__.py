"""Standard test images.

For more images, see

 - http://sipi.usc.edu/database/database.php

"""

import os as _os

from ..io import imread
from skimage import data_dir


__all__ = ['load',
           'camera',
           'lena',
           'text',
           'checkerboard',
           'coins',
           'moon',
           'page',
           'horse',
           'clock',
           'immunohistochemistry',
           'chelsea',
           'IMG-1',
           'IMG-2',
           'IMG-3',
           'IMG-4',
           'IMG-5',
           'IMG-6',
           'IMG-7',
           'coffee']


def load(f):
    """Load an image file located in the data directory.

    Parameters
    ----------
    f : string
        File name.

    Returns
    -------
    img : ndarray
        Image loaded from skimage.data_dir.
    """
    return imread(_os.path.join(data_dir, f))


def camera():
    """Gray-level "camera" image.

    Often used for segmentation and denoising examples.

    """
    return load("camera.png")


def lena():
    """Colour "Lena" image.

    The standard, yet sometimes controversial Lena test image was
    scanned from the November 1972 edition of Playboy magazine.  From
    an image processing perspective, this image is useful because it
    contains smooth, textured, shaded as well as detail areas.

    """
    return load("lena.png")


def text():
    """Gray-level "text" image used for corner detection.

    Notes
    -----
    This image was downloaded from Wikipedia
    <http://en.wikipedia.org/wiki/File:Corner.png>`__.

    No known copyright restrictions, released into the public domain.

    """

    return load("text.png")


def checkerboard():
    """Checkerboard image.

    Checkerboards are often used in image calibration, since the
    corner-points are easy to locate.  Because of the many parallel
    edges, they also visualise distortions particularly well.

    """
    return load("chessboard_GRAY.png")


def coins():
    """Greek coins from Pompeii.

    This image shows several coins outlined against a gray background.
    It is especially useful in, e.g. segmentation tests, where
    individual objects need to be identified against a background.
    The background shares enough grey levels with the coins that a
    simple segmentation is not sufficient.

    Notes
    -----
    This image was downloaded from the
    `Brooklyn Museum Collection
    <http://www.brooklynmuseum.org/opencollection/archives/image/617/image>`__.

    No known copyright restrictions.

    """
    return load("coins.png")


def moon():
    """Surface of the moon.

    This low-contrast image of the surface of the moon is useful for
    illustrating histogram equalization and contrast stretching.

    """
    return load("moon.png")


def page():
    """Scanned page.

    This image of printed text is useful for demonstrations requiring uneven
    background illumination.

    """
    return load("page.png")


def horse():
    """Black and white silhouette of a horse.

    This image was downloaded from
    `openclipart <http://openclipart.org/detail/158377/horse-by-marauder>`

    Released into public domain and drawn and uploaded by Andreas Preuss
    (marauder).

    """
    return load("horse.png")


def clock():
    """Motion blurred clock.

    This photograph of a wall clock was taken while moving the camera in an
    aproximately horizontal direction.  It may be used to illustrate
    inverse filters and deconvolution.

    Released into the public domain by the photographer (Stefan van der Walt).

    """
    return load("clock_motion.png")


def immunohistochemistry():
    """Immunohistochemical (IHC) staining with hematoxylin counterstaining.

    This picture shows colonic glands where the IHC expression of FHL2 protein
    is revealed with DAB. Hematoxylin counterstaining is applied to enhance the
    negative parts of the tissue.

    This image was acquired at the Center for Microscopy And Molecular Imaging
    (CMMI).

    No known copyright restrictions.

    """
    return load("ihc.png")


def chelsea():
    """Chelsea the cat.

    An example with texture, prominent edges in horizontal and diagonal
    directions, as well as features of differing scales.

    Notes
    -----
    No copyright restrictions.  CC0 by the photographer (Stefan van der Walt).

    """
    return load("chelsea.png")


def coffee():
    """Coffee cup.

    This photograph is courtesy of Pikolo Espresso Bar.
    It contains several elliptical shapes as well as varying texture (smooth
    porcelain to course wood grain).

    Notes
    -----
    No copyright restrictions.  CC0 by the photographer (Rachel Michetti).

    """
    return load("coffee.png")

def abc():
    return load("abc.jpg")

def IMG0():
    return load("IMG-0.png")

def IMG1():
    return load("IMG-1.png")

def IMG2():
    return load("IMG-2.png")

def IMG3():
    return load("IMG-3.png")

def IMG4():
    return load("IMG-4.png")

def IMG5():
    return load("IMG-5.png")

def IMG6():
    return load("IMG-6.png")

def IMG7():
    return load("IMG-7.png")

def IMG8():
    return load("IMG-7.png")

def IMG9():
    return load("IMG-7.png")

def IMG10():
    return load("IMG-7.png")

def IMG11():
    return load("IMG-7.png")

def IMG12():
    return load("IMG-7.png")

def IMG13():
    return load("IMG-7.png")

def IMG14():
    return load("IMG-7.png")

def IMG15():
    return load("IMG-7.png")

def IMG16():
    return load("IMG-7.png")

def IMG17():
    return load("IMG-7.png")

def IMG18():
    return load("IMG-7.png")

def IMG19():
    return load("IMG-7.png")

def IMG20():
    return load("IMG-7.png")

def IMG21():
    return load("IMG-7.png")

def IMG22():
    return load("IMG-7.png")

def IMG23():
    return load("IMG-7.png")

def IMG24():
    return load("IMG-7.png")

def IMG25():
    return load("IMG-7.png")

def IMG26():
    return load("IMG-7.png")

def IMG27():
    return load("IMG-7.png")

def IMG28():
    return load("IMG-7.png")

def IMG29():
    return load("IMG-7.png")

def IMG30():
    return load("IMG-7.png")

def IMG31():
    return load("IMG-7.png")

def IMG32():
    return load("IMG-7.png")

def IMG33():
    return load("IMG-7.png")
