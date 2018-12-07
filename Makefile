all:
	python 5hellC0der.py
	as rshell.s -o rshell.o
	ld -N rshell.o -o rshell
	objcopy -O binary rshell rshell.bin
	hexdump -v -e '"\\""x" 1/1 "%02x" ""' rshell.bin > opcode
	clear
	cat opcode

clear:
	rm r*
