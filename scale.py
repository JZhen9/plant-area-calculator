import cv2
import matplotlib.pyplot as plt
import argparse

def measure_pixel_distance(image_path):
    # read image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to load image at {image_path}")
        return

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(image_rgb)
    ax.set_title('click two points corresponding to 1 cm')

    # click two points corresponding to 1 cm
    points = plt.ginput(2)
    plt.close()

    if len(points) < 2:
        print("Error: Two points were not selected.")
        return

    # distance
    (x1, y1), (x2, y2) = points
    pixel_distance = ((x2 - x1)**2 + (y2 - y1)**2)**0.5

    print(f"1 cm = {pixel_distance:.2f} pixels")

def main():
    parser = argparse.ArgumentParser(description="Measure pixel distance for 1 cm on an image.")
    parser.add_argument("--input", type=str, required=True, help="Input image path.")
    args = parser.parse_args()

    measure_pixel_distance(args.input)

if __name__ == "__main__":
    main()
