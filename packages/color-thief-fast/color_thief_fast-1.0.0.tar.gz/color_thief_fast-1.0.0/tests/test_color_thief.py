# -*- coding:utf8 -*-
import time
from lazy_loader import load
from PIL import Image
from colorthief import ColorThief

# image_path = "00007-1829545141.png"
image_path = "files/3d-1-512-512-1.png"

# image = Image.open(image_path)
color_thief = ColorThief(image_path)
t0 = time.time()
result = color_thief.get_palette(quality=1)
print(result)
print(f"耗时:{time.time() - t0}")
