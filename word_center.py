def get_words(response):
    words = []

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    curr_word = ''
                    for symbol in word.symbols:
                        curr_word += symbol.text
                    words.append(
                        {
                            'word': curr_word,
                            'confidence': word.confidence,
                            'center': {
                                'x': (word.bounding_box.vertices[0].x
                                      + word.bounding_box.vertices[2].x) / 2,
                                'y': (word.bounding_box.vertices[0].y
                                      + word.bounding_box.vertices[2].y) / 2
                            }

                        }
                    )

    return words
