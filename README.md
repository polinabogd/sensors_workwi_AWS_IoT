# Wokwi Project: IoT Sensor Data Display and AWS IoT Core Integration
Project Overview
This project demonstrates how to use an ESP32 microcontroller to read data from a DHT22 temperature and humidity sensor, as well as an MH-Z19 CO2 sensor, display the sensor data on an OLED screen, and send the data to AWS IoT Core.

# Components Used
ESP32 Microcontroller
DHT22 Temperature and Humidity Sensor
MH-Z19 CO2 Sensor
SSD1306 OLED Display (128x64)
AWS IoT Core for data logging and monitoring
Circuit Diagram

# Setup Instructions
Hardware Connections
DHT22 Sensor:

VCC to 3.3V
GND to GND
Data to GPIO 15
MH-Z19 Sensor:

VCC to 5V
GND to GND
TX to GPIO 16 (RX on ESP32)
RX to GPIO 17 (TX on ESP32)
SSD1306 OLED Display:

VCC to 3.3V
GND to GND
SCL to GPIO 22
SDA to GPIO 21
Software Setup
Install Wokwi Simulator:

Visit Wokwi and create an account if you don't have one.
# Create a New Project:

Start a new project and select the ESP32 board.
Add Components:

Add the DHT22 sensor, MH-Z19 sensor, and SSD1306 OLED display to the project workspace.
Connect the components according to the circuit diagram provided above.
Upload Certificate Files:

Upload AmazonRootCA1.txt, certificate.pem.txt, and private.pem.txt files to the ESP32 filesystem in Wokwi.
Copy and Paste the Code:

Copy the provided code into the main script of your Wokwi project.
Running the Project
Start the Simulation:
Click the "Start Simulation" button in Wokwi.
View Data:
The OLED display will show the temperature, humidity, and CO2 levels.
The data will be sent to AWS IoT Core for logging and monitoring.
<img width="732" alt="Screenshot 2024-05-30 at 15 27 57" src="https://github.com/polinabogd/sensors_workwi_AWS_IoT/assets/74895012/37f15449-aea4-42ba-ab05-8bfb7cb29093">
