#include "Wire.h" // this line must go before everything else
#include "I2Cdev.h"
#include "MPU6050_6Axis_MotionApps20.h"
    
// Set up MPU6050 variables
MPU6050 accelgyro;
int16_t ax,ay,az, gx, gy, gz;

// Set up state variables
int16_t state = 0;

void setup() {
    Wire.begin();
    accelgyro.initialize();
    accelgyro.setXGyroOffset(77);
    accelgyro.setYGyroOffset(34);
    accelgyro.setZGyroOffset(-24);
    accelgyro.setXAccelOffset(-2390);
    accelgyro.setYAccelOffset(-482);
    accelgyro.setZAccelOffset(1188);
    Serial.begin(115200);
}

void loop() {
  // Get state
  if(Serial.available())
  {
      state = Serial.read();
  }

  // Stream IMU data if state = 1
  if(state == 49){
    // Read data
    accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
    
    // Print data to serial
    // Format: ax, ay, az, gx, gy, gz
    
    delay(10);
    Serial.println("");
    Serial.print(ax);
    Serial.print(",");
    Serial.print(ay);
    Serial.print(",");
    Serial.print(az);
    Serial.print(",");
    Serial.print(gx);
    Serial.print(",");
    Serial.print(gy);
    Serial.print(",");
    Serial.print(gz);
  }
}
