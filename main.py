import argparse
import cv2
import numpy as np
import os

def calculate_green_area(image_path, output_folder, count, 
                         pixels_per_cm,
                         lower_green, upper_green, 
                         min_area, text_file, 
                         font_scale, text_color):
    """
    Analyzes an image to detect and measure green areas.
    Saves the results as annotated images and text data.

    Parameters:
        image_path (str): Path to the input image file.
        output_folder (str): Directory where results will be saved.
        count (int): Initial counter for labeling detected green areas.
        pixels_per_cm (float): Number of pixels representing 1 cm.
        lower_green (tuple): Lower HSV bound for green detection.
        upper_green (tuple): Upper HSV bound for green detection.
        min_area (float): Minimum area threshold for detected regions.
        text_file (str): Name of the output text file for results.
        font_scale (float): Scale of the text annotation in the image.
        text_color (tuple): Color of the annotation text (BGR format).
    """
    # Read the image
    image = cv2.imread(image_path)
    
    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Create a mask to filter out the green areas
    mask = cv2.inRange(hsv, np.array(lower_green), np.array(upper_green))
    
    # Find contours of the green areas
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Process each detected green area
    for i, contour in enumerate(contours):
        # Draw detected contours in red
        cv2.drawContours(image, [contour], 0, (0, 0, 255), 1)
        
        # Calculate the area of the contour
        area_pixels = cv2.contourArea(contour)
        area_cm2 = (area_pixels / (pixels_per_cm ** 2))
        
        # Only process contours with a significant area
        if area_cm2 >= min_area:
            # Get bounding box coordinates for the contour
            x, y, w, h = cv2.boundingRect(contour)
            
            # Label the detected area with its index and size in cm^2
            cv2.putText(image, f'{count}:{area_cm2:.2f} cm^2', (x, y + h + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, 2)
            
            # Save the area information to a text file
            with open(f'{output_folder}/{text_file}', 'a') as file:
                file.write(f'{count}:{area_cm2:.2f} cm^2\n')
            
            # Increment the count for labeling
            count += 1
            
            # Highlight the detected green area in blue
            cv2.drawContours(image, [contour], 0, (255, 0, 0), 2)
    
    # Ensure the output directory exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Extract the filename and extension from the image path
    _, filename = os.path.split(image_path)
    file_base, file_ext = os.path.splitext(filename)
    
    # Determine an appropriate output format based on input format
    output_format = file_ext[1:].lower() if file_ext else "jpg"
    
    # Define output file paths
    output_path = os.path.join(output_folder, filename)
    
    # Save the processed image and mask
    cv2.imwrite(output_path, image)

def main():
    parser = argparse.ArgumentParser(description="Custom argv example")
    parser.add_argument("--input", type=str, required=True, help="Input folder path.")
    parser.add_argument("--output", type=str, required=True, help="Output folder path.")
    parser.add_argument("--pixels_per_cm", type=float, required=True, help="Number of pixels representing 1 cm.")
    parser.add_argument("--lowerG", type=tuple, default=(25, 70, 30), help="Lower HSV bound for green detection.")
    parser.add_argument("--upperG", type=tuple, default=(80, 255, 255), help="Upper HSV bound for green detection.")
    parser.add_argument("--min_area_cm", type=float, default=0.1, help="Minimum area(cm) threshold for detected regions.")
    parser.add_argument("--text_file", type=str, default="data.txt", help="Name of the output text file for results.")
    parser.add_argument("--font_scale", type=float, default=3, help="Scale of the text annotation in the image.")
    parser.add_argument("--text_color", type=tuple, default=(255, 255, 255), help="Color of the annotation text (BGR format).")

    args = parser.parse_args()
    os.makedirs(args.output, exist_ok=True)
    
    # Remove existing data.txt if present
    data_file_path = os.path.join(args.output, args.text_file)
    if os.path.exists(data_file_path):
        os.remove(data_file_path)

    process_images_in_directory(args.input, args.output, 1, args.pixels_per_cm, args.lowerG, args.upperG, args.min_area_cm, args.text_file, args.font_scale, args.text_color)

def process_images_in_directory(input_directory, output_directory, count, pixels_per_cm,
                                    lower_green, upper_green, 
                                    min_area, text_file, 
                                    font_scale, text_color):
    # Ensure output directory exists
    os.makedirs(output_directory, exist_ok=True)
    
    # Process each image in the input directory
    for filename in sorted(os.listdir(input_directory)):
        if filename.lower().endswith((".jpg", ".png")):
            # Construct full input and output paths
            input_path = os.path.join(input_directory, filename)
            
            with open(f'{output_directory}/data.txt', 'a') as file:
                file.write(filename + "\n")
            
            # Process the image to detect green areas
            calculate_green_area(input_path, output_directory, count, pixels_per_cm,
                                    lower_green, upper_green, 
                                    min_area, text_file, 
                                    font_scale, text_color)

if __name__ == '__main__':
    main()
