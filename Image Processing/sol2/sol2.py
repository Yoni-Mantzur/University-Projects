import numpy as np
from scipy import signal
from scipy.misc import imread as imread
from skimage.color import rgb2gray
import matplotlib.pyplot as plt


GRAY_REP = 1
L_INTESITY = np.float32(255)

D_X_CONV = np.array([1, 0, -1]).reshape(1,3).astype(np.float32)
D_Y_CONV = D_X_CONV.T

I, PI = np.complex128(0+1j), np.pi

BASICE_GAUSSIAN = np.array([1,1,1,1]).reshape(2,2)


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

def dft_mat(N):
    """
    :param N: Dimension of dft
    :return: the dft matrix
    """
    range = np.arange(N).astype(np.complex128)
    exp = np.exp((-2*PI*I*range)/N).astype(np.complex128)
    return np.vander(exp, increasing=True).astype(np.complex128)

def DFT(signal):
    """
    Function that transform a 1D discrete signal to its Fourier representation
    :param signal - an array of dtype float32 with shape (N,1)
    :return fourier_signal - an array of dtype complex128 with the same shape
    """

    N = signal.shape[0]
    fourier_signal = np.dot(dft_mat(N), signal)
    return fourier_signal.astype(np.complex128)

def IDFT(fourier_signal):
    """
    Function that transform a 1D discrete Fourier to its signal representation
    :param signal - an array of dtype complex128 with shape (N,1)
    :return fourier_signal - an array of dtype complex128 with the same shape
    """

    N = fourier_signal.shape[0]

    # Notice that inverse furier is the conj of the furier
    signal = np.dot(np.conj(dft_mat(N)), fourier_signal) / N
    return signal.astype(np.complex128)



def func2D(narray, func):
    """
    Operates func on rows and then on columns
    :param narray: 2D array N * M
    :param func: Unary function to operate on 1D arr
    :return: 2D array after operates func
    """
    N, M = narray.shape
    newArray = narray.copy().astype(np.complex128)

    # transform of rows
    j=0
    for row in narray:
        newArray[j,:] = func(row.reshape(M,1)).reshape(M)
        j+=1

    k = 0
    for column in newArray.T:
        newArray[:,k] = func(column.reshape(N,1)).reshape(N)
        k+=1

    return newArray


def DFT2(image):
    """
    Function that convert a 2D discrete signal to its Fourier representation
    :param image: 2D signal
    :return fourier_signal - an array of dtype complex128 with the same shape
    """
    return func2D(image, DFT)

def IDFT2(image):
    """
    Function that convert a 2D discrete signal to its inverse Fourier representation
    :param image: 2D signal
    :return fourier_signal - an array of dtype complex128 with the same shape
    """
    return func2D(image, IDFT)

def conv_im(im, conv_vector):
    """
    Convolution with image.
    :param im: some image
    :param conv_vector: conv vector
    :return: the convolution
    """
    return signal.convolve2d(im, conv_vector, mode='same')


def conv_der(im):
    """
    A function that computes the magnitude of image derivatives
    :param im: a grayscale images of type float32.
    :return: a grayscale images of type float32.
    """

    dx = conv_im(im, D_X_CONV)
    dy = conv_im(im, D_Y_CONV)

    mag = np.sqrt(np.abs(dx)**2 + np.abs(dy)**2)
    return mag

def fourier_der(im):
    """
    A function that computes the magnitude of image derivatives using Fourier transform.
    :param im: are float32 grayscale images
    :return: are float32 grayscale images
    """
    furier_im = DFT2(im)
    furier_im_shift = np.fft.fftshift(furier_im)

    N, M = im.shape
    range_y = np.arange(-N/2,N/2)
    range_x = np.arange(-M/2,M/2)

    dx = (2*I*PI/N)*(IDFT2(np.multiply(furier_im_shift,range_x)))
    dy = (2*I*PI/N)*(IDFT2(np.multiply(furier_im_shift.T,range_y).T))

    mag = np.sqrt(np.abs(dx)**2 + np.abs(dy)**2)
    return mag.astype(np.float32)


def creat_kernel(kernel_size):
    """
    Generates Gaussian kernel.
    :param kernel_size: the size of the gaussian kernel in each dimension (an odd integer).
    :return: 2D kernel (as float32 type)
    """
    if kernel_size <= 1:
        return np.array([1])

    kernel = BASICE_GAUSSIAN.astype(np.float32)
    for i in range(kernel_size-2):
        kernel = signal.convolve2d(kernel, BASICE_GAUSSIAN)

    norm_kernel = kernel / np.sum(kernel)
    return norm_kernel.astype(np.float32)


def blur_spatial (im, kernel_size):
    """
    Function that performs image blurring using 2D convolution between the image f and a gaussian
    kernel g.
    :param im: image to be blurred (grayscale float32 image).
    :param kernel_size: the size of the gaussian kernel in each dimension (an odd integer).
    :return: blurry image (grayscale float32 image).
    """
    return signal.convolve2d(im, creat_kernel(kernel_size), mode='same', boundary='wrap')

def pad_kernel(kernel, kernel_size, im_shape):
    """
    Padding the kernel to image size with zeroes
    :param kernel: the kenel to pad
    :param kernel_size: the size of the kernel before padding
    :param im_shape: the shape of the image
    :return: the padding kernel
    """
    size_x_im, size_y_im = im_shape

    padding = ((0, np.abs(size_x_im-kernel_size)), (0, np.abs(size_y_im-kernel_size)))
    KERNEL_pading = np.lib.pad(kernel, padding, 'constant', constant_values=np.complex128(0))

	# Move the kernel to center
    KERNEL_pading = np.roll(KERNEL_pading, int((size_x_im-kernel_size)/2 + 1), axis=0)
    KERNEL_pading = np.roll(KERNEL_pading, int((size_y_im-kernel_size)/2 + 1), axis=1)

    return KERNEL_pading

def blur_fourier(im, kernel_size):
    """
    Function that performs image blurring with gaussian kernel in Fourier space.
    :param im: image to be blurred (grayscale float32 image).
    :param kernel_size: is the size of the gaussian in each dimension (an odd integer).
    :return: is the output blurry image (grayscale float32 image).
    """
    kernel = creat_kernel(kernel_size).astype(np.complex128)
    
    KERNEL_pading = pad_kernel(kernel, kernel_size, im.shape)
    KERNEL_ishifted = np.fft.ifftshift(KERNEL_pading)

	# Use the convolution theorem
    KERNEL, IM = DFT2(KERNEL_ishifted), DFT2(im)
    
    mult_ker_im = np.multiply(IM, KERNEL)
    
    
    return np.real(IDFT2(mult_ker_im)).astype(np.float32)
