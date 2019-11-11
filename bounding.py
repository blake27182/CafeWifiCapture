from PIL import Image
import base64


def main_test(option):
    if option == 1:
        image_path = "handwriting.png"
    if option == 2:
        image_path = "devocion_test.jpg"
    if option == 3:
        image_path = "devocion_test copy.jpg"

    image = Image.open(image_path)
    data = image.getdata()
    data = list(data)

    for i in range(100, 200):
        for j in range(100, 200):
            pos = image.size[0]*i+j
            data[pos] = (0, 254, 0)

    new_image = Image.new(image.mode, image.size)
    new_image.putdata(data=data)
    new_image.save("new_image", format=image.format)
    new_image.show()


def place_box(corners, image):
    pass


if __name__ == '__main__':
    main_test(3)
