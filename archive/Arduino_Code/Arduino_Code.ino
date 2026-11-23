int relay_1 = 8;
int relay_2 = 9;
int relay_3 = 10;
int Buzzer = 11;
int pirSensor = 2;

void setup()
{
  // put your setup code here, to run once:
  Serial.begin(9600);

  pinMode(relay_1, OUTPUT);
  pinMode(relay_2, OUTPUT);
  pinMode(relay_3, OUTPUT);
  pinMode(Buzzer, OUTPUT);
  pinMode(pirSensor, INPUT);
}

void loop()
{

  /*digitalWrite(relay_1, HIGH);
  digitalWrite(relay_2, HIGH);
  digitalWrite(relay_3, HIGH);
  digitalWrite(relay_4, HIGH);

  Serial.println("All relays ON");

  delay(1000);

  digitalWrite(relay_1, LOW);
  digitalWrite(relay_2, LOW);
  digitalWrite(relay_3, LOW);
  digitalWrite(relay_4, LOW);

  Serial.println("All relays OFF");
  delay(1000);*/

  Serial.println(digitalRead(pirSensor));

  while (digitalRead(pirSensor) == 1)
  {
    if (Serial.available() > 0)
    {
      char data = Serial.read(); // Read the incoming data
      if (data == '8')
      {
        digitalWrite(relay_1, HIGH); // Turn off the LED
        Serial.println("relay_1 OFF");
      }
      else if (data == '2')
      {
        digitalWrite(relay_1, LOW); // Turn on the LED
        Serial.println("relay_1 ON");
      }
      else if (data == '3')
      {
        digitalWrite(relay_2, HIGH); // Turn off the LED
        Serial.println("relay_2 OFF");
      }
      else if (data == '4')
      {
        digitalWrite(relay_2, LOW); // Turn on the LED
        Serial.println("relay_2 ON");
      }
      else if (data == '5')
      {
        digitalWrite(relay_3, HIGH); // Turn off the LED
        Serial.println("relay_3 OFF");
      }
      else if (data == '6')
      {
        digitalWrite(relay_3, LOW); // Turn on the LED
        Serial.println("relay_3 ON");
      }
      else if (data == '7')
      {
        digitalWrite(Buzzer, LOW); // Turn on the Buzzer
      }
      else if (data == '10')
      {
        digitalWrite(Buzzer, HIGH); // Turn on the LED
      }
      else if (data == '1')
      {
        digitalWrite(relay_1, LOW); // Turn on the LED
        digitalWrite(relay_2, LOW); // Turn on the LED
        digitalWrite(relay_3, LOW); // Turn on the LED
        digitalWrite(Buzzer, HIGH); // Turn off the Buzzer
        Serial.println("All relays ON");
      }
      else if (data == '9')
      {
        digitalWrite(relay_1, HIGH); // Turn off the LED
        digitalWrite(relay_2, HIGH); // Turn off the LED
        digitalWrite(relay_3, HIGH); // Turn off the LED
        digitalWrite(Buzzer, LOW);   // Turn on the Buzzer
        Serial.println("All relays OFF!");
      }
    }
  }
}