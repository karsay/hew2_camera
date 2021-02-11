import serial
import binascii
import time
import sys
import RPi.GPIO as GPIO


class FingerPrint:

    def __init__(self,port,baund,timeOut,pin):
        self.ser = serial.Serial(port, baund, timeout=timeOut)
        self.pin = pin
        GPIO.setwarnings(False) 
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN)

    def getImage(self):
        self.ser.write(b"\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x03\x01\x00\x05")
        data = self.ser.readline()

        time.sleep(1)

    def genChar(self):
        self.ser.write(b"\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x04\x02\x01\x00\x08")
        data = self.ser.readline()

        time.sleep(1)

    def checkGetImage(self):
        data = self.ser.read()
        if data == b"\xEF":
            for num in range(10):
                data = self.ser.read()
                if num == 7:
                    if data == b"\x00":
                        return True
                    else:
                        return False
        else:
            return False

        


    def enroll(self):


        ts = GPIO.input(self.pin)

        dataresult = b''

        # one time
        while True:
            if ts == 1:

                self.ser.write(b"\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x03\x01\x00\x05")
                for j in range(12):
                    data = self.ser.read()
                    if j == 9:
                        dataresult = data
                if dataresult == b'\x00':    
                    self.ser.write(b"\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x04\x02\x01\x00\x08")
                    for i in range(12):
                        data = self.ser.read()
                        if i == 9:
                            dataresult = data
                    if dataresult == b'\x00':
                        print("1/5成功")
                        ts = GPIO.input(self.pin)
                        print("指を離してください")
                        while ts == 1:
                            time.sleep(1)
                            ts = GPIO.input(self.pin)
                        ts = GPIO.input(self.pin)
                        break
                    else:
                        print("やり直し")
                else:
                    print("やり直し")
            else:
                print("指を乗せてください")
            time.sleep(1)
            ts = GPIO.input(self.pin)




        # two time
        while True:
            if ts == 1:

                self.ser.write(b"\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x03\x01\x00\x05")
                for j in range(12):
                    data = self.ser.read()
                    if j == 9:
                        dataresult = data
                if dataresult == b'\x00':    
                    self.ser.write(b"\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x04\x02\x02\x00\x09")
                    for i in range(12):
                        data = self.ser.read()
                        if i == 9:
                            dataresult = data
                    if dataresult == b'\x00':
                        print("2/5成功")
                        ts = GPIO.input(self.pin)
                        print("指を離してください")
                        while ts == 1:
                            time.sleep(1)
                            ts = GPIO.input(self.pin)
                        ts = GPIO.input(self.pin)
                        break
                    else:
                        print("やり直し")
                else:
                    print("やり直し")
            else:
                print("指を乗せてください")
            time.sleep(1)
            ts = GPIO.input(self.pin)
                    
            



        # three time
        while True:
            if ts == 1:

                self.ser.write(b"\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x03\x01\x00\x05")
                for j in range(12):
                    data = self.ser.read()
                    if j == 9:
                        dataresult = data
                if dataresult == b'\x00':    
                    self.ser.write(b"\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x04\x02\x03\x00\x0A")
                    for i in range(12):
                        data = self.ser.read()
                        if i == 9:
                            dataresult = data
                    if dataresult == b'\x00':
                        print("3/5成功")
                        ts = GPIO.input(self.pin)
                        print("指を離してください")
                        while ts == 1:
                            time.sleep(1)
                            ts = GPIO.input(self.pin)
                        ts = GPIO.input(self.pin)
                        break
                    else:
                        print("やり直し")
                else:
                    print("やり直し")
            else:
                print("指を乗せてください")
            time.sleep(1)
            ts = GPIO.input(self.pin)
        


        # four time

        while True:
            if ts == 1:
                self.ser.write(b"\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x03\x01\x00\x05")
                for j in range(12):
                    data = self.ser.read()
                    if j == 9:
                        dataresult = data
                if dataresult == b'\x00':    
                    self.ser.write(b"\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x04\x02\x04\x00\x0B")
                    for i in range(12):
                        data = self.ser.read()
                        if i == 9:
                            dataresult = data
                    if dataresult == b'\x00':
                        print("4/5成功")
                        ts = GPIO.input(self.pin)
                        print("指を離してください")
                        while ts == 1:
                            time.sleep(1)
                            ts = GPIO.input(self.pin)
                        ts = GPIO.input(self.pin)
                        break
                    else:
                        print("やり直し")
                else:
                    print("やり直し")
            else:
                print("指を乗せてください")
            time.sleep(1)
            ts = GPIO.input(self.pin)



        # five time

        while True:
            if ts == 1:
                self.ser.write(b"\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x03\x01\x00\x05")
                for j in range(12):
                    data = self.ser.read()
                    if j == 9:
                        dataresult = data
                if dataresult == b'\x00':    
                    self.ser.write(b"\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x04\x02\x05\x00\x0C")
                    for i in range(12):
                        data = self.ser.read()
                        if i == 9:
                            dataresult = data
                    if dataresult == b'\x00':
                        print("5/5成功")
                        ts = GPIO.input(27)
                        print("指を離してください")
                        while ts == 1:
                            time.sleep(1)
                            ts = GPIO.input(27)
                        ts = GPIO.input(27)
                        break
                    else:
                        print("やり直し")
                else:
                    print("やり直し")
            else:
                print("指を乗せてください")
            time.sleep(1)
            ts = GPIO.input(27)
        

    def loadChar2(self):
        self.ser.write(b"\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x06\x07\x01\x00\x02\x00\x11")
        data = self.ser.readline()
        # print(data)
        time.sleep(1)


    def loadChar1(self):
        self.ser.write(b"\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x06\x07\x01\x00\x01\x00\x10")
        data = self.ser.readline()
        # print(data)
        time.sleep(1)

    def upImageImage(self):
        self.ser.write(b"\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x03\x0A\x00\x0E")
        data = self.ser.readline()
        data = self.ser.readline()



    def downImageImage(self):
        self.ser.write(b"\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x03\x0B\x00\x0F")
        data = self.ser.readline()
        # print(data)


    def match(self):
        self.ser.write(b"\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x03\x03\x00\x07")

        resultNum = 100

        for i in range(14):  
            data = self.ser.read()
            if i == 9:
                if data == b'\x00':
                    resultNum = 1
                elif data == b'\x08':
                    resultNum = 2
                else:
                    resultNum = -1
        return resultNum



    def downLoadImage2(self,finger):
        self.ser.write(b"\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x04\x09\x02\x00\x10")
        data = self.ser.readline()
        # print(data)
        self.ser.write(finger)



    def upImage1(self):
        self.ser.write(b"\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x04\x08\x01\x00\x0E")
        data = self.ser.readline()
        # print(data)
        countNum = 0
        datapacket = b''
        while  countNum < 10:
            data = self.ser.readline()
            datapacket = datapacket + data
            countNum += 1

        return datapacket
        
        # for i in range(7):
        #     data = ser.read()
        #     print(data)
        # print("\n何回")
        # data = ser.read()
        # print(data)
        # data = ser.read()
        # print(data)
        # print("\n")
        # countNum = 0
        # data = data.hex()
        
        # data16 = int(data,16)
        # datapacket = b''
        # while countNum < 2000:
        #     data = ser.read()
        #     datapacket = datapacket + data
        #     countNum += 1
        # print(datapacket)


    def upImage2(self):
        self.ser.write(b"\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x04\x08\x02\x00\x0F")
        data = self.ser.readline()
        print(data)
        data = self.ser.readline()
        return data

    def regModel(self):
        self.ser.write(b"\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x03\x05\x00\x09")
        data = self.ser.readline()
        # print(data)
        # time.sleep(1)

    def storeChar1(self):
        self.ser.write(b"\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x06\x06\x01\x00\x01\x00\x0F")
        data = self.ser.readline()
        print(data)
        time.sleep(1)

    def storeChar2(self):
        self.ser.write(b"\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x06\x06\x01\x00\x02\x00\x10")
        data = self.ser.readline()
        print(data)
        time.sleep(1)

    def storeCharLogIn(self):
        self.ser.write(b"\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x06\x06\x01\x00\x05\x00\x13")
        data = self.ser.readline()
        print(data)
        time.sleep(1)

    def search(self):
        self.ser.write(b"\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x08\x04\x01\x00\x00\x00\x63\x00\x71")
        data = self.ser.readline()
        print(data)
        time.sleep(1)



    def loginFinger(self):

        ts = GPIO.input(self.pin)
        dataresult = b''
        while True:
            if ts == 1:
                self.ser.write(b"\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x03\x01\x00\x05")
                for j in range(12):
                    data = self.ser.read()
                    if j == 10:
                        dataresult = data
                if dataresult == b'\x00': 

                    self.ser.write(b"\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x04\x02\x01\x00\x08")
                    for i in range(12):
                        data = self.ser.read()
                        if i == 9:
                            dataresult = data
                    if dataresult == b'\x00':

                        print("指紋読み取り完了")
                        ts = GPIO.input(self.pin)
                        j = 0
                        i = 0
                        print("指を離してください")
                        while ts == 1:
                            time.sleep(1)
                            ts = GPIO.input(self.pin)
                        ts = GPIO.input(self.pin)
                        break
                    else:
                        print("やり直し")
                else:
                    print("やり直し")
            else:
                print("指を乗せてください")
            time.sleep(1)
            ts = GPIO.input(self.pin)






