from math import ceil, floor

from PIL import Image


def image_fit_to(image: Image, width, height):
    img_cp = image.copy()
    img_cp.thumbnail((width, height))
    return img_cp


def image_resize(image: Image, width, height):
    img = image.copy()
    w, h = img.size
    o_ratio = w / h
    i_ratio = width / height
    o_w = w if o_ratio < i_ratio else int(round(h * i_ratio))
    o_h = int(round(w / i_ratio)) if o_ratio < i_ratio else h
    diff_w = w - o_w
    diff_h = h - o_h
    img = img.crop((ceil(diff_w / 2),
                    ceil(diff_h / 2),
                    w - floor(diff_w / 2),
                    h - floor(diff_h / 2)))

    return img.resize((width, height))
