#include "I2Cdev.h"
#include "MPU6050_6Axis_MotionApps20.h"
#include "Wire.h"
    
// Set up MPU6050 variables
MPU6050 accelgyro;
int16_t ax,ay,az, gx, gy, gz;

void setup() {
    Wire.begin();
    accelgyro.initialize();
    Serial.begin(9600);
}

void loop() {
    // Read data
    accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
    
    // Print data to serial to be read by Matlab
    // Format:
    // ax, ay, az, gx, gy, gz
    
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

    //delay(10);
}
