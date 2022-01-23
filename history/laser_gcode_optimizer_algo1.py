import sys
import re

CLUSTERS = 9

rg0 = re.compile("^G0")
rxy = re.compile("X([^ ]*) Y([^ $]*)")
rm2 = re.compile("^M2")

if len(sys.argv) != 3:
	print("Usage: %s <gcode file in> <gode file out>" % sys.argv[0])
	exit()

filein = sys.argv[1]
fileout  = sys.argv[2]

block = []
GOBlocks = []
top = []

number = 0
xy2index = []

xmin = float("inf")
xmax = -float("inf")
ymin = float("inf")
ymax = -float("inf")

##########################################
# Parse input file and create GO blocks 
##########################################

with open(filein,'r') as f:
	for line in f:
		if rg0.search(line):
			if number == 0:
				top = block
			else:
				GOBlocks.append(block)
			block=[]			
			md = rxy.search(line)
			if md:
				x = float(md.group(1))
				y = float(md.group(2))
				if (x > xmax): xmax = x
				if (x < xmin): xmin = x
				if (y > ymax): ymax = y
				if (y < ymin): ymin = y
				xy2index.append((x,y,number))
			number+=1
		elif rm2.search(line):
			GOBlocks.append(block)
			block = []					
		block.append(line[:-1])
if len(block) > 1:
	GOBlocks.append(block)
		
print("Number of G0 blocks: %d" %len(GOBlocks))
print("GO index size %d" % len(xy2index))

##########################################
# Create 9 clusters
##########################################

#print(xy2index)
print("X range: ",(xmin,xmax))
print("Y range: ",(ymin,ymax))

xm = (xmax-xmin)/2 + xmin
ym = (ymax-ymin)/2 + ymin



cluster_centers = [(xmin,ymin),(xm,ymin),(xmax,ymin),(xmin,ym),(xm,ym),(xmax,ym),(xmin,ymax),(xm,ymax),(xmax,ymax)]
cluster_table = [[],[],[],[],[],[],[],[],[]]

print("number of item per cluster:")

for j in range(10):
	sys.stdout.write("\tIteration %d : " % j)
	cluster_table = [[],[],[],[],[],[],[],[],[]]
	for item in xy2index:
		d2min = float("inf")
		indice = 0
		for i in range(CLUSTERS):
			dist2 = (cluster_centers[i][0] - item[0])**2 + (cluster_centers[i][1]- item[1])**2
			if dist2 < d2min:
				d2min = dist2
				indice = i
		cluster_table[indice].append(item)
		
	for i in range(CLUSTERS):
		n = len(cluster_table[i])
		sys.stdout.write(str(n) + " ")
		if (n >0):
			x = 0
			y = 0
			for pt in cluster_table[i]:
				x+=pt[0]
				y+=pt[1]
			cluster_centers[i] = (x/n,y/n)
	print("")	

print("Cluster centers:")	
for pt in cluster_centers:
	print("\t%s" % repr(pt))
	
# sort each luster_indexes
for i in range(CLUSTERS):
	temp=[]
	temp = sorted(cluster_table[i],key=lambda v : v[1])
	cluster_table[i] = temp
	
reorder = [top]
for i in range(CLUSTERS):
	for item in cluster_table[i]:
		#print(pt[0],pt[1],GOBlocks[pt[2]][0])
		reorder.append(GOBlocks[item[2]])

with open(fileout,"w") as f:		
	for arr in reorder:
		for line in arr:
			f.write(line + '\n')
	f.write("M2" + '\n')


		
