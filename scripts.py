from PIL import Image


def resize_photo(new_file_name, width, height):
    image = Image.open(new_file_name)
    resized_image = image.resize((width, height))
    resized_file_name = f"resized_{new_file_name}"
    resized_image.save(resized_file_name)
    return resized_file_name


def png_2_ascii(img):
    chars = ["%", "*", "+", "8", ",", ".", "`"]

    # L - convert image to monochrome
    # 1 - convert image to black and white
    with Image.open("photo.jpg") as img:
        img = img.convert('L')
        width, height = img.size
        px = img.load()
        art = []
        for i in range(height):
            art.append('Q'*width)
