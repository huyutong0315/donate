from PIL import Image


def resize_picture(url):
    img = Image.open(url)
    out = img.resize((200, 150))
    out.save(url)
