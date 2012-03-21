from funcs import *

fout = open('out.txt', 'a')
with open("in.txt") as f:
    for line in f:
	fout.write("input: " + line)
        in_args = line.split(' ')
	if (len(in_args) == 3) and (in_args[0] == 'double_des') :
		cipher = double_DES(in_args[1], in_args[2])
		fout.write("output: " + cipher + '\n')
	elif (len(in_args) == 4) and (in_args[0] == 'break_2des') :
		break_key = break_2DES(in_args[1], in_args[2], in_args[3])
		fout.write("output: " + break_key.upper() + '\n')
	else:
		fout.write("output: incorrect format!\n")
		fout.write("input format is:\ndouble_des + 112 bit key + 64 bit plain text\nbreak_2des + 64 bit plain text + 64 bit cipher text + 112 bit key\n")

fout.close()
