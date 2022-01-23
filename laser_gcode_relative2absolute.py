import sys
import re
import random

CLUSTERS = 20

rg0 = re.compile("^G0 X")
rxy = re.compile("G(.) X([^ ]*) Y([^ $]*)")
rm2 = re.compile("^M2")
rg91 = re.compile("^^G91")
rg90 = re.compile("^^G90")

if len(sys.argv) != 3:
	print("Usage: %s <gcode file in> <gode file out>" % sys.argv[0])
	exit()

filein = sys.argv[1]
fileout  = sys.argv[2]

rel = 0
X = 0
Y = 0
bufout = []
##########################################
# Parse input file and create GO blocks 
##########################################

with open(filein,'r') as f:
	for line in f:
		if rg91.search(line):
			# relative
			rel = 1
		if rg90.search(line):
			# absolute
			rel = 0
		if rel == 0:
			md = rxy.search(line)
			if md:
				X = float(md.group(2))
				Y = float(md.group(3))
			bufout.append(line[:-1])
		else:
			md = rxy.search(line)
			if md:
				c = md.group(1)
				x = float(md.group(2))
				y = float(md.group(3))
				X += x
				Y += y
				bufout.append("G%c X%f Y%f" % (c,X,Y))
			else:
				if rg91.search(line):
					bufout.append("G90")
				else:
					bufout.append(line[:-1])

with open(fileout,"w") as f:		
	for line in bufout:
		f.write(line + '\n')


		
