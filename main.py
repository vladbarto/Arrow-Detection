import cv2
import numpy as np


def print_img(img):
    """
    The method uses imshow to display the image and waitKey + destroyAllWindows to close the window.
    :param img: CV2 Image
    :return: nothing
    """
    cv2.imshow("image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def image_width_and_height(img):
    dimensions = img.shape
    height = dimensions[0]
    width = dimensions[1]

    return width, height


def binarisierung(g, threshold_value):
    """
    Binarisation of an image
    Image with gray values => Black-White image
    :param g: input image (in grayscale !!)
    :param threshold_value: for deciding if the pixel will become black or white
    :return: a binarised Black-White image
    """
    width, height = image_width_and_height(g)
    copy = g

    for i in range(height):
        for j in range(width):
            if g[i, j] <= threshold_value:
                copy[i, j] = 0
            else:
                copy[i, j] = 255

    return copy


def dilatation(g):
    width, height = image_width_and_height(g)
    copy = g.copy()

    for i in range(1, height - 1):
        for j in range(1, width - 1):
            array = []
            array.append(g[i, j])
            # if i > 0: array.append(g[i-1, j])
            # if i < height-1: array.append(g[i+1, j])
            # if j > 0: array.append(g[i, j-1])
            # if j < width-1: array.append(g[i, j+1])
            array.append(g[i - 1, j])
            array.append(g[i + 1, j])
            array.append(g[i, j - 1])
            array.append(g[i, j + 1])
            array.sort()
            copy[i, j] = array[-1]

    return copy


def erosion(g):
    width, height = image_width_and_height(g)
    copy = g.copy()

    for i in range(height):
        for j in range(width):
            array = []
            array.append(g[i, j])
            if i > 0: array.append(g[i - 1, j])
            if i < height - 1: array.append(g[i + 1, j])
            if j > 0: array.append(g[i, j - 1])
            if j < width - 1: array.append(g[i, j + 1])
            array.sort()
            copy[i, j] = array[0]

    return copy


def opening(img, n):
    for i in range(n):
        img = erosion(img)

    for i in range(n):
        img = dilatation(img)

    return img


def closing(img, n):
    for i in range(n):
        img = dilatation(img)

    for i in range(n):
        img = erosion(img)

    return img

# TODO: overcome maximum recursion depth exceeded
# def start_marking_component(img, label, i, j):
#     # By default N4 (nachbarn 4)
#     N4_dx = [1, 0, -1, 0]
#     N4_dy = [0, 1, 0, -1]
#
#     for idx in range(4):
#         if img[i + N4_dx[idx], j + N4_dy[idx]] == 255:
#             img[i + N4_dx[idx], j + N4_dy[idx]] = label
#             start_marking_component(img, label, i + N4_dx[idx], j + N4_dy[idx])
#
#     return img
#
#
# def zusammenhangskomponenten(img):
#     """
#     Implements Flood Fill Algorithm (german: Zusammenhangskomponenten / ZHK)
#     :param img: image that passed the binarising, opening and closing process
#     :return: the same image with each pixel marked with a label
#     """
#     label = 0
#     width, height = image_width_and_height(img)
#
#     for j in range(width):
#         for i in range(height):
#             if img[i, j] == 255:
#                 label += 1
#                 copy = start_marking_component(img, label, i, j)
#
#     return copy


def delete_first_three_components(img):
    width, height = image_width_and_height(img)
    for j in range(width):
        for i in range(height):
            if not (img[i, j] == 255 or img[i, j] == 4):
                img[i, j] = 0
    return img

if __name__ == "__main__":
    orig = cv2.imread("Media/Pfeile.png", cv2.IMREAD_GRAYSCALE)
    print_img(orig)
    schwellwert = 225
    n_value = 3

    res1 = binarisierung(orig, schwellwert)
    print_img(res1)

    res2 = closing(res1, n_value)
    print_img(res2)

    res3 = opening(res2, n_value)
    print_img(res3)

    # TODO: overcome maximum recursion depth exceeded
    # res4 = zusammenhangskomponenten(res3)
    # res5 = delete_first_three_components(res4)
    # print_img(res5)

