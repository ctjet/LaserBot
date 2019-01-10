#include <AccelStepper.h>


// Define a stepper motor 1 for arduino 
// direction Digital 9 (CW), pulses Digital 8 (CLK)
AccelStepper vertStepper(1, 7, 6);
AccelStepper horStepper(1, 9, 8);

int yFreedom = 200;
int yCenter = 0;
int xFreedom = 200;
int xCenter = 0;

String tempModify;
char buff[32];
int index = 0;

bool okDebounce = true;

void setup()
{  
  Serial.begin(9600);
  while(!Serial);
  // Change these to suit your stepper if you want
  vertStepper.setMaxSpeed(5000);//1100
  vertStepper.setAcceleration(3000);
  vertStepper.moveTo(yCenter);
  
  horStepper.setMaxSpeed(5000);//1100
  horStepper.setAcceleration(3000);
  horStepper.moveTo(xCenter);


        
}

void loop()
{
  if (Serial.available() > 0) {
    char b = Serial.read();
    buff[index] = b;
    index++;

    if(b=='\n'){ 
      buff[index] = '\0';
      index = 0;
      tempModify = String(buff);
      

     vertStepper.moveTo(min(max(parseDataY(tempModify),-yFreedom),yFreedom)+yCenter);
      horStepper.moveTo(min(max(parseDataX(tempModify),-xFreedom),xFreedom)+xCenter);
      okDebounce=true;
    }
  
  }
    if(vertStepper.distanceToGo()==0&&horStepper.distanceToGo()==0&&okDebounce){
      Serial.println("OK");
      okDebounce=false;
    }
    
    vertStepper.run();
    horStepper.run();
}

//void serialEvent() {
//    tempModify = Serial.readString();
//    Serial.println(tempModify);
////    serX.write(parseDataX(tempModify));
////    serY.write(parseDataY(tempModify));
//    vertStepper.moveTo(max(min(parseDataY(tempModify),-yFreedom),yFreedom));
//    horStepper.moveTo(max(min(parseDataX(tempModify),-xFreedom),xFreedom));
//}

int parseDataX(String data){
    data.remove(data.indexOf(":"));
    data.remove(data.indexOf("X"), 1);
    return data.toInt();
}

int parseDataY(String data){
    data.remove(0,data.indexOf(":") + 1);
    data.remove(data.indexOf("Y"), 1);
    return data.toInt();
}

