# coding: utf-8

from os.path import walk, join, splitext
import sys
from os import system
import cv2
import numpy as np
import aircv as ac
from functools import partial
from time import sleep, time
from config import adb_path, interval_check_ad_movie
import logging

logger = logging.getLogger('rules')


# Postion
back_btn = (80, 714)
championship_fight_btn = (905, 717)
fight_btn = (680, 626)
next_click = (934, 218)

ad_movie_flag = True
no_movie_time = None


def run_rules(screen, templates):
    # screen = cv2.cvtColor(cur_screen, cv2.COLOR_BGR2GRAY)
    for rule in rules:
        if rule(screen, templates):
            break


def click(position):
    cmd = ' '.join([adb_path, 'shell', 'input', 'tap', '%d %d' % position])
    system(cmd)


def click_back():
    system(adb_path + " shell input keyevent 4")


def common_rule(screen, templates, name, threshold=0.8, target=None, wait_time=1):
    global ad_movie_flag, no_movie_time
    if name in ['normal_box', 'super_box'] and not ad_movie_flag:
        if time() - no_movie_time > interval_check_ad_movie:
            ad_movie_flag = True
            logger.info('Reset ab_movie_flag to %s' % ad_movie_flag)
        return False

    template = templates[name]

    result = ac.find_template(screen, template, threshold=threshold)
    print name, result
    if not result:
        return False

    click_position = result['result']
    if target:
        click_position = target

    logger.info("Detected: %s, Click:%s" % (name, result['result']))
    click(click_position)

    sleep(wait_time)

    return True


def play_ad(screen, templates):
    if common_rule(screen, templates, 'play_ad', threshold=0.9):
        ad_movie_flag = True
        logger.info('Playing ad movie for 35s')
        sleep(35)
        click_back()
        return True

    return False


def no_play_ad(screen, templates):
    result = ac.find_template(screen, templates['open_im'], threshold=0.9)
    if not result:
        return False

    result = ac.find_template(screen, templates['play_ad'], threshold=0.9)
    if result:
        return False

    result = ac.find_template(screen, templates['chacha'], threshold=0.9)
    if not result:
        return False

    logger.warn("Unlock box, but no ad movie to play, quit")
    global ad_movie_flag, no_movie_time
    ad_movie_flag = False
    no_movie_time = time()
    click_back()
    sleep(2)


def idle_click(screen, templates):
    # click_back()
    click(next_click)
    sleep(2)


unlock_box = partial(common_rule, name='unlock_box')
normal_box = partial(common_rule, name='normal_box', threshold=0.97)
super_box = partial(common_rule, name='super_box', threshold=0.90)
fight = partial(common_rule, name='fight', wait_time=1)
quick_fight_start = partial(common_rule, name='quick_fight_start', wait_time=12)
ok = partial(common_rule, name='ok', threshold=0.9)
# fight_ok = partial(common_rule, name='fight_ok')
get = partial(common_rule, name='get')
collect_award = partial(common_rule, name='collect_award')
championship_fight = partial(common_rule, name='championship_fight', threshold=0.99,
                             target=back_btn)

rules = [
    championship_fight, unlock_box, play_ad, no_play_ad, ok, normal_box, super_box, fight,
    quick_fight_start, get, collect_award, idle_click
]

if __name__ == '__main__':
    from play import load_all_templates, load_screen
    # fname = join(sys.path[0], 'r', 'quick_fight_1')
    screen = load_screen()
    # win_ok(screen, load_all_templates())
