from sol5_utils import *
import numpy as np
from scipy.misc import imread as imread
from skimage.color import rgb2gray
from  scipy.ndimage.filters import convolve
from keras.models import Model
from keras.layers import Input, Convolution2D, Activation, merge
from keras.optimizers import Adam

GRAY_REP = 1
RGB_REP = 2

SUB_VALUE = .5
GRAY_CHANNEL = 1
CONV_SIZE = (3, 3)
TRAIN_DATA_SIZE = .8

MIN_INTENS = np.float32(0.0)
MAX_INTENS = np.float32(1.0)

NUMBER_RES_BLOCKS = 5

L_INTESITY = np.float32(255)


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


# ===================== Load data sets =============================


def load_dataset(filenames, batch_size, corruption_func, crop_size):
    """

    :param filenames: A list of filenames of clean images.
    :param batch_size: The size of the batch of images for each iteration of Stochastic Gradient Descent.
    :param corruption_func: A function receiving a numpy’s array representation of an image as a single argument,
                            and returns a randomly corrupted version of the input image.
    :param crop_size: A tuple (height, width) specifying the crop size of the patches to extract.
    :return:  Python’s generator object which outputs random tuples of the form
              (source_batch, target_batch)
    """
    height_patch, width_patch = crop_size
    source_batch, target_batch = [np.empty((batch_size, GRAY_CHANNEL, height_patch, width_patch), dtype=np.float32)]*2

    def extract_random_patch(im, corrupted_im, im_shape):
        row, col = np.random.randint(0, im_shape[0] - height_patch), \
                   np.random.randint(0, im_shape[1] - width_patch)

        def extract_im(image):
            return np.copy(image[row:row+height_patch, col:col+width_patch] - [SUB_VALUE])
        return extract_im(corrupted_im), extract_im(im)

    def gen_dataset():

        images_cache = {}
        while True:
            for i in range(batch_size):
                picked_im_path = random.choice(filenames)
                picked_im = images_cache.setdefault(picked_im_path, read_image(picked_im_path, GRAY_REP))
                corrupted_im = corruption_func(picked_im)
                shape_im = picked_im.shape
                source_batch[i,0], target_batch[i,0] = extract_random_patch(corrupted_im, picked_im, shape_im)

            yield source_batch, target_batch

    return gen_dataset()


# ===================== Build the model =============================

def convolution_layer(input_ten, num_channels):
    return Convolution2D(num_channels, CONV_SIZE[0], CONV_SIZE[1], border_mode='same')(input_ten)


def resblock(input_tensor, num_channels):
    """
    function takes as input a symbolic input tensor and the number of channels for each of its
    convolutional layers, and returns the symbolic output tensor of the layer configuration
    :param input_tensor: a symbolic input tensor
    :param num_channels: number of channels for each of its convolutional layers
    :return: returns the symbolic output tensor of the layer configuration
    """

    output_tensor = convolution_layer(input_tensor, num_channels)
    output_tensor = Activation('relu')(output_tensor)
    output_tensor = convolution_layer(output_tensor, num_channels)
    output_tensor = merge([input_tensor, output_tensor], mode='sum')
    return output_tensor


def build_nn_model(height, width, num_channels):
    """

    :param height: height,
    :param width: width
    :param num_channels: number of output channels except the very last convolutional layer
                         which should have a single output channel.
    :return: untrained Keras model
    """
    input_tensor = Input(shape=(GRAY_CHANNEL, height, width))
    middle_tensor = convolution_layer(input_tensor, num_channels)
    middle_tensor = Activation('relu')(middle_tensor)

    in_block_tensor, out_block_tensor = [middle_tensor]*2
    for i in range(NUMBER_RES_BLOCKS):
        out_block_tensor = resblock(in_block_tensor, num_channels)
        in_block_tensor = out_block_tensor

    output_tensor = merge([middle_tensor, out_block_tensor], mode='sum')
    output_tensor = convolution_layer(output_tensor, GRAY_CHANNEL)

    return Model(input=input_tensor, output=output_tensor)

# ===================== Training the model =============================

def train_model(model, images, corruption_func, batch_size, samples_per_epoch, num_epochs, num_valid_samples):
    """

    :param model: a general neural network model for image restoration.
    :param images: a list of file paths pointing to image files. You should assume these paths are complete, and
                   should append anything to them.
    :param corruption_func:
    :param batch_size: the size of the batch of examples for each iteration of SGD.
    :param samples_per_epoch: The number of samples in each epoch (actual samples, not batches!).
    :param num_epochs: The number of epochs for which the optimization will run.
    :param num_valid_samples: The number of samples in the validation set to test on after every epoch.
    :return:
    """
    N = np.int(len(images)*0.8)
    train_date, validation_data = images[:N], images[N:]

    crop_size = model.input_shape[2:]

    def call_load_dataset(data):
        return load_dataset(data, batch_size, corruption_func, crop_size)

    train_gen, valid_gen = call_load_dataset(train_date), call_load_dataset(validation_data)

    model.compile(loss='mean_squared_error', optimizer=Adam(beta_2=0.9))

    model.fit_generator(train_gen, samples_per_epoch=samples_per_epoch, nb_epoch=num_epochs,
                        validation_data=valid_gen, nb_val_samples=num_valid_samples)

# ===================== Image restoration =============================

def restore_image(corrupted_image, base_model, num_channels):
    """

    :param corrupted_image: a grayscale image of shape (height, width) and with values in the [0, 1] range of
                            type float32 that is affected by a corruption generated
                            from the same corruption function encountered during training
    :param base_model: a neural network trained to restore small patches  The input and output of the network are
                       images with values in the [−0.5, 0.5] range
    :param num_channels: the number of channels used in the base model. Use it to construct the larger model.
    :return:
    """

    height, width = corrupted_image.shape
    new_model = build_nn_model(height, width, num_channels)

    new_model.set_weights(base_model.get_weights())

    corrupted_image = corrupted_image.reshape((GRAY_CHANNEL, height, width))
    restored_image = new_model.predict(corrupted_image[np.newaxis,...] - [SUB_VALUE])[0] + [SUB_VALUE]

    return np.clip(restored_image, a_min=MIN_INTENS, a_max=MAX_INTENS).reshape(height, width).astype(np.float32)

# ===================== Application restoration =============================


# ============= Image denoising ================

def add_gaussian_noise(image, min_sigma, max_sigma):
    """

    :param image: a grayscale image with values in the [0, 1] range of type float32.
    :param min_sigma: a non-negative scalar value representing the minimal variance of the gaussian distribution.
    :param max_sigma: a non-negative scalar value larger than or equal to min_sigma, representing the maximal
                      variance of the gaussian distribution
    :return:
    """

    sigma = float(np.random.uniform(low=min_sigma, high=max_sigma))
    random_variable = np.random.normal(scale=sigma, size=image.shape)

    return np.clip(image + random_variable, a_min=MIN_INTENS, a_max=MAX_INTENS).astype(np.float32)


def get_configurations(quick_mode, isBlur):

    if isBlur:
        num_epochs = 10
    else:
        num_epochs = 5

    if quick_mode:
        batch_size, samples_per_epoch, num_epochs, samples_for_val = 10, 30, 2, 30
    else:
        batch_size, samples_per_epoch, num_epochs, samples_for_val = 100, 10000, num_epochs, 1000

    return batch_size, samples_per_epoch, num_epochs, samples_for_val


def learn_denoising_model(quick_mode=False):
    """
    should train a network which expect patches of size 24×24, using 48 channels for all but the last layer.
    :param quick_mode: If quick_mode equals True, instead of the above
                       arguments, use only 10 images in a batch, 30 samples per epoch, just 2 epochs and only 30
                       samples for the validation set. else, use 100 images in a batch, 10000 samples per epoch,
                       5 epochs overall and 1000 samples for testing on the validation set.
    :return: model, number_channels
    """

    crop_size, number_channels = (24,24), 48

    batch_size, samples_per_epoch, num_epochs, samples_for_val = get_configurations(quick_mode, isBlur=False)
    images = images_for_denoising()
    model = build_nn_model(crop_size[0], crop_size[1], number_channels)

    train_model(model, images, lambda im: add_gaussian_noise(im, 0.0, 0.2), batch_size, samples_per_epoch,
                num_epochs, samples_for_val)

    return model, number_channels


# ============= Image deblurring ================

def add_motion_blur(image, kernel_size, angle):
    """
    simulate motion blur on the given image
    :param image: a grayscale image with values in the [0, 1] range of type float32.
    :param kernel_size: square kernel of size
    :param angle: an angle in radians in the range [0, π).
    :return: blurred image
    """
    blur_kernel = motion_blur_kernel(kernel_size, angle)
    motion_blur_image = convolve(image, blur_kernel).astype(np.float32)

    return motion_blur_image


def random_motion_blur(image, list_of_kernel_sizes):
    """
    :param image: a grayscale image with values in the [0, 1] range of type float32.
    :param list_of_kernel_sizes: a list of odd integers.
    :return:
    """
    angle, kernel_size = np.random.uniform(0, np.pi), random.choice(list_of_kernel_sizes)

    return add_motion_blur(image, kernel_size, angle)


def  learn_deblurring_model(quick_mode=False):
    """
    should train a network which expect patches of size 16×16, and have 32 channels in all layers except the last.
    :param quick_mode: If quick_mode equals True, instead of the above arguments, use only 10 images in a batch,
                       30 samples per epoch, just 2 epochs and only 30 samples for the validation set.
                       else.  100 images in a batch, 10000 samples per epoch, 10 epochs overall and 1000
                       samples for testing on the validation set.
    :return: model, number_channels
    """
    crop_size, number_channels = (16,16), 32

    batch_size, samples_per_epoch, num_epochs, samples_for_val = get_configurations(quick_mode, isBlur=True)

    images = images_for_deblurring()

    model = build_nn_model(crop_size[0], crop_size[1], number_channels)

    train_model(model, images, lambda im: random_motion_blur(im, [7]), batch_size, samples_per_epoch,
                num_epochs, samples_for_val)

    return model, number_channels
