int sensor1 = A0;
int sensor1val = 0.0;

void setup() {
  // put your setup code here, to run once:
Serial.begin(57600);
}

void loop() {
  // put your main code here, to run repeatedly:
/*sensor1val = map(analogRead(sensor1),0,1023,0,50);
sensor2val = map(analogRead(sensor2),0,1023,0,50);
*/
sensor1val = analogRead(sensor1);
sensor1val = map(sensor1val,300,400,0,100);
Serial.println(sensor1val);
//Serial.print("\t");
//Serial.println(sensor2val);

delay(1);

}
