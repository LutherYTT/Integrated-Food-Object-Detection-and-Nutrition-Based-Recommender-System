# -*- coding: utf-8 -*-
import os
from rembg import remove
from PIL import Image, ImageChops

# triming the blank spaces
def trim_image(image):
    bg = Image.new(image.mode, image.size, image.getpixel((0, 0)))
    diff = ImageChops.difference(image, bg) # Increase contrast for better detection
    diff = ImageChops.add(diff, diff, 2.0)
    bbox = diff.getbbox()
    if bbox:
        return image.crop(bbox)
    else:
        return image  # If there are no significant differences, the original image is returned.

def remove_background_and_convert_to_png(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
            input_path = os.path.join(input_folder, filename)
            output_filename = os.path.splitext(filename)[0] + '.png'  # Change extension to .png
            output_path = os.path.join(output_folder, output_filename)
            try:
                input_image = Image.open(input_path)
                # remove background
                output_image = remove(input_image)
                # triming the blank spaces
                trimmed_image = trim_image(output_image)
                # output
                trimmed_image.save(output_path, 'PNG')
                print(f"Background Removed: {filename} -> {output_filename}")
            except Exception as e:
                print(f"Error {filename}: {e}")

if __name__ == "__main__":
    input_folder = 'RemoveBackgroundInput'
    output_folder = 'RemoveBackgroundOutput'
    remove_background_and_convert_to_png(input_folder, output_folder)
    print("Finished.")
