import base64
import re


def base64_img(img, path):
    img_info = img.split(',')
    data = base64.b64decode(img_info[1])
    with open(path, 'wb') as f:
        f.write(data)
