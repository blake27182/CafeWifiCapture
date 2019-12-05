from google.cloud import vision
import io
# This isnt a super safe way to do this but whatever right now
from scripts.bounding_center import *
from scripts.word_center import *
from scripts.network_center import *


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

    network_names = get_ssid_list()
    matches = get_matches(words, network_names, num_res=5)
    print(network_names)
    for match in matches:
        print(match)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## Determine password section

    # passwords = get_passwords(words)
    # print("passwords:")
    # for word in passwords:
    #     print(word)
    # # try password
    # # if it doesnt work, first try concatenating the next word
    # next_word = get_next_word_on_line(
    #     passwords[0],   # just say its the first one for testing sake
    #     words
    # )
    # if next_word:
    #     next_try = passwords[0].word + next_word.word
    #     print('next try would be:')
    #     print(next_try)
    # else:
    #     print('no next found')


if __name__ == '__main__':
    # path = 'src_images/handwriting.png'
    # path = 'src_images/rand_words.jpg'
    # path = 'src_images/skytown.jpg'
    path = 'src_images/router.jpg'
    # path = "src_images/devocion_test.jpg"
    # path = 'src_images/skytown2.jpg'
    # path = 'src_images/blockchain_ctr.jpg'

    detect_document(
        path,
        box_words=True,
        box_paragraphs=False,
        box_letters=False
    )
