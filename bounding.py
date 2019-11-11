from PIL import Image
from google.cloud import vision
import io


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

def box_document(path, box_words=True, box_letters=False):
    """Detects document features in an image."""

    client = vision.ImageAnnotatorClient.from_service_account_json('creds.json')

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.document_text_detection(image=image)

    boxes = []      # list of list of dict

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        if box_letters:
                            box = []
                            for vertex in symbol.bounding_box.vertices:
                                box.append({'x': vertex.x, 'y': vertex.y})
                            boxes.append(box)
                    # draw larger box after small ones
                    if box_words:
                        box = []
                        for vertex in word.bounding_box.vertices:
                            box.append({'x': vertex.x,
                                        'y': vertex.y,
                                        'color': (254, 0, 0)})
                        boxes.append(box)

    box_image = Image.open(path)
    for box in boxes:
        if 'color' in box[0].keys():
            box_image = place_box(box, box_image, box[0]['color'])
        else:
            box_image = place_box(box, box_image)

    return box_image


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
