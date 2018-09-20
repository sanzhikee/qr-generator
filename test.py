from threading import *
import time
from PIL import Image
import draw_qr
import numpy as np
from math import sqrt

def job_1():
    print(time.time())

    qr = draw_qr.create_qr('https://pillow.readthedocs.io/en/3.1.x/reference/Image.html',
                           gradient_pos=(0.3, 0.3), from_hex_color='#144a10', to_hex_color='#001a00')

    qr_filename = 'qr_images/test_job.jpg'
    qr.save(qr_filename, 'JPEG')

    print(time.time())


def array_method():
    print(time.time())

    qr_filename = 'qr_images/black.jpg'
    test_filename = 'qr_images/test_array.jpg'
    qr = Image.open(qr_filename)

    black_qr_array = np.array(qr)

    print(black_qr_array.shape, black_qr_array.shape[0])

    rgb_qr_array = np.zeros((black_qr_array.shape[0], black_qr_array.shape[1], 3), 'uint8')+255

    print(rgb_qr_array.shape, rgb_qr_array.shape[0])

    pos_x = int(black_qr_array.shape[0] * 0.3)
    pos_y = int(black_qr_array.shape[1] * 0.3)

    from_color = (20, 70, 10)
    to_color = (0, 20, 0)

    for x in range(black_qr_array.shape[0]):
        for y in range(black_qr_array.shape[1]):
            # Find the distance to the center
            distanceToCenter = sqrt((x - pos_x) ** 2 + (y - pos_y) ** 2)

            # Make it on a scale from 0 to 1
            distanceToCenter = float(distanceToCenter) / 750

            # Calculate r, g, and b values
            r = from_color[0] * max(0, 1 - distanceToCenter) + to_color[0] * min(1, distanceToCenter)
            g = from_color[1] * max(0, 1 - distanceToCenter) + to_color[1] * min(1, distanceToCenter)
            b = from_color[2] * max(0, 1 - distanceToCenter) + to_color[2] * min(1, distanceToCenter)

            grey = black_qr_array[x][y]

            r = min(255, r+grey)
            g = min(255, g+grey)
            b = min(255, b+grey)

            # Place the pixel
            rgb_qr_array[x][y] = (int(r), int(g), int(b))

    test_img = Image.fromarray(rgb_qr_array)
    test_img.save(test_filename)

    print(time.time())


array_method()

print('-----------------------------------')

job = Timer(0, job_1)
job.start()
