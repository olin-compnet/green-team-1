#
## Lab 2.2 - Physical Layer  - Send Tuples as blinks
#
from MorseTX import MorseTX
from SetPin import SetPin
from MorseCode import MorseCode
import time, random
address = 'AB'
morseNumbers = {1 : '.----', 2 : '..---', 3 : '...--', 4 : '....-', 5 : '.....', 6 : '-....', 7 : '--...', 8 : '---..', 9 : '----.', 0 :'-----'}

class BlinkTX(SetPin):
    def __init__(self,headerpin,BCM,direction="TX"):
        if direction != "TX":
            raise ValueError("direction must be 'TX'")
        super().__init__(headerpin,BCM,direction="TX")

    def __call__(self,tups):
        for state,direction in tups:
            self.blinkTX(state,direction)

    def blinkTX(self,state,duration):
        self.turn_high() if state else self.turn_low()
        time.sleep(duration * .075)      
def getquote():
    x = makeMorseHappy(quotes[random.randint(0,len(quotes)-1)])
    return x

def blinkTargetAddress(blink, addressTarget):
    for c in addressTarget:
        for Dd in MorseCode[c]:
            blink.blinkTX(1, 1) if Dd == '.' else blink.blinkTX(1,3)
            blink.blinkTX(0, 1)
        blink.blinkTX(0, 2)
    blink.blinkTX(0, 4)

def blinkOwnAddress(blink):
    for c in thisAddress:
        for Dd in MorseCode[c]:
            blink.blinkTX(1, 1) if Dd == '.' else blink.blinkTX(1,3)
            blink.blinkTX(0, 1)
        blink.blinkTX(0, 2)
    blink.blinkTX(0, 4)

def splitMessages(morseMsg, msgSize):
    ans = []
    while len(morseMsg) > msgSize:
        

def blinkMessagePart(blink, num, maxNum):
    for c in str(num)[::-1]:
        for dd in morseNumbers[int(c)]:
            blink.blinkTX(1, 1) if d == '.' else blink.blinkTX(1, 3)
            blink.blinkTX(0, 1)
        blink.blinkTX(0, 2)
    blink.blinkTX(0, 4)
    for c in str(maxNum)[::-1]:
        for dd in morseNumbers[int(c)]:
            blink.blinkTX(1, 1) if d == '.' else blink.blinkTX(1, 3)
            blink.blinkTX(0, 1)
        blink.blinkTX(0, 2)
    blink.blinkTX(0, 4)
    # if(num > 9):
    #     for d in morseNumbers[int(num/10)]:
    #         blink.blinkTX(1, 1) if d == '.' else blink.blinkTX(1, 3)
    #         blink.blinkTX(0, 1)
    #     blink.blinkTX(0, 3)
    # for d in morseNumbers[num%10]:
    #     blink.blinkTX(1, 1) if d == '.' else blink.blinkTX(1, 3)
    #     blink.blinkTX(0, 1)
    # blink.blinkTX(0, 6)
    # if(maxNum > 9):
    #     for d in morseNumbers[int(maxNum/10)]:
    #         blink.blinkTX(1, 1) if d == '.' else blink.blinkTX(1, 3)
    #         blink.blinkTX(0, 1)
    #     blink.blinkTX(0, 3)
    # for d in morseNumbers[maxNum%10]:
    #     blink.blinkTX(1, 1) if d == '.' else blink.blinkTX(1, 3)
    #     blink.blinkTX(0, 1)
    # blink.blinkTX(0, 9)

def blinkChecksum(blink, msg):
    chk = 0
    for l in msg:
        chk += ord(l.upper())
    parity = chr((65 + chk) % 26)
    for c in MorseCode[parity]:
       blink.blinkTX(1, 1) if c == '.' else blink.blinkTX(1, 3)
       blink.blinkTX(0, 1)
    blink.blinkTX(0, 6)



def makeMorseHappy(Q):
    return "".join([a if a in string.ascii_uppercase+" " else " "+"".join(unicodedata.name(a,"").split("-"))+" " for a in Q.upper() ])

def sendMessage():
    with BlinkTX(15,"GPIO_22",direction="TX") as blink:
        with SetPin(16, 'GPIO_23', direction='RX') as RXpin:
            RXpin.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            while True:
                clear = True
                msg = input("MESSAGE TO SEND (EMPTY ENTRY YIELDS RANDOM QUOTE) :")
                for i in range(random.randint(5, 30)):
                    print('Checking for clear connection')
                    if(RXpin.read_pin()):
                        clear = False
                        break
                    time.sleep(.1)
                if(clear):
                    if not msg:
                        send = getquote()
                    else:
                        send = msg.upper()
                    morseMsg = ''
                    for W in send.split(" "):
                        for L in W:
                            for Dd in MorseCode[L]:
                                morseMsg += '.' if Dd == "." else '.'*3
                                morseMsg += '*'
                            morseMsg += '*'*2
                        morseMsg += '*'*4
                    morseMsg += '*'*8
                    # morseArray = []
                    # while len(morseMsg) > 120:
                    #     morseArray.append(morseMsg[:120])
                    #     morseMsg = morseMsg[120:]
                    # morseArray.append(morseMsg)
                    morseArray = splitMessages(morseMsg, 120)
                    targetAddress = input('TARGET ADDRESS: ').upper()
                    for blinkIndex in range(len(morseArray)):
                        blinkTargetAddress(blink, targetAddress) # datalink
                        blinkOwnAddress(blink)
                        blinkChecksum(blink, msg)
                        blinkTargetAddress(blink, targetAddress) # network
                        blinkOwnAddress(blink)
                        blinkMessagePart(blink, blinkIndex + 1, len(morseArray))
                        for char in morseArray[blinkIndex]:
                            if(char == '.'):
                                blink.blinkTX(1, 1)
                            else:
                                blink.blinkTX(0, 1)
                else:
                    ranTime = random.random() * 5 + 10
                    print('Collision detected, timeout for {} seconds'.format(ranTime))
                    time.sleep(ranTime)
                    print('Ready for next message')

if __name__ == "__main__":
    import random
    import mobydickquotes
    import string
    import unicodedata
    quotes = mobydickquotes.quotes
    sendMessage()
    

    
