import serial
import requests
import time
import math
from PIL import Image, ImageDraw

subToPewds = [(65,29),(50,31),(40,44),(41,35),(50,45),(60,47),(66,54),(64,65),(54,68),(42,68),(34,62),(80,42),(79,50),(80,58),(81,67),(90,68),(99,69),(100,59),(100,50),(100,40),(114,25),(114,36),(114,45),(113,55),(113,64),(122,67),(132,64),(137,57),(137,45),(129,42),(123,44),(178,29),(188,29),(197,29),(206,29),(214,29),(193,39),(196,48),(195,55),(195,65),(232,42),(224,49),(223,58),(229,68),(240,66),(245,56),(242,46),(37,118),(37,129),(37,137),(36,148),(37,156),(46,138),(56,136),(59,127),(53,117),(44,116),(69,149),(77,146),(83,144),(90,140),(89,133),(80,131),(72,137),(72,154),(83,157),(92,155),(106,133),(105,142),(107,150),(111,160),(114,148),(118,141),(121,132),(124,140),(124,148),(126,156),(132,158),(135,150),(138,139),(139,131),(174,116),(174,124),(173,134),(174,144),(173,154),(164,157),(154,156),(150,148),(150,139),(157,132),(165,133),(203,133),(195,131),(188,136),(191,142),(200,145),(207,150),(202,158),(192,159),(186,155)]

ser = serial.Serial('COM23') #Change this com port if needed
def move(steps):
    ser.write(str.encode("X"+str(int(steps[0]))+":Y"+str(int(steps[1]))+"\n"))
    wait = True
    while(wait):
        read = ser.readline().decode("utf-8") 
        print(read)
        if "OK" in read:
            wait = False

# move((0,0))
shouldShoot=True #Should you shoot at all, useful for laser pointer mode
imgpts = subToPewds #which image to use
yFreedom = 200 #1/2 the number of steps it can take in the y direction
xFreedom = 200
stepsPerRev = 3200


mins = imgpts[0]
maxs =(0,0)


def shoot():
	print("You don screwed up")
	if (shouldShoot):
        
		url = 'http://192.168.1.185'
		payload = {'key1': 'value1', 'key2': 'value2'}

		# GET
		r = requests.get(url+'/ledOn')


while(True):
    shoot()



for pt in imgpts:
    mins = (min(pt[0],mins[0]),min(pt[1],mins[1]))
    maxs = (max(pt[0],maxs[0]),max(pt[1],maxs[1]))



    



def processPoint(pt):
    return (int( pt[0]-mins[0]-(maxs[0]-mins[0])/2),int(pt[1]-mins[1]-(maxs[1]-mins[1])/2))

processed = list(map(processPoint,imgpts))
    
# for pt in processed:
# #     x =int( pt[0]-mins[0]-(maxs[0]-mins[0])/2)
# #     y = int(pt[1]-mins[1]-(maxs[1]-mins[1])/2)
#     print(str(pt[0])+","+str(pt[1]))

def getMax(pts):
    maxs = pts[0]
    for pt in pts:
        maxs = (max(pt[0],maxs[0]),max(pt[1],maxs[1]))
    return max(maxs[0],maxs[1])



maxAngle = xFreedom/stepsPerRev*2*3.14159265359
z=getMax(processed)/math.tan(maxAngle)
# print (getMax(processed))
# print (maxAngle)
# print(z)

def calcSteps(pt,z):
    return (int(math.atan(pt[0]/z)*stepsPerRev/(2*3.14159265359)),int(math.atan(pt[1]/z)*stepsPerRev/(2*3.14159265359)))



def moveAndShoot(steps):
    move(steps)
    time.sleep(.2)
    shoot()
    time.sleep(.3)

im = Image.new("RGB",(500,500))

draw = ImageDraw.Draw(im)


# move((0,-200))
# move((0,0))

# move((0,-200))
# move((0,0))

# move((0,-200))
# move((0,0))

# move((0,-200))

# move((0,0))
# shoot()


# for pt in processed:
#     print(calcSteps(pt,z))
#     pt = calcSteps(pt,z)
#     draw.ellipse((pt[0]+200, pt[1]+200,pt[0]+205, pt[1]+205), fill=(255,0,0))
#     moveAndShoot(pt)
# #im.show()
# move((0,0))
# ser.close()