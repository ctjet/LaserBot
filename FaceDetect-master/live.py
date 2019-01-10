# This script will detect faces via your webcam.
# Tested with OpenCV3

import cv2
import serial
import requests



cap = cv2.VideoCapture(0)

# Create the haar cascade
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")



ser = serial.Serial('COM23') #Change this com port if needed
deadzone = 10 #Don't move if in the deadzone. This is a radius from the center prevents oscillation
shouldShoot=True #Should you shoot at all, useful for laser pointer mode
shootingRadius = 40 #Shoot when the face's center is withing this value of the center
shootingWidth = 30 #Shoot only if the width of the detected face is greater than this. Set to zero to shoot whenever centered
aimForEye=False
aimForEyeXRatio = 0.3
aimForEyeYRatio = 0.4

def clamp(n, smallest, largest): return max(smallest, min(n, largest))


def getSpeed(val):
	if(val<100):
		return b'S'
	return b'F'

def shoot():
	print("You don screwed up")
	if (shouldShoot):
		url = 'http://192.168.1.185'
		payload = {'key1': 'value1', 'key2': 'value2'}

		# GETqqqqqq
		r = requests.get(url+'/ledOn')


def movementDir(point, center):
	px, py = point
	cx, cy = center
	sent = False
	

	if(px>cx+deadzone):
		ser.write(b'R')
		ser.write(getSpeed(px-cx))
		print('R')
		# ser.write(clamp(px-cx,0,255))
		sent = True
	if(deadzone+px<cx):
		ser.write(b'L')
		ser.write(getSpeed(-px+cx))
		print('L')
		sent = True

	if(py>cy+deadzone):
		print('D')
		
		ser.write(b'D')
		ser.write(getSpeed(py-cy))
		print(getSpeed(py-cy))
		# ser.write(clamp(py-cy,0,255))
		# print(clamp(py-cy,0,255))
		sent = True
	if(deadzone+py<cy):
		print('U')
		ser.write(b'U')
		ser.write(getSpeed(cy-py))
		print(getSpeed(cy-py))
		# ser.write(clamp(-py+cy,0,255))
		# print(clamp(-py+cy,0,255))
		sent = True
	if(sent == False):
		print('N')
		ser.write(b'N')
		
	# return string #Do Nothing


while(True):
	# Capture frame-by-frame
	ret, frame = cap.read()

	# Our operations on the frame come here
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# Detect faces in the image
	faces = faceCascade.detectMultiScale(
		gray,
		scaleFactor=1.1,
		minNeighbors=5,
		minSize=(30, 30)
		#flags = cv2.CV_HAAR_SCALE_IMAGE
	)

	# print("Found {0} faces!".format(len(faces)))

	# Draw a rectangle around the faces
	for (x, y, w, h) in faces:
		cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
		
		
	height, width, channels = frame.shape
	center = (int(width/2),int(height/2))
	pt = (0,0)
	if(len(faces)>0):
		(x, y, w, h) = faces[0]
		if(aimForEye):
			pt = (int(x+w*aimForEyeXRatio),int(y+h*aimForEyeYRatio))
		else:
			pt = (int(x+w/2),int(y+h/2))
		cv2.circle(frame,pt,5,(0,0,255))
		# print(pt)
		movementDir(pt,center)

		if(w>shootingWidth):
			if((pt[0]-center[0])**2+(pt[1]-center[1])**2<=shootingRadius**2):
				shoot()

		


		# for char in movementDir(pt,center).encode():
		# 	ser.write(char)
		# ser.write(bytearray(movementDir(pt,center), 'ASCII')) #return to center
		
		# print(movementDir(pt,center))
	else:
		pt = center
		cv2.circle(frame,pt,5,(0,0,255))
		# print('No faces found')
		ser.write(b'CC') #return to center
		print('C')



	# Display the resulting frame
	cv2.imshow('frame', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break



# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
ser.close()