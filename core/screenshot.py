# -*- coding: utf-8 -*-

import Image
from time import sleep

from django.conf import settings
from django.core.cache import cache


class NotAllowed(Exception):
    pass

class LockError(Exception):
    pass


def make_screenshot(ip):
    if not can_make_screenshot(ip):
        raise NotAllowed()
    
    number = increase_current_number()
    mozaic = Image.new("RGB", (3000, 500), '#fff')
    for y in xrange(settings.TABLE[1]):
        for x in xrange(settings.TABLE[0]):
            try:
                cell = Image.open("%s/data/%s_%s.jpg" % (settings.MEDIA_ROOT, x+1, y+1))
                mozaic.paste(cell, (x * 100, y * 100))
            except IOError:
                pass

    mozaic.save("%s/data/screenshot_%s.jpg" % (settings.MEDIA_ROOT, number))
    return number

    
def can_make_screenshot(ip):
    u"""Не чаще раза в час"""
    if cache.get('%s/screenshot/%s' % (settings.CACHE_ROOT, ip)):
        return False
        
    cache.set('%s/screenshot/%s' % (settings.CACHE_ROOT, ip), True, 60*60)
    return True


def get_current_number():
    return cache.get('%s/screenshot_number' % settings.CACHE_ROOT) or 1


def increase_current_number():
    for _ in xrange(3):
        if cache.add('%s/screenshot_number_lock' % settings.CACHE_ROOT, True, 2):
            break
        sleep(0.2)
    else:
        raise LockError('Cannot acquire lock')
    
    number = get_current_number() + 1
    if number > 100:
        number = 1
    
    cache.set('%s/screenshot_number' % settings.CACHE_ROOT, number)
    cache.delete('%s/screenshot_number_lock' % settings.CACHE_ROOT)
    
    return number