
from sol4_utils import *
from sol4_add import *

from scipy.ndimage.interpolation import map_coordinates

D_X_CONV = np.array([1, 0, -1]).reshape((1,3)).astype(np.float32)
D_Y_CONV = D_X_CONV.T

KERNEL_SIZE = 3
K = np.float32(0.04)
DESC_RADIUS = 3
COLS_AXIS = 0
ROWS_AXIS = 1
CORNER_POINT = 1

NUMBER_SAMPLES = 4

def der_im(im, conv_vec):
    """
    Return the der of an image
    """
    return ndimage.filters.convolve(im, conv_vec, mode='constant').astype(np.float32)

def defineM(IxIx, IyIy, IxIy):
    """
    Define M given the relevant images
    """
    shape = IxIx.shape
    M = np.empty(shape+(2, 2), dtype=np.float32)
    M[:,:,0,0], M[:,:,0,1], M[:,:,1,0], M[:,:,1,1] = IxIx, IxIy, IxIy, IyIy
    return M.astype(np.float32)

def trace(M):
    """
    Return trace of M
    """
    return np.trace(M, axis1=2, axis2=3, dtype=np.float32)

def harris_corner_detector(im):
    """
    Detects corners in im
    :param im: grayscale image to find key points inside.
    :return: An array with shape (N,2) of [x,y] key points locations in im.
    """

    Ix, Iy = der_im(im, D_X_CONV), der_im(im, D_Y_CONV)
    IxIx, IyIy, IxIy = np.multiply(Ix, Ix),  np.multiply(Iy, Iy),  np.multiply(Ix, Iy)

    blur_IxIx, blur_IyIy, blur_IxIy = blur_spatial(IxIx, KERNEL_SIZE), \
                                      blur_spatial(IyIy, KERNEL_SIZE), \
                                      blur_spatial(IxIy, KERNEL_SIZE)

    M = defineM(blur_IxIx, blur_IyIy, blur_IxIy)

    # Rais warnings
    np.seterr(invalid='ignore')
    R = np.linalg.det(M) - K * trace(M)**2

    lcl_max_R = non_maximum_suppression(R)

    corners = np.transpose(np.where(lcl_max_R == CORNER_POINT))

    cornersT = np.empty(corners.shape)
    cornersT[:,0], cornersT[:,1] = corners[:,1], corners[:,0]

    return cornersT

def bring_neighbors(im, pos, size, hood_size):
    """
    Return the neighbors of pos in im - in (pos-size, pos+size)
    """

    nx, ny = hood_size
    y = np.linspace(pos[0] - size, pos[0] + size, nx)
    x = np.linspace(pos[1] - size, pos[1] + size, ny)
    xv, yv = np.meshgrid(x, y)

    xv, yv = xv.reshape((hood_size[0]*hood_size[1],)), \
             yv.reshape((hood_size[0]*hood_size[1],))

    return map_coordinates(im,[xv, yv], order=1, prefilter=False, output=np.float32).reshape(hood_size).T

def sample_descriptor(im, pos, desc_rad):
    """
    Creates descriptors from given feature detections
    :param im: grayscale image to sample within.
    :param pos: An array with shape (N,2) of [x,y] positions to sample descriptors in im.
    :param desc_rad: ”Radius” of descriptors to compute
    :return: A 3D array with shape (K,K,N) containing the ith descriptor at desc(:,:,i). The per−descriptor dimensions
             KxK are related to the desc rad argument as follows K = 1+2∗desc rad.
    """
    N = pos.shape[0]
    hood_size = (1+2*desc_rad, 1+2*desc_rad)
    desc = np.empty(hood_size + (N,), dtype=np.float32)

    for i in range(N):
        neighbors = bring_neighbors(im, pos[i], desc_rad, hood_size)
        mean_neighbors = neighbors - np.mean(neighbors, dtype=np.float32)
        norm_neighbors = np.linalg.norm(mean_neighbors)
        if norm_neighbors == .0:
            desc[:, :, i] = .0
            continue

        desc[:, :, i] = mean_neighbors / norm_neighbors

    return desc

def convert_corners(des_level, origin_level, origin_corners):
    """

    :param des_level:
    :param origin_corners:
    :return:
    """
    return np.multiply(2**(origin_level-des_level), origin_corners).astype(np.float32)

def find_features (pyr):
    """
    Return feature detection of pyr
    :param pyr: Gaussian pyramid of a grayscale image having 3 levels.
    :return: pos − An array with shape (N,2) of [x,y] feature location per row found in the (third pyramid level of the) image. These
             coordinates are provided at the pyramid level pyr[0].
            desc − A feature descriptor array with shape (K,K,N).

    """
    corners_level0 = spread_out_corners(pyr[0], 7, 7, 14)

    corners_level2 = convert_corners(2, 0, corners_level0)

    desc = sample_descriptor(pyr[2], corners_level2, DESC_RADIUS)

    return corners_level0, desc


def calc_score(desc1, desc2, K, N1, N2):
    """

    :param desc1:
    :param desc2:
    :param K:
    :param N1:
    :param N2:
    :return:
    """
    desc1Flat, desc2Flat = desc1.reshape(K*K, N1), desc2.reshape(K*K, N2)
    return np.dot(desc1Flat.T, desc2Flat).astype(np.float32)


def find_second_max(arr, N):
    """

    :param arr:
    :param axis:
    :return:

    """
    sec_max = np.empty((N,1))
    for i in range(N):
        sec_max[i] = np.max(np.delete(arr[i], np.argmax(arr[i])))
    return sec_max

def propeties_for_match(score, N1, N2, min_score):
    """

    :param score:
    :param N1:
    :param N2:
    :param min_score:
    :return:
    """
    second_max_frame1, second_max_frame2 = find_second_max(score, N1), find_second_max(score.T, N2)
    # Computes which indices answer the 3 properties.
    matches = np.transpose(np.where(np.logical_and(np.logical_and(score >= second_max_frame1.reshape(N1, 1),
                                                                  score >= second_max_frame2.reshape(1, N2)),
                                                                  score >= min_score)))
    return matches


def match_features(desc1, desc2, min_score):
    """

    :param desc1: A feature descriptor array with shape (K,K,N1).
    :param desc2: A feature descriptor array with shape (K,K,N2).
    :param min_score: Minimal match score between two descriptors required to be regarded as corresponding points.
    :return: match_ind1 − Array with shape (M,) and dtype int of matching indices in desc1.
             match_ind2 − Array with shape (M,) and dtype int of matching indices in desc2.
    """
    K, N1, N2 = desc1.shape[0], desc1.shape[2], desc2.shape[2]
    match_score = calc_score(desc1, desc2, K, N1, N2)
    matches = propeties_for_match(match_score, N1, N2, min_score)

    return matches[:,0].astype(np.int), matches[:,1].astype(np.int)

def apply_homography(pos1, H12):
    """
    applies a homography transformation on a set of points
    :param pos1: An array with shape (N,2) of [x,y] point coordinates.
    :param H12: A 3x3 homography matrix.
    :return: An array with the same shape as pos1 with [x,y] point coordinates in image i+1 obtained from transforming pos1
             using H12
    """

    homogens_points = np.append(pos1, np.ones((pos1.shape[0],1), dtype=pos1.dtype), axis=1)
    pos2Temp = np.dot(homogens_points, H12.T)
    z = pos2Temp[:,2]
    pos2 = np.empty(pos1.shape, dtype=np.float32)

    z[np.where(z==0.)] = 0.1* np.exp(-15)

    pos2[:,0], pos2[:,1] = pos2Temp[:,0] / z, pos2Temp[:,1] / z


    return pos2.astype(np.float32)

def ransac_homography(pos1, pos2, num_iters, inlier_tol):
    """
    RANSAC implementation
    :param pos1: shape (N,2) containing n rows of [x,y] coordinates of matched points.
    :param pos2: shape (N,2) containing n rows of [x,y] coordinates of matched points.
    :param num_iters: Number of RANSAC iterations to perform
    :param inlier_tol: inlier tolerance threshold.
    :return: H12 − A 3x3 normalized homography matrix.
             inliers − An Array with shape (S,) where S is the number of inliers, containing the indices
             in pos1/pos2 of the maximal set of inlier matches found.
    """

    N = pos1.shape[0]
    max_J_in = np.array([])
    for i in range(num_iters):
        random_4_points = np.random.permutation(N)[:NUMBER_SAMPLES]

        # STEP1: RANDOM POINTS
        P1J, P2J = pos1[random_4_points], pos2[random_4_points]

        # STEP2: CALCULATE H12
        H12 = least_squares_homography(P1J, P2J)
        if H12 is None:
            continue

        # STEP3: CALCULATE ERROR
        pos_HAT_2 = apply_homography(pos1,H12)
        E_J = (np.linalg.norm(pos_HAT_2 - pos2, axis=ROWS_AXIS)**2)

        inliners_matches = np.transpose(np.where(E_J < inlier_tol))
        if len(max_J_in) <= len(inliners_matches):
            max_J_in = inliners_matches.reshape(len(inliners_matches))
    H12 = least_squares_homography(pos1[max_J_in], pos2[max_J_in])

    return H12, max_J_in

def display_matches(im1, im2, pos1, pos2, inliers):
    """
    visualize the full set of point matches and the inlier matches detected by RANSAC
    :param im1: grayscale images
    :param im2: grayscale images
    :param pos1: arrays with shape (N,2) each, containing N rows of [x,y] coordinates of matched points
                 in im1
    :param pos2: arrays with shape (N,2) each, containing N rows of [x,y] coordinates of matched points
                 in im1
    :param inliers: An array with shape (S,) of inlier matches
    :return: None
    """
    plt.figure()
    plt.imshow(np.hstack((im1, im2)), cmap=plt.cm.gray)
    plt.axis('off')

    im1_shape = im1.shape
    pos1_inline, pos2_inline = pos1[inliers], pos2[inliers]

    pos_x_in, pos_y_in = [pos1_inline[:,0], pos2_inline[:,0]+im1_shape[1]], \
                         [pos1_inline[:,1], pos2_inline[:,1]]
    plt.plot(pos_x_in, pos_y_in, linestyle='-', mfc='red', color='yellow', lw=.4, ms=5, marker='o')
    pos1Temp, pos2Temp = pos1.copy(), pos2.copy()
    pos1Temp[inliers], pos2Temp[inliers] = False, False
    N = len(pos1) - len(inliers)
    pos1_outline, pos2_outline = pos1[np.where(pos1Temp != [False])].reshape(N,2),\
                                 pos2[np.where(pos2Temp != [False])].reshape(N,2)

    pos_x_out, pos_y_out = [pos1_outline[:,0], pos2_outline[:,0]+im1.shape[1]], \
                         [pos1_outline[:,1], pos2_outline[:,1]]
    plt.plot(pos_x_out, pos_y_out, linestyle='-', mfc='r', color='blue', lw=.4, ms=5, marker='o')

    plt.show()


def accumulate_homographies(H_successive, m):
    """

    :param H_successive: A list of M −1 3x3 homography matrices where H successive[i] is a homography that transforms points
           from coordinate system i to coordinate system i+1.
    :param m: Index of the coordinate system we would like to accumulate the given homographies towards
    :return: A list of M 3x3 homography matrices, where H2m[i] transforms points from coordinate system i to coordinate
             system m.
    """

    M = len(H_successive) + 1
    H2m = [np.empty((3,3), dtype=np.float32)]*M

    H2m[m] = np.eye(3)
    for i in range(m-1,-1,-1):
        H2m[i] = np.dot(H2m[i+1], H_successive[i])
        H2m[i] /= H2m[i][2,2]

    for j in range(m,M-1):
        H2m[j+1] = np.dot(H2m[j], np.linalg.inv(H_successive[j]))
        H2m[j+1] /= H2m[j+1][2, 2]

    return H2m



def get_im_corners(im):
    """

    :param im:
    :return:
    """
    y, x = im.shape
    return np.array([[0, 0], [x-1, 0], [0, y-1], [x-1, y-1]])

def get_im_center(im):
    """

    :param im:
    :return:
    """
    y, x = im.shape
    return np.array([x/2, y/2], dtype=np.int).reshape(1,2)



def blend_panorama(mask, panorama, num_lev):
    """

    :param panorama:
    :param strips:
    :return:
    """

    height, width = mask.shape
    closest_height = int((2 ** num_lev) * (np.floor(height / (2 ** num_lev))))
    closest_width = int((2 ** num_lev) * (np.floor(width / (2 ** num_lev))))
    cropped_pano = (panorama[0,:closest_height, :closest_width], panorama[1,:closest_height, :closest_width])
    cropped_mask = mask[:closest_height, :closest_width]

    return cropped_pano, cropped_mask

def backward_wraping(ims, Hs, Xmin, Xmax, Ymin, Ymax, corners_ims, strips):
    """

    :param ims:
    :param Hs:
    :param Xmin:
    :param Xmax:
    :param Ymin:
    :param Ymax:
    :param corners_ims:
    :param strips:
    :return: A backward_wraping image
    """
    num_ims = len(ims)
    panorama1 = np.zeros((Ymax-Ymin+1, Xmax-Xmin+1), dtype=np.float32)
    panorama2 = np.zeros((Ymax - Ymin + 1, Xmax - Xmin + 1), dtype=np.float32)
    mask = np.ones((Ymax - Ymin + 1, Xmax - Xmin + 1))
    add_r, add_l = 25, 0

    for i in range(num_ims):
        if i == num_ims -1:
            add_r = 0
        if i > 0:
            add_l = 25

        if i % 2 == 0:
            panorama = panorama1
            mask_im = np.ones(shape=ims[i].shape, dtype=np.float32)
        else:
            panorama = panorama2
            mask_im = np.zeros(shape=ims[i].shape, dtype=np.float32)

        grid_x = np.arange(strips[i, 0]-add_l, strips[i + 1, 0]+add_r)
        grid_y = np.arange(Ymin, Ymax)
        grid_i = np.transpose(np.meshgrid(grid_x,grid_y)).reshape((len(grid_x)*len(grid_y),2))

        grid_x_for_mask, grid_y_for_mask = np.arange(strips[i,0], strips[i+1,0]), np.arange(Ymin, Ymax)
        grid_i_for_mask = np.transpose(np.meshgrid(grid_x_for_mask,grid_y_for_mask)) \
            .reshape((len(grid_x_for_mask)*len(grid_y_for_mask),2))

        back_corrdinate = apply_homography(grid_i, np.linalg.inv(Hs[i]))
        back_corrdinate_for_mask = apply_homography(grid_i_for_mask, np.linalg.inv(Hs[i]))

        panorama[[grid_i[:,1]-Ymin, grid_i[:,0]-Xmin]] = map_coordinates(ims[i], [back_corrdinate[:,1], back_corrdinate[:,0]],
                                                                         order=1, prefilter=False, output=np.float32)
        mask[[grid_i_for_mask[:,1]-Ymin, grid_i_for_mask[:,0]-Xmin]] = map_coordinates(mask_im,
                                                                                       [back_corrdinate_for_mask[:,1], back_corrdinate_for_mask[:,0]],
                                                                                       order=1, prefilter=False,
                                                                                       output=np.float32)

    crop_pano, crop_mask = blend_panorama(mask, np.array([panorama1, panorama2]), 4)
    panorama_blended = pyramid_blending(crop_pano[0], crop_pano[1], crop_mask, 4, 7, 7)
    return panorama_blended


def render_panorama(ims, Hs):
    """

    :param ims: A list of grayscale images. (Python list)
    :param Hs: A list of 3x3 homography matrices. Hs[i] is a homography that transforms points from
               the coordinate system of ims[i] to the coordinate system of the panorama. (Python list)

    :return: A grayscale panorama image composed of vertical strips, backwarped using homographies from Hs, one from
             every image in ims
    """
    num_im = len(ims)
    corners_ims, centers_ims = np.empty((num_im,4, 2)), np.empty((num_im,2))

    for i in range(num_im):
        centers_ims[i] = apply_homography(get_im_center(ims[i]), Hs[i])
        corners_ims[i] = apply_homography(get_im_corners(ims[i]), Hs[i])

    Xmin, Xmax = np.min(corners_ims[:,:,0]), np.max(corners_ims[:,:,0])
    Ymin, Ymax = np.min(corners_ims[:,:,1]), np.max(corners_ims[:,:,1])

    strips = np.zeros((num_im+1,2))
    strips[0,0], strips[num_im,0] = Xmin, Xmax
    strips[1:num_im,0] = centers_ims[1:,0]/[2] + centers_ims[:num_im-1,0]/[2]


    return backward_wraping(ims, Hs, np.int(Xmin), np.int(Xmax), np.int(Ymin), np.int(Ymax),
                            corners_ims.astype(np.int), strips.astype(np.int))









