import sys
import re
import random

CLUSTERS = 20

rg0 = re.compile("^(G0|G00) X")
rxy = re.compile("X([^ ]*) Y([^ $]*)")
rm2 = re.compile("^(M2|M02)")
rg91 = re.compile("^G91")
rgx = re.compile("^(G.|G0.) X")

if len(sys.argv) != 3:
	print("Usage: %s <gcode file in> <gode file out>" % sys.argv[0])
	exit()

filein = sys.argv[1]
fileout  = sys.argv[2]

block = []
GOBlocks = []
top = []

number = 0
segmentIn2index = []
segmentOut = []



##########################################
# Parse input file and create GO blocks 
##########################################
lastG = ""
with open(filein,'r') as f:
	for line in f:
		if rg91.search(line):
			print("Error: Can't deal with relative coordonate mode")
			exit()
		if rg0.search(line):
			if number == 0:
				top = block
			else:
				GOBlocks.append(block)
				if len(lastG) > 0:
					md = rxy.search(lastG)
					if md:
						x = float(md.group(1))
						y = float(md.group(2))
						segmentOut.append((x,y))
				lastG = ""
			block=[]			
			md = rxy.search(line)
			if md:
				x = float(md.group(1))
				y = float(md.group(2))
				segmentIn2index.append((x,y,number))
			number+=1
		# elif rm2.search(line):
			# GOBlocks.append(block)
			# block = []	
		if rgx.search(line):
			lastG = line				
		block.append(line[:-1])
if len(block) > 1:
	#print(block)
	GOBlocks.append(block)
	if len(lastG) > 0:
		md = rxy.search(lastG)
		if md:
			x = float(md.group(1))
			y = float(md.group(2))
			segmentOut.append((x,y))	
		lastG = ""
		
print("Number of G0 blocks: %d" %len(GOBlocks))
print("GO index size %d" % len(segmentIn2index))
print("GO out size %d" % len(segmentOut))

# for i in range(len(segmentIn2index)):
	# print(segmentIn2index[i][0],segmentIn2index[i][1],segmentOut[i][0],segmentOut[i][1])
	


listin = segmentIn2index.copy()
listout = []
listout.append(listin[0])
#current = listin[0]
current = segmentOut[0]
del listin[0]
n = len(listin)
while( n > 0 ):
	d2min = float("inf")
	index = 0

	for i in range(n):
		dist2 = (current[0] - listin[i][0])**2 + (current[1] - listin[i][1])**2
		if dist2 < d2min:
			index = i
			d2min = dist2
	listout.append(listin[index])
	current = segmentOut[listin[index][2]]
	#current = listin[index]
	del listin[index]
	n-=1
	
print("final size %d" % len(listout))
reorder = [top]
for item in listout:
	reorder.append(GOBlocks[item[2]])

with open(fileout,"w") as f:		
	for arr in reorder:
		for line in arr:
			f.write(line + '\n')
	f.write("M2" + '\n')


		
