const int relayPin = 2;  // Pin to which the relay module is connected

void setup() {
  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, LOW);  // Initialize the relay as OFF
  Serial.begin(9600);
}

void loop() {
  // Read serial input to control the water pump
  if (Serial.available() > 0) {
    char command = Serial.read();

    // Toggle the water pump based on the received command
    if (command == 'ON') {
      digitalWrite(relayPin, HIGH);  // Turn ON the water pump
      Serial.println("Water pump is ON");
    } else if (command == 'OFF') {
      digitalWrite(relayPin, LOW);   // Turn OFF the water pump
      Serial.println("Water pump is OFF");
    }
  }
}
