class PrinterStatus:
    """ The Printer Status
    """
    IDLE, PRINT, BUSY, UPDATE = range(4)


class ResponseCode:
    """ The Current Response Code
    """
    (RET_OK, RET_HOLD, E_NOT_INITIALIZE, E_NOT_FOUND,
    E_CONNECT, E_MAKE_SOCKET, E_SND_TIMEOUT, E_RCV_TIMEOUT,
    E_RCV_FRAME, E_MEMORY, E_FILM_EMPTY, E_BATTERY_EMPTY,
    E_CAM_POINT, E_MOTOR, E_IMAGE_SIZE_OVER, E_NOT_IMAGE_DATA,
    E_OTHER_USED, E_PRINTING, E_COVER_OPEN, E_EJECTING,
    E_TESTING, E_PI_SENSOR, E_INVALID_PASS, E_UNMATCH_PASS,
    E_CHARGE, E_NOT_SUPPORTED, E_NOT_FIRMWARE_DATA,
    E_FWUPDATE_FAIL, E_FWUPDATING) = range(29)


class Response:

    def __init__(self, replyBytes, payload, responseCode=ResponseCode.RET_OK, status=PrinterStatus.IDLE):
        self.replyBytes = replyBytes
        self.responseCode = responseCode
        self.status = status
        self.payload = payload

        pass

    def dump(self):
        print('response : ', self.responseCode)
        print('status : ', self.status)
        for key in self.payload:
            print(key , ':', self.payload[key])
