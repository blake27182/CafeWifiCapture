from google.cloud import vision
import io, requests, json


def detect_document(path):
    """Detects document features in an image."""

    client = vision.ImageAnnotatorClient.from_service_account_json('creds.json')

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.document_text_detection(image=image)

    print(type(response))

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            print(f'\nBlock confidence: {block.confidence}\n')

            for paragraph in block.paragraphs:
                print(f'Paragraph confidence: {paragraph.confidence}')

                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    print(f'Word text: {word_text} (confidence: {word.confidence})')

                    for symbol in word.symbols:
                        print(f'\tSymbol: {symbol.text} (confidence: {symbol.confidence})')


if __name__ == '__main__':
    detect_document("devocion_test.jpg")
