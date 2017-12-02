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

#set variables --------------------------------------------------------------------------------------------------------------------------------------------------------
im = Image.open("amazon 2.jpg")
im = resizeImage(im)
pix = im.load()
x,y = 0,0
width, height = im.size
length = (width*height)-1
green = (0,255,0)
blue = (0,0,255)

#start script ---------------------------------------------------------------------------------------------------------------------------------------------------------
print("size : " + str(im.size))
print("width : " + str(width))
print("height : " + str(height))
print("length : " + str(length))
sleep(5)

for i in range(0,length):
	print("x : " + str(x) + " y : " + str(y) + " i : " + str(i))
	print(pix[x,y])
	valueR, valueG, valueB = pix[x,y]
	
	if valueG > valueB:
		pix[x,y] = green
	if valueB > valueG:
		pix[x,y] = blue
		
	if x<width-1:
		x = x + 1
	else:
		x = 0
		y = y + 1

im.save("new5.png")
print "saved"
