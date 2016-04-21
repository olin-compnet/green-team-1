from MorseCode import MorseCode
Inverted = {MorseCode[letter]: letter for letter in MorseCode}
Numbers = {1: '.----', 2: '..---', 3: '...--', 4: '....-', 5: '.....', 6: '-....', 7: '--...', 8: '---..', 9: '----.', 10: '-----'}
InvertNumbers = {Numbers[n]: n for n in Numbers}
thisAddress = 'AA'

def splitAsterisks(incoming):
	out = []
	second = []
	first = incoming.split('**')
	for i in first:
		second += i.split('***')
	for j in second:
		out += j.split('****')
	return out

def processMessagePart(msgPart, msgMax):
	nums1 = msgPart.split('***')
	rec1 = ''
	for n in nums1:
		rec1 += Inverted[n.replace('...', '-').replace('*', '')]
	nums2 = msgMax.split('***')
	rec2 = ''
	for n in nums2:
		rec2 += Inverted[n.replace('...', '-').replace('*', '')]
	print('Message is part {} of {}'.format(rec1, rec2))
	return int(rec1), int(rec2)


def processToAddress(header, curAddress):
	# Process header
	letters = header.split('***')
	rec = ''
	for l in letters:
		rec += Inverted[l.replace('...', '-').replace('*', '')]
	print('Message intended for {}'.format(rec))
	if rec == curAddress:
		print('This is the correct recipient')
	else:
		print('This is the incorrect recipient')

def processFromAddress(header):
	letters = header.split('***')
	rec = ''
	for l in letters:
		rec += Inverted[l.replace('...', '-').replace('*', '')]
	print('Message received from for {}'.format(rec))

def nwOperations(msgList):
	processToAddress(msgList[0], thisAddress)
	processFromAddress(msgList[1])
	processMessagePart(msgList[2], msgList[3])
	return msgList[4:]