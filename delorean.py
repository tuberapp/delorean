#!/usr/bin/env python

import time
import json
import pyupm_i2clcd
import pyupm_grove
import pyupm_buzzer

import requests as r
import collections

base_url = 'http://tuberapp.azurewebsites.net/hack/'
R_BUTTON = 0
L_BUTTON = 1
N_BUTTON = 3

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

class TimeSelector(pyupm_grove.GroveRotary):
    def __init__(self):
        pyupm_grove.GroveRotary.__init__(self,0)

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

def send_status(year,loc={}):
    data = {'date':str(year),'lat':'','long':''}
    print data
    headers = {'content-type': 'application/json'}
    req = r.post(base_url+'/setdriverlocation', data=json.dumps(data), headers=headers)
    print req.status_code

def look_for_ride(lcd):
    lcd.clear()
    lcd.setCursor(0,0)
    lcd.write('Pimp My Delorian')
    lcd.setCursor(1,0)
    lcd.write('Searching time..')
    #ride = {'city': 'Seattle', 'name': 'surya', 'state': 'WA', 'weather': '48', 'result': True, 'address': 'example', 'date': '20120101'}
    return req_ride()

def get_button(lbutton, rbutton, timeout=0):
    time_running = 0
    button = N_BUTTON
    while time_running <= timeout:
        if lbutton.value():
            button = L_BUTTON
            break
        if rbutton.value():
            button = R_BUTTON
            break
        time.sleep(0.1)
        if timeout:
            time_running += 0.1
    return button
def scroll_msg(lcd,msg):
    lcd.clear()
    lcd.setCursor(0,0)
    lcd.write(msg[0])
    lcd.setCursor(1,0)
    lcd.write(msg[1])
    time.sleep(2)
    msg[0] = msg[0][:32]
    msg[1] = msg[1][:32]
    for i in range(0,max(len(msg[0]),len(msg[1]))):
        lcd.scroll(True)
        time.sleep(0.3)
def show_ride(buttons,lcd,ride):
    s1 = "Ride for %s"%ride['name']
    s2 = "Location: %s, %s, %s."%(ride['address'],ride['city'],ride['state'])
    scroll_msg(lcd,[s1,s2])
    time.sleep(0.5)
    s1 = "Date: %s"%ride['date']
    s2 = "Weather: %s deg"%ride['weather']
    scroll_msg(lcd,[s1,s2])
    time.sleep(0.5)
    lcd.clear()
    lcd.setCursor(0,0)
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
    timesel = TimeSelector()
    buzzer = pyupm_buzzer.Buzzer(5)
    buzzer.playSound(0,200000)

    lcd.setColor(255,0,0)
    while True:
        try:
            ride = look_for_ride(lcd)
            print ride
            buzzer.playSound(chords[0],200000)
            buzzer.playSound(0,200000)
            button = N_BUTTON
            show_ride((lbutton,rbutton),lcd,ride)
            while button == N_BUTTON:
                button = get_button(lbutton, rbutton,0.2)
            time.sleep(0.5)
            if button == L_BUTTON:
                #They Clicked Accept
                show_accept_ride(lcd,ride)
                while True:
                    year = 2015 - int(timesel.abs_deg()/5)
                    print year
                    send_status(year)
                    button = get_button(lbutton, rbutton, timeout=1)
                    if button == L_BUTTON:
                        #Trip Endded
                        break
            else:
                #They Click Decline
                continue
        except:
            pass
if __name__ == '__main__':
    main()
