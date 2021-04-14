#!/usr/bin/python3

from bottle import route, run, template, request, abort
import rxv
import os
import time

OK = {"message":"ok"}

class Receiver(object):
    def __init__ (self, rx):
        self._rx = rx

    def on(self):
      self._rx.on = True

    def off(self):
      self._rx.on = False

    def input(self,input):
      self._rx.input = input

    def fade (self, vol):
      self._rx.volume_fade(vol,2)

    def menu_status (self):
      return self._rx.menu_status()

    def serverstream(self, path):
        self._rx.server(path)

    @property
    def volume (self):
      return self._rx.volume

    @volume.setter
    def volume (self, vol):
      self._rx.volume = vol

rx = Receiver(rxv.RXV(os.environ["RX600"]))
KEY = os.environ["KEY"]

def checkKey (fn):
    def _wrapper (*args, **kwargs):
        key = request.query.key
        if key != KEY:
            abort(401, "Sorry, access denied.")
        else:
            return fn(*args, **kwargs)
    return _wrapper

@route('/on')
@checkKey
def on():
    rx.on()
    return OK

@route('/off')
@checkKey
def off():
    rx.off()
    return OK

@route('/srv/<volume>/<menupath>')
@checkKey
def onWithServerPath(volume,menupath):
    # menupath must be aka: "Fritz7590>Internetradio>Rock-Antenne>Rock-Antenne%20Stream"
    rx.on()
    time.sleep(2)
    rx.volume = -70
    rx.serverstream(menupath)
    time.sleep(5) # receiver needs at least 5 secs for next commands
    rx.fade(int(volume))
    return OK

@route('/on/<input>/<volume>')
@checkKey
def onWithVolume(input, volume):
    rx.on()
    rx.input(input)
    time.sleep(2)
    rx.volume = int(volume)
    return OK

@route('/off/<volume>')
@checkKey
def offWithVolume(volume):
    rx.fade(int(volume))
    rx.off()
    return OK

@route('/volumeup')
@checkKey
def volumeup():
    vol = rx.volume
    rx.volume = vol + 5
    return OK

@route('/volumedown')
@checkKey
def volumedown():
    vol = rx.volume
    rx.volume = vol - 5
    return OK

@route('/volume/<volume>')
@checkKey
def volume(volume):
    rx.volume = int(volume)
    return OK

run(host='0.0.0.0', port=8080, reloader=True)
