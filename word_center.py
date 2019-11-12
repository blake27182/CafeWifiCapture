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


def get_matches(word_list, network_names, num_res=3):
    # high pass
    for word in word_list:
        if word in network_names:
            return [(word, word, 1)]

    # medium pass
    top_results = []
    for word in word_list:
        temp_list = [similarity(word, x) for x in network_names]
        # Pick the top 2 for this word and put them in top_results
        for _ in range(3):
            best = temp_list[0]
            for temp in temp_list:
                if temp[2] > best[2]:
                    best = temp
            top_results.append(best)
            temp_list.remove(best)

    final = []
    for _ in range(num_res):
        best = top_results[0]
        for res in top_results:
            if res[2] > best[2]:
                best = res
        final.append(best)
        top_results.remove(best)
    return final


def similarity(x, y):
    # known issues with this algorithm:
    # hello / hellx receives the same score as hello / hell0
    # hello / hell receives the same score as hello / hell0
    if len(x) > len(y):
        return (x, y, similarity_helper(0, 0, y, x) / len(x))
    else:
        return (x, y, similarity_helper(0, 0, x, y) / len(y))


def similarity_helper(a_low, b_low, a, b):
    best = 0
    for i in range(a_low, len(a)):          # try every letter as the first letter
        for j in range(b_low, len(b)):      # for every letter in a, check it against b
            if a[i] == b[j]:                # if it matches, recurse on the rest
                temp = similarity_helper(i+1, j+1, a, b) + 1
                if temp > best:
                    best = temp
    return best

def get_passwords(words):
    pass


if __name__ == '__main__':
    word1 = 'helmo'
    word2 = 'hnello'
    print(similarity(word1, word2))