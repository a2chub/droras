#!/usr/bin/env python
# -*- coding: utf-8 -*-


from gpiozero import LED
from time import sleep

from datetime import datetime
from random import randint
import pygame


#define the 4 GPIO lines we want to use
four=LED(26)
pygame.init()

def led_on():
    #turn relay J2 on
    four.on()

def led_off():
    #turn relay J2 off
    four.off()

LAST_PLAY = datetime.now()
PLAY_DUR = 2.0
PLAY_FLG = True

def isPlayable():
  global LAST_PLAY, PLAY_FLG
  _cur_time = datetime.now()
  _diff = _cur_time - LAST_PLAY
  print("diff_time", _diff.microseconds /100000.0)
  if _diff.microseconds/10000.0 > PLAY_DUR:
    LAST_PLAY = _cur_time
    print('duration is %s'%(_diff.microseconds / 100000))
    return True
  else:
    print("no playable : False")
    return False

def start_sound():
  global PLAY_FLG
  #if isPlayable() and PLAY_FLG:
  if True:
    PLAY_FLG = False
    #GPIO.output(27,  0)
    led_on()
    random_start = pygame.mixer.Sound("snd/pipipi.wav")
    random_start.play()
    dur_time = float(randint(30, 50))/10.0
    sleep( dur_time )
    print(dur_time)
    start_signal()
  else:
    print("Need more duration")

def start_signal():
  start_alert = pygame.mixer.Sound("snd/po-n.wav")
  start_alert.play()
  sleep(1.0)
  #GPIO.output(27,  1)
  led_off()


if __name__ == "__main__":
  start_sound()
