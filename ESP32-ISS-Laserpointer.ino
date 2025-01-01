#include <WiFi.h>
#include <HTTPClient.h>
#include <Servo.h>

Servo servoAzimuth;  // Servo for azimuth (rotation)
Servo servoAltitude; // Servo for altitude (tilt)

const int pinAzimuth = 9;  // Servo control pin for azimuth
const int pinAltitude = 10; // Servo control pin for altitude
const int laserPin = 13;    // Laser control pin (set to appropriate pin)

const char* ssid = "your_SSID";
const char* password = "your_PASSWORD";

// User location: Alkmaar, Netherlands (latitude, longitude)
float latitude_user = 52.632381;
float longitude_user = 4.748206;

// Endpoint for ISS position from Mimic API
const String apiUrl = "https://iss-mimic.github.io/Mimic/";

// Setup Wi-Fi and servos
void setup() {
  Serial.begin(115200);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Attach servos
  servoAzimuth.attach(pinAzimuth);
  servoAltitude.attach(pinAltitude);

  // Set initial servo positions (pointing to the sky)
  servoAzimuth.write(90); // Azimuth 90° (North)
  servoAltitude.write(90); // Altitude 90° (horizontal)

  // Initialize laser pin
  pinMode(laserPin, OUTPUT);
  digitalWrite(laserPin, LOW); // Turn off the laser initially
}

// Main loop
void loop() {
  // Fetch the ISS position
  String response = getISSPosition();

  // Parse the response to extract latitude, longitude, and altitude
  float latitude_ISS = parseLatitude(response);
  float longitude_ISS = parseLongitude(response);
  float altitude_ISS = parseAltitude(response);

  // Calculate the azimuth and altitude
  float azimuth = calculateAzimuth(latitude_user, longitude_user, latitude_ISS, longitude_ISS);
  float altitude = calculateAltitude(latitude_user, longitude_user, latitude_ISS, longitude_ISS);

  // Map azimuth (0-360°) to servo range (0-180°)
  int azimuthServoAngle = map(azimuth, 0, 360, 0, 180);
  // Map altitude (0-90°) to servo range (0-180°)
  int altitudeServoAngle = map(altitude, 0, 90, 0, 180);

  // Update the servos only if the altitude is above the horizon (positive altitude)
  servoAzimuth.write(azimuthServoAngle);
  servoAltitude.write(altitudeServoAngle);

  // Turn the laser on only if the ISS is at least 10° above the horizon
  if (altitude > 10) {
    digitalWrite(laserPin, HIGH);  // Turn the laser on
  } else {
    digitalWrite(laserPin, LOW);   // Turn the laser off
  }

  // Delay before next update
  delay(1000);  // Update every second
}

// Function to get the ISS position from the Mimic API
String getISSPosition() {
  HTTPClient http;
  String response = "";

  // Make the GET request to the API
  http.begin(apiUrl);
  int httpCode = http.GET();
  if (httpCode > 0) {
    response = http.getString(); // Get the response body as a string
  } else {
    Serial.println("Error in HTTP request");
  }
  http.end();
  return response;
}

// Functions to parse the ISS data from the response (assuming JSON format)
float parseLatitude(String response) {
  int latStart = response.indexOf("\"latitude\":") + 11;
  int latEnd = response.indexOf(",", latStart);
  String latStr = response.substring(latStart, latEnd);
  return latStr.toFloat();
}

float parseLongitude(String response) {
  int lonStart = response.indexOf("\"longitude\":") + 12;
  int lonEnd = response.indexOf(",", lonStart);
  String lonStr = response.substring(lonStart, lonEnd);
  return lonStr.toFloat();
}

float parseAltitude(String response) {
  int altStart = response.indexOf("\"altitude\":") + 11;
  int altEnd = response.indexOf(",", altStart);
  String altStr = response.substring(altStart, altEnd);
  return altStr.toFloat();
}

// Calculate the Azimuth (bearing) in degrees
float calculateAzimuth(float lat1, float lon1, float lat2, float lon2) {
  float deltaLon = radians(lon2 - lon1);
  lat1 = radians(lat1);
  lat2 = radians(lat2);

  float x = sin(deltaLon) * cos(lat2);
  float y = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(deltaLon);

  float azimuth = atan2(x, y);
  azimuth = degrees(azimuth);
  if (azimuth < 0) {
    azimuth += 360; // Normalize azimuth to 0-360°
  }

  return azimuth;
}

// Calculate the Altitude (elevation angle) in degrees
float calculateAltitude(float lat1, float lon1, float lat2, float lon2) {
  lat1 = radians(lat1);
  lat2 = radians(lat2);
  lon1 = radians(lon1);
  lon2 = radians(lon2);

  float deltaLon = lon2 - lon1;
  float sinAltitude = sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(deltaLon);

  float altitude = asin(sinAltitude);  // Altitude in radians
  return degrees(altitude); // Convert to degrees
}

