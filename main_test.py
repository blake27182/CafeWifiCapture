from google.cloud import vision
import io
from bounding_center import box_document
from word_center import get_words


def detect_document(image_path, **kwargs):
    """Detects document features in an image."""

    client = vision.ImageAnnotatorClient.from_service_account_json('creds.json')
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)
    response = client.document_text_detection(image=image)

    words = get_words(response)

    for word in words:
        print(word)

    # box_image = box_document(image_path, **kwargs)
    # box_image.show()


if __name__ == '__main__':
    # path = "devocion_test.jpg"
    # path = 'devocion_test copy.jpg'
    path = 'handwriting.png'

    detect_document(path, box_paragraphs=True, box_letters=True)
