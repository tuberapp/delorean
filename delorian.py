#!/usr/bin/env python

import time
import pyupm_i2clcd
import pyupm_grove
import pyupm_buzzer

import requests as r
import collections

base_url = 'http://tuberapp.azurewebsites.net/hack/'
R_BUTTON = 0
L_BUTTON = 1


chords = [pyupm_buzzer.DO, pyupm_buzzer.RE, pyupm_buzzer.MI, pyupm_buzzer.FA, 
          pyupm_buzzer.SOL, pyupm_buzzer.LA, pyupm_buzzer.SI, pyupm_buzzer.DO,
          pyupm_buzzer.SI];


class LCD(pyupm_i2clcd.Jhd1313m1):
    def __init__(self):
        pyupm_i2clcd.Jhd1313m1.__init__(self, 0, 0x3e, 0x62)
        self.setCursor(0,0)

    def button_label(self,b1,b2):
        self.setCursor(1,0)
        self.write(16*' ')
        self.setCursor(1,0)
        self.write(b1[:8])
        self.setCursor(1,8)
        self.write(b2[:8])

class Button(pyupm_grove.GroveButton):
    def __init__(self,pin):
        pyupm_grove.GroveButton.__init__(self,pin)

def unicode_dict_str(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(unicode_dict_str, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(unicode_dict_str, data))
    else:
        return data

def req_ride():
    while True:
        req = r.get(base_url+'/rideavailable')
        req_json = req.json()
        if(req_json['result']):
            req_json = unicode_dict_str(req_json)
            return req_json
        time.sleep(0.1)
    
def look_for_ride(lcd):
    lcd.clear()
    lcd.setCursor(0,0)
    lcd.write('Pimp My Delorian')
    lcd.setCursor(1,0)
    lcd.write('Searching time..')
    #ride = {'city': 'Seattle', 'name': 'surya', 'state': 'WA', 'weather': '48', 'result': True, 'address': 'example', 'date': '20120101'}
    return req_ride()

def get_button(lbutton, rbutton):
    while True:
        if lbutton.value():
            button = L_BUTTON
            break
        if rbutton.value():
            button = R_BUTTON
            break
    time.sleep(0.5)
    return button

def show_ride(buttons,lcd,ride):
    lcd.clear()
    lcd.setCursor(0,0)
    print ride
    lcd.write('Ride for %s'%ride['name'])
    lcd.button_label('accept', 'decline')

def show_accept_ride(lcd,ride):
    lcd.clear()
    lcd.setCursor(0,0)
    lcd.write('Going to %s'%ride['name'])
    lcd.setCursor(1,0)
    lcd.write('End Ride')

def main():
    lcd = LCD()
    lbutton = Button(2)
    rbutton = Button(3)
    buzzer = pyupm_buzzer.Buzzer(5)
    buzzer.playSound(0,200000)

    lcd.setColor(255,0,0)
    while True:
        try:
            ride = look_for_ride(lcd)
            buzzer.playSound(chords[0],200000)
            buzzer.playSound(0,200000)
            show_ride((lbutton,rbutton),lcd,ride)
            button = get_button(lbutton, rbutton)
            if button == L_BUTTON:
                #They Clicked Accept
                show_accept_ride(lcd,ride)
                while True:
                    button = get_button(lbutton, rbutton)
                    if button == L_BUTTON:
                        #Trip Endded
                        break
            else:
                #They Click Decline
                continue
            show_ride(lcd,{})
        except:
            pass

if __name__ == '__main__':
    main()
