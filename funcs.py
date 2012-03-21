from Crypto.Cipher import DES
from bitstring import BitArray
import itertools
import sys
import copy

L = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']

odd_parity = dict()
for i in range(pow(2,7)):
	k = BitArray(uint=i, length=7)
	p = copy.copy(k)
	if k.count(1)%2 == 0: p.append('0b1')
	else: p.append('0b0')
	odd_parity[k.bin] = p.tobytes()

def replace(indices, elements, keylist):
	for i in range(len(indices)):
		keylist[indices[i]] = elements[i]


def DES_crypt(keybits, plainbytes, mode):
	rev_keybytes = ''
	for k in range(0, 56, 7):
		rev_keybytes += (odd_parity[keybits[k:k+7]])

	obj = DES.new(rev_keybytes, DES.MODE_ECB)
	if mode == True:
		cipherbytes = obj.encrypt(plainbytes)
	else:
		cipherbytes = obj.decrypt(plainbytes) 
	return cipherbytes

def double_DES(key, plain):
	keybits = BitArray(hex = key)
	plainbits= BitArray(hex = plain)


	if len(keybits) != 112:
		print "length of double DES key is not 112 bits!"
		return
	if len(plainbits) != 64:
		print "length of double DES plain text is not 64 bits!"
		return

	rev_keybytes = ''
	for k in keybits.cut(7):
		rev_keybytes += (odd_parity[k.bin])

	obj1 = DES.new(rev_keybytes[0:8], DES.MODE_ECB)
	midbytes = obj1.encrypt(plainbits.tobytes())
	obj2 = DES.new(rev_keybytes[8:16], DES.MODE_ECB)
	cipherbytes = obj2.encrypt(midbytes)
	return BitArray(bytes = cipherbytes).hex




def break_2DES(plain, cipher, key):

	plainbytes = BitArray(hex = plain).tobytes()
	cipherbytes = BitArray(hex = cipher).tobytes()
	keylist = list(key)
	key1list = keylist[0:14]
	key2list = keylist[14:28]
	key1indices = [i for i, x in enumerate(key1list) if x == "?"]
	key2indices = [i for i, x in enumerate(key2list) if x == "?"]
	mode = True

	if len(key1indices) > len(key2indices):
		key1list, key2list = key2list, key1list
		key1indices, key2indices = key2indices, key1indices
		plainbytes, cipherbytes = cipherbytes, plainbytes
		mode = False	
	
	table = dict()

	first_candidatelist = list(itertools.product(L, repeat = len(key1indices)))
	for first_candidate in first_candidatelist:
		replace(key1indices, first_candidate, key1list)
		first_string = ''.join(key1list)
		midbytes = DES_crypt(BitArray(hex = first_string).bin, plainbytes, mode)
		table[midbytes] = first_string
	del first_candidatelist

	second_candidatelist = list(itertools.product(L, repeat = len(key2indices)))
	for second_candidate in second_candidatelist:
		replace(key2indices, second_candidate, key2list)
		second_string = ''.join(key2list)
		midbytes = DES_crypt(BitArray(hex = second_string).bin, cipherbytes, not mode)
		if table.has_key(midbytes):
			if mode:
				return table[midbytes] + second_string
			else:
				return second_string + table[midbytes] 
			
	print "no key found!"
	return
