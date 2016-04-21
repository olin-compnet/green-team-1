# from SetPin import SetPin
import time, string
import datalink_layer_receive as dl
import network_layer_recieve as nw
delimiters = ['**', '***', '****']

from MorseCode import MorseCode
Inverted = {MorseCode[letter]: letter for letter in MorseCode}
Numbers = {1: '.----', 2: '..---', 3: '...--', 4: '....-', 5: '.....', 6: '-....', 7: '--...', 8: '---..', 9: '----.', 10: '-----'}
InvertNumbers = {Numbers[n]: n for n in Numbers}

def splitAsterisks(incoming):
	out = []
	second = []
	first = incoming.split('**')
	for i in first:
		second += i.split('***')
	for j in second:
		out += j.split('****')
	return out

def process(input_message):
	input_message = input_message.split('*' * 15)[0].split('*' * 7)
	
	curMsg = nw.nwOperations(dl.dlOperations(input_message, address))

	incoming = curMsg[0]
	# Process message
	newwords = []
	words = incoming.split('*******')
	for w in words:
		letters = splitAsterisks(w)
		for i in range(len(letters)):
			letter = letters[i]
			letters[i] = Inverted[letter.replace('...', '-').replace('*','')]
		newwords.append(''.join(letters))
	return ' '.join(newwords)
