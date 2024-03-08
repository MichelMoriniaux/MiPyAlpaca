# domeDriver: Simple Alpaca Roll Off Roof device

import uasyncio
import wlancred   # contains WLAN SSID and password
from mipyalpaca.alpacaserver import AlpacaServer
from mipyalpaca.mipyalpacaror import MiPyRoRDevice

# Asyncio coroutine
async def main():
    await AlpacaServer.startServer()


# Create Alpaca Server
srv = AlpacaServer("MyPicoServer", "MMX", "0.01", "Unknown")

# Install dome device
srv.installDevice("dome", 0, MiPyRoRDevice(0, "ESP32 RollOffRoof", "0d5cfb76-51ad-464f-841e-6451e6ba0f44","dome_config.json"))

# Connect to WLAN
AlpacaServer.connectStationMode(wlancred.ssid, wlancred.password)

# run main function via asyncio
uasyncio.run(main())

