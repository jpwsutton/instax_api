import instax
import time


def printSeparator():
    print('--------------------------------------------------')


print("Instax SP-2 Example App")
myInstax = instax.SP2()
# host = "localhost"
host = "192.168.0.251"

printSeparator()
print("Preparing Image")
# Initialize The Instax Image
instaxImage = instax.InstaxImage()
instaxImage.loadImage("test.jpg")
instaxImage.convertImage()
#instaxImage.previewImage()
instaxImage.saveImage("test.bmp")
encodedImage = instaxImage.encodeImage()
printSeparator()


myInstax.connect(ip=host)

printSeparator()

# -- Step 1, send version and model name commands.
printerVersion = myInstax.getPrinterVersion()
printerVersion.printDebug()
printerModel = myInstax.getPrinterModelName()
printerModel.printDebug()
myInstax.close()


# -- Step 2, send pre-print commands.
myInstax.connect(ip=host)
for x in range(1, 9):
    prePrintCmd = myInstax.sendPrePrintCommand(x)
    print("PrePrint - C: %s, R: %s" % (x, prePrintCmd.respNumber))
myInstax.close()

# -- Step 3, Model Name, Version, Print Count, Specs Commands
myInstax.connect(ip=host)
printerVersion = myInstax.getPrinterVersion()
printerVersion.printDebug()
printerModel = myInstax.getPrinterModelName()
printerModel.printDebug()
printCount = myInstax.getPrintCount()
printCount.printDebug()
printerSpecifications = myInstax.getPrinterSpecifications()
printerSpecifications.printDebug()
myInstax.close()

# -- Step 4, Lock Printer
myInstax.connect(ip=host)
lockPrinter = myInstax.sendLockCommand(1)
lockPrinter.printDebug()
myInstax.close()

# -- Step 5, Model name
myInstax.connect(ip=host)

printerModel = myInstax.getPrinterModelName()
printerModel.printDebug()
myInstax.close()

# -- Step 6, Count, Specs, Reset
myInstax.connect(ip=host)

printCount = myInstax.getPrintCount()
printCount.printDebug()
printerSpecifications = myInstax.getPrinterSpecifications()
printerSpecifications.printDebug()
sendReset = myInstax.sendResetCommand()
sendReset.printDebug()
myInstax.close()


# -- Step 7, Prep then Image
myInstax.connect(ip=host)

prepImage = myInstax.sendPrepImageCommand(16, 0, 1440000)
prepImage.printDebug()
for segment in range(24):
    start = segment * 60000
    end = start + 60000
    segmentBytes = encodedImage[start:end]
    print("Segment: %s, start: %s, end: %s, len: %s" % (segment,
                                                        start,
                                                        end,
                                                        len(segmentBytes)))
    sendImageCommand = myInstax.sendSendImageCommand(segment,
                                                     bytes(segmentBytes))
    sendImageCommand.printDebug()

type83cmd = myInstax.sendT83Command()
type83cmd.printDebug()
myInstax.close()

# -- Step 8, model name
myInstax.connect(ip=host)
printerVersion = myInstax.getPrinterVersion()
printerVersion.printDebug()
printerModel = myInstax.getPrinterModelName()
printerModel.printDebug()
myInstax.close()

# -- Step 9, version, lockstate
myInstax.connect(ip=host)
printerVersion = myInstax.getPrinterVersion()
printerVersion.printDebug()
lockPrinter = myInstax.sendLockCommand(0)
lockPrinter.printDebug()
myInstax.close()


# -- Step 10, 195 command.
myInstax.connect(ip=host)
type195cmd = myInstax.sendT195Command()
type195cmd.printDebug()
myInstax.close()
