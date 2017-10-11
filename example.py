import instax


def printSeparator():
    print('--------------------------------------------------')


print("Instax SP-2 Example App")
myInstax = instax.SP2()
myInstax.connect(ip='localhost')
myInstax.connect()
printSeparator()
printerVersion = myInstax.getPrinterVersion()
printerVersion.printDebug()
printerModel = myInstax.getPrinterModelName()
printerModel.printDebug()
printCount = myInstax.getPrintCount()
printCount.printDebug()
printerSpecifications = myInstax.getPrinterSpecifications()
printerSpecifications.printDebug()
print("Locking Printer")
lockPrinter = myInstax.sendLockCommand(1)
lockPrinter.printDebug()

for x in range(1, 9):
    prePrintCmd = myInstax.sendPrePrintCommand(x)
    print("PrePrint - C: %s, R: %s" % (x, prePrintCmd.respNumber))
printSeparator()

sendReset = myInstax.sendResetCommand()
sendReset.printDebug()


prepImage = myInstax.sendPrepImageCommand(16, 0, 1440000)
prepImage.printDebug()

# Ready to send photo


# Initialize The Instax Image
instaxImage = instax.InstaxImage()
# Load the image from the filesystem
instaxImage.loadImage("test.jpg")
# Convert the image (Will Resize, Rotate and Crop to fix 600x800)
instaxImage.convertImage()
# Open the image in the OS image viewer of choice
instaxImage.previewImage()
# Save the new image to disk
instaxImage.saveImage("test.bmp")
# Get the Byte stream of the image (This is in BITMAP RGB format)
encodedImage = instaxImage.encodeImage()

for segment in range(24):
    start = segment * 60000
    end = start + 60000
    segmentBytes = encodedImage[start:end]
    print("Segment: %s, start: %s, end: %s, len: %s" % (segment, start, end, len(segmentBytes)))
    sendImageCommand = myInstax.sendSendImageCommand(segment, bytes(segmentBytes))
    sendImageCommand.printDebug()

type83cmd = myInstax.sendT83Command()
type83cmd.printDebug()


lockPrinter = myInstax.sendLockCommand(0)
lockPrinter.printDebug()
printSeparator()
myInstax.close()
printSeparator()
