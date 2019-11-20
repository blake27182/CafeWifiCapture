import math
from scripts.classes import Vertex, WordPoly, Match, Constraint


def get_word_polys(response):
    """Parses out all the words in the response object to a list of WordPoly

    Args:
        response: (Google API response object): The data to process

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
        a_x: (str): First string
        a_y: (str): Second string
        case_sense: (bool): Case sensitivity on or off

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
    """Recursive helper function for similarity.

    Args:
        a_low: (int): Low index on string a
        b_low: (int): Low index on string b
        a: (str): First string
        b: (str): Second string

    Returns:
        (float): highest similarity found at this depth

    """
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
    """Gets words based on a given location scope relative to key_word.

    Uses subtractive boolean unions to scope to an area of the image.
    i.e. If you want to find words in the upper right quadrant,
    (remember key_word is the origin) set above and right to True.
        It is important to know that each exclusion doesn't originate at
    key_word.center. It actually will start either left of or above etc.
    so that the key_word itself would be included in the results. This is
    done to allow contradictions (like above=True, below=True) to return
    the words between those termination lines.

    Args:
        key_word: (obj:`WordPoly`): Origin for scoping around.
        a_word_pool: (`list` of obj:`WordPoly`): Words to choose from
        response: (Google API response object): Words to choose from
        right: (bool): exclude left
        left: (bool): exclude right
        above: (bool): exclude below
        below: (bool): exclude above

    Returns:
        (`list` of obj:`WordPoly`): The words you asked for
    """
    # assuming the document was aligned straight and oriented correctly
    if a_word_pool is None:
        if response is None:
            raise Exception("you must give me either word_pool "
                            "or a response object")
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


def proximity_sort(anchor, words, bias):
    """Quick-sort based algorithm sorts in-place closest to furthest

    Args:
        anchor: (obj:`WordPoly`): The word every distance will be relative to
        words: (`list` of obj:`WordPoly`): The words to sort
        bias: (float): Alignment bias when calculating proximity.
            1 is square, (0,1) prioritizes vertical words, (1,∞) for horizontal
    """
    # decided to use a quick-sort because its great for in-place sorting
    # and has O(logn) time complexity. Not too worried about the space
    # complexity by using recursion because our list will usually range
    # from 3 to 10, giving us a typical depth of 3 or so.
    # If this algorithm becomes too expensive, it will probably be because
    # of the cost of calculating distance for each comparison.

    # would like to write a couple test cases for this. I know it generally
    # works, but its hard to tell if there are small discrepancies
    prox_sort_helper(0, len(words)-1, words, anchor, bias)


def prox_sort_helper(low, high, words, anchor, bias):
    """Recursive helper function for proximity_sort

    Args:
        low: (int): Low index (inclusive)
        high: (int): High index (inclusive)
        words: (`list` of obj:`WordPoly`): Words we are sorting
        anchor: (obj:`WordPoly`): Word to calculate distance relative to
        bias: (float): Alignment bias for calculating distance (see previous)
    """
    partition = words[low]
    i = low + 1
    j = high
    while i < j:
        while (
                prox_calc(anchor, words[j], bias)
                > prox_calc(anchor, partition, bias)
                and j > i
        ):
            j -= 1
        while (
                prox_calc(anchor, words[i], bias)
                < prox_calc(anchor, partition, bias)
                and i < j
        ):
            i += 1

        temp = words[j]
        words[j] = words[i]
        words[i] = temp

    if (prox_calc(anchor, words[i], bias)
            < prox_calc(anchor, partition, bias)):
        temp = words[i]
        words[i] = partition
        words[low] = temp

    if i - low > 1:
        prox_sort_helper(low, i-1, words, anchor, bias)
    if high - i > 0:
        prox_sort_helper(i, high, words, anchor, bias)


def prox_calc(f_word, t_word, bias=1):
    """Calculates the distance between two given words.

    Uses the manhattan distance instead of pythagorean to discourage diagonal
    words. We also use a bias for choosing which axis to "squish". If you want
    to look for words on the same line, choose a high bias (1,∞). If you want
    to find words in a column, use a low bias (0,1).

    Args:
        f_word: (obj:`WordPoly`): First word
        t_word: (obj:`WordPoly`): Second word
        bias: (float): Alignment bias (see description)

    Returns:
        (float): Distance between the given word center vertices

    """
    x_delta = abs(f_word.center.x - t_word.center.x)
    y_delta = abs(f_word.center.y - t_word.center.y)
    y_delta *= bias
    return math.sqrt(x_delta**2 + y_delta**2)


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
    final_passwords = []

    # horizontal scope and sort
    words_in_scope = get_words_from_pool(
        pass_key_match.from_poly,
        words,
        right=True,
        below=True,
        above=True,
    )
    proximity_sort(pass_key_match.from_poly, words_in_scope, 10)
    for word in words_in_scope:
        if len(word) > 5:
            final_passwords.append(word)
            break

    # vertical scope and sort
    words_in_scope = get_words_from_pool(
        pass_key_match.from_poly,
        words,
        right=True,
        below=True,
        left=True,
    )
    proximity_sort(pass_key_match.from_poly, words_in_scope, .5)
    # print('vertical sort:')
    # for word in words_in_scope:
    #     print(word)
    for word in words_in_scope:
        if len(word) > 5:
            final_passwords.append(word)
            break

    return final_passwords


if __name__ == '__main__':
    pass

