import numpy as np
from scipy.misc import imread as imread
from skimage.color import rgb2gray
import matplotlib.pyplot as plt

GRAY_REP = 1
RGB_REP = 2

L_INTESITY = 255
MIN_INTENS = np.float32(0.0)
MAX_INTENS = np.float32(1.0)

MATRIX_2_YIQ = np.array([[0.299, 0.587, 0.114],
                        [0.596, -0.275, -0.321],
                        [0.212, -0.523, 0.311]]).astype(np.float32)

MATRIX_2_RGB = np.linalg.inv(MATRIX_2_YIQ).astype(np.float32)

SIZE_SHAPE_GRAYSCALE = 2

'''
Convert image to float32 values between [0,1]
'''
def im_to_float(image):

    return image.astype(np.float32) / L_INTESITY

'''
Convert image to uint8
'''
def im_to_int(image):

    return np.around(image * [L_INTESITY]).astype(np.int)

'''
The function that reads a given image file and converts it into a given representation.
@:param - filename - string containing the image filename to read.
@:param - representation - representation code, either 1 or 2
defining if the output should be either a grayscale OR RGB image respectively
@:return - The new image.
'''
def read_image(filename, representation):
    try:
        im = imread(filename)

        if representation == GRAY_REP:
            return rgb2gray(im).astype(np.float32)

        return im_to_float(im)

    except:
        print("Cant read the image")
        exit(-1)

'''
The function should open a new figure and display the loaded image in the converted representation
@:param - image - the image.
@:param - representation - representation code, either 1 or 2
defining if the output should be either a grayscale OR RGB image respectively
'''
def image_to_dispaly(image, representation):

    plt.figure()

    cmap = None
    if representation == GRAY_REP:
        cmap = plt.cm.gray

    plt.imshow(image, cmap=cmap)
    plt.axis('off')
    plt.show()

'''
The function should open a new figure and display the loaded image in the converted representation
@:param - filename - string containing the image filename to read.
@:param - representation - representation code, either 1 or 2
defining if the output should be either a grayscale OR RGB image respectively
'''
def imdispaly(filename, representation):

    image = read_image(filename, representation)
    image_to_dispaly(image, representation)

'''
The function s transform an RGB image into the YIQ color space
@:param - imRGB - height×width×3 np.float32 matrices with values in [0, 1].
@:return - height×width×3 np.float32 matrices with YIQ values.
'''
def rgb2yiq(imRGB):
    try:
        return np.dot(imRGB, np.transpose(MATRIX_2_YIQ))

    except:
        print("bad matrix size")
        exit(-1)
'''
The function s transform an YIQ image into the RGB color space
@:param - imYIQ - height×width×3 np.float32 matrices with values in [0, 1].
@:return - height×width×3 np.float32 matrices with RGB values.
'''
def yiq2rgb(imYIQ):
    try:
        return np.dot(imYIQ, np.transpose(MATRIX_2_RGB))
    except:
        print("bad matrix size")
        exit(-1)

'''
The function s transform an YIQ image (if necassery) and return the Y value
@:param - image - is the input grayscale or RGB int32.
@:return - image_tmp -  The YIQ image if in RGB, None otherwise
@:return - y_value - The Y component if RGB, or the image otherwise.
'''
def get_Y_value(image, shape_im):

    image_tmp = None
    if len(shape_im) > SIZE_SHAPE_GRAYSCALE:
        image_tmp = rgb2yiq(image)
        y_value = image_tmp[:,:,0]

    else:
        y_value = image

    return image_tmp, y_value

'''
The function s transform an RGB image (if necassery) and return the new image with values in [0, 1].
@:param - image -  is the input grayscale or None value if the not.
@:param - new_Y_value -  The Y Component if in RGB, grayscale image otherwise
@:return - new_im - The RGB or grayscale image union with the new Y component, in float32  with values in [0, 1].
'''
def get_RGB_values(YIQ_im, new_Y_value):
    new_im = im_to_float(new_Y_value)

    if YIQ_im is not None:
        YIQ_im[:,:,0] = new_im
        new_im = yiq2rgb(YIQ_im)

    return new_im


'''
The function s transform an YIQ image into the RGB color space
@:param - im_orig - is the input grayscale or RGB float32 image with values in [0, 1].
@:return - im_eq - is the equalized image. grayscale or RGB float32 image with values in [0, 1].
@:return - hist_orig - is a 256 bin histogram of the original image (array with shape (256,).
@:return - hist_eq - is a 256 bin histogram of the equalized image (array with shape (256,)
'''
def histogram_equalize(im_orig):
    shape_im = im_orig.shape
    size_image = shape_im[0] * shape_im[1]

    # Get the Y component
    im_orig_tmp, im_orig = get_Y_value(im_orig, shape_im)

    im_orig = im_to_int(im_orig)

    # Original histogram
    hist_orig = np.histogram(im_orig, L_INTESITY + 1, [0, L_INTESITY])[0]

    # Cumulative sum
    cum_sum = np.cumsum(hist_orig)

    # The first value isn't zero in cum_sum
    s_m = cum_sum[tuple(np.transpose(cum_sum.nonzero())[0])]

    LUT = np.zeros(L_INTESITY)
    try:
        # The look up table.
        LUT = np.around(L_INTESITY * (cum_sum - s_m) / (size_image - s_m))
    except:
        print("bad image values - dividing zero")
        exit(-1)

    # Change the image regard to the LUT
    im_eq = LUT[im_orig]

    hist_eq = np.histogram(im_eq, L_INTESITY + 1, [0, L_INTESITY])[0]

    # change to float rgb image if need so.
    im_eq = get_RGB_values(im_orig_tmp, im_eq)

    return im_eq.clip(MIN_INTENS, MAX_INTENS), hist_orig, hist_eq

'''
Initialize the z values for the first iteration
@:param quant - the number of ranges = n_quant
@:param hist_orig - the  histogram of the image
@:param size_im - the size of the image
@:return q - the q values
'''
def init_z(quant, size_im, hist_orig):

    z = np.zeros(quant + 1).astype(np.int)
    z[0], z[quant] = 0, L_INTESITY
    # Cumulative sum
    cum_sum = np.cumsum(hist_orig)

    # size of each segment
    size_seg = np.int(size_im / quant)

    # As we told, we can use for on quant = n_quant
    for i in range(1, quant):
        z[i] = np.where(cum_sum <= i * size_seg)[0][-1]

    return z

'''
Set the q values given z values
@:param z - the z ranges
@:param hist - the  histogram of the table
@:param quant - the n_quant
@:return q - the q values
'''
def cal_q(z, hist, quant):

    q = np.zeros(quant)

    # As we told, we can use for on quant = n_quant
    for i in range(0, quant):
        # Just for taking the first bin.
        values = np.arange(z[i], z[i+1]+1)
        hist_seg = hist[z[i]:z[i+1]+1]
        q[i] = np.dot(hist_seg, np.transpose(values)) / np.sum(hist_seg)

    # return q
    return np.around(q).astype(np.int)
'''
Set the z values given q values
@:param q - the q values
@:return z - the z values
'''
def cal_z(q, z):
    z[1:-1] = np.around((q[0:-1] + q[1:]) / 2)
    return z.astype(np.int)


'''
Set the error of the quantization given current iteration
@:param q - the q values
@:param z - the z ranges
@:param hist - the  histogram of the table
@:param quant - the n_quant
@:return error - the error of iteration in the quantization
'''
def cal_error(q, z, quant, hist):

    error = 0
    # As we told, we can use for on quant = n_quant
    for i in range(0, quant):
        values = np.arange(z[i], z[i+1]+1)
        hist_seg = hist[z[i]:z[i+1]+1]
        error += np.dot(np.square(q[i] - values), hist_seg)

    return error

'''
Set the LUT given q and z
@:param q - the q values
@:param z - the z ranges
@:quant - the n_quant
@:return LUT - the map table
'''
def set_LUT(q, z, quant):

    LUT = np.zeros(L_INTESITY + 1)

    # As we told, we can use for on quant = n_quant
    for i in range(quant):
        LUT[z[i]:z[i+1]] = q[i]

    LUT[L_INTESITY] = q[quant - 1]
    return LUT

'''
The a function that performs optimal quantization of a given grayscale or RGB image.
@:param - im_orig - is the input grayscale or RGB float32 image with values in [0, 1].
@:param - n_quant - is the number of intensities your output im_quant image should have.
@:param - n_iter - is the maximum number of     iterations of the optimization procedure (may converge earlier.)
@:return - im_quant - is the quantize output image.
@:return - error - is an array with shape (n_iter,) (or less) of the total intensities error for each iteration in the
                   quantization procedure.

'''
def quantize(im_orig, n_quant, n_iter):
    if n_quant == 0:
        print("bad n_quant size")
        exit(-1)

    shape_im = im_orig.shape
    size_image = shape_im[0] * shape_im[1]

    # Get the Y component
    im_orig_tmp, im_orig = get_Y_value(im_orig, shape_im)
    im_orig = im_to_int(im_orig)

    # Original histogram
    histogram = np.histogram(im_orig, L_INTESITY + 1, [0, L_INTESITY])[0]

    # Initial values
    z, q, error = init_z(n_quant, size_image, histogram), np.zeros(n_quant), np.zeros(n_iter)

    for iter in range(0, n_iter):
        z_tmp = z.copy()

        # Calculate the new values
        q = cal_q(z, histogram, n_quant)
        z = cal_z(q, z)
        error[iter] = cal_error(q, z, n_quant, histogram)

        # Check if there was a converge
        if np.all(z == z_tmp):
            error = np.resize(error, (iter,))
            break

    # Create new image given the LUT
    LUT = set_LUT(q, z, n_quant)
    im_quant = LUT[im_orig]

    # change to float rgb image if need so.
    im_quant = get_RGB_values(im_orig_tmp, im_quant)
    return im_quant, error