import sys
import re

rg0 = re.compile("^G0")
rg1 = re.compile("^G1")
rg2 = re.compile("^G2")
rg3 = re.compile("^G3")
rm2 = re.compile("^M2")

filein = sys.argv[1]

mode = 1

print("""G21 ; Set units to mm
G17 ; Select XY plane
G90 ; Set absolute coordinate mode
M5 ; Ensure LASER is turned off
G0 X0 Y0 F200 S0 ; Move to work origin
G91 ; Set relative coordinate mode""")

with open(filein,'r') as f:
	for line in f:
		if mode == 1:
			if rg0.search(line) or rm2.search(line):
				mode = 0
				print("M5")
		else:
			if rg1.search(line) or rg2.search(line) or rg3.search(line):
				mode = 1
				print ("M3 S300")
		print(line[:-1])
print("M5")
		
		
