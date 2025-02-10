#include <Arduino_HS300x.h>       // For HS3003 sensor (temperature and humidity)
#include <Arduino_LPS22HB.h>      // For barometric pressure sensor (LPS22HB)
#include <PDM.h>                  // For microphone
#include <Arduino_APDS9960.h>             // For APDS9960 (ambient light, proximity, gesture)
#include <Wire.h>
#include <SPI.h>
#include <Arduino_BMI270_BMM150.h>               // For accelerometer and gyroscope (BMI270) and for magnetometer (BMM150)
#include <ArduinoBLE.h>

// Global variables for microphone
#define SAMPLE_RATE 16000
#define PDM_BUF_SIZE 256
int16_t samples[PDM_BUF_SIZE];
int sampleIndex = 0;

int proximity = 0;
int r = 0, g = 0, b = 0;
unsigned long lastUpdate = 0;



// BLE service and characteristic
BLEService sensorService("1101"); // Create a service with a UUID
BLEUnsignedCharCharacteristic tempChar("2A1C", BLERead | BLENotify); // Temperature characteristic
BLEUnsignedCharCharacteristic humidityChar("2A6F", BLERead | BLENotify); // Humidity characteristic
BLEUnsignedCharCharacteristic pressureChar("2A6D", BLERead | BLENotify); // Pressure characteristic
BLEUnsignedCharCharacteristic microphoneChar("2A78", BLERead | BLENotify); // Microphone data characteristic



// For microphone output
void onSampleReceived() {
  int numSamples = PDM.available();
  if (numSamples) {
    PDM.read(samples, numSamples);
    for (int i = 0; i < numSamples; i++) {
      // Print a simple waveform based on microphone input (debugging)
      Serial.print(samples[i]);
      Serial.print(" ");
    }
    Serial.println();
  }
}

void test_APDS() {

  // Check if a proximity reading is available.
  if (APDS.proximityAvailable()) {
    proximity = APDS.readProximity();
  }

  // Check if a gesture reading is available
  if (APDS.gestureAvailable()) {
    int gesture = APDS.readGesture();
    switch (gesture) {
      case GESTURE_UP:
        Serial.println("Detected UP gesture");
        break;

      case GESTURE_DOWN:
        Serial.println("Detected DOWN gesture");
        break;

      case GESTURE_LEFT:
        Serial.println("Detected LEFT gesture");
        break;

      case GESTURE_RIGHT:
        Serial.println("Detected RIGHT gesture");
        break;

      default:
        // Ignore
        break;
    }
  }

  // Check if a color reading is available
  if (APDS.colorAvailable()) {
    APDS.readColor(r, g, b);
  }

  // Print updates every 100 ms
  if (millis() - lastUpdate > 100) {
    lastUpdate = millis();
    Serial.print("PR=");
    Serial.print(proximity);
    Serial.print(" RGB=");
    Serial.print(r);
    Serial.print(",");
    Serial.print(g);
    Serial.print(",");
    Serial.println(b);
  }
}

void test_IMU() {
  float x, y, z;

  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(x, y, z);

    Serial.print("Gyroscope");
    Serial.print(x);
    Serial.print('\t');
    Serial.print(y);
    Serial.print('\t');
    Serial.println(z);
  }

  if (IMU.magneticFieldAvailable()) {
    IMU.readMagneticField(x, y, z);
    Serial.print("Magnetic");
    Serial.print(x);
    Serial.print('\t');
    Serial.print(y);
    Serial.print('\t');
    Serial.println(z);
  }

  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);
    Serial.print("Accellerator");
    Serial.print(x);
    Serial.print('\t');
    Serial.print(y);
    Serial.print('\t');
    Serial.println(z);
  }
}


void setup() {
  // Start serial communication
  Serial.begin(9600);
  while (!Serial);

  // Initialize HTS221 for temperature and humidity
  if (!HS300x.begin()) {
    Serial.println("Failed to initialize HS300x sensor!");
    while (1);
  }

  // Initialize LPS22HB for barometric pressure
  if (!BARO.begin()) {
    Serial.println("Failed to initialize LPS22HB sensor!");
    while (1);
  }

  // Initialize PDM (Microphone)
  PDM.begin(1, SAMPLE_RATE);
  PDM.setBufferSize(PDM_BUF_SIZE);
  PDM.onReceive(onSampleReceived);

  // Initialize APDS9960 for gesture, ambient light, proximity, and color
  if (!APDS.begin()) {
    Serial.println("Failed to initialize APDS9960 sensor!");
    while (1);
  }


  // Initialize BMI270 and BMI150 (Accelerometer and Gyroscope)
  if (!IMU.begin()) {
    Serial.println("Failed to initialize BMI270 and BMI150 sensors!");
    while (1);
  }

  Serial.print("Gyroscope sample rate = ");
  Serial.print(IMU.gyroscopeSampleRate());
  Serial.println(" Hz");
  Serial.println();
  Serial.println("Gyroscope in degrees/second");
  Serial.println("X\tY\tZ");

  Serial.println("Sensors initialized successfully.");

  // Initialize BLE
  if (!BLE.begin()) {
    Serial.println("Starting BLE failed!");
    while (1);
  }

  // Set up the BLE service and characteristics
  BLE.setLocalName("Arduino_Sensor");
  BLE.setAdvertisedService(sensorService);

  sensorService.addCharacteristic(tempChar);
  sensorService.addCharacteristic(humidityChar);
  sensorService.addCharacteristic(pressureChar);
  sensorService.addCharacteristic(microphoneChar);

  BLE.addService(sensorService);

  // Start advertising BLE service
  BLE.advertise();
  Serial.println("BLE Peripheral is now advertising...");
}


void loop() {
  // Read temperature and humidity from HTS221
  float temperature = HS300x.readTemperature();
  float humidity = HS300x.readHumidity();

  // Read barometric pressure from LPS22HB
  float pressure = BARO.readPressure();



  // Print data to Serial Monitor
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.print(" °C, Humidity: ");
  Serial.print(humidity);
  Serial.print(" %, Pressure: ");
  Serial.print(pressure);
  Serial.println(" hPa");


  BLEDevice central = BLE.central();

  if (central)
  {
    Serial.print("Connected to central: ");
    Serial.println(central.address());
    digitalWrite(LED_BUILTIN, HIGH);

    // Update BLE characteristics with sensor data
    tempChar.writeValue(temperature);

    humidityChar.writeValue(humidity);

    pressureChar.writeValue(pressure);
  }

  test_APDS();

  test_IMU();

  delay(500); // Wait a bit before next reading

}
