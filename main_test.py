from google.cloud import vision
import io
from bounding_center import box_document
from word_center import get_words, get_matches
from network_center import get_network_info


def detect_document(image_path, **kwargs):
    """Detects document features in an image."""

    client = vision.ImageAnnotatorClient.from_service_account_json('creds.json')
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)
    response = client.document_text_detection(image=image)

    # box_image = box_document(image_path, **kwargs)
    # box_image.show()

    words = get_words(response)
    network_names = get_network_info()
    words = [x['word'] for x in words]
    matches = get_matches(words, network_names, num_res=5)

    print(network_names)
    print(matches)

    # determine password
    # try the password or passwords on each of our matches


if __name__ == '__main__':
    path = "devocion_test.jpg"
    # path = 'devocion_test copy.jpg'
    # path = 'handwriting.png'

    detect_document(path, box_paragraphs=True, box_letters=True)
