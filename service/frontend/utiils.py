from PIL import Image


def logo_abb(logo, size_w, size_h):
    size_w = int(size_w)
    size_h = int(size_h)

    logo = logo.resize((size_w, size_h), Image.ANTIALIAS)

    return logo


def merge_image(bg, qr, size_w, size_h):
    # if img.mode != 'RGBA':
    #     img = img.convert('RGBA')

    layer = Image.new('RGBA', bg.size, (0, 0, 0, 0))
    layer.paste(qr, (size_w, size_h))
    im = Image.composite(layer, bg, layer)

    return im
