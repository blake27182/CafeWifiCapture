from PIL import Image
import base64


def main_test(corners, image_path):
    width = 10
    # make corners comply with list of dict format
    # e.g. [{"x": 50, "y": 100},
    #       {"x":100, "y": 100}, ... ]

    image = Image.open(image_path)

    # Draw top line
    for i in range(corners[0]['y'], corners[0]['y'] + width):
        for j in range(corners[0]['x'], corners[1]['x']):
            image.putpixel((j, i), (0, 254, 0))

    dot_idx = image_path.rfind('.')
    new_name = image_path[:dot_idx] + "_boxed" + image_path[dot_idx:]
    image.save(new_name, image.format)

    image.show()


def place_box(corners, image_path):
    # make corners comply with list of dict format
    # e.g. [{"x": 50, "y": 100},
    #       {"x":100, "y": 100}, ... ]

    image = Image.open(image_path)
    width = int(image.size[1]/300)

    # Draw top line
    for i in range(corners[0]['y'], corners[0]['y'] + width):
        for j in range(corners[0]['x'], corners[1]['x']):
            image.putpixel((j, i), (0, 254, 0))

    dot_idx = image_path.rfind('.')
    new_name = image_path[:dot_idx] + "_boxed" + image_path[dot_idx:]
    image.save(new_name, image.format)

    image.show()


if __name__ == '__main__':
    # path = 'devocion_test.jpg'
    # path = 'devocion_test copy.jpg'
    path = 'handwriting.png'

    corners = [
        {
            "x": 100,
            "y": 100,
        },
        {
            "x": 200,
            "y": 100,
        },
        {
            "x": 200,
            "y": 200,
        },
        {
            "x": 100,
            "y": 200,
        },
    ]

    # main_test(corners, path)
    place_box(corners, path)
