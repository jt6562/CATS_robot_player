#!/usr/bin/env python
# coding: utf-8

from os.path import walk, join, splitext
import sys
from os import system
import cv2
from rules import run_rules, adb_path


def load_all_templates():
    templates = {}

    def load_template(arg, dirname, fnames):
        for fname in fnames:
            img_rgb = cv2.imread(join(dirname, fname))
            # img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
            templates[splitext(fname)[0]] = img_rgb

    walk(join(sys.path[0], 'templates'), load_template, None)
    return templates


def load_screen():
    output = 'tmp_screen.png'
    cmd = ' '.join([adb_path, 'shell', 'screencap', '-p', '>', output])
    system(cmd)
    img_rgb = cv2.imread(join(sys.path[0], output))
    return img_rgb


def run(templates):
    while 1:
        # Download screen capture
        screen = load_screen()

        # Go
        run_rules(screen, templates)


def main():
    templates = load_all_templates()
    run(templates)


if __name__ == '__main__':
    main()
