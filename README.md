# Photomosaic Creator

## To run
To install the modules:

* Install `virtualenv` and `pip`
* `virtualenv env`
* `pip install -r requirements.txt`

Then whenever you need to run the code, first run:

* `source env/bin/activate`

to load the modules.

Place all your source images in a directory, then run
`python crop_into_squares.py -d <source_images_directory>` to convert them into squares. Then run
`python mosaic.py -i <input_image> -o <output_image> -d <source_images_directory>`.

Voila! You got a photomosaic'd version of your input image.
