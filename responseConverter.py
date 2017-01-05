
responseDict = {
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

facebookValues = {
    'confirm_logout' : 0,
    'is_cropped' : 1,
    'logout_text' : 2,
    'tooltip_mode' : 3,
    'aux_view' : 4
}


# Command Specific functions
def printByteArray( byteArray):
    hexString = ''.join('%02x'%i for i in byteArray)
    return(' '.join(hexString[i:i+4] for i in range(0, len(hexString), 4)))


def convertPayload(byteArray):
    startBit = (byteArray[0] & 0xFF)
    cmdBit = (byteArray[1] &0xFF)
    packetLength = ((byteArray[2] &0xFF) << 8 | (byteArray[3] &0xFF) << 0)
    time = ((byteArray[4] &0xFF) << 24 | (byteArray[5] &0xFF) << 16 | (byteArray[6] &0xFF) << 8 | (byteArray[7] &0xFF) << 0)
    mystBit2 =  (byteArray[12] &0xFF)
    print('Start Bit (0)         : ' + str(startBit))
    print('Command Bit (1)       : ' + str(cmdBit))
    print('Packet Length (2 & 3) : ' + str(packetLength) + ' bytes')
    print('Time        (4,5,6,7) : ' + str(time))
    print('ReturnCode  (12)      : ' + str(mystBit2) + ' : ' + responseDict[mystBit2])
    print('16+ Check   : ' + str(abv16Check(byteArray)))
    print('16+ Check 2 : ' + str(abv16Check2(byteArray)))
    if(cmdBit == 192):
        command192Processor(byteArray)
    if(cmdBit == 196):
        command196Processor(byteArray)
    if(cmdBit == 79):
        command79Processor(byteArray)
    if(cmdBit == 198):
        command198Processor(byteArray)


myByteArray = bytearray.fromhex('2ac0 0014 e759 eede 0000 0000 f700 0027 fad7 0d0a')
resp2       = bytearray.fromhex('2ac2 0018 e759 eede 0000 0000 0000 0027 5350 2d32 fac6 0d0a')
resp3       = bytearray.fromhex('2ac0 001c e759 eede 0000 0000 0000 0027 0101 0113 0000 0000 fbb0 0d0a')
resp4       = bytearray.fromhex('2ac1 0024 e759 eede 0000 0000 0000 0027 0000 0003 00f3 c048 0000 1645 001e 0000 f946 0d0a')
resp5       = bytearray.fromhex('2a4f 0030 e759 eede 0000 0000 0000 0027 0258 0320 0100 000a 0000 0000 ea60 1000 0000 0000 0000 0000 0000 0000 fa41 0d0a')

print("Converting Payload: " + printByteArray(myByteArray))
convertPayload(myByteArray)

print()
print("Converting Payload: " + printByteArray(resp2))
convertPayload(resp2)

print()
print("Converting Payload: " + printByteArray(resp3))
convertPayload(resp3)
print()
print("Converting Payload: " + printByteArray(resp4))
convertPayload(resp4)

print()
print("Converting Payload: " + printByteArray(resp5))
convertPayload(resp5)
