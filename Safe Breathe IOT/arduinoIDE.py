//Include the library
String packet;
#include <MQUnifiedsensor.h>
#include <SoftwareSerial.h>
SoftwareSerial mySerial(9,10);
SoftwareSerial BTSerial(2, 3);
const int buzzer = 8;
/****Hardware Related Macros****/
#define         Board                   ("Arduino UNO")
#define         Pin                     (A5)  //Analog input 4 of your arduino
/***Software Related Macros****/
#define         Type                    ("MQ-9") //MQ9
#define         Voltage_Resolution      (5)
#define         ADC_Bit_Resolution      (10) // For arduino UNO/MEGA/NANO
#define         RatioMQ9CleanAir        (9.6) //RS / R0 = 60 ppm 
/***Globals*****/
//Declare Sensor MQ9
MQUnifiedsensor MQ9(Board, Voltage_Resolution, ADC_Bit_Resolution, Pin, Type);

//Definitions
#define placa "Arduino UNO"
#define Voltage_Resolution 5
#define pin A0 //Analog input 0 of your arduino
#define type "MQ-135" //MQ135
#define ADC_Bit_Resolution 10 // For arduino UNO/MEGA/NANO
#define RatioMQ135CleanAir 3.6//RS / R0 = 3.6 ppm  
//#define calibration_button 13 //Pin to calibrate your sensor

//Declare Sensor
MQUnifiedsensor MQ135(placa, Voltage_Resolution, ADC_Bit_Resolution, pin, type);


void setup() {
  BTSerial.begin(9600);
  mySerial.begin(9600);
  Serial.begin(9600);
  delay(100);
  pinMode (buzzer, OUTPUT);

  //Set math model to calculate the PPM concentration and the value of constants
  MQ9.setRegressionMethod(1); //_PPM =  a*ratio^b
  MQ9.init();
  MQ9.setRL(1);
  Serial.print("Calibrating MQ 9 please wait.");
  float calcR0 = 0;
  for (int i = 1; i <= 10; i ++)
  {
    MQ9.update(); // Update data, the arduino will read the voltage from the analog pin
    calcR0 += MQ9.calibrate(RatioMQ9CleanAir);
    Serial.print(".");
  }
  MQ9.setR0(calcR0 / 10);
  Serial.println("  done!.");

  if (isinf(calcR0)) {
    Serial.println("Warning: Conection issue, R0 is infinite (Open circuit detected) please check your wiring and supply");
    while (1);
  }
  if (calcR0 == 0) {
    Serial.println("Warning: Conection issue found, R0 is zero (Analog pin shorts to ground) please check your wiring and supply");
    while (1);
  }


  //MQ135 setup

  MQ135.setRegressionMethod(1); //_PPM =  a*ratio^b
  MQ135.init();
  MQ135.setRL(1);
  Serial.print("Calibrating please wait.");
  float calcR0135 = 0;
  for (int i = 1; i <= 10; i ++)
  {
    MQ135.update(); // Update data, the arduino will read the voltage from the analog pin
    calcR0135 += MQ135.calibrate(RatioMQ135CleanAir);
    Serial.print(".");
  }
  MQ135.setR0(calcR0135 / 10);
  Serial.println("  done!.");

  if (isinf(calcR0135)) {
    Serial.println("Warning: Conection issue, R0 is infinite (Open circuit detected) please check your wiring and supply");
    while (1);
  }
  if (calcR0135 == 0) {
    Serial.println("Warning: Conection issue found, R0 is zero (Analog pin shorts to ground) please check your wiring and supply");
    while (1);
  }
  /****  MQ CAlibration *****/
  

}
void SendMessage() {
  Serial.println("I am in send");
  mySerial.println("AT+CMGF=1");
  delay(1000);
  mySerial.println("AT+CMGS=\"+918287311463+++\"\r");
  mySerial.println("Hi Iptisha CO2 levels are high ,can carry emergency oxygen bottle");
  delay(100);
  mySerial.println((char)26);
  delay(1000);
}

void loop() {
  packet = "<LPG, S, CO,CH4,CO2,Toulene,NH4,NO2 \n";
  Serial.println("* Values from MQ-9 *");
  Serial.println("|    LPG   |  S |   CH4 |");
  MQ9.update(); 


  MQ9.setA(1000.5); MQ9.setB(-2.186); 
  float LPG = MQ9.readSensor(); 
  

  MQ9.setA(4269.6); MQ9.setB(-2.648);
  float CH4 = MQ9.readSensor(); 
  

  MQ9.setA(599.65); MQ9.setB(-2.244); 
  float CO9 = MQ9.readSensor(); 

  Serial.print("|    "); Serial.print(LPG);
  packet +=  (String)LPG;
  packet += ",";
  
  Serial.print("    |    "); Serial.print(CO9);
  packet +=  (String)CO9;
  Serial.println("    |");
  packet += ",";
  Serial.print("    |    "); Serial.print(CH4);
  packet +=  (String)CH4;
  packet += ",";


  Serial.println("* Values from MQ-135 *");
  Serial.println("|   CO   |   CO2  |  Toluene  |  NH4  |  NO2  |");


  MQ135.update(); 

  MQ135.setA(605.18); MQ135.setB(-3.937); 
  float CO = MQ135.readSensor(); 

  MQ135.setA(77.255); MQ135.setB(-3.18); 
  float Alcohol = MQ135.readSensor(); 

  MQ135.setA(110.47); MQ135.setB(-2.862); 
  float CO2 = MQ135.readSensor(); 

  MQ135.setA(44.947); MQ135.setB(-3.445); 
  float Toluen = MQ135.readSensor(); 
  MQ135.setA(102.2 ); MQ135.setB(-2.473); 
  float NH4 = MQ135.readSensor(); 
  MQ135.setA(34.668); MQ135.setB(-3.369); 
  float Aceton = MQ135.readSensor(); 
  Serial.print("|   "); Serial.print(CO); 
  packet +=  (String)CO;
  packet += ",";
  Serial.print("   |   "); Serial.print(CO2); 
  packet +=  (String)(CO2);
  packet += ",";
  Serial.print("   |   "); Serial.print(Toluen);   
  packet +=  (String)Toluen;
  packet += ",";
  Serial.print("   |   "); Serial.print(NH4); 
  packet +=  (String)NH4;
  packet += ",";
  Serial.print("   |   "); Serial.print(Aceton);
  packet += (String)Aceton;
  Serial.println("   |"); 
  packet += ">";
  if(CO2<=5){
  digitalWrite(buzzer,LOW);
  }

else if (CO2 > 10)
  {
    Serial.println("HIGH CO2 CONCENTRATION");
    digitalWrite(buzzer, HIGH);
  }
  else if(CH4>12.4){
     Serial.println("HIGH SULPHUR CONCENTRATION");

    }

  Serial.println("\n\n");
  // <LPG, CH4, CO, Alcohol, CO2, Sulphur, NH4, Aceton>
  Serial.println(packet);
  BTSerial.println(packet);
  Serial.println("\n\n");
  delay(5000); //Sampling frequency
   
  if (CO2 > 5) {
    SendMessage();
    Serial.print("High level of CO2 ");
    delay(1000);
  }
  else if(LPG>7.5){
    SendMessage();
    Serial.print("High level of Flamable gas, reach a secure place ");
    delay(1000);
    }
 
  
  
  
}