import qrcode
import time
from PIL import Image
from math import sqrt, ceil
from colormap.colors import hex2rgb


def create_qr(data, gradient_pos=(0.5, 0.5), from_hex_color='#000000', to_hex_color='#000000'):
    qr = qrcode.QRCode(version=7, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    return make_image(qr.modules, gradient_pos=gradient_pos, from_color=hex2rgb(from_hex_color), to_color=hex2rgb(to_hex_color))


def luminance(pixel):
    return (0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2])


def is_similar(pixel_a, pixel_b, threshold):
    return abs(luminance(pixel_a) - luminance(pixel_b)) < threshold


def normalize(img, to_color, threshold = 18):
    width, height = img.size
    pixels = img.load()

    for x in range(width):
        for y in range(height):
            if is_similar(pixels[x, y], to_color, threshold):
                pixels[x, y] = to_color

    return img


def gradient(img, from_x, from_y, power, from_color, to_color):

    grd = Image.new('RGB', img.size, (255, 255, 255))

    for y in range(img.size[1]):
        for x in range(img.size[0]):
            # Find the distance to the center
            distanceToCenter = sqrt((x - from_x) ** 2 + (y - from_y) ** 2)

            # Make it on a scale from 0 to 1
            distanceToCenter = float(distanceToCenter) / power

            # Calculate r, g, and b values
            r = from_color[0] * max(0, 1 - distanceToCenter) + to_color[0] * min(1, distanceToCenter)
            g = from_color[1] * max(0, 1 - distanceToCenter) + to_color[1] * min(1, distanceToCenter)
            b = from_color[2] * max(0, 1 - distanceToCenter) + to_color[2] * min(1, distanceToCenter)

            grey = img.getpixel((x, y))

            r += grey
            g += grey
            b += grey

            # Place the pixel
            grd.putpixel((x, y), (int(r), int(g), int(b)))

    return grd


def solid(img, color):

    grd = Image.new('RGB', img.size, (255, 255, 255))

    for y in range(img.size[1]):
        for x in range(img.size[0]):

            c = img.getpixel((x, y))

            r = color[0] + c
            g = color[1] + c
            b = color[2] + c

            # Place the pixel
            grd.putpixel((x, y), (int(r), int(g), int(b)))

    return grd


def make_image(modules, from_color, to_color, gradient_pos=(0.5, 0.5),
               logo='/var/www/qr/pic/logo_black.tif', logo_radius_modules=7):

    modules_count = len(modules)
    box_size = 10
    qr_size = modules_count*box_size

    logo_x = ceil(modules_count * 0.5)
    logo_y = ceil(modules_count * 0.5)

    gradient_pos_x = int(qr_size * gradient_pos[0])
    gradient_pos_y = int(qr_size * gradient_pos[1])

    img = Image.new("L", (qr_size, qr_size), 255)

    im_logo = Image.open(logo)
    im_eye = Image.open('/var/www/qr/pic/eye_round.tif')

    im_dot = Image.open('/var/www/qr/pic/dot.tif')
    im_dot_square = Image.open('/var/www/qr/pic/dot_square.tif')
    im_dot_left = Image.open('/var/www/qr/pic/dot_left.tif')
    im_dot_right = Image.open('/var/www/qr/pic/dot_right.tif')
    im_dot_up = Image.open('/var/www/qr/pic/dot_up.tif')
    im_dot_down = Image.open('/var/www/qr/pic/dot_down.tif')
    im_dot_top_left = Image.open('/var/www/qr/pic/dot_top_left.tif')
    im_dot_top_right = Image.open('/var/www/qr/pic/dot_top_right.tif')
    im_dot_bot_left = Image.open('/var/www/qr/pic/dot_bot_left.tif')
    im_dot_bot_right = Image.open('/var/www/qr/pic/dot_bot_right.tif')

    img.paste(im_logo, box=(int(qr_size/2 - im_logo.size[0]/2), int(qr_size/2 - im_logo.size[1]/2)))
    img.paste(im_eye, box=(0, 0))
    img.paste(im_eye, box=(qr_size-70, 0))
    img.paste(im_eye, box=(0, qr_size - 70))

    if logo:
        for x in range(len(modules)):
            for y in range(len(modules)):

                if (x > logo_x + logo_radius_modules) and (y > logo_y + logo_radius_modules):
                    module_in_logo = (sqrt((logo_x - x) ** 2 + (logo_y - y) ** 2) - logo_radius_modules) < 0
                else:
                    module_in_logo = (sqrt((logo_x - x-1) ** 2 + (logo_y - y-1) ** 2) - logo_radius_modules) < 0

                if module_in_logo:
                    modules[x][y] = False

    for x in range(len(modules)):
        for y in range(len(modules)):

            module_in_eye = (x <= 7 and y <= 7) or (x <= 7 and y >= modules_count-7) or (x >= modules_count-7 and y <= 7)

            if logo is None:
                module_in_logo = False
            else:
                if (x > logo_x + logo_radius_modules) and (y > logo_y + logo_radius_modules):
                    module_in_logo = (sqrt((logo_x - x) ** 2 + (logo_y - y) ** 2) - logo_radius_modules) < 0
                else:
                    module_in_logo = (sqrt((logo_x - x-1) ** 2 + (logo_y - y-1) ** 2) - logo_radius_modules) < 0

            if (module_in_eye or (modules[y][x] is False) or module_in_logo) is False:

                if y == 0:
                    up = False
                else:
                    up = modules[y-1][x]

                if x == modules_count-1:
                    right = False
                else:
                    right = modules[y][x+1]

                if y == modules_count-1:
                    down = False
                else:
                    down = modules[y + 1][x]

                if x == 0:
                    left = False
                else:
                    left = modules[y][x-1]

                neighbors_count = up + right + down + left

                if neighbors_count == 0:
                    img.paste(im_dot, box=(x*box_size, y*box_size))

                if neighbors_count == 1:
                    if up:
                        img.paste(im_dot_down, box=(x*box_size, y*box_size))

                    if right:
                        img.paste(im_dot_left, box=(x*box_size, y*box_size))

                    if down:
                        img.paste(im_dot_up , box=(x*box_size, y*box_size))

                    if left:
                        img.paste(im_dot_right, box=(x*box_size, y*box_size))

                if neighbors_count == 2:
                    if down and right:
                        img.paste(im_dot_top_left, box=(x*box_size, y*box_size))
                    elif down and left:
                        img.paste(im_dot_top_right, box=(x*box_size, y*box_size))
                    elif up and right:
                        img.paste(im_dot_bot_left, box=(x*box_size, y*box_size))
                    elif up and left:
                        img.paste(im_dot_bot_right, box=(x*box_size, y*box_size))
                    else:
                        img.paste(im_dot_square, box=(x * box_size, y * box_size))

                if neighbors_count > 2:
                    img.paste(im_dot_square, box=(x * box_size, y * box_size))

    """ 
    im_logo = Image.open(logo)
    print(im_logo.size)
    coef = (logo_radius_modules*1.8*box_size)/sqrt(im_logo.size[0]**2 + im_logo.size[1]**2)
    print(coef)
    logo_size = (int(im_logo.size[0]*coef), int(im_logo.size[1]*coef))
    print(logo_size)
    im_logo = im_logo.resize(logo_size, Image.BOX)
    img.paste(im_logo, box=(int(qr_size/2 - logo_size[0]/2), int(qr_size/2 - logo_size[1]/2)))
    """

    if not(from_color == (0, 0, 0) and to_color == (0, 0, 0)):
        img = gradient(img, gradient_pos_x, gradient_pos_y, 750, from_color, to_color)
    elif (from_color == to_color) and from_color != (0, 0, 0):
        solid(img, from_color)

    return img


