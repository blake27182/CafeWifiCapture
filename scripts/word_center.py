import math
import numpy as np
import sys
from scripts.classes import Vertex, WordPoly, Match, Constraint


def get_word_polys(response):
    """Parses out all the words in the response object to a list of WordPoly

    Args:
        response: Google API response object

    Returns:
        (`list` of obj:`WordPoly`): The list of words in the document.
    """
    words = []
    for page in response.full_text_annotation.pages:
        for b, block in enumerate(page.blocks):
            for p, paragraph in enumerate(block.paragraphs):
                for word in paragraph.words:
                    curr_word = ''
                    for symbol in word.symbols:
                        curr_word += symbol.text
                    vertices = word.bounding_box.vertices
                    words.append(
                        WordPoly(
                            vertices=vertices,
                            confidence=word.confidence,
                            word=curr_word,
                            para_idx=p,
                            block_idx=b
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


def get_matches(a_from_list, a_to_list, num_res=3, case_sense=True):
    """Finds the top matches in any two list of strings.

    Args:
        a_from_list: (list of obj:`WordPoly` or str): detected words
        a_to_list: (list of obj:`WordPoly` or str): Words to compare to
        num_res: (int): maximum number of results to return. If an exact match
            is found, only that match is returned.
        case_sense: (bool): Weather or not the match should be case sensitive

    Returns:
        (list of tuple of WordPoly, str, str, float): Matches by words
            compared & similarity
    """
    # if its a list of str, convert to WordPoly
    # also take care of case sensitivity
    if type(a_from_list[0]) is str:
        from_list = [WordPoly(word=x) for x in a_from_list]
    elif type(a_from_list[0]) is WordPoly:
        from_list = a_from_list
    else:
        raise Exception("you have to give me either a list of WordPoly or str")
    if type(a_to_list[0]) is str:
        to_list = [WordPoly(word=x) for x in a_to_list]
    elif type(a_to_list[0]) is WordPoly:
        to_list = a_to_list
    else:
        raise Exception("you have to give me either a list of WordPoly or str")

    # high pass (return exact match)
    for f_word in from_list:
        for t_word in to_list:
            if case_sense and f_word.word == t_word.word:
                return Match(
                    from_poly=f_word,
                    to_poly=t_word,
                    similarity=1
                )
            elif f_word.word.upper() == t_word.word.upper():
                return Match(
                    from_poly=f_word,
                    to_poly=t_word,
                    similarity=1
                )

    # medium pass (top results out of top 3's of each detected word)
    top_results = []
    for f_word in from_list:
        temp_list = [
            similarity(
                f_word.word,
                t_word.word,
                case_sense=case_sense
            )
            for t_word in to_list
        ]
        # Pick the top 3 for this word and put them in top_results
        for _ in range(3):
            best = temp_list[0]
            for temp in temp_list:
                if temp.similarity > best.similarity:
                    best = temp
            top_results.append(best)
            temp_list.remove(best)

    final = []
    for _ in range(num_res):
        best = top_results[0]
        for res in top_results:
            if res.similarity > best.similarity:
                best = res
        final.append(best)
        top_results.remove(best)
    if num_res == 1:
        return final[0]
    return final


def similarity(a_x, a_y, case_sense=True):
    """Assesses how similar two strings are.

    Hard bias for characters in the same order. Will return extremely low
    similarity for palindromes. It is also case-sensitive.

    Args:
        x: (str): first string
        y: (str): second string

    Returns:
        (obj:`Match`): The Match object--two strings compared, and similarity.
            Closer to 1 is more similar, closer to 0 is less similar.
    """
    # known issues with this algorithm:
    # hello / hellx receives the same score as hello / hell0
    # hello / hell receives the same score as hello / hell0

    r_match = Match()
    if type(a_x) is WordPoly:
        r_match.from_poly=a_x
        x = a_x.word
    else:
        x = a_x
    if type(a_y) is WordPoly:
        r_match.to_poly = a_y
        y = a_y.word
    else:
        y = a_y

    if not case_sense:
        x = x.upper()
        y = y.upper()

    r_match.word_to = y
    r_match.word_from = x

    if len(x) > len(y):
        sim = similarity_helper(0, 0, y, x) / len(x)
    else:
        sim = similarity_helper(0, 0, x, y) / len(y)

    r_match.similarity = sim
    return r_match


def similarity_helper(a_low, b_low, a, b):
    best = 0
    for i in range(a_low, len(a)):          # try every letter as the first letter
        for j in range(b_low, len(b)):      # for every letter in a, check it against b
            if a[i] == b[j]:                # if it matches, recurse on the rest
                temp = similarity_helper(i+1, j+1, a, b) + 1
                if temp > best:
                    best = temp
    return best


def get_words_from_pool(key_word, a_word_pool=None, response=None, right=False,
                        left=False, above=False, below=False):
    # assuming the document was aligned straight and oriented correctly
    if a_word_pool is None:
        if response is None:
            raise Exception("you must give me either word_pool or a response object")
        word_pool = get_word_polys(response)
    else:
        word_pool = a_word_pool

    pool_constraint = Constraint()

    if right:
        def constrain_right(a_word):
            left_max = key_word.center.x - key_word.get_width()
            return a_word.center.x > left_max
        pool_constraint.add_constraint(constrain_right)

    if left:
        def constrain_left(a_word):
            right_max = key_word.center.x + key_word.get_width()
            return a_word.center.x < right_max
        pool_constraint.add_constraint(constrain_left)

    if above:
        def constrain_above(a_word):
            lowest = key_word.center.y + key_word.get_height()
            return a_word.center.y < lowest     # coords are in 4th quadrant
        pool_constraint.add_constraint(constrain_above)

    if below:
        def constrain_below(a_word):
            highest = key_word.center.y - key_word.get_height()
            return a_word.center.y > highest    # coords are in 4th quadrant
        pool_constraint.add_constraint(constrain_below)

    words_from_pool = []
    for word in word_pool:
        if word == key_word:
            continue
        if pool_constraint.satisfies(word):
            words_from_pool.append(word)

    return words_from_pool


def get_passwords(words):
    # find the 'password' keyword location
    # make a group containing all the words on that line
    # if theres a colon, use the words after it
    # if none of the words work, and there are multiple words
    # that are close together, try concatenating them
    # and using the result

    # find a suitable password key
    suitable_keys = ['PASSWORD', 'PW', 'PIN']
    pass_key_match = get_matches(
        words,
        suitable_keys,
        case_sense=False,
        num_res=1
    )
    print('suitable_key_match:', pass_key_match)

    # get the words in the scope of the suitable key
    # this scope might change or we might use multiple scopes
    words_in_scope = get_words_from_pool(
        pass_key_match.from_poly,
        words,
        right=True,
        below=True,
        above=True,
    )


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

