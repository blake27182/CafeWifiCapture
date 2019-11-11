from google.cloud import vision
import io
from bounding import box_document


def detect_document(path):
    """Detects document features in an image."""

    # client = vision.ImageAnnotatorClient.from_service_account_json('creds.json')
    # with io.open(path, 'rb') as image_file:
    #     content = image_file.read()
    # image = vision.types.Image(content=content)
    # response = client.document_text_detection(image=image)

    box_image = box_document(path)
    box_image.show()


if __name__ == '__main__':
    path = "devocion_test.jpg"
    # path = 'devocion_test copy.jpg'
    # path = 'handwriting.png'

    detect_document(path)
