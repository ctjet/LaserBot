# -*- coding: utf-8 -*-


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
shootingRadius = 50 #Shoot when the face's center is withing this value of the center
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

import os

import google.oauth2.credentials

import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

import time
import os

pewdsShouldShoot=False

ONLY_PEWDS = 1
NEUTRAL=0
ONLY_TSERIES = 2
EVIL_NEUTRAL=3

state = NEUTRAL

from pygame import mixer # Load the required library

mixer.init()
def playSound(name):
    mixer.music.load(os.path.dirname(__file__)+'/'+name)
    mixer.music.play()

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def print_response(response):
  print(response)

# Build a resource based on a list of properties given as key-value pairs.
# Leave properties with empty values out of the inserted resource.
def build_resource(properties):
  resource = {}
  for p in properties:
    # Given a key like "snippet.title", split into "snippet" and "title", where
    # "snippet" will be an object and "title" will be a property in that object.
    prop_array = p.split('.')
    ref = resource
    for pa in range(0, len(prop_array)):
      is_array = False
      key = prop_array[pa]

      # For properties that have array values, convert a name like
      # "snippet.tags[]" to snippet.tags, and set a flag to handle
      # the value as an array.
      if key[-2:] == '[]':
        key = key[0:len(key)-2:]
        is_array = True

      if pa == (len(prop_array) - 1):
        # Leave properties without values out of inserted resource.
        if properties[p]:
          if is_array:
            ref[key] = properties[p].split(',')
          else:
            ref[key] = properties[p]
      elif key not in ref:
        # For example, the property is "snippet.title", but the resource does
        # not yet have a "snippet" object. Create the snippet object here.
        # Setting "ref = ref[key]" means that in the next time through the
        # "for pa in range ..." loop, we will be setting a property in the
        # resource's "snippet" object.
        ref[key] = {}
        ref = ref[key]
      else:
        # For example, the property is "snippet.description", and the resource
        # already has a "snippet" object.
        ref = ref[key]
  return resource

# Remove keyword arguments that are not set
def remove_empty_kwargs(**kwargs):
  good_kwargs = {}
  if kwargs is not None:
    for key, value in kwargs.items():
      if value:
        good_kwargs[key] = value
  return good_kwargs

def subscriptions_list_by_channel_id(client, **kwargs):
  # See full sample for function
  kwargs = remove_empty_kwargs(**kwargs)

  response = client.subscriptions().list(
    **kwargs
  ).execute()
  
  #print_response(response)
  return response



if __name__ == '__main__':
	# When running locally, disable OAuthlib's HTTPs verification. When
	# running in production *do not* leave this option enabled.
	os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
	client = get_authenticated_service()
	timeSinceCheck = time.time()
	while(True):

		if(time.time()-timeSinceCheck>1):
			timeSinceCheck = time.time()
			response = subscriptions_list_by_channel_id(client, part='snippet,contentDetails', channelId='UCtpR_LxM6ib96ehx7rHDffg')
			if "T-Series" in str(response):
				if "PewDiePie" in str(response):
					print("PEWD AND TSERIES")   
				
				elif(state==NEUTRAL):
					playSound('Turret_turret_deploy_3.wav')
					pewdsShouldShoot = True
					state = ONLY_TSERIES
					print("ONLY TSERIES")
			elif "PewDiePie" in str(response):
				if(state == ONLY_TSERIES):
					state = NEUTRAL
					print("No TSERIES")
					pewdsShouldShoot = False
					playSound('Turret_turret_retire_2.wav')
			else:
				print("NEUTRAL")
        

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
		if(pewdsShouldShoot):
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
			else:
				pt = center
				cv2.circle(frame,pt,5,(0,0,255))
				# print('No faces found')
				ser.write(b'CC') #return to center
				print('C')
		else:
			pt = center
			cv2.circle(frame,pt,5,(0,0,255))
			# print('No faces found')
			ser.write(b'ZZ') #return to center
			print('Z')


		# Display the resulting frame
		cv2.imshow('frame', frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break



	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()
	ser.close()