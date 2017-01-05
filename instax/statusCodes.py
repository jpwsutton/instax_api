class PrinterStatus:
    """ The Printer Status
    """
    IDLE, PRINT, BUSY, UPDATE = range(4)

    def __init__(self, status):
        self.status = status


class ResponseCode:
    """ The Current Response Code
    """

    RET_HOLD, ST_UPDATE, E_OTHER_USED, E_NOT_IMAGE_DATA,
     E_BATTERY_EMPTY, E_PRINTING, E_EJECTING, E_TESTING,
      E_CHARGE, E_CONNECT, E_RCV_FRAME, E_FILM_EMPTY,
       E_CAM_POINT, E_MOTOR, E_UNMATCH_PASS, E_PI_SENSOR,
        E_RCV_FRAME = range(17)

    def __init__(self, status):
        self.status = status




"""
errorCodes = {
    127: 'ST_UPDATE & RET_HOLD',
    160: 'E_OTHER_USED',
    161: 'E_NOT_IMAGE_DATA',
    162: 'E_BATTERY_EMPTY',
    163: 'ST_PRINT & E_PRINTING',
    164: 'E_EJECTING',
    165: 'E_TESTING',
    180: 'E_CHARGE',
    224: 'E_CONNECT',
    240: 'E_RCV_FRAME',
    241: 'E_RCV_FRAME',
    242: 'E_RCV_FRAME',
    243: 'E_RCV_FRAME',
    244: 'E_FILM_EMPTY',
    245: 'E_CAM_POINT',
    246: 'E_MOTOR',
    247: 'E_UNMATCH_PASS',
    248: 'E_PI_SENSOR',
    0: 'E_RCV_FRAME'
}
"""
