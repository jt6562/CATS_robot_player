#!/usr/bin/env python
# coding: utf-8

from os.path import walk, join, splitext
import sys
from os import system, remove
import cv2
from rules import run_rules
from config import adb_path
import logging
from subprocess import call
from time import sleep
from tempfile import mktemp
import atexit

temp_screencap = mktemp('.png')

logger = logging.getLogger('main')
logger.info("Output screen capture temporary %s" % temp_screencap)


def remove_tempfile():
    remove(temp_screencap)


atexit.register(remove_tempfile)


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
    # cmd = [adb_path, 'shell', 'screencap', '-p', '/sdcard/' + output]
    # call(cmd, stdout=None)
    # cmd = [adb_path, 'pull', '/sdcard/' + output, '.']
    # call(cmd, stdout=None)
    # cmd = [adb_path, 'shell', 'rm', '/sdcard/' + output]
    # call(cmd)

    cmd = [adb_path, 'shell', 'screencap', '-p', '>', temp_screencap]
    print ' '.join(cmd)
    system(' '.join(cmd))
    img_rgb = cv2.imread(temp_screencap)
    # img_rgb = cv2.imread(join(sys.path[0], temp_screencap))
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
