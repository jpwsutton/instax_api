#import instax
import binascii
import sys
print("Instax Packet Capture Replay...")
'''
    Accepts a 'RAW' TCP stream that has been exported from wireshark and
    converts it into an instax-sp2 message flow. The flow is then printed
    to the console showing the contents of the messages.
'''

filename = "packet_captures/test3/cmd_79_80"
#filename = "packet_captures/test3/cmd_51_52_image"

print('Reading: ' + filename)

def printByteArray(byteArray):
    hexString = ''.join('%02x'%i for i in byteArray)
    data = ' '.join(hexString[i:i+4] for i in range(0, len(hexString), 4))
    #info = (data[:80] + '..') if len(data) > 80 else data
    info = data
    return(info)



def getMessages(filename):
    messages = []
    with open(filename, "rb") as f:
        data = f.read()

        temp = []
        for i in range(len(data)):
                if (len(temp) > 0 ) and (temp[-1] == 13) and (data[i] == 10):
                    if (len(data) > i+1):
                        if((data[i+1] == 36) or (data[i+1] == 42)):
                            temp.append(data[i])
                            messages.append(temp)
                            temp = []
                    else:
                        temp.append(data[i])
                        messages.append(temp)
                        temp = []
                else:
                    temp.append(data[i])
        return messages




messages = getMessages(filename)

#packetFactory = instax.PacketFactory()
for msg in messages:
    #packet = packetFactory.getPacket(msg)
    print(printByteArray(msg))
