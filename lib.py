from itertools import product
from PIL import Image, ImageDraw
import sys


def get_pixel_matrix(img: Image) -> list:
    """
    Returns the pixel matrix of the image

    Args:
        img (PIL.Image): Image to be used for drawing

    Returns:
        list: Pixel matrix of the image
    """
    pixels = list(img.getdata())
    return [pixels[i:i+img.width] for i in range(0, len(pixels), img.width)]


def average_rgb(pixels: list) -> tuple:
    """
    Returns the average RGB of the pixel matrix
    """
    r_sum = 0
    g_sum = 0
    b_sum = 0
    n = 0

    for row in pixels:
        for p in row:
            r_sum += p[0]
            g_sum += p[1]
            b_sum += p[2]

            n += 1

    return (r_sum / n, g_sum / n, b_sum / n)


def get_average_rgbs(img_files: list, dir: str) -> list:
    """
    Calculates average RGB of every image in `img_list`

    Args:
        img_list: List of images

    Returns:
        List of RGB values of every image in `img_list`
    """
    average_rgb_dict = {}
    progress = 0
    for file in img_files:
        img = Image.open(dir + "/" + file)
        average_rgb_dict[file] = average_rgb(get_pixel_matrix(img))
        print("\rProgress: {}%".format(
            round(progress/len(img_files)*100, 2)), end="", flush=True)
        progress += 1
    print("\rProgress: 100%  ")
    return average_rgb_dict


def pixelize(img: Image, d: int) -> Image:
    """
    Return pixelized version of the image
    """
    img_draw = ImageDraw.Draw(img)
    w, h = img.size

    grid = product(range(0, w, d), range(0, h, d))
    for i, j in grid:
        img_draw.rectangle(
            (i, j, i+d, j+d), fill=average_rgb(img.crop((i, j, i+d, j+d))))

    return img


def pythagoras_nearest_rgb(target_rgb: list, average_rgb_dict: dict) -> str:
    """
    Finds the source image with the smallest color difference to the target_rgb

    Args:
        target_rgb: RGB values of the target square
        average_rgb_dict: dictionary of source files => average RGB value of the file

    Returns:
        The name of the source image with the smallest color difference to the target_rgb
    """
    best_match = None
    best_match_diff = None
    for file, average_rgb in average_rgb_dict.items():
        diff = pythagoras_color_difference(target_rgb, average_rgb)
        if best_match_diff is None or diff < best_match_diff:
            best_match = file
            best_match_diff = diff

    return best_match


def pythagoras_color_difference(pixel1: list, pixel2: list) -> float:
    """
    Calculates the color difference between two squares using the pythagorean theorem in 3D

    Args:
        pixel1: RGB values of pixel1
        pixel2: RGB values of pixel2

    Returns:
        The color difference between pixel1 and pixel2
    """
    total = 0
    for c1, c2 in zip(pixel1, pixel2):
        total += (c1 - c2)**2
    return total**0.5


def get_square(pixels: list, corner: tuple, size: int) -> list:
    """
    Returns a square sub-section of the `pixels` matrix,
    with top-left corner at `corner`, and each side of the
    square `size` pixels in length.

    Args:
        pixels: the pixels matrix of the entire image
        corner: the top-left corner of the sub-section
        size: the size of each side of the sub-section

    Returns:
        A pixel matrix of a sub-section of the original matrix
    """
    opposite_corner = (corner[0] + size, corner[1] + size)
    square = []
    square_rows = pixels[corner[0]:opposite_corner[0]]

    for row in square_rows:
        square.append(row[corner[1]:opposite_corner[1]])

    return square
