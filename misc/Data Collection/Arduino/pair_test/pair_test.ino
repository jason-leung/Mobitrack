void setup() {
    Serial.begin(115200);
}
 
void loop()
{
    if(Serial.available())
    {
        Serial.print("received: ");
        Serial.write(Serial.read());
        Serial.println("");
    }
}
