from PIL import Image, ImageEnhance
import os
import subprocess


def change_metadata(image_path, new_metadata):
    try:
        subprocess.run(['exiftool', '-overwrite_original', *new_metadata, image_path])
        print('Metadata changed successfully for', image_path)
    except Exception as e:
        print('Error:', str(e))

def change_color_scheme(image_path, output_path):
    def shift_hue(image, hue_shift_factor):
        rgb_image = image.convert('RGB')

        # Create a new image to store the shifted hue
        shifted_image = Image.new('RGB', image.size)

        for y in range(image.height):
            for x in range(image.width):
                r, g, b = rgb_image.getpixel((x, y))

                # Convert RGB to HSV
                max_value = max(r, g, b)
                min_value = min(r, g, b)
                delta = max_value - min_value

                value = max_value / 255.0
                saturation = 0 if max_value == 0 else delta / max_value

                if delta == 0:
                    hue = 0  # undefined, but we'll set it to 0
                elif max_value == r:
                    hue = ((g - b) / delta) % 6
                elif max_value == g:
                    hue = (b - r) / delta + 2
                else:
                    hue = (r - g) / delta + 4

                # Adjust hue
                hue = (hue + hue_shift_factor) % 6

                # Convert HSV back to RGB
                c = value * saturation
                x1 = c * (1 - abs(hue % 2 - 1)) + 1e-6
                m = value - c

                if 0 <= hue < 1:
                    rgb_shifted = (c, x1, 0)
                elif 1 <= hue < 2:
                    rgb_shifted = (x1, c, 0)
                elif 2 <= hue < 3:
                    rgb_shifted = (0, c, x1)
                elif 3 <= hue < 4:
                    rgb_shifted = (0, x1, c)
                elif 4 <= hue < 5:
                    rgb_shifted = (x1, 0, c)
                else:
                    rgb_shifted = (c, 0, x1)

                r_shifted = int((rgb_shifted[0] + m) * 255)
                g_shifted = int((rgb_shifted[1] + m) * 255)
                b_shifted = int((rgb_shifted[2] + m) * 255)

                # Ensure RGB values are integers
                r_shifted = int(round(r_shifted))
                g_shifted = int(round(g_shifted))
                b_shifted = int(round(b_shifted))
                print(r_shifted, x, y)
                shifted_image.putpixel((round(x), y), (r_shifted, g_shifted, b_shifted))

        return shifted_image

    imagee = Image.open(image_path)
    shifted_image_out = shift_hue(imagee, 0.1)
    shifted_image_out.save(output_path)
    print('Color scheme changed successfully for', image_path)

if __name__ == "__main__":
    input_folder = 'YOUR_INPUT_FOLDER'  # Replace with the actual folder path
    output_folder = 'YOUR_OUTPUT_FOLDER'  # Output folder to save processed images

    # Example new metadata (replace with desired metadata)
    new_metadata = ['-Make=MyCamera', '-Model=Motorola G9']

    # Example enhancement factor (1.0 for no change, <1.0 for desaturation, >1.0 for saturation)

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over each file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(('.jpg', '.jpeg', '.png')):  # Check if it's an image file
            input_image_path = os.path.join(input_folder, filename)
            output_image_path = os.path.join(output_folder, filename)

            # Change metadata
            change_metadata(input_image_path, new_metadata)

            # Change color scheme
            change_color_scheme(input_image_path, output_image_path)
