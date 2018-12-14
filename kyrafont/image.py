#!/usr/bin/env python3

from PIL import Image
import numpy as np

def get_bg_color(row_size, f):
    BGS = [224, 192]

    def get_bg(idx):
        return BGS[f(idx) % len(BGS)]
    return get_bg

def convert_to_pil_image(frame):
    npp = np.array(frame, dtype=np.uint8)
    im = Image.fromarray(npp, mode='L')
    return im

def resize_pil_image(w, h, bg, im):
    nbase = convert_to_pil_image([[bg] * w] * h)
    nbase.paste(im, box=(0, 0))
    return nbase

def save_image_grid(filename, frames):
    w = 24
    h = 24

    im_frames = [convert_to_pil_image(frame) for frame in frames]
    
    get_bg = get_bg_color(16, lambda idx: idx + int(idx / 16))

    stack = [resize_pil_image(w, h, get_bg(idx), frame) for idx, frame in enumerate(im_frames)]

    enpp = np.array([[0] * w * 16] * h * 16, dtype=np.uint8)
    bim = Image.fromarray(enpp, mode='L')

    bim.putpalette([(133 * x % 256) for x in range(256)]*3)

    for idx, frame in enumerate(stack):
        bim.paste(frame, box=((idx % 16) * w, int(idx / 16) * h))

    bim.save(filename)
    # print(list(np.asarray(bim)))
