# simple web control panel
# combines multi core (_threads) and multi tasking (uasyncio)

import utime
import uasyncio
import _thread
# Librerias propias
from extras.RequestParser import RequestParser
from jugador.WiFiConnection import WiFiConnection
from extras.ResponseBuilder import ResponseBuilder

if not WiFiConnection.start_station_mode(True):
    raise R