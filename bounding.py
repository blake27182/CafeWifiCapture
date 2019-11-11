from PIL import Image
import base64


def main_test(corners, image_obj):
    # make corners comply with list of dict format
    # e.g. [{"x": 50, "y": 100},
    #       {"x":100, "y": 100}, ... ]

    width = int(image_obj.size[1] / 300)

    # Draw top line
    for i in range(corners[0]['y'], corners[0]['y'] + width):
        for j in range(corners[0]['x'], corners[1]['x']):
            image_obj.putpixel((j, i), (0, 254, 0))

    # Draw bottom line
    for i in range(corners[2]['y'], corners[2]['y'] + width):
        for j in range(corners[3]['x'], corners[2][
                                            'x'] + width):  # google draws their corners in a circular pattern
            image_obj.putpixel((j, i), (0, 254, 0))

    # Draw left line
    for i in range(corners[0]['y'], corners[3]['y']):
        for j in range(corners[0]['x'], corners[0]['x'] + width):
            image_obj.putpixel((j, i), (0, 254, 0))

    # Draw right line
    for i in range(corners[1]['y'], corners[2]['y']):
        for j in range(corners[1]['x'], corners[1]['x'] + width):
            image_obj.putpixel((j, i), (0, 254, 0))

    return image_obj


def place_box(corners, image_obj, color=(0, 254, 0)):
    # make corners comply with list of dict format
    # e.g. [{"x": 50, "y": 100},
    #       {"x":100, "y": 100}, ... ]

    width = int(image_obj.size[1] / 300)

    # Draw top line
    for i in range(corners[0]['y'], corners[0]['y'] + width):
        for j in range(corners[0]['x'], corners[1]['x']):
            image_obj.putpixel((j, i), color)

    # Draw bottom line
    for i in range(corners[2]['y'], corners[2]['y'] + width):
        for j in range(corners[3]['x'], corners[2][
                                            'x'] + width):  # google draws their corners in a circular pattern
            image_obj.putpixel((j, i), color)

    # Draw left line
    for i in range(corners[0]['y'], corners[3]['y']):
        for j in range(corners[0]['x'], corners[0]['x'] + width):
            image_obj.putpixel((j, i), color)

    # Draw right line
    for i in range(corners[1]['y'], corners[2]['y']):
        for j in range(corners[1]['x'], corners[1]['x'] + width):
            image_obj.putpixel((j, i), color)

    return image_obj


if __name__ == '__main__':
    # path = 'devocion_test.jpg'
    # path = 'devocion_test copy.jpg'
    path = 'handwriting.png'

    corners = [
        {   # Corner 0
            "x": 360,
            "y": 59
        },
        {   # Corner 1
            "x": 408,
            "y": 59
        },
        {   # Corner 2
            "x": 408,
            "y": 102
        },
        {   # Corner 3
            "x": 360,
            "y": 102
        }
    ]

    image = Image.open(path)
    new_image = place_box(corners, image)
    new_image.show()
