from google.cloud import vision
import io
from bounding import box_document


def detect_document(path):
    """Detects document features in an image."""

    client = vision.ImageAnnotatorClient.from_service_account_json('creds.json')
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)
    response = client.document_text_detection(image=image)

    words = []

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    curr_word = ''
                    for symbol in word.symbols:
                        curr_word += symbol.text
                    words.append({'word': curr_word,
                                  'confidence': word.confidence})

    for word in words:
        print(word)

    # box_image = box_document(path, box_words=True)
    # box_image.show()


if __name__ == '__main__':
    path = "devocion_test.jpg"
    # path = 'devocion_test copy.jpg'
    # path = 'handwriting.png'

    detect_document(path)
