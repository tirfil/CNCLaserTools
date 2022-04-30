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
hedges = image.filter(ImageFilter.Kernel((3, 3), (-1, 0, -1, -2, 0, 2, -1, 0, 1), 1, 0))
vedges = image.filter(ImageFilter.Kernel((3, 3), (1, 2, 1, 0,0,0 , -1, -2, -1), 1, 0))

#hedges.show()
#vedges.show()
w,h = image.size
edges = Image.new('L',(w,h))
for y in range(h):
	for x in range(w):
		a = hedges.getpixel((x,y))
		b = vedges.getpixel((x,y))
		val = int((a+b)/2)
		edges.putpixel((x,y),val)
edges.show()
		
edges.save('edges.png','png')
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

