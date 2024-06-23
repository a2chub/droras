#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
from datetime import datetime
from random import randint
from time import sleep

import pygame
from gpiozero import LED

logger = logging.getLogger(__name__)

# define the 4 GPIO lines we want to use
four = LED(26)
pygame.init()
pygame.mixer.init()

def led_on():
    # turn relay J2 on
    four.on()
    logger.info("LED on")


def led_off():
    # turn relay J2 off
    four.off()
    logger.info("LED off")


LAST_PLAY = datetime.now()
PLAY_DUR = 2.0
PLAY_FLG = True


def isPlayable():
    global LAST_PLAY, PLAY_FLG
    _cur_time = datetime.now()
    _diff = _cur_time - LAST_PLAY
    logger.debug("diff_time: %s", _diff.microseconds / 100000.0)
    if _diff.microseconds / 10000.0 > PLAY_DUR:
        LAST_PLAY = _cur_time
        logger.info("duration is %s", _diff.microseconds / 100000)
        return True
    else:
        logger.info("no playable: False")
        return False


def start_sound():
    global PLAY_FLG
    # if isPlayable() and PLAY_FLG:
    if True:
        PLAY_FLG = False
        # GPIO.output(27,  0)
        led_on()
        _snd_pipipi = get_resource_path("sound", "pipipi.wav")
        print(_snd_pipipi)
        random_start = pygame.mixer.Sound(_snd_pipipi)
        random_start.play()
        dur_time = float(randint(30, 50)) / 10.0
        sleep(dur_time)
        logger.info("Sound played for %s seconds", dur_time)
        start_signal()
    else:
        logger.warning("Need more duration")


def start_signal():
    _snd_pon = get_resource_path("sound", "po-n.wav")
    print(_snd_pon)
    start_alert = pygame.mixer.Sound(_snd_pon)
    start_alert.play()
    sleep(0.35)
    # GPIO.output(27,  1)
    led_off()

def get_resource_path(resoure="", file_name=""):
    base_path = os.path.dirname(os.path.abspath(__file__))
    resoure_path = os.path.join(base_path, "..", "..", resoure, file_name)
    return resoure_path

if __name__ == "__main__":
    start_sound()
