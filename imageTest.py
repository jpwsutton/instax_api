import instax
import time

print("Instax SP-2 Example App")

# Initialize The Instax Image
instaxImage = instax.InstaxImage()

# Load the image from the filesystem
instaxImage.loadImage("DSC_0480.jpg")

# Convert the image (Will Resize, Rotate and Crop to fix 600x800)
instaxImage.convertImage()

# Open the image in the OS image viewer of choice
instaxImage.previewImage()

# Save the new image to disk
instaxImage.saveImage( str(int(time.time())) + ".bmp")

# Get the Byte stream of the image (This is in BITMAP RGB format)
myBytes = instaxImage.getBytes()

print("length: ", len(myBytes))
