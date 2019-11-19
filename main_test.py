from google.cloud import vision
import io
from scripts.bounding_center import box_document
from scripts.word_center import *
from scripts.network_center import get_ssid_list


def detect_document(image_path, **kwargs):
    """Detects document features in an image."""
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## API request section

    client = vision.ImageAnnotatorClient.from_service_account_json('json_stuff/creds.json')
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)
    response = client.document_text_detection(image=image)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## Boxing section

    # box_image = box_document(image_path, response, **kwargs)
    # box_image.show()
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## Word gathering section

    words = get_word_polys(response)
    for word in words:
        print(word)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## Network scanning and matching section

    # words = get_word_polys(response)
    # network_names = get_ssid_list()
    # matches = get_matches_string(words, network_names, num_res=5)
    # print(network_names)
    # for match in matches:
    #     print(match)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # determine password

    pass_matches = get_passwords(words)
    print("password scope:")
    for match in pass_matches:
        print(match)


if __name__ == '__main__':
    # path = "src_images/devocion_test.jpg"
    # path = 'src_images/skytown.jpg'
    path = 'src_images/skytown2.jpg'
    # path = 'src_images/handwriting.png'
    # path = 'src_images/rand_words.jpg'
    # path = 'src_images/router.jpg'

    detect_document(
        path,
        box_words=True,
        box_paragraphs=False,
        box_letters=False
    )
