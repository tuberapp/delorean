import time
import pyupm_i2clcd
import pyupm_grove

R_BUTTON = 0
L_BUTTON = 1

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
def look_for_ride(lcd):
    lcd.clear()
    lcd.setCursor(0,0)
    lcd.write('Pimp My Delorian')
    lcd.setCursor(1,0)
    lcd.write('Looking for a Ride')
    while True:
        #make some requests oh look i found a ride
        time.sleep(2)
        ride = {'name':'biff','s_addr':'999 3rd ave','e_addr':'into the future','weather':'wicked cool'}
        return ride

def get_button(lbutton, rbutton):
    while True:
        if lbutton.value():
            button = L_BUTTON
            break
        if rbutton.value():
            button = R_BUTTON
            break
    time.sleep(2)
    return button

def show_ride(buttons,lcd,ride):
    lcd.clear()
    lcd.setCursor(0,0)
    lcd.write('Ride for %s'%ride['name'])
    lcd.button_label('accept', 'decline')

def show_accept_ride(lcd,ride):
    lcd.clear()
    lcd.setCursor(0,0)
    lcd.write('Got to %s'%ride['name'])
    lcd.setCursor(1,0)
    lcd.write('End Ride')

def main():
    lcd = LCD()
    lbutton = Button(2)
    rbutton = Button(3)

    lcd.setColor(255,0,0)
    while True:
        ride = look_for_ride(lcd)
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


if __name__ == '__main__':
    main()
