from google.cloud import vision
from PIL import Image as pilImage
import io, requests, json
from bounding import place_box


def detect_document(path):
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
                        box = []
                        for vertex in symbol.bounding_box.vertices:
                            box.append({'x': vertex.x, 'y': vertex.y})
                        boxes.append(box)
                    # draw larger box after small ones
                    box = []
                    for vertex in word.bounding_box.vertices:
                        box.append({'x': vertex.x,
                                    'y': vertex.y,
                                    'color': (254, 0, 0)})
                    boxes.append(box)

    box_image = pilImage.open(path)
    for box in boxes:
        if 'color' in box[0].keys():
            box_image = place_box(box, box_image, box[0]['color'])
        else:
            box_image = place_box(box, box_image)

    box_image.show()


if __name__ == '__main__':
    # path = "devocion_test.jpg"
    path = 'devocion_test copy.jpg'
    # path = 'handwriting.png'

    detect_document(path)
