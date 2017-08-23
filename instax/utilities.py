class Utilities:

    def __init__(self):
        pass

    def getFourByteInt(self, offset, byteArray):
        if(len(byteArray) < (offset + 4)):
            return 0
        else:
            return (((byteArray[offset] & 0xFF) << 24) | (
                    (byteArray[(offset) + 1] & 0xFF) << 16) | (
                    (byteArray[(offset) + 2] & 0xFF) << 8) | (
                    (byteArray[(offset) + 3] & 0xFF) << 0))

    def encodeFourByteInt(self, numberToEncode):
        fourByteInt = bytearray()
        fourByteInt.append((numberToEncode >> 24) & 0xFF)  # B1
        fourByteInt.append((numberToEncode >> 16) & 0xFF)  # B2
        fourByteInt.append((numberToEncode >> 8) & 0xFF)  # B3
        fourByteInt.append((numberToEncode >> 0) & 0xFF)  # B4
        return fourByteInt

    def getTwoByteInt(self, offset, byteArray):
        if(len(byteArray) < (offset + 2)):
            return 0
        else:
            return (((byteArray[offset] & 0xFF) << 8) | (
                (byteArray[(offset) + 1] & 0xFF) << 0))

    def encodeTwoByteInt(self, numberToEncode):
        twoByteInt = bytearray()
        twoByteInt.append((numberToEncode >> 8) & 0xFF)  # B1
        twoByteInt.append((numberToEncode >> 0) & 0xFF)  # B2
        return twoByteInt

    def getOneByteInt(self, offset, byteArray):
        if(len(byteArray) < (offset + 1)):
            return 0
        else:
            return (byteArray[offset] & 0xFF)

    def encodeOneByteInt(self, numberToEncode):
        oneByteInt = bytearray()
        oneByteInt.append((numberToEncode >> 0) & 0xFF)
        return oneByteInt

    def getEjecting(self, offset, byteArray):
        if(len(byteArray) < (offset + 1)):
            return 0
        else:
            return ((byteArray[offset] >> 2) & 0xFF)

    def encodeEjecting(self, eject):
        ejectState = bytearray()
        ejectState.append((eject >> 2) & 0xFF)
        return ejectState

    def getBatteryLevel(self, byteArray):
        if(len(byteArray) < 16):
            return -1
        else:
            return ((byteArray[15] >> 4) & 7)

    def getPrintCount(self, byteArray):
        if(len(byteArray) < 16):
            return -1
        else:
            return ((byteArray[15] >> 0) & 15)

    def encodeBatteryAndPrintCount(self, battery, printCount):
        oneByteInt = bytearray()
        oneByteInt.append((battery << 4) | printCount << 0)
        return oneByteInt

    def printByteArray(self, byteArray):
        hexstr = ''.join('%02x' % i for i in byteArray)
        return(' '.join(hexstr[i:i + 2] for i in range(0, len(hexstr), 2)))

    def abv16Check(self, byteArray):
        if(len(byteArray) > 16):
            return((byteArray[15] >> 7) & 1)
        else:
            return 0

    def abv16Check2(self, byteArray):
        if(len(byteArray) > 16):
            return((byteArray[15] >> 4) & 1)
        else:
            return 0

    def formatVersionNumber(self, version):
        part2 = version & 0xFF
        part1 = ((65280 & version) >> 8)
        return('%s.%s' % ("%0.2X" % part1, "%0.2X" % part2))

    def encodeModelString(self, model):
        # TODO - Work out how to encode the Model String
        return bytearray.fromhex('5350 2d32')

    def getPrinterModelString(self, byteArray):
        modelString = ''
        modelStringLength = len(byteArray) - 20
        if(modelStringLength < 1):
            return ''
        index = 0
        while(index < modelStringLength):
            modelString += chr(byteArray[index])
            index += 1

        return modelString

    def getPayloadBytes(self, offset, length, byteArray):
        return byteArray[offset:offset + length + 1]
