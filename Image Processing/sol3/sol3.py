import numpy as np
from scipy.misc import imread as imread
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
from scipy import ndimage
from scipy import signal
import os

GRAY_REP = 1
RGB_REP = 2

L_INTESITY = np.float32(255)
MIN_INTENS = np.float32(0.0)
MAX_INTENS = np.float32(1.0)

SIZE_FILTER_IM = 7
SIZE_FILTER_MASK = 7
MAX_LEVELS = 24


BASICE_GAUSSIAN = np.array([1,1]).reshape(1,2)

LIMIT_RES = 16

def im_to_float(image):
    """
    Convert image to float32 values between [0,1]
    """
    return image.astype(np.float32) / L_INTESITY




def read_image(filename, representation):
    """
    The function that reads a given image file and converts it into a given representation.
    :param - filename - string containing the image filename to read.
    :param - representation - representation code, either 1 or 2
             defining if the output should be either a grayscale OR RGB image respectively
    :return - The new image.
    """
    try:
        im = imread(filename)

        if representation == GRAY_REP:
            return rgb2gray(im).astype(np.float32)

        return im_to_float(im)

    except:
        print("Cant read the image")
        exit(-1)

def image_to_display(image, representation):
    """
    The function should open a new figure and display the loaded image in the converted representation
    :param - image - the image.
    :param - representation - representation code, either 1 or 2
             defining if the output should be either a grayscale OR RGB image respectively
    """

    plt.figure()

    cmap = None
    if representation == GRAY_REP:
        cmap = plt.cm.gray

    plt.imshow(image, cmap=cmap)
    plt.axis('off')
    plt.show()

def build_filter(filter_size):
    """
    Generates Gaussian kernel.
    :param filter_size: the size of the gaussian kernel in each dimension (an odd integer).
    :return: 1D kernel (as float32 type)
    """
    if filter_size <= 1:
        return np.array([1]).astype(np.float32)

    filter = BASICE_GAUSSIAN.astype(np.float32)
    for i in range(filter_size-2):
        filter = signal.convolve2d(filter, BASICE_GAUSSIAN)

    norm_filter = filter / np.float32(2**(filter_size-1))

    return norm_filter.astype(np.float32)

def filter_im(im, filter):
    """
    Filter the image given the filter
    :param im: a grayscale image with double values in [0, 1]
    :param filter: 1D gaussian like filter as float32 type
    :return: the image filtered
    """

    # Applied filter as row vector
    filtred_im = ndimage.filters.convolve(im, filter, mode='constant')

    # Applied filter as coloumn vector
    filtred_im = ndimage.filters.convolve(filtred_im, filter.T, mode='constant')

    return filtred_im.astype(np.float32)

def sample_im(im):
    """
    Return reduced im by half
    :param im: grayscale image with double values in [0, 1]
    :return:  grayscale image with double values in [0, 1] half the size
    """
    sampled_image = im[::2,::2]
    return sampled_image.astype(np.float32)

def  build_gaussian_pyramid(im, max_levels, filter_size):
    """
    Function that construct a Gaussian pyramid
    :param im: a grayscale image with double values in [0, 1]
    :param max_levels: the maximal number of levels in the resulting pyramid.
    :param filter_size: – the size of the Gaussian filter (an odd scalar that represents a squared filter)
                          to be used in constructing the pyramid filter
    :return: output the resulting pyramid pyr as a standard python array (i.e. not
             numpy’s array) with maximum length of max_levels, where each element of the array
             is a grayscale image also output filter_vec which is 1D-row of size filter_size used for the
             pyramid construction
    """

    filter_vec = build_filter(filter_size)
    pyr = [im]

    for i in range(1, max_levels):
        # If resolution isn't up to LIMIT_RES then break
        if np.any(np.array(pyr[i-1].shape)/2 < LIMIT_RES):
            break

        filtered_im = filter_im(pyr[i-1], filter_vec)
        sampled_im = sample_im(filtered_im)
        pyr.append(sampled_im)

    return pyr, filter_vec

def expand_im(im):
    """
    Expand the image by factor 2
    :param im: the image to expand. a grayscale image with double values in [0, 1]
    :return: The expanded image
    """
    # Add zeores im odd index
    expanded_im = np.zeros(np.multiply(2, im.shape), dtype=np.float32)
    expanded_im[::2,::2] = im

    return expanded_im.astype(np.float32)

def build_laplacian_pyramid(im, max_levels, filter_size):
    """
    Function that construct a La[lacian pyramid
    :param im: a grayscale image with double values in [0, 1]
    :param max_levels: the maximal number of levels in the resulting pyramid.
    :param filter_size: – the size of the Gaussian filter (an odd scalar that represents a squared filter)
                          to be used in constructing the pyramid filter
    :return: output the resulting pyramid pyr as a standard python array (i.e. not
             numpy’s array) with maximum length of max_levels, where each element of the array
             is a grayscale image also output filter_vec which is 1D-row of size filter_size used for the
             pyramid construction
    """

    gaussian_pyr, filter_vec = build_gaussian_pyramid(im, max_levels, filter_size)
    len_gaus_pyr = len(gaussian_pyr)
    pyr = []
    for i in range(len_gaus_pyr-1):
        expanded_im = expand_im(gaussian_pyr[i+1])
        filtered_ex_im = filter_im(expanded_im, np.float32(2)*filter_vec)
        pyr.append(gaussian_pyr[i] - filtered_ex_im)

    # L_n = G_n by definition
    pyr.append(gaussian_pyr[len_gaus_pyr-1])

    return pyr, filter_vec

def laplacian_to_image(lpyr, filter_vec, coeff):
    """
    reconstruction of an image from its Laplacian Pyramid
    :param lpyr: Laplacian pyramid as defined above
    :param filter_vec: filter defined as above
    :param coeff: A vector. The vector size is the same as the number of levels in the pyramid lpyr
    :return: reconstructed laplacian pyr to image
    """
    image = lpyr[-1] * np.float32(coeff[-1])
    for i in range(len(lpyr)-1, 0, -1):
        image = filter_im(expand_im(image), np.float32(2) * filter_vec) + (lpyr[i-1] * np.float32(coeff[i-1]))
    return image.astype(np.float32)

def stretch_vals(im):
    """
    Stretching the values of im to [0,1]
    :param im: the image to stretch
    :return: new image streched to [0,1]
    """
    x_min, x_max = np.min(im), np.max(im)
    stretch_im = (im - x_min) / (x_max - x_min) if x_min != x_max else 1
    return stretch_im.astype(np.float32)

def render_pyramid(pyr, levels):
    """
    Create a single black image in which the pyramid levels of the given pyramid pyr
    :param pyr: pyr is either a Gaussian or Laplacian pyramid as defined above.
    :param levels: levels is the number of levels to present in the result ≤ max_levels.
    :return:  a single black image in which the pyramid levels of the given pyramid pyr
              are stacked horizontally (after stretching the values to [0, 1])
    """
    # Calculate the width of new image.
    if len(pyr) < levels:
        levels = len(pyr)
    shape_orig = pyr[0].shape
    res = np.zeros((shape_orig[0], int(shape_orig[1]*(2-(1/2)**(levels-1)))))
    cols = 0
    for i in range(levels):
        rows_im, cols_im = pyr[i].shape
        res[:rows_im,cols:cols+cols_im] = stretch_vals(pyr[i])
        cols += cols_im

    return res.astype(np.float32)

def display_pyramid(pyr, levels):
    """
    Display of pyramids
    :param pyr: pyr is either a Gaussian or Laplacian pyramid as defined above.
    :param levels: levels is the number of levels to present in the result ≤ max_levels.
    :return: None
    """
    im = render_pyramid(pyr, levels)
    plt.figure()
    plt.imshow(im, cmap=plt.cm.gray)
    plt.axis('off')
    plt.show()


def pyramid_blending(im1, im2, mask, max_levels, filter_size_im, filter_size_mask):
    """
    Implement pyramid blending as described in the lecture.
    :param im1: grayscale image to be blended.
    :param im2: grayscale image to be blended.
    :param mask: a boolean (i.e. dtype == np.bool) mask containing True and False representing which parts
                 of im1 and im2 should appear in the resulting im_blend.
    :param max_levels: the max_levels parameter you should use when generating the Gaussian and Laplacian
                       pyramids.
    :param filter_size_im: the size of the Gaussian filter (an odd scalar that represents a squared filter) which
                           defining the filter used in the construction of the Laplacian pyramids of im1 and im2.
    :param filter_size_mask: the size of the Gaussian filter(an odd scalar that represents a squared filter) which
                             defining the filter used in the construction of the Gaussian pyramid of mask.
    :return:  Reconstruct the resulting blended image from the Laplacian pyramid.
    """

    L_1, filter_vec = build_laplacian_pyramid(im1, max_levels, filter_size_im)
    L_2 = build_laplacian_pyramid(im2, max_levels, filter_size_im)[0]

    G_m = build_gaussian_pyramid(mask.astype(np.float32), max_levels, filter_size_mask)[0]

    L_out = []

    size_pyr = len(L_1)
    for k in range(size_pyr):
        L_out.append(G_m[k]*L_1[k] + (1-G_m[k])*L_2[k])

    blended_im = laplacian_to_image(L_out, filter_vec, np.ones(size_pyr))
    return blended_im.clip(min=0, max=1).astype(np.float32)

def return_rgb(im):
    """
    Return the rgb representation
    :param im: color image
    :return: r,g,b values
    """
    return im[:,:,0], im[:,:,1], im[:,:,2]


def display_images(im1, im2, mask, im_blend):
    """
    Display the given images
    :return: None
    """
    images = [im1, im2, mask, im_blend]
    n = len(images)
    fig = plt.figure()
    for i in range(n):
        a = fig.add_subplot(int(n/2), int(n/2), i+1)
        if i == n-2:
            plt.imshow(images[i].astype(np.float32), cmap=plt.cm.gray)
        else:
            plt.imshow(images[i])

        a.axis('off')
    plt.show()


def blending_example(im1, im2, mask):
    """
    performing pyramid blending on two sets of image pairs and mask
    :param im1: image to be blended.
    :param im2: image to be blended.
    :param mask: path to a binary mask containing True and False representing which parts
                 of im1 and im2 should appear in the resulting im_blend.
    :return: the resulting blended image (im_blend).
    """
    r1, g1, b1 = return_rgb(im1)
    r2, g2, b2 = return_rgb(im2)

    blen_r, blen_g, blen_b = pyramid_blending(r1, r2, mask, MAX_LEVELS, SIZE_FILTER_IM, SIZE_FILTER_MASK),\
                             pyramid_blending(g1, g2, mask, MAX_LEVELS, SIZE_FILTER_IM, SIZE_FILTER_MASK),\
                             pyramid_blending(b1, b2, mask, MAX_LEVELS, SIZE_FILTER_IM, SIZE_FILTER_MASK)

    im_blend = np.zeros(im1.shape)
    im_blend[:,:,0], im_blend[:,:,1], im_blend[:,:,2] = blen_r, blen_g, blen_b

    display_images(im1, im2, mask, im_blend)

    return im_blend.astype(np.float32)



def blending_example1():
    """
    Example for blending two images
    :return: resulting blended image (im_blend).
    """
    im1, im2 = read_image(relpath('snownew.jpg'), RGB_REP), read_image(relpath('fishesnew.jpg'), RGB_REP)

    mask = read_image(relpath('maskSnow.jpg'), GRAY_REP).astype(np.int).astype(np.bool)

    return im1.astype(np.float32), im2.astype(np.float32), mask, blending_example(im1, im2, mask)

def blending_example2():
    """
    Example for blending two images
    :return: resulting blended image (im_blend).
    """
    im1, im2 = read_image(relpath('tvnew.jpg'), RGB_REP), read_image(relpath('yoniNoam.jpg'), RGB_REP)

    mask = read_image(relpath('tvMask.jpg'), GRAY_REP).astype(np.int).astype(np.bool)

    return im1.astype(np.float32), im2.astype(np.float32), mask, blending_example(im1, im2, mask)


def relpath(filename):
    """
    Convert from relative to abs path
    :param filename: relative path
    :return: the abs path
    """
    return os.path.join(os.path.dirname(__file__), filename)

