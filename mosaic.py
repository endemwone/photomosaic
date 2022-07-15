from PIL import Image
import argparse
import os

from lib import JSONCache, average_rgb, get_average_rgbs, get_pixel_matrix, get_square, pythagoras_nearest_rgb

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="Input image", required=True)
parser.add_argument("-o", "--output", help="Output image", required=True)
parser.add_argument(
    "-d", "--dir", help="Directory of source images", required=True)
parser.add_argument("-s", "--square_size", type=int,
                    help="Square size of source images", required=True)

args = parser.parse_args()

# Input file
input_file = args.input

# Size of image square
square_size = args.square_size


source_img_files = os.listdir(args.dir)
print("Found {} images".format(len(source_img_files)))


# Check if cache exists
cache = JSONCache("./average_rgb_cache.json")

# Get average RGB of every image in `img_list`
print("Getting average RGBs of the images...")
average_rgbs = get_average_rgbs(source_img_files, args.dir, cache.read())
cache.write(average_rgbs)


average_rgb_dict = cache.read()


target_img = Image.open(input_file)
print("Converting input image to pixel matrix...")
target_pixels = get_pixel_matrix(target_img)
target_width, target_height = target_img.size

print("Creating target image...")
output_img = Image.new('RGB', (target_width, target_height), (255, 255, 255))

# Output file
output_file = args.output

progress = 0
total_squares = target_width * target_height / (square_size * square_size)
for x in range(0, target_width-1, square_size):
    for y in range(0, target_height-1, square_size):
        square = get_square(target_pixels, (y, x), square_size)
        target_rgb = average_rgb(square)
        filename = pythagoras_nearest_rgb(target_rgb, average_rgb_dict)

        source_img = Image.open(args.dir + "/" + filename)
        source_img.resize((square_size, square_size))

        output_img.paste(source_img, (x, y))
        print("\rProgress: {}%".format(
            round(progress/total_squares*100, 2)), end="", flush=True)
        progress += 1
print("\rProgress: 100%   ")

print("Done!")
output_img.show()
output_img.save(output_file)
