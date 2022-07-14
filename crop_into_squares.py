from PIL import Image
import os
import argparse

parser = argparse.ArgumentParser(description="Crop images to squares")
parser.add_argument(
    "-d", "--dir", help="Directory containing images", required=True)

args = parser.parse_args()

progress = 0
image_files = os.listdir(args.dir)

for file in image_files:
    img = Image.open(args.dir + "/" + file)
    w, h = img.size
    _min = min(w, h)
    img.crop((0, 0, _min, _min)).save(args.dir + "/" + file)
    print("\rProgress: {}%".format(
        round(progress/len()*100, 2)), end="", flush=True)
