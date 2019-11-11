from google.cloud import vision
import io, requests, json


def detect_document(path):
    """Detects document features in an image."""

    # client = vision.Client.from_service_account_json('/path/to/keyfile.json')

    client = vision.ImageAnnotatorClient.from_service_account_json('creds.json')

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.document_text_detection(image=image)

    # print(response)

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            print('\nBlock confidence: {}\n'.format(block.confidence))

            for paragraph in block.paragraphs:
                print('Paragraph confidence: {}'.format(
                    paragraph.confidence))

                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    print('Word text: {} (confidence: {})'.format(
                        word_text, word.confidence))

                    for symbol in word.symbols:
                        print('\tSymbol: {} (confidence: {})'.format(
                            symbol.text, symbol.confidence))


if __name__ == '__main__':
    # authenticate()
    detect_document("handwriting.png")
