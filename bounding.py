from PIL import Image
from google.cloud import vision
import io


def main_test():
    pass


def place_box(a_corners, image_obj, color=(0, 254, 0)):
    # make sure corners comply with list of dict format
    # top left and bottom right corners only
    # e.g. [{"x": 50, "y": 100},
    #       {"x": 80, "y": 150}]

    width = int(image_obj.size[1] / 300)

    # Draw top line
    for i in range(a_corners[0]['y'], a_corners[0]['y'] + width + 1):
        for j in range(a_corners[0]['x'], a_corners[1]['x'] + 1):
            image_obj.putpixel((j, i), color)

    # Draw bottom line
    for i in range(a_corners[1]['y'] - width, a_corners[1]['y'] + 1):
        for j in range(a_corners[0]['x'], a_corners[1]['x'] + 1):  # google draws their corners in a circular pattern
            image_obj.putpixel((j, i), color)

    # Draw left line
    for i in range(a_corners[0]['y'], a_corners[1]['y'] + 1):
        for j in range(a_corners[0]['x'], a_corners[0]['x'] + width + 1):
            image_obj.putpixel((j, i), color)

    # Draw right line
    for i in range(a_corners[0]['y'], a_corners[1]['y'] + 1):
        for j in range(a_corners[1]['x'] - width, a_corners[1]['x'] + 1):
            image_obj.putpixel((j, i), color)

    return image_obj


def get_corners(response, box_words=True, box_letters=False, box_paragraphs=False):
    boxes = []  # list of list of dict

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        if box_letters:
                            box = [
                                {
                                    'x': symbol.bounding_box.vertices[0].x,
                                    'y': symbol.bounding_box.vertices[0].y
                                },
                                {
                                    'x': symbol.bounding_box.vertices[2].x,
                                    'y': symbol.bounding_box.vertices[2].y
                                },
                            ]
                            boxes.append(box)
                    # draw larger boxes after small ones
                    if box_words:
                        box = [
                            {
                                'x': word.bounding_box.vertices[0].x,
                                'y': word.bounding_box.vertices[0].y,
                                'color': (255, 0, 0)
                            },
                            {
                                'x': word.bounding_box.vertices[2].x,
                                'y': word.bounding_box.vertices[2].y,
                            },
                        ]
                        boxes.append(box)
                # draw larger boxes after small ones
                if box_paragraphs:
                    box = [
                        {
                            'x': paragraph.bounding_box.vertices[0].x,
                            'y': paragraph.bounding_box.vertices[0].y,
                            'color': (0, 0, 255)
                        },
                        {
                            'x': paragraph.bounding_box.vertices[2].x,
                            'y': paragraph.bounding_box.vertices[2].y,
                        },
                    ]
                    boxes.append(box)

    return boxes


def box_document(a_path, **kwargs):

    client = vision.ImageAnnotatorClient.from_service_account_json('creds.json')

    with io.open(a_path, 'rb') as image_file:
        content = image_file.read()

    o_image = vision.types.Image(content=content)
    response = client.document_text_detection(image=o_image)

    boxes = get_corners(response, **kwargs)
    box_image = Image.open(a_path)

    for box in boxes:
        if 'color' in box[0].keys():
            box_image = place_box(box, box_image, box[0]['color'])
        else:
            box_image = place_box(box, box_image)

    return box_image


if __name__ == '__main__':
    pass
