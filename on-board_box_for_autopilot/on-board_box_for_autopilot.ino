#include <Servo.h>
#include <WirelessLibrary.h>
#include <DistanceSensorLibrary.h>
#include <GPSLibrary.h>
#include <FilesystemLibrary.h>

// Константы для пинов и параметров автопилота
const int servoPin = 9;
const int altitudeSensorPin = A0;
const int targetAltitude = 100;
const int numPoints = 3;

// Константы для пинов и параметров люка
const int hatchPin = 10;
const int openAngle = 90;
const int closeAngle = 0;

// Константы для пинов и параметров контроля скорости
const int speedControlPin = 11;
const int minSpeed = 20;

// Переменные состояния автопилота
int currentPoint = 0;
int currentAltitude = 0;
int currentSpeed = 0;
int batteryLevel = 0;

// Переменные состояния люка
bool hatchOpen = false;

Servo rudder;
Servo hatchServo;
Servo speedControlServo;
WirelessModule wireless;
DistanceSensor distanceSensor;
GPSModule gpsModule;
File logFile;

void setup() {
  rudder.attach(servoPin);
  rudder.write(90);
  hatchServo.attach(hatchPin);
  hatchServo.write(closeAngle);
  speedControlServo.attach(speedControlPin);
  speedControlServo.write(90);

  wireless.init();

  distanceSensor.init();
  gpsModule.init();

  logFile = filesystem.open("/blackbox.txt", FILE_WRITE);
  sendPlaneData();

  delay(5000);
  autopilot();
}

void loop() {
  checkConnection();
  receiveCommands();
  updatePlaneState();
  sendPlaneData();
  checkErrors();
  checkAltitudePriority();
  checkDistance();
  logData();
}

void autopilot() {
  while (currentPoint < numPoints) {
    moveToNextPoint();
    dropCargo();
    delay(5000);
  }

  finishFlight();
}

void checkErrors() {
  // Проверка наличия ошибок и отправка сообщений на пульт управления
  if (currentAltitude > targetAltitude) {
    sendMessage("Error: Target altitude exceeded");
  }

  if (currentSpeed < minSpeed) {
    sendMessage("Error: Speed below minimum");
  }
}

void checkAltitudePriority() {
  if (currentAltitude > secondAltitude + 3) {
  } else if (currentAltitude + 3 < secondAltitude) {
  }
}

void checkDistance() {
  float distance = distanceSensor.getDistance();
}

void updatePlaneState() {
  // Обновление состояния самолета, например, текущей высоты, скорости и уровня заряда батареи
  currentAltitude = readAltitude();
  currentSpeed = readSpeed();
  batteryLevel = readBatteryLevel();
}

void sendPlaneData() {
  wireless.sendData("Plane Data: ID=" + String(planeID) + ", Altitude=" + String(currentAltitude) + "m, Speed=" + String(currentSpeed) + "km/h, Battery=" + String(batteryLevel) + "%, Drop Status=" + (dropStatus ? "Dropped" : "Not Dropped"));
}

void sendDistance(float distance) {
  wireless.sendData("Distance: " + String(distance) + "m");
}

void sendMessage(String message) {
  wireless.sendData("Message: " + message);
}

void checkConnection() {
  if (!wireless.isConnected()) {
    sendMessage("Error: Connection lost");
  }
}

void receiveCommands() {
  String command = wireless.receiveData();

  if (

command == "Open Hatch") {
    openHatch();
  } else if (command == "Close Hatch") {
    closeHatch();
  } else if (command == "Increase Speed") {
    increaseSpeed();
  } else if (command == "Decrease Speed") {
    decreaseSpeed();
  }
}

void openHatch() {
  hatchServo.write(openAngle);
  hatchOpen = true;
}

void closeHatch() {
  hatchServo.write(closeAngle);
  hatchOpen = false;
}

void increaseSpeed() {
  speedControlServo.write(180);
}

void decreaseSpeed() {
  speedControlServo.write(0);
}

void finishFlight() {
  // Код для завершения полета
}

void logData() {
  String logEntry = "Altitude: " + String(currentAltitude) + "m, Speed: " + String(currentSpeed) + "km/h, Latitude: " + String(gpsModule.getLatitude()) + ", Longitude: " + String(gpsModule.getLongitude()) + ", Hatch: " + (hatchOpen ? "Open" : "Closed");
  logFile.println(logEntry);
}
}
