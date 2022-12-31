"""Image transformation utilities."""
from loguru import logger
from PIL import Image, ImageOps


class InstaxImage:
    """Image Utilities class."""

    dimensions = {1: (600, 800), 2: (600, 800), 3: (800, 800)}

    def __init__(self, type=2):
        """Initialise the instax Image."""
        self.type = type
        self.printHeight, self.printWidth = self.dimensions[self.type]

    def loadImage(self, imagePath):
        """Load an image from a path."""
        self.sourceImage = Image.open(imagePath)

    def encodeImage(self):
        """Encode the loaded Image."""
        imgWidth, imgHeight = self.myImage.size
        # Quick check that it's the right dimensions
        if imgWidth + imgHeight != (self.printHeight + self.printWidth):
            raise Exception("Image was not 800x600 or 600x800, it was : w:%d, h:%d" % (imgWidth, imgHeight))
        if imgWidth != self.printWidth:
            # Rotate the image
            self.myImage = self.myImage.rotate(-90, expand=True)
        if self.printWidth == self.printHeight:
            # Square images are a bit tricky, we have to assume they are oriented correctly
            logger.info("Rotating Square Image")
            self.myImage = self.myImage.rotate(-90, expand=True)
        imagePixels = self.myImage.getdata()
        arrayLen = len(imagePixels) * 3
        encodedBytes = [None] * arrayLen
        for h in range(self.printHeight):
            for w in range(self.printWidth):
                r, g, b = imagePixels[(h * self.printWidth) + w]
                redTarget = (((w * self.printHeight) * 3) + (self.printHeight * 0)) + h
                greenTarget = (((w * self.printHeight) * 3) + (self.printHeight * 1)) + h
                blueTarget = (((w * self.printHeight) * 3) + (self.printHeight * 2)) + h
                encodedBytes[redTarget] = int(r)
                encodedBytes[greenTarget] = int(g)
                encodedBytes[blueTarget] = int(b)
        return encodedBytes

    def decodeImage(self, imageBytes):
        """Decode the byte array into an image."""
        targetImg = []
        # Packing the individual colours back together.
        for h in range(self.printHeight):
            for w in range(self.printWidth):
                redTarget = (((w * self.printHeight) * 3) + (self.printHeight * 0)) + h
                greenTarget = (((w * self.printHeight) * 3) + (self.printHeight * 1)) + h
                blueTarget = (((w * self.printHeight) * 3) + (self.printHeight * 2)) + h
                targetImg.append(imageBytes[redTarget])
                targetImg.append(imageBytes[greenTarget])
                targetImg.append(imageBytes[blueTarget])
        preImage = Image.frombytes("RGB", (self.printWidth, self.printHeight), bytes(targetImg))
        self.myImage = preImage.rotate(90, expand=True)

    def convertImage(self, crop_type="middle", backgroundColour=(255, 255, 255, 0)):
        """Rotate, Resize and Crop the image.

        Rotate, Resize and Crop the image, so that it is the correct
        dimensions for printing to the Instax SP-2.
        """
        maxSize = self.printHeight, self.printWidth  # The Max Image size

        # Strip Exif and rotate image correctly
        rotatedImage = ImageOps.exif_transpose(self.sourceImage)

        # Fit the image to the required ratio
        fittedImage = ImageOps.fit(rotatedImage, maxSize, bleed=0, centering=(0.5, 0.5))

        self.myImage = pure_pil_alpha_to_color_v2(fittedImage, (255, 255, 255))

    def previewImage(self):
        """Preview the image."""
        self.myImage.show()

    def saveImage(self, filename):
        """Save the image to the specified path."""
        logger.info(("Saving Image to: ", filename))
        self.myImage.save(filename, "BMP", quality=100, optimise=True)

    def getBytes(self):
        """Get the Byte Array from the image."""
        myBytes = self.myImage.tobytes()
        return myBytes


def pure_pil_alpha_to_color_v2(image, color=(255, 255, 255)):
    """Alpha composite an RGBA Image with a specified color.

    Simpler, faster version than the solutions above.

    Source: 098

    Keyword Arguments:
    image -- PIL RGBA Image object
    color -- Tuple r, g, b (default 255, 255, 255)

    """
    image.load()  # needed for split()
    background = Image.new("RGB", image.size, color)
    background.paste(image)  # 3 is the alpha channel
    return background
