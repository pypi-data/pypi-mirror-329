# -*- coding:utf8 -*-
import time
from unittest import TestCase
from color_thief_fast import ColorThiefFast, MMCQ
from PIL import Image
import numpy as np


class TestMMCQ(TestCase):
    def test_get_histo(self):
        image_path = "00007-1829545141.png"
        image = Image.open(image_path)
        image = np.array(image)
        image = image.reshape(-1, 3)

        # histo1 = MMCQ.get_histo(image)
        # t0 = time.time()
        # MMCQ.vbox_from_pixels(image, histo1)
        # print(f"耗时:{time.time() - t0}")

        histo2 = MMCQ.get_histo(image)
        t0 = time.time()
        MMCQ.vbox_from_pixels(image, histo2)
        print(f"耗时:{time.time() - t0}")
        print()

    def test_get_color(self):
        # image_path = "00007-1829545141.png"
        # image_path = "1.jpg"
        # image_path = "files/2d-512-512.png"
        image_path = "files/3d-1-512-512-1.png"
        p = ColorThiefFast(image_path, True)
        t0 = time.time()
        result = p.get_palette(quality=1)
        print(result)
        print(f"耗时:{time.time() - t0}")
