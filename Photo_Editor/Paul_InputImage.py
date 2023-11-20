from PIL import Image, ImageFilter
import numpy as np

# Function to perform box blur
def blur_image(image):
    # Apply box blur filter to the image
    blurred_image = image.filter(ImageFilter.BoxBlur(5))
    
    return blurred_image

# Function to save modified image
def save_image(image,outputPath, filename):
    image.save(outputPath+filename)

# Example usage
input_path = input("Enter path to input image (eg. C:/image.jpg): ")

# Open the image

input_image = Image.open(input_path)

# Blur image
blurred_image = blur_image(input_image)

# Save modified image
output_path = input("Enter output file path: ")
output_fileName = input("input output file name(xxx.jpg): ")
save_image(blurred_image, output_path, output_fileName)

print("Image editing completed and saved successfully!")