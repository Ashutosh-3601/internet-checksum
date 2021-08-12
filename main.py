import time
import random

data = input('Enter the data to send\n')

class CheckSum:
    def __init__(self, data):
        self.data = data
        self.frames = []
        self.hexedData = []
        self.checksum = "0000"

    def init(self, inject=False):
        for i in range(0, len(self.data), 2):
            self.frames.append(self.data[i:i+2])
        self.generate()
        if inject: 
            self.injectError()
        return self.checksum
        
    def generate(self):
        for frame in self.frames:
            hex = ''
            for framebit in frame:
                if len(frame) % 2 != 0:
                    framebit += '\0'
                hex += framebit.encode('utf-8').hex()
            
            self.hexedData.append(hex)
        self.hexedData.append(self.checksum)
        self.partialSum()

    def partialSum(self):
        partial = 0
        for hexcode in self.hexedData:
            partial += int(hexcode, 16)

        sum = hex(partial)
        self.checkSum(sum[2:])

    def checkSum(self, partial):
        self.checksum = partial
        if len(partial) % 2 != 0:
            carry = partial[0]
            checksum = hex(int(partial[1:],16)+int(carry, 16))
            self.checksum = checksum[2:]

    def injectError(self):
        chars = 'abcedef0123456789'
        print('Error injected')
        print(f'Original Sum was : {self.checksum}\n')
        self.checksum = self.checksum.replace(self.checksum[random.randint(0,3)], chars[random.randint(0,15)])


    
class SenderCheckSum(CheckSum):
    def process(self, error=False):
        self.printSender()
        nonComplementedChecksum = self.init(error)
        checksum = hex(int('FFFF',16)-int(nonComplementedChecksum, 16))
        return checksum[2:]
    
    def printSender(self):
        print('\n\33[33m#########################################')
        print('#\t Generating Sender Side CheckSum \t#')
        print('#########################################\33[0m\n')

class RecieverCheckSum(CheckSum):
    def __init__(self, sender):
        CheckSum.__init__(self, data)
        self.checksum = sender

    def validate(self):
        self.printReciever()
        nonComplementedChecksum = self.init()
        checksum = hex(int('FFFF', 16)-int(nonComplementedChecksum, 16))
        return checksum[2:]
    
    def printReciever(self):
        print('\n\33[33m#########################################')
        print('#\t   Validating Recieved CheckSum   \t#')
        print('#########################################\33[0m\n')

sender = SenderCheckSum(data).process()
print('Generated Checksum: ', sender)
print('\33[5mSending data => \t\33[0m', data)
time.sleep(2)

reciever = RecieverCheckSum(sender).validate()
print('Checksum :', reciever)
if reciever != '0':
    print('Error in data recieved. \33[31m[Rejected]\33[0m')
else:
    print('No error in data \33[32m[Accepted]\33[0m')
