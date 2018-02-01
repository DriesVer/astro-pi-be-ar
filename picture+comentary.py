#Import libraries ------------------------------------------------------------------------------------------------------------------------------
from PIL import Image			#Library for examining the picture.			sudo apt-get install python-PIL
from picamera import PiCamera		#Library for using the camera.
from sense_hat import SenseHat		#Library for using the Sense Hat.
import time				#Library for using wait functions and get the time.
import csv				#Library for writing CSV-files.
#Define functions ----------------------------------------------------------------------------------------------------------------------------------
def resizeImage(img):							#Functions ask after an image.
	maxSize = 300,300						#Max size of the image in width and height
	state = True							#State for getting in the while loop.
	w,h = img.size							#The original height (h) and wdth (w).
	while state:
		if img.size > maxSize:					#If the size of the image is smaller than te max size
			w, h = w/2, h/2					#The width (w) and height (h) wil be divided by 2.
			newSize = w,h					#The new size equals the new width AND HEIGHT.
			img = img.resize(newSize, Image.ANTIALIAS)	#The image wil be resized to the new size.
		else:
			state = False					#If the image is the right size, state wil be false and the wile loop stops.
	return img;							#The resized image wil be returned

#set variables and objects -----------------------------------------------------------------------------------------------------------------
camera = PiCamera()					#Set the object camera for later use of the camera.
sense = SenseHat()					#Set the object sebse for later use of the Sense Hat.

green = (0,255,0)					#Setting colors for easy use later in the script.
blue = (0,0,255)
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)

imgBase = "VegCam_"					#Name of the picture
imgNumb = 1						#Nummber of the picture
imgSort = ".jpg"					#Sort of Image

x,y = 0,0						#Setting start coordinate examination of the picture

countG = 0						#Setting counting variables for counting how many of that specific color has been found in the picture.
countB = 0
countW = 0

display = [ ]						#Name of list of colors that wil be displayed on the Sense Hat

timeStart = time.ctime()				#The time on the moment when the script starts.

with open("trackingTime.csv", "wb") as csvfile:		#Open a new CSV-file with the start time
	w = csv.writer(csvfile)				#Setting w as a CSV-writer
	w.writerow(["Start time: " + timeStart])	#Write in the CSV-file the starttime
	w.writerow([])					#Write an enter.

#start script-------------------------------------------------------------------------------------------------------------------------------------

camera.start_preview()						#Starting the camera.

while(True):
	imgName = imgBase + str(imgNumb) + imgSort		#Setting the image name.
	camera.capture(imgName)					#Capturing a picture of space.
	timeNow = time.ctime()					#Getting the tile on the current moment.
	with open("trackingTime.csv", "a") as csvfile:		#Opening again the CSV-file.
		w = csv.writer(csvfile)				#Setting w as a CSV-writer
		w.writerow([timeNow + "  ||  " + imgName])	#Writing the time and the name in the CSV-file.
	sense.set_pixel(7,7,red)				#Setting a pixel int he corner red for indicating that he capture it. Also for showing that he isn't blocked.

	im = Image.open(imgName)				#Open the image that is captured.
	im = resizeImage(im)					#Resizing the picture in a function. (See functions for explenation.
	pix = im.load()						#Load the pixels in from the image.

	width, height = im.size					#Setting width and height to the width and height of the picture
	length = (width*height)-1				#Length equals the afiche of the image minus 1 because a list starts telling at 0. (The list of pixels)
	"""
	print("size : " + str(im.size))				#Was printing the size of the image.
	print("width : " + str(width))				#The printing is removed to win time.
	print("height : " + str(height))
	print("length : " + str(length))
	"""
	for i in range(0,length):
		#print("x : " + str(x) + " y : " + str(y) + " i : " + str(i))	#Was printing the position of the pixel.
		#print(pix[x,y])						#Was printing the color of the pixel.
		valueR, valueG, valueB = pix[x,y]				#Setting the RGB-values of the pixel to 3 seperate variables.
	
		if valueG > valueB and valueR<100:				#Cheking of the pixel is green.
			pix[x,y] = green					#If green he sets the pixel to pure green.
			countG = countG + 1					#Add to the counter of green 1.
		if valueB > valueG and valueR>100:				#Cheking of the pixel is blue.
			pix[x,y] = blue						#If blue he sets the pixel to pure blue.
			countB = countB + 1					#Add to the counter of blue 1.
		if valueR>220 and valueG>220 and valueB>220:			#Same as above but for white.
			pix[x,y] = white								
			countW = countW + 1							
		if valueR<20 and valueG<20 and valueB<20:			#Same as above but for black. Black isn't counted because the counting is for the display and black don't shine.
			pix[x,y] = black								
		
		
		if x<width-1:							#Setting the coordinates for the next pixel in the row.
			x = x + 1
		else:								#If he is at the end of the row he gos to the next row.
			x = 0
			y = y + 1

	#im.save(imgBase + str(imgNumb) + "(processed)" + imgSort)	#He's saving the image under the same name but with "(processed)"
	#print "saved as " + imag + " (processed)" +imgSort		#Was printing that he saved it.

	senseB = int(float(countB)/length*63)				#Calculating the procents but because the sense hat is 8x8 and one pixel is for indicate process.
	senseG = int(float(countG)/length*63)				#He calculate it for 63.
	senseW = int(float(countW)/length*63)				#He divided the count of the color with the amount of pixels in the image and multiply it with 63.
									#The division nbeeds a float (other wise is the answer always 0) but the for loops needs a intiger.
	for i in range(0,senseB):					#Adding the colors to the display for giving a percentage
		display.append(blue)
	for i in range(0,senseG):
		display.append(green)
	for i in range(0,senseW):
		display.append(white)

	sense_colors = len(display)					#Getting the length of the list display with the colors.
	for i in range(0, 64-sense_colors):				#Adding black leds to display for that the length of display equals 64. (For no erors.)
		display.append(black)
	sense.set_pixels(display)					#Setting the display on the screen.
	
	imgNumb = imgNumb + 1						#Chaching the image number with 1

camera.stop_preview()							#Stopping the camera.
