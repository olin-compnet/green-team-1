from MorseCode import MorseCode
Inverted = {MorseCode[letter]: letter for letter in MorseCode}
Numbers = {1: '.----', 2: '..---', 3: '...--', 4: '....-', 5: '.....', 6: '-....', 7: '--...', 8: '---..', 9: '----.', 10: '-----'}
InvertNumbers = {Numbers[n]: n for n in Numbers}
thisAddress = 'AA'

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

def splitAsterisks(incoming):
	out = []
	second = []
	first = incoming.split('**')
	for i in first:
		second += i.split('***')
	for j in second:
		out += j.split('****')
	return out

def processChecksum(parity, msg):
	# Process parity
	words = msg.split('*******')
	for w in words:
		letters = splitAsterisks(w)
		for i in range(len(letters)):
			letter = letters[i]
			letters[i] = Inverted[letter.replace('...', '-').replace('*','')]
	pSum = 0
	for c in letters:
		pSum += ord(c.upper())
	parityCalculated = chr((65 + pSum) % 26)
	if parity == parityCalculated:
		print('Checksums match')
	else:
		print('Checksums do not match')

def dlOperations(msgList, address):
	processToAddress(msgList[0], thisAddress)
	processFromAddress(msgList[1])
	processChecksum(msgList[2], msgList[7]) # second argument will have to be changed after all headers are decided, unsure of which segment is the payload
	return msgList[3:]