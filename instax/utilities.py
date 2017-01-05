class Utilities:

    def __init__(self):
        #do Nothing
        pass

    def getFourByteInt(self, offset, byteArray):
        if(len(byteArray) < (16 + offset + 4)):
            return 0
        else:
            return (((byteArray[16+offset] & 0xFF)<< 24) | ((byteArray[(16+offset) + 1 ] & 0xFF) << 16)| ((byteArray[(16+offset) + 2 ] & 0xFF) << 8)| ((byteArray[(16+offset) + 3 ] & 0xFF) << 0))


    def getTwoByteInt(self, offset, byteArray):
        if(len(byteArray) < (16 + offset + 2)):
            return 0
        else:
            return (((byteArray[16+offset] & 0xFF)<< 8) | ((byteArray[(16+offset) + 1 ] & 0xFF) << 0))

    def getOneByteInt(self, offset, byteArray):
        if(len(byteArray) < (16 + offset + 1)):
            return 0
        else :
            return (byteArray[16 + offset] & 0xFF)

    def getOneByteIntAt15(self, byteArray):
        if(len(byteArray) < 16):
            return -1
        else:
            return ((byteArray[15] >> 4) & 7)

    def printByteArray(self, byteArray):
        hexString = ''.join('%02x'%i for i in byteArray)
        return(' '.join(hexString[i:i+4] for i in range(0, len(hexString), 4)))

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
        return('%s.%s' %("%0.2X" % part1, "%0.2X" %part2))

    def getPrinterModelString(self, byteArray):
        modelString = ''
        modelStringLength = len(byteArray) -20
        if(modelStringLength < 1):
            return ''
        index = 0
        while(index < modelStringLength):
            modelString += chr(byteArray[16 + index])
            index += 1

        return modelString
