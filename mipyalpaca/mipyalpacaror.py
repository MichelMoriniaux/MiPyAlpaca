#
# mipyalpacaror an implementation for an ESP32 controller based Roll Off Roof
# Roll off roof is implemented with a sliding gate opener (Aleko for eg) 
# the ESP32 has 3 pins: output connected to a relay that actuates the gate (Open-stop-close-stop cycle)
# 2 inputs for the endstops


import time
from mipyalpaca.alpacadome import DomeDevice
from machine import Pin
from machine import PWM
from machine import ADC
from microdot_utemplate import render_template


# MicroPython dome device
# support easy configuration of most common dome functions for MicroPython controllers:
# - GPIO outputs
# - GPIO inputs
class MiPyRoRDevice(DomeDevice):
    
    def __init__(self, devnr, devname, uniqueid, config_file):
        super().__init__(devnr, devname, uniqueid, config_file)       
        self.description = "MicroPython Alpaca dome device"
        self.swpin = []
        self.state = 0  # state of the next button push 0: open, 1: stop, 2:close, 3:stop
        self.closed = 0
        self.open = 0
        self.action = 0
        self.closedstate = 0
        self.openstate = 0

        # configure all MicroPython pins
        for i in range(self.maxswitch):
            sw = self.domedescr[i]
            
            if sw["swfct"] == "MiPyPin":
                cfg = sw["pincfg"]
                pnr = int(cfg["pin"])
                
                if cfg["pinfct"] == "OUTP":
                    # output pin
                    p = Pin(pnr, Pin.OUT)
                    if cfg["initval"] != None:
                        # set initial value
                        self.switchValue[i] = int(cfg["initval"])
                        p.init(value=int(cfg["initval"]))
                        p.value(int(cfg["initval"]))
                    self.swpin.insert(i, p)
                    if sw["name"] == "Action":
                        self.action = i

                    
                if cfg["pinfct"] == "INP":
                    # input pin
                    p = Pin(pnr, Pin.IN)
                    # setup pullup 
                    if cfg["pull"] == "PULL_UP":
                        p.init(pull=Pin.PULL_UP)
                    if cfg["pull"] == "PULL_DOWN":
                        p.init(pull=Pin.PULL_DOWN)
                    self.switchValue[i] = int(p.value())
                    self.swpin.insert(i, p)
                    if sw["name"] == "Closed":
                        self.closed = i
                        self.closedstate = self.switchValue[i]
                        p.irq(handler=self.ClosedTriggered, trigger=Pin.IRQ_FALLING || Pin.IRQ_RISING , hard=False)
                    if sw["name"] == "Open":
                        self.open = i
                        self.openstate = self.switchValue[i]
                        p.irq(handler=self.OpenTriggered, trigger=Pin.IRQ_FALLING || Pin.IRQ_RISING , hard=False)
                    
                if cfg["pinfct"] == "PWM":
                    # PWM pin
                    p = PWM(Pin(pnr))
                    p.freq(int(cfg["freq"]))
                    if cfg["initval"] != None:
                        # set initial value
                        self.domeValue[i] = int(cfg["initval"])
                        p.duty_u16(int(cfg["initval"]))                   
                    self.swpin.insert(i, p)
                    
                if cfg["pinfct"] == "ADC":
                    # ADC pin
                    p = ADC(Pin(pnr))
                    self.swpin.insert(i, p)
            else:
                self.swpin.insert(i, "UserDef")
        # we now need to figure out the state of the shutter and if unknown bring it to a known state
        # we assume that we want the shutter to close if the state is unknown
        if self.swpin[self.open].value() == self.swpin[self.closed].value():
            # Shutter is in undertermined state in between the endstops
            self.syncShutter()
        elif self.swpin[self.open].value() == 1:
            self.ShutterStatus = 0
            self.state = 2
        elif self.swpin[self.closed].value() == 1:
            self.ShutterStatus = 1
            self.state = 0


    def OpenTriggered(self):
        # Trigger has happened, determine if the switch was activated or de-activated
        # activated first
        if self.swpin[self.open].value() == 1:
            self.ShutterStatus = 0
            self.state = 2
            self.Slewing = False
        elif self.swpin[self.open].value() == 0:
            self.ShutterStatus = 3
            self.state = 3
            self.Slewing = True
        # here might be interesting to add logic to bring back the shutter in place in case the move was not commanded ( wind or manual)
    
    
    def ClosedTriggered(self):
        # Trigger has happened, determine if the switch was activated or de-activated
        # activated first
        if self.swpin[self.closed].value() == 1:
            self.ShutterStatus = 1
            self.state = 0
            self.Slewing = False
        elif self.swpin[self.closed].value() == 0:
            self.ShutterStatus = 2
            self.state = 1
            self.Slewing = True
        # here might be interesting to add logic to bring back the shutter in place in case the move was not commanded ( wind or manual)


    def pulseButton(self):
        self.swpin[self.action].on()
        time.sleep_ms(500)
        self.swpin[self.action].off()
        self.state += 1
        if self.state > 3:
            self.state = 0

    
    def syncShutter(self):
        self.pulseButton()
        self.Slewing = True


    def abortslew(self):
        super().abortslew()
        if self.Slewing:
            self.pulseButton()
        return
    

    def closeshutter(self):
        super().closeshutter()
        if self.ShutterStatus == 0:
            self.pulseButton()
            self.Slewing = True
            self.Slaved = False
            self.ShutterStatus == 3
        return
    

    def openshutter(self):
        super().openshutter()
        if self.ShutterStatus == 1:
            self.pulseButton()
            self.Slewing = True
            self.ShutterStatus == 2
        return
    

    # return setup page
    def setupRequest(self, request):
        return render_template('setupswitch0.html', devname=self.name, cfgfile=self.configfile)
