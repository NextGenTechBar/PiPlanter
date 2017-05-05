#testing i2c connection to arduino
import smbus
import time

bus = smbus.SMBus(1)

address = 0x04

def writeNumber(value):
    bus.write_byte(address,value)
    return -1

def readNumbers():
    number = bus.read_byte(address)
 
    print("number 1 is "+str(number))
    return number

while True:
    '''
    var = input("Enter 1-9: ")
    if not var:
        continue
    writeNumber(var)
    '''
    
    print("Water sensor value is ")
    time.sleep(1)
    number = readNumbers()
    print(number)
    print()
    time.sleep(5)



