#import libraries -----------------------------------------------------------------------------------------------------------------------------------------------------
from PIL import Image
from time import sleep

#define functions -----------------------------------------------------------------------------------------------------------------------------------------------------
def resizeImage(img):
	#size = 200,200
	state = True
	w,h = img.size
	while state:
		if img.size>(250,250):
			w, h = w/2, h/2
			newSize = w,h
			img = img.resize(newSize, Image.ANTIALIAS)
		else:
			state = False
	return img;
#EnviroPi_20160223_095210.jpg	
baseName = "amazon 2"
sortImg = "jpg"
a = 3
b = -1
c = ""
	
#witchImg = baseName + str(a) +"_" + c + str(b) + "." + sortImg
witchImg = baseName + "." + sortImg
print witchImg
im = Image.open(witchImg)
im = resizeImage(im)
pix = im.load()
x,y = 0,0
width, height = im.size
length = (width*height)-1

veg = (34, 139, 34)
wat = (0, 255, 255)

green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)
black = (0,0,0)

#start script ---------------------------------------------------------------------------------------------------------------------------------------------------------
print("size : " + str(im.size))
print("width : " + str(width))
print("height : " + str(height))
print("length : " + str(length))
#sleep(1)

for i in range(0,length):
	print("x : " + str(x) + " y : " + str(y) + " i : " + str(i))
	print(pix[x,y])
	valueR, valueG, valueB = pix[x,y]
	value = pix[x,y]

	if valueG> valueB and valueR<100:
		pix[x,y] = green

	if valueB > valueG and valueR>100:
		pix[x,y] = blue
	if valueR>180 and valueG>180 and valueB>180:
		pix[x,y] = white
	if valueR<80 and valueG<80 and valueB<80:
		pix[x,y] = black

	if x<width-1:
		x = x + 1
	else:
		x = 0
		y = y + 1


im.save(witchImg + " (processed)." +sortImg)
print "saved as " + witchImg + " (processed)." +sortImg
#os.remove(witchImg)
