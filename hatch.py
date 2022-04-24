from PIL import Image, ImageFilter
import sys

if len(sys.argv) !=3:
	print("Usage %s #hatch filename")
	exit(0)

H = int(sys.argv[1])
filename = sys.argv[2]

#H = 4
image = Image.open(filename)
image = image.convert('L')
#edges = image.filter(ImageFilter.FIND_EDGES) 
#edges = image.filter(ImageFilter.EMBOSS)
edges = image.filter(ImageFilter.Kernel((3, 3), (-1, -1, -1, -1, 8, -1, -1, -1, -1), 1, 0))
#edges = edges.filter(ImageFilter.Kernel((3, 3), (1,1,1,1,-8,1,1,1,1), 1, 0))
#edges.show()
w,h = image.size
out = Image.new('L',(w,h))
for y in range(h):
	for x in range(w):
		p = edges.getpixel((x,y))
		if p < 128:
			if ((x+y)%H==0):
				q = image.getpixel((x,y))
			else:
				q = 255
		else:
			#q = image.getpixel((x,y))		
			#q = 255 - p
			q = 255 - p
		out.putpixel((x,y),q)
		
out.show()
out.save('out.png', 'png')
