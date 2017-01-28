from PIL import Image, ExifTags, ImageOps
import sys, io

class InstaxImage:
    'Image Utilities class'

    def __init__(self):
        pass

    def loadImage(self, imagePath):
        self.sourceImage = Image.open(imagePath)

    def convertImage(self, crop_type='middle', backgroundColour=(255,255,255,0)):
        """
        Rotate, Resize and Crop the image so that it is the correct
        dimensions for printing to the Instax SP-2
        """
        maxSize = 600, 800 # The Max Image size
        rotatedImage = rotate_image(self.sourceImage)
        image_ratio = rotatedImage.size[0] / float(rotatedImage.size[1])

        if image_ratio == 1.0:
            img = crop_square(rotatedImage, maxSize, backgroundColour)
        else:
            img = crop_rectangle(rotatedImage, maxSize, crop_type)

        # Stip away any exif data.
        newImage = Image.new(img.mode, img.size)
        newImage.putdata(img.getdata())
        self.myImage = newImage

    def previewImage(self):
        self.myImage.show()

    def saveImage(self, filename):
        print("Saving Image to: ", filename)
        self.myImage.save(filename, 'JPEG', quality=100, optimise=True)

    def getBytes(self):
        myBytes = self.myImage.tobytes()
        return myBytes



def rotate_image(source):
    """
    Rotates and/or flips an image to the correct orientation
    for the instax printer.

    args:
        source: The Source ImageOps
    """
    exif_orientation = 274
    img_ratio = source.size[0] / float(source.size[1])
    if img_ratio > 1:
        # Image is landscape
        exif_data = dict(source._getexif().items())
        if exif_orientation in exif_data:
            orientation = exif_data[exif_orientation]
            if orientation == 1:
                tmpImage=source.rotate(270, expand=True)
            elif orientation == 2:
                tmpImage = ImageOps.mirror(source)
                tmpImage = tmpImage.rotate(270, expand=True)
            elif orientation == 3:
                tmpImage=source.rotate(90, expand=True)
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
                tmpImage=source.rotate(270, expand=True)
        else:
            # No Orientation Exif data, As it's landscape, just rotate 270
            tmpImage=source.rotate(270, expand=True)
    else:
        exif_data = dict(source._getexif().items())
        if exif_orientation in exif_data:
            orientation = exif_data[exif_orientation]
            if orientation == 1:
                tmpImage = source
            elif orientation == 2:
                tmpImage = ImageOps.mirror(source)
            elif orientation == 3:
                tmpImage=source.rotate(180, expand=True)
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

def crop_square(source, size, backgroundColour=(255,255,255,0)):
    """
    Resize and crop a square image to fit the specified size
    """
    source.thumbnail(size, Image.ANTIALIAS)
    offset_x = int(max((size[0] - source.size[0]) / 2, 0))
    offset_y = int(max((size[1] - source.size[1]) / 2, 0))
    offset_tuple = (offset_x, offset_y)
    img = Image.new(mode='RGBA', size=size, color=backgroundColour)
    img.paste(source, offset_tuple)
    return img

def crop_rectangle(source, size, crop_type='top'):
    """
    Resize and crop an image to fit the specified size

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
    # The image is scaled/cropped vertically or horizontally depending on the ratio
        img = source.resize((size[0], int(round(size[0] * source.size[1] / source.size[0]))),
            Image.ANTIALIAS)
        # Crop in the top, middle or bottom
        if crop_type == 'top':
            box = (0, 0, img.size[0], size[1])
        elif crop_type == 'middle':
            box = (0, int(round((img.size[1] - size[1]) / 2)), img.size[0],
             int(round((img.size[1] + size[1]) /2)))
        elif crop_type == 'bottom':
            box = (0, img.size[1] - size[1], img.size[0], img.size[1])
        else:
            raise ValueError('ERROR: invalid value for crop_type: ', crop_type)
        img = img.crop(box)
    elif ratio < new_ratio:
        img = source.resize((int(round(size[1] * source.size[0] / source.size[1])), size[1]),
        Image.ANTIALIAS)
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
