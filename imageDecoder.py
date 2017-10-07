from PIL import Image, ExifTags, ImageOps
"""Test file to decode an encoded bitmap into a bitmap file."""
height = 600
width = 800


def replace(target, source, startPos):
    final = []
    final = final + target[:startPos]
    final.append(source)
    final.append(target[startPos + len(source):])
    return final


def main():
    """Main function."""
    files = [
        "test_img/encodedImage-20171004-172001.instax",
        "test_img/encodedImage-20171004-172040.instax",
        "test_img/encodedImage-20171004-172115.instax",
        "test_img/encodedImage-20171004-172158.instax"
    ]

    #for myfile in files:
    #    decodeImage(myfile)
    filename = "encodedImage-20170930-111524.instax" # Cup and Muffin
    cat = "encodedImage-20171004-204806.instax"
    inFile = "1485542112.bmp"
    decodeImage(cat)
    #encodeImage(inFile)
    #encodeImageOld(inFile)


def decodeImage(filename):
    """Decoding Image."""
    print("Decoding combined image file into bitmap : %s" % filename)
    with open(filename, 'rb') as infile:
        rawBytes = infile.read()
        filebytes = bytearray(rawBytes)
        print("Type: %s" % type(filebytes))
        print("There are %s bytes in this file." % len(filebytes))
        targetImg = []

        # Re-packing the individual colours back together.
        for h in range(height):
            for w in range(width):
                redTarget = (((w * height) * 3) + (height * 0)) + h
                greenTarget = (((w * height) * 3) + (height * 1)) + h
                blueTarget = (((w * height) * 3) + (height * 2)) + h
                targetImg.append(filebytes[redTarget])
                targetImg.append(filebytes[greenTarget])
                targetImg.append(filebytes[blueTarget])

        image = Image.frombytes('RGB', (width, height), bytes(targetImg)) # pass in the bytestring
        image.show()
        image.save(filename + "600x800_decoded_raw.bmp")


def encodeImage(filename):

    totalBytes = (width * height) * 3
    messages = int(totalBytes / 60000)
    if (totalBytes % 60000) != 0:
        ++messages
    print("Number of messages: %s" % messages)
    print("Total Size: %s" % (messages * 60000))
    """
    Basically do a reverse of the decode image process, make sure that the image is 800x600
    """







if __name__ == "__main__":
    main()
