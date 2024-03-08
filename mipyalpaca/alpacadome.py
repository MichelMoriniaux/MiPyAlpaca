from mipyalpaca.alpacaserver import *
from mipyalpaca.alpacadevice import AlpacaDevice

# ASCOM Alpaca dome device
class DomeDevice(AlpacaDevice):
    
    def __init__(self, devnr, devname, uniqueid, config_file):
        super().__init__(devnr, devname, uniqueid)
        self.interfaceVersion = 2   # this implementation supports dome interface version 2
        self.maxswitch = 0  # number of switches for the dome
        self.domedescr = []  # dome configuration
        self.switchValue = []  # current dome control values ( command pins, endstops, etc)
        self.driverinfo = "MicroPython ASCOM Alpaca Dome Driver" # dome driver MiPy
        self.driverVersion = "v0.01"   # driver version
        self.configfile = config_file  # name of JSON file with dome config
        self.ShutterStatus = 1  # the state of the shutter: 0: Open, 1: closed, 2: opening, 3: Closing, 4: Error
        self.Slewing = False
        self.Slaved = False
        self.AtPark = None
        self.AtHome = None
        self.Altitude = None
        self.Azimuth = None
        self.CanFindHome = False
        self.CanPark = False
        self.CanSetAltitude = False
        self.CanSetAzimuth = False
        self.CanSetPark = False
        self.CanSetShutter = True
        self.CanSlave = False
        self.CanSyncAzimuth = False

        self.domedescr = readJson(self.configfile)  # load dome configuration
        self.maxswitch = len(self.domedescr)        # get number of domees
        # create initial list of dome values
        for i in range(self.maxswitch):
            self.switchValue.append(0)               


    def abortslew(self):
        if self.Slewing:
            self.Slewing = False
            self.Slaved = False

    
    def PUT_abortslew(self, request):
        return self.reply(request, self.abortslew())
    

    def closeshutter(self):
        return


    def PUT_closeshutter(self, request):
        return self.reply(request, self.closeshutter())
    

    def PUT_findhome(self, request):
        raise NotImplementedError()
    

    def openshutter(self):
        return


    def PUT_openshutter(self, request):
        return self.reply(request, self.openshutter())
    

    def PUT_park(self, request):
        raise NotImplementedError()
    

    def PUT_setpark(self, request):
        raise NotImplementedError()
    

    def PUT_slewtoaltitude(self, request):
        raise NotImplementedError()
    

    def PUT_slewtoazimuth(self, request):
        raise NotImplementedError()
    

    def PUT_synctoazimuth(self, request):
        raise NotImplementedError()
    

    def GET_altitude(self, request):
        raise NotImplementedError()
    

    def GET_athome(self, request):
        raise NotImplementedError()
    

    def GET_azimuth(self, request):
        raise NotImplementedError()
    

    def GET_canfindhome(self, request):
        return self.reply(request, self.CanFindHome)
    
    
    def GET_canpark(self, request):
        return self.reply(request, self.CanPark)
    

    def GET_cansetaltitude(self, request):
        return self.reply(request, self.CanSetAltitude)
    

    def GET_cansetazimuth(self, request):
        return self.reply(request, self.CanSetAzimuth)
    

    def GET_cansetpark(self, request):
        return self.reply(request, self.CanSetPark)
    

    def GET_cansetshutter(self, request):
        return self.reply(request, self.CanSetShutter)
    

    def GET_canslave(self, request):
        return self.reply(request, self.CanSlave)
    

    def GET_cansyncazimuth(self, request):
        return self.reply(request, self.CanSyncAzimuth)
    

    def GET_shutterstatus(self, request):
        return self.reply(request, self.ShutterStatus)
    

    def GET_slaved(self, request):
        return self.reply(request, self.Slaved)
    

    def GET_slewing(self, request):
        return self.reply(request, self.Slewing)
