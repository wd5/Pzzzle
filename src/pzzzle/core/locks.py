# -*- coding: utf-8 -*-

from time import time, sleep

from django.conf import settings
from django.core.cache import cache


class NotAllowed(Exception):
    pass

class LockError(Exception):
    pass


def lock_cell(ip, x, y):
    for _ in xrange(3):
        if cache.add('%s/lock_lock' % settings.CACHE_ROOT, True, 2):
            break
        sleep(0.2)
    else:
        raise LockError('Cannot acquire lock')
        
    can_lock, reason = can_lock_cell(ip, x, y)
    
    if not can_lock:
        cache.delete('%s/lock_lock' % settings.CACHE_ROOT)
        return can_lock, reason
    
    set_cell_lock(ip, x, y)
    cache.delete('%s/lock_lock' % settings.CACHE_ROOT)
    
    return True, u"Заблокировано"    


def can_lock_cell(ip, x, y):
    if cache.get('%s/lock/%s' % (settings.CACHE_ROOT, ip)):
        return False, u"Блокировка не чаще раза в 10 секунд"

    if cache.get('%s/lock_cell/%s_%s_%s' % (settings.CACHE_ROOT, x, y, ip)):
        return False, u"Вы уже блокировали эту ячейку меньше суток назад"
    
    if cache.get('%s/lock_cell/%s_%s' % (settings.CACHE_ROOT, x, y)):
        return False, u"Ячейка уже заблокирована"
    
    return True, u"Можно"


def set_cell_lock(ip, x, y):
    cache.set('%s/lock/%s' % (settings.CACHE_ROOT, ip), True, settings.IP_LOCK_PERIOD)
    cache.set('%s/lock_cell/%s_%s_%s' % (settings.CACHE_ROOT, x, y, ip), True, settings.IP_CELL_LOCK_PERIOD)
    cache.set('%s/lock_cell/%s_%s' % (settings.CACHE_ROOT, x, y), time(), settings.CELL_LOCK_PERIOD)


def get_cells_lock():
    return [ {'x': x+1,
                'y': y+1,
                'lock': get_cell_lock(x+1, y+1),
        } for y in xrange(settings.TABLE[1]) for x in xrange(settings.TABLE[0]) ]


def get_cell_lock(x, y):
    timing = cache.get('%s/lock_cell/%s_%s' % (settings.CACHE_ROOT, x, y))
    if timing:
        return time() - timing
    else:
        return None