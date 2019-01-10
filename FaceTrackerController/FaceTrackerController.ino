#include <AccelStepper.h>


// Define a stepper motor 1 for arduino 
// direction Digital 9 (CW), pulses Digital 8 (CLK)
AccelStepper vertStepper(1, 7, 6);
AccelStepper horStepper(1, 9, 8);

int yFreedom = 200;
int yCenter = 0;
int xFreedom = 200;
int xCenter = 0;
int xSpeed = 1;
int ySpeed=1;

char dir = 'C';

void setup()
{  
  Serial.begin(9600);
  while(!Serial);
  // Change these to suit your stepper if you want
  vertStepper.setMaxSpeed(1000);//1100
  vertStepper.setAcceleration(300);
  vertStepper.moveTo(yCenter);
  
  horStepper.setMaxSpeed(1000);//1100
  horStepper.setAcceleration(300);
  horStepper.moveTo(xCenter);


        
}

void loop()
{
if (Serial.available() > 0) {
        // read the incoming byte:
        char prevDir = dir;
        dir = Serial.read();

        if(dir =='S'){
          if(prevDir == 'D'||prevDir == 'U' ){
            vertStepper.setMaxSpeed(200);//1100
            vertStepper.setAcceleration(500); 
            ySpeed=0;
          }
          if(prevDir == 'L'||prevDir == 'R' ){
            horStepper.setMaxSpeed(200);//1100
            horStepper.setAcceleration(500); 
            xSpeed=0;
          }
        }
        if(dir =='F'){
          if(prevDir == 'D'||prevDir == 'U' ){
            vertStepper.setMaxSpeed(5000);//1100
            vertStepper.setAcceleration(2000); 
            ySpeed=1;
          }
          if(prevDir == 'L'||prevDir == 'R' ){
            horStepper.setMaxSpeed(5000);//1100
            horStepper.setAcceleration(2000); 
            xSpeed=1;
          }
        }
        
//        int speed = Serial.read();
        
        if(dir=='U'){
          //Serial.println(speed);
          moveUp(1000);
        }
        if(dir=='D'){
          moveDown(1000);
        }
        if(dir=='L'){
          //Serial.println(speed);
          moveLeft(1000);
        }
        if(dir=='R'){
          moveRight(1000);
        }
        if(dir=='C'){
          vertStepper.moveTo(yCenter);
          horStepper.moveTo(xCenter);
        }
        
        
}

        
//  vertStepper.run();

  
//    // If at the end of travel go to the other end
//    if (vertStepper.distanceToGo() == 0){
//      vertStepper.moveTo( -vertStepper.currentPosition() );
//    }
//    
    vertStepper.run();
    horStepper.run();
}

void moveUp(int speed){
  if(ySpeed==0){
  vertStepper.moveTo(constrain(vertStepper.currentPosition()-10,yCenter-yFreedom,yCenter+yFreedom));
  }else{
      vertStepper.moveTo(constrain(vertStepper.currentPosition()-50,yCenter-yFreedom,yCenter+yFreedom));

  }
}
void moveDown(int speed){
if(ySpeed==0){
  vertStepper.moveTo(constrain(vertStepper.currentPosition()+10,yCenter-yFreedom,yCenter+yFreedom));
  }else{
      vertStepper.moveTo(constrain(vertStepper.currentPosition()+50,yCenter-yFreedom,yCenter+yFreedom));

  }
}
void moveLeft(int speed){
if(xSpeed==0){
  horStepper.moveTo(constrain(horStepper.currentPosition()-10,xCenter-xFreedom,xCenter+xFreedom));
  }else{
      horStepper.moveTo(constrain(horStepper.currentPosition()-50,xCenter-xFreedom,xCenter+xFreedom));

  }
}
void moveRight(int speed){
if(xSpeed==0){
  horStepper.moveTo(constrain(horStepper.currentPosition()+10,xCenter-xFreedom,xCenter+xFreedom));
  }else{
      horStepper.moveTo(constrain(horStepper.currentPosition()+50,xCenter-xFreedom,xCenter+xFreedom));

  }
}
