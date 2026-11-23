// Gesture Home Automation - Arduino UNO side.
// Reads newline-terminated commands from the Python app (9600 baud) and
// switches three relay channels and a buzzer.
//
// The relay module AND the buzzer module in the original build are
// ACTIVE-LOW: writing LOW turns the channel ON, HIGH turns it OFF.
// (The command handlers below use LOW = ON, as in the original wiring.)
// If your module is active-HIGH, swap ON/OFF below.

const int relay_1 = 8;   // module IN3 - charger
const int relay_2 = 9;   // module IN2 - fan
const int relay_3 = 10;  // module IN1 - bulb
const int Buzzer = 11;
const int pirSensor = 2;

const int ON = LOW;
const int OFF = HIGH;

void setup()
{
    // Write OFF *before* pinMode so the relays never click on at boot.
    digitalWrite(relay_1, OFF);
    digitalWrite(relay_2, OFF);
    digitalWrite(relay_3, OFF);
    digitalWrite(Buzzer, OFF);

    Serial.begin(9600);

    pinMode(relay_1, OUTPUT);
    pinMode(relay_2, OUTPUT);
    pinMode(relay_3, OUTPUT);
    pinMode(Buzzer, OUTPUT);
    pinMode(pirSensor, INPUT);
}

void loop()
{
    // PIR state (0/1) is streamed on every loop, as in the original build.
    Serial.println(digitalRead(pirSensor));

    if (Serial.available() > 0)
    {
        String signal = Serial.readStringUntil('\n');
        signal.trim();

        if (signal == "OKAY") {
            digitalWrite(relay_1, ON);
            digitalWrite(relay_2, ON);
            digitalWrite(relay_3, ON);
            digitalWrite(Buzzer, ON);
            Serial.println("All components ON");
        }
        else if (signal == "STOP") {
            digitalWrite(relay_1, OFF);
            digitalWrite(relay_2, OFF);
            digitalWrite(relay_3, OFF);
            digitalWrite(Buzzer, OFF);
            Serial.println("All components OFF");
        }
        else if (signal == "SMILE") {
            digitalWrite(relay_1, ON);
            Serial.println("relay_1 ON");
        }
        else if (signal == "LIVE_LONG") {
            digitalWrite(relay_1, OFF);
            Serial.println("relay_1 OFF");
        }
        else if (signal == "THUMBS_UP") {
            digitalWrite(relay_2, ON);
            Serial.println("relay_2 ON");
        }
        else if (signal == "THUMBS_DOWN") {
            digitalWrite(relay_2, OFF);
            Serial.println("relay_2 OFF");
        }
        else if (signal == "PEACE") {
            digitalWrite(relay_3, ON);
            Serial.println("relay_3 ON");
        }
        else if (signal == "CALL_ME") {
            digitalWrite(relay_3, OFF);
            Serial.println("relay_3 OFF");
        }
        else if (signal == "FIST") {
            digitalWrite(Buzzer, ON);
            Serial.println("Buzzer ON");
        }
        else if (signal == "ROCK") {
            digitalWrite(Buzzer, OFF);
            Serial.println("Buzzer OFF");
        }
    }
}
