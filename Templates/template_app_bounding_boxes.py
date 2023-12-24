import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import imageio

def read_bmp_image(image_path):
    bmp_image = imageio.imread(image_path)
    return Image.fromarray(bmp_image)


def parse_annotations(annotation_text=False):
    # Rewrite according to the annotations

    lines = annotation_text.strip().split('\n')
    # Extract filename
    filename = lines[0].strip()

    annotations = []
    for line in lines[1:]:
        x, y, class_number = map(int, line.strip().split(','))
        annotations.append((x, y, class_number))

    return filename, annotations


def draw_annotations(image, annotations):
    draw = ImageDraw.Draw(image)


    classes = {
        1: ('class 1',(0,128,0)),
        2: ('class 2', (128,0,0))}

    font = ImageFont.truetype("arial.ttf", 25)

    offset = 80
    for x, y, class_number in annotations:
          text=f"{classes[class_number][0]}"
          text_width = font.getlength(text)
          text_x = x - text_width // 2
          draw.rectangle((x-offset, y-offset, x+offset, y+offset), outline=classes[class_number][1], width=4)
          draw.text((text_x, y-10), text, fill=(0,0,0), font=font)
    return image


def main():
    st.title("Template Streamlit App")

    # Upload image file through Streamlit
    uploaded_image = st.file_uploader("Choose an image file...", type=["jpg", "png", 'bmp'])

    if uploaded_image is not None:
        # Read the image
        image = Image.open(uploaded_image).convert("RGB")
        image.thumbnail((960, 600))

        # Display the original image on the left
        #st.image(image, caption="Input Image", use_column_width=True, clamp=True)


        annotations =  """filename.jpg
        430 400 1""" #x y class

        filename, annotations = parse_annotations(annotations)

        # Draw bounding boxes based on annotations
        left_column, right_column = st.columns(2)

        # Display the original image on the left
        left_column.image(image, caption="Input Image", use_column_width=True, clamp=True)

        # Draw bounding boxes based on annotations
        output_image = draw_annotations(image.copy(), annotations)


        # Display the output image on the right
        right_column.image(output_image, caption="Output Image with Bounding Boxes", use_column_width=True, clamp=True)


if __name__ == "__main__":
    main()
