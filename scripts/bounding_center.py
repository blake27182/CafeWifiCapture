from PIL import Image


def main_test():
    pass


def place_box(a_corners, image_obj, color=(0, 254, 0)):
    """Draws a box with the given corners on the image object.

    The width of the lines is determined by the dimensions of the image.

    Args:
        a_corners: (`list` of `dict`): Top-left and bottom-right corners
        image_obj: (obj:`PIL.Image`): Image object to draw on
        color: (`tuple` of int): Color in RGB you want the box to be

    Returns:
        (obj:`PIL.Image`): The image after being drawn on

    """
    # make sure corners comply with list of dict format
    # top-left and bottom-right corners only
    # e.g. [{"x": 50, "y": 100},
    #       {"x": 80, "y": 150}]

    width = int(image_obj.size[1] / 300)

    # Draw top line
    for i in range(a_corners[0]['y'], a_corners[0]['y'] + width + 1):
        for j in range(a_corners[0]['x'], a_corners[1]['x'] + 1):
            image_obj.putpixel((j, i), color)

    # Draw bottom line
    for i in range(a_corners[1]['y'] - width, a_corners[1]['y'] + 1):
        for j in range(a_corners[0]['x'], a_corners[1]['x'] + 1):  # google draws their corners in a circular pattern
            image_obj.putpixel((j, i), color)

    # Draw left line
    for i in range(a_corners[0]['y'], a_corners[1]['y'] + 1):
        for j in range(a_corners[0]['x'], a_corners[0]['x'] + width + 1):
            image_obj.putpixel((j, i), color)

    # Draw right line
    for i in range(a_corners[0]['y'], a_corners[1]['y'] + 1):
        for j in range(a_corners[1]['x'] - width, a_corners[1]['x'] + 1):
            image_obj.putpixel((j, i), color)

    return image_obj


def get_corners(
        response,
        box_words=True,
        box_letters=False,
        box_paragraphs=False
):
    """Parses out the corner information required by the place_box function

    Args:
        response: (Google API response object):
        box_words: (bool): Include words in parsing
        box_letters: (bool): Include letters in parsing
        box_paragraphs: (bool): Include paragraphs in parsing

    Returns:
        (`list` of `list` of `dict`): List of pairs of corners.

    """
    # should probably refactor this to use our Vertex class

    boxes = []  # list of list of dict

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        if box_letters:
                            box = [
                                {
                                    'x': symbol.bounding_box.vertices[0].x,
                                    'y': symbol.bounding_box.vertices[0].y
                                },
                                {
                                    'x': symbol.bounding_box.vertices[2].x,
                                    'y': symbol.bounding_box.vertices[2].y
                                },
                            ]
                            boxes.append(box)
                    # draw larger boxes after small ones
                    if box_words:
                        box = [
                            {
                                'x': word.bounding_box.vertices[0].x,
                                'y': word.bounding_box.vertices[0].y,
                                'color': (255, 0, 0)
                            },
                            {
                                'x': word.bounding_box.vertices[2].x,
                                'y': word.bounding_box.vertices[2].y,
                            },
                        ]
                        boxes.append(box)
                # draw larger boxes after small ones
                if box_paragraphs:
                    box = [
                        {
                            'x': paragraph.bounding_box.vertices[0].x,
                            'y': paragraph.bounding_box.vertices[0].y,
                            'color': (0, 0, 255)
                        },
                        {
                            'x': paragraph.bounding_box.vertices[2].x,
                            'y': paragraph.bounding_box.vertices[2].y,
                        },
                    ]
                    boxes.append(box)

    return boxes


def box_document(a_path, response, **kwargs):
    boxes = get_corners(response, **kwargs)
    box_image = Image.open(a_path)

    for box in boxes:
        if 'color' in box[0].keys():
            box_image = place_box(box, box_image, box[0]['color'])
        else:
            box_image = place_box(box, box_image)

    return box_image


if __name__ == '__main__':
    pass
