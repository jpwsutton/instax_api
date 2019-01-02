"""Image transformation utilities."""
from PIL import Image, ImageOps
import logging


class InstaxImage:
    """Image Utilities class."""

    dimensions = {
        1 : (600, 800),
        2 : (600, 800),
        3 : (800, 800)
    }


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
        logging.info("Initial Image Size: W: %s, H: %s" % (imgWidth, imgHeight))
        # Quick check that it's the right dimensions
        if(imgWidth + imgHeight != (self.printHeight + self.printWidth)):
            raise Exception("Image was not 800x600 or 600x800, it was : w:%d, h:%d" % (imgWidth, imgHeight))
        if(imgWidth != self.printWidth):
            # Rotate the image
            logging.info("Rotating")
            self.myImage = self.myImage.rotate(-90, expand=True)
        if (self.printWidth == self.printHeight):
            # Square images are a bit tricky, we have to assume they are oriented correctly
            logging.info("Rotating Square Image")
            self.myImage = self.myImage.rotate(-90, expand=True)
        logging.info("New Image Size: W: %s, H: %s" % (self.myImage.size))
        imagePixels = self.myImage.getdata()
        logging.info("Mode: %s" % (self.myImage.mode))
        arrayLen = len(imagePixels) * 3
        logging.info("Encoded Array Length: %s" % arrayLen)
        encodedBytes = [None] * arrayLen
        for h in range(self.printHeight):
            for w in range(self.printWidth):
                r, g, b= imagePixels[(h * self.printWidth) + w]
                redTarget = (((w * self.printHeight) * 3) +
                             (self.printHeight * 0)) + h
                greenTarget = (((w * self.printHeight) * 3) +
                               (self.printHeight * 1)) + h
                blueTarget = (((w * self.printHeight) * 3) +
                              (self.printHeight * 2)) + h
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
                redTarget = (((w * self.printHeight) * 3) +
                             (self.printHeight * 0)) + h
                greenTarget = (((w * self.printHeight) * 3) +
                               (self.printHeight * 1)) + h
                blueTarget = (((w * self.printHeight) * 3) +
                              (self.printHeight * 2)) + h
                targetImg.append(imageBytes[redTarget])
                targetImg.append(imageBytes[greenTarget])
                targetImg.append(imageBytes[blueTarget])
        preImage = Image.frombytes('RGB',
                                   (self.printWidth,
                                    self.printHeight),
                                   bytes(targetImg))
        self.myImage = preImage.rotate(90, expand=True)

    def convertImage(self, crop_type='middle',
                     backgroundColour=(255, 255, 255, 0)):
        """Rotate, Resize and Crop the image.

        Rotate, Resize and Crop the image, so that it is the correct
        dimensions for printing to the Instax SP-2.
        """
        maxSize = self.printHeight, self.printWidth  # The Max Image size
        rotatedImage = rotate_image(self.sourceImage)
        image_ratio = rotatedImage.size[0] / float(rotatedImage.size[1])

        if(rotatedImage.size[0] + rotatedImage.size[1] == (self.printHeight + self.printWidth)):
            img = rotatedImage
        else:
            if image_ratio == 1.0:
                img = crop_square(rotatedImage, maxSize, backgroundColour)
            else:
                img = crop_rectangle(rotatedImage, maxSize, crop_type)

        # Stip away any exif data.
        newImage = Image.new(img.mode, img.size)
        newImage.putdata(img.getdata())
        self.myImage = pure_pil_alpha_to_color_v2(newImage, (255,255,255))

    def previewImage(self):
        """Preview the image."""
        self.myImage.show()

    def saveImage(self, filename):
        """Save the image to the specified path."""
        logging.info(("Saving Image to: ", filename))
        self.myImage.save(filename, 'BMP', quality=100, optimise=True)

    def getBytes(self):
        """Get the Byte Array from the image."""
        myBytes = self.myImage.tobytes()
        return myBytes


def rotate_image(source):
    """Rotate the image.

    Rotates and/or flips an image to the correct orientation
    for the instax printer.

    args:
        source: The Source ImageOps
    """
    exif_orientation = 274
    img_ratio = source.size[0] / float(source.size[1])
    if(source._getexif() is None):
        return source
    exif_data = dict(source._getexif().items())
    if img_ratio > 1:
        # Image is landscape
        if exif_orientation in exif_data:
            orientation = exif_data[exif_orientation]
            if orientation == 1:
                tmpImage = source.rotate(270, expand=True)
            elif orientation == 2:
                tmpImage = ImageOps.mirror(source)
                tmpImage = tmpImage.rotate(270, expand=True)
            elif orientation == 3:
                tmpImage = source.rotate(90, expand=True)
            elif orientation == 4:
                tmpImage = ImageOps.mirror(source)
                tmpImage = tmpImage.rotate(90, expand=True)
            elif orientation == 5:
                tmpImage = ImageOps.flip(source)
                tmpImage = tmpImage.rotate(270, expand=True)
            elif orientation == 6:
                tmpImage = source.rotate(270, expand=True)
            elif orientation == 7:
                tmpImage = ImageOps.flip(source)
                tmpImage = tmpImage.rotate(90, expand=True)
            elif orientation == 8:
                tmpImage = source.rotate(90, expand=True)
            else:
                # Invalid Orientation, As it's landscape, just rotate 270
                tmpImage = source.rotate(270, expand=True)
        else:
            # No Orientation Exif data, As it's landscape, just rotate 270
            tmpImage = source.rotate(270, expand=True)
    else:
        if exif_orientation in exif_data:
            orientation = exif_data[exif_orientation]
            if orientation == 1:
                tmpImage = source
            elif orientation == 2:
                tmpImage = ImageOps.mirror(source)
            elif orientation == 3:
                tmpImage = source.rotate(180, expand=True)
            elif orientation == 4:
                tmpImage = ImageOps.mirror(source)
                tmpImage = tmpImage.rotate(180, expand=True)
            elif orientation == 5:
                tmpImage = ImageOps.flip(source)
                tmpImage = tmpImage.rotate(180, expand=True)
            elif orientation == 6:
                tmpImage = source.rotate(180, expand=True)
            elif orientation == 7:
                tmpImage = ImageOps.flip(source)
            elif orientation == 8:
                tmpImage = source
            else:
                tmpImage = source
        else:
            tmpImage = source
    return tmpImage


def crop_square(source, size, backgroundColour=(255, 255, 255, 0)):
    """Crop the image to a square."""
    source.thumbnail(size, Image.ANTIALIAS)
    offset_x = int(max((size[0] - source.size[0]) / 2, 0))
    offset_y = int(max((size[1] - source.size[1]) / 2, 0))
    offset_tuple = (offset_x, offset_y)
    img = Image.new(mode='RGBA', size=size, color=backgroundColour)
    img.paste(source, offset_tuple)
    return img


def crop_rectangle(source, size, crop_type='top'):
    """Crop the Image to a rectangle.

    args:
        source: The source image
        size: `(width, height)` tuple
        crop_type: can be 'top', 'middle' or 'bottom', depending on this
            value, the image will be cropped getting the 'top/left', 'middle'
            or 'bottom/right' of the image to fid the size.

    raises:
        ValueError: if an invalid `crop_type` is provided.

    """
    ratio = size[0] / float(size[1])
    new_ratio = source.size[0] / float(source.size[1])

    if ratio > new_ratio:
        # The image is scaled/cropped vertically or horizontally
        targetSize = int(round(size[0] * source.size[1] / source.size[0]))
        img = source.resize((size[0], targetSize), Image.ANTIALIAS)
        # Crop in the top, middle or bottom
        if crop_type == 'top':
            box = (0, 0, img.size[0], size[1])
        elif crop_type == 'middle':
            box = (0, int(round((img.size[1] - size[1]) / 2)), img.size[0],
                   int(round((img.size[1] + size[1]) / 2)))
        elif crop_type == 'bottom':
            box = (0, img.size[1] - size[1], img.size[0], img.size[1])
        else:
            raise ValueError('ERROR: invalid value for crop_type: ', crop_type)
        img = img.crop(box)
    elif ratio < new_ratio:
        targetSize = int(round(size[1] * source.size[0] / source.size[1]))
        img = source.resize((targetSize, size[1]), Image.ANTIALIAS)
        # Crop in the top, middle or bottom
        if crop_type == 'top':
            box = (0, 0, img.size[0], size[1])
        elif crop_type == 'middle':
            box = (int(round((img.size[0] + size[0]) / 2)), 0,
                   int(round((img.size[0] + size[0]) / 2)), img.size[1])
        elif crop_type == 'bottom':
            box = (img.size[0] - size[0], 0, img.size[0], img.size[1])
        else:
            raise ValueError('ERROR: invalid value for crop_type: ', crop_type)
        img = img.crop(box)
    else:
        img = source.resize((size[0], size[1]), Image.ANTIALIAS)

    return img

def pure_pil_alpha_to_color_v2(image, color=(255, 255, 255)):
    """Alpha composite an RGBA Image with a specified color.

    Simpler, faster version than the solutions above.

    Source: 098

    Keyword Arguments:
    image -- PIL RGBA Image object
    color -- Tuple r, g, b (default 255, 255, 255)

    """
    image.load()  # needed for split()
    background = Image.new('RGB', image.size, color)
    background.paste(image)  # 3 is the alpha channel
    return background