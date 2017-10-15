import instax
import pprint
print("Instax SP-2 Example App")
# host = "localhost"
host = "192.168.0.251"
myInstax = instax.SP2(ip=host)

info = myInstax.getPrinterInformation()
pprint.pprint(info)


print("Preparing Image")
# Initialize The Instax Image
instaxImage = instax.InstaxImage()
instaxImage.loadImage("test.jpg")
instaxImage.convertImage()
instaxImage.saveImage("test.bmp")
encodedImage = instaxImage.encodeImage()

print = myInstax.printPhoto(encodedImage)
