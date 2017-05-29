# coding: utf-8

from os.path import walk, join, splitext
import sys
from os import system
import cv2
import numpy as np
import aircv as ac
from functools import partial
from time import sleep, time
from config import adb_path

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


def common_rule(screen, templates, name, threshold=0.99):
    global ad_movie_flag, no_movie_time
    # print 'ad_movie_flag', ad_movie_flag, name
    if name in ['normal_box', 'super_box'] and not ad_movie_flag:
        if time() - no_movie_time > 600:
            print 'Reset', ad_movie_flag
            ad_movie_flag = True
        return False

    template = templates[name]

    result = ac.find_template(screen, template, threshold=threshold)
    if not result:
        return False

    print "Detected: %s, Click:%s" % (name, result['result'])
    click(result['result'])

    return True


def play_ad(screen, templates):
    if common_rule(screen, templates, 'play_ad'):
        ad_movie_flag = True
        print 'Playing ad movie for 35s'
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

    print "Unlock box, but no ad movie to play, quit"
    global ad_movie_flag, no_movie_time
    ad_movie_flag = False
    no_movie_time = time()
    click_back()
    sleep(2)


def idle_click(screen, templates):
    # click_back()
    click(next_click)


unlock_box = partial(common_rule, name='unlock_box')
normal_box = partial(common_rule, name='normal_box')
super_box = partial(common_rule, name='super_box')
fight = partial(common_rule, name='fight')
quick_fight_start = partial(common_rule, name='quick_fight_start')
ok = partial(common_rule, name='ok', threshold=0.9)
# fight_ok = partial(common_rule, name='fight_ok')
get = partial(common_rule, name='get')
collect_award = partial(common_rule, name='collect_award')

rules = [
    unlock_box, play_ad, no_play_ad, ok, normal_box, super_box, fight,
    quick_fight_start, get, collect_award, idle_click
]

if __name__ == '__main__':
    from play import load_all_templates, load_screen
    # fname = join(sys.path[0], 'r', 'quick_fight_1')
    screen = load_screen()
    # win_ok(screen, load_all_templates())
