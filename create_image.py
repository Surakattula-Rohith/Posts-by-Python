from PIL import Image, ImageDraw, ImageFont
import random

# Function to create and save an image with multi-line texts and an additional image between them
def create_image(text1, text2, background_image_path='bkg.jpg', additional_image_path='image.jpg', output_path='output_image.png'):
    # Create a blank image with the background image resized to 800x800
    width, height = 800, 800
    background_image = Image.open(background_image_path)
    background_image = background_image.resize((width, height))
    
    # Composite the background image with a blank image
    image = Image.new('RGB', (width, height))
    image.paste(background_image, (0, 0))

    # Draw the texts
    draw = ImageDraw.Draw(image)
    
    # Load a TrueType font (make sure to specify a valid path to a TTF font file)
    font_path = "arial.ttf"  # Path to your .ttf font file
    font_size_large = 40
    font_size_small = 20
    try:
        font_large = ImageFont.truetype(font_path, font_size_large)
        font_small = ImageFont.truetype(font_path, font_size_small)
    except IOError:
        # Fallback to default font if the TTF font cannot be loaded
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Text color and accents
    text_color = (43, 45, 66)  # Deep blue-gray
    border_color = (0, 119, 182)  # #0077b6
    accent_color = (205, 127, 50)  # Bronze
    red_color = (255, 0, 0)  # Red

    # Split text into lines
    def wrap_text(text, max_width, font):
        lines = []
        words = text.split(' ')
        line = ''
        for word in words:
            test_line = f'{line} {word}'.strip()
            if draw.textbbox((0, 0), test_line, font=font)[2] > max_width:
                lines.append(line)
                line = word
            else:
                line = test_line
        lines.append(line)
        return lines

    # Wrap texts
    max_width = width - 40
    text1_lines = wrap_text(text1, max_width, font_large)
    text2_lines = wrap_text(text2, max_width, font_small)

    # Position for the texts and image
    top_padding = 20
    line_height_large = 40
    line_height_small = 20
    text1_height = len(text1_lines) * line_height_large
    text2_height = len(text2_lines) * line_height_small
    image_position = (20, top_padding + text1_height + 10)
    image_height = height - text1_height - text2_height - 60  # Adjusted for new size

    # Draw the first text
    for i, line in enumerate(text1_lines):
        draw.text(((width - draw.textbbox((0, 0), line, font=font_large)[2]) // 2, top_padding + i * line_height_large), line, fill=text_color, font=font_large)
    
    # Open and resize the additional image
    try:
        additional_image = Image.open(additional_image_path)
        additional_image = additional_image.resize((width - 40, image_height))
        # Crop the image if needed to fit within the designated area
        if additional_image.height > image_height:
            additional_image = additional_image.crop((0, additional_image.height - image_height, additional_image.width, additional_image.height))
        # Paste the image in the remaining area
        image.paste(additional_image, image_position)
    except FileNotFoundError:
        print(f"Image file {additional_image_path} not found. Skipping image.")
    
    # Draw the second text with random red words
    words = text2.split(' ')
    random_red_words = random.sample(words, max(1, len(words) // 5))  # Randomly choose about 20% of words
    
    current_x, current_y = 20, height - text2_height - 20
    for line in text2_lines:
        line_words = line.split(' ')
        for word in line_words:
            word_color = red_color if word in random_red_words else text_color
            draw.text((current_x, current_y), word, fill=word_color, font=font_small)
            current_x += draw.textbbox((0, 0), word, font=font_small)[2] + 5  # Add spacing between words
        current_y += line_height_small
        current_x = 20  # Reset x position for next line

    # Draw thin border
    border_thickness = 6
    # Adjust border position to ensure it fully covers the image edges
    draw.rectangle([0, 0, width - 1, height - 1], outline=border_color, width=border_thickness)
    
    # Save the final image
    image.save(output_path)
    print(f"Image saved as {output_path}")

# Example usage
text1 = "Spiritual Monument in the Hills"
text2 = "Discover a tranquil spiritual monument nestled in the hills. Enjoy serene views and a peaceful retreat from everyday life. Experience a unique blend of natural beauty and spiritual reflection."

create_image(text1, text2)
