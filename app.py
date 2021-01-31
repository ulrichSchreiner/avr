#!/usr/bin/python

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
      self._rx.volume_fade(vol)

    def menu_status (self):
      return self._rx.menu_status()

    def serverstream(self, source, path):
        layers = path.split(">")
        self.input(source)

        for i in range(10):
            menu = self.wait_for_menu()
            for line, value in menu.current_list.items():
                if menu.layer > len(layers):
                    # now click the "... stream" menu item
                    self._rx.menu_jump_line(1)
                    self._rx.menu_sel()
                    return
                if value == layers[menu.layer - 1]:
                    lineno = line[5:]
                    self._rx.menu_jump_line(lineno)
                    self._rx.menu_sel()
                    break

    def wait_for_menu (self):
        for attempts in range (20):
            menu = self.menu_status()
            if menu.ready:
                return menu
            else:
                time.sleep(1)

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
    # menupath must be aka: "Fritzbox>Internetradio>mystream"
    rx.on()
    time.sleep(2)
    rx.volume = -80
    rx.serverstream("SERVER", menupath)
    rx.wait_for_menu()
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
