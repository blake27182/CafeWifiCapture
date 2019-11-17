import math
import numpy as np
import sys
from scripts.classes import Vertex, WordPoly


def get_word_polys(response):
    """Parses out all the words in the response object to a list of WordPolys

    Args:
        response: Google API response object

    Returns:
        (`list` of obj:`WordPoly`): The list of words in the document
            as WordPolys.
    """
    words = []
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    curr_word = ''
                    for symbol in word.symbols:
                        curr_word += symbol.text
                    vertices = word.bounding_box.vertices
                    words.append(
                        WordPoly(
                            vertices=vertices,
                            confidence=word.confidence,
                            word=curr_word
                        )
                    )
    return words


# def word_proximity(a, b, response):


def get_poly(a_word, response, str_type='word'):
    """Gets the WordPoly version of a given string.

    Args:
        a_word: (str): Must be present in response object
        response: (Google API response): response object
        str_type: (str): paragraph or word or symbol

    Returns:
        (obj:`WordPoly`): WordPoly for the given string
    """
    if str_type == 'word':
        for word in response.text_annotations:
            if word.description == a_word:
                return WordPoly(
                    word=a_word,
                    confidence=word.confidence,
                    vertices=word.bounding_box.vertices
                )
    # elif str_type == 'paragraph':
    #     for page in response.full_text_annotation.pages:
    #         for block in page.blocks:
    #             for paragraph in block.paragraphs:



def get_matches(word_list, network_names, num_res=3):
    """Finds the top matches in any two list of strings.

    Args:
        word_list: (list of obj:`WordPoly` or str): detected words
        network_names: (list of str): ssids scanned on airport
        num_res: (int): maximum number of results to return. If an exact match
            is found, only that match is returned.

    Returns:
        (list of tuple of str, str, float): Matches by words compared & smlrty
    """
    # convert to strings if its a list of WordPoly
    if type(word_list[0]) is WordPoly:
        word_list = [x.word for x in word_list]

    # high pass (return exact match)
    for word in word_list:
        if word in network_names:
            return [(word, word, 1)]

    # medium pass (top results out of top 3's of each detected word)
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
    """Assesses how similar two strings are.

    Hard bias for characters in the same order. Will return extremely low
    similarity for palindromes.

    Args:
        x: (str): first string
        y: (str): second string

    Returns:
        (tuple of str, str, float): The two strings compared, and similarity.
            Closer to 1 is more similar, closer to 0 is less similar.
    """
    # known issues with this algorithm:
    # hello / hellx receives the same score as hello / hell0
    # hello / hell receives the same score as hello / hell0
    if len(x) > len(y):
        return x, y, similarity_helper(0, 0, y, x) / len(x)
    else:
        return x, y, similarity_helper(0, 0, x, y) / len(y)


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
    word_list = [x['word'] for x in words]
    samples = ['password', 'PASSWORD', 'pw', 'PW']
    p_match = get_matches(word_list, samples, num_res=1)
    best_center = {}
    for word in words:
        if word['word'] == p_match[0]:
            best_center = word['center']
            break

    # grab the closest words to this one
    # return those words


if __name__ == '__main__':
    a_poly = {
        "vertices": [
            {
                "x": 195,
                "y": 59
            },
            {
                "x": 408,
                "y": 59
            },
            {
                "x": 408,
                "y": 155
            },
            {
                "x": 195,
                "y": 155
            }
        ]
    }
    b_poly = {
        "vertices": [
            {
                "x": 360,
                "y": 59
            },
            {
                "x": 408,
                "y": 59
            },
            {
                "x": 408,
                "y": 102
            },
            {
                "x": 360,
                "y": 102
            }
        ]
    }

