import network
import time
import ujson
from machine import Pin, I2C, UART
from ssd1306 import SSD1306_I2C
import dht
from umqtt.simple import MQTTClient

# Wi-Fi configuration
SSID = 'Wokwi-GUEST'
PASSWORD = ''

# AWS IoT Core configuration
MQTT_BROKER = 'a4l1kcx96lrly-ats.iot.eu-north-1.amazonaws.com'
CLIENT_ID = 'RP2040_Sensor'
TOPIC = 'sensors/data'

# Paths to certificates and keys (renamed as .txt)
ROOT_CA = '/AmazonRootCA1.txt'
CLIENT_CERT = '/certificate.pem.txt'
PRIVATE_KEY = '/private.pem.txt'

# Initialize DHT22 sensor
dht_pin = Pin(15)
dht_sensor = dht.DHT22(dht_pin)

# Initialize MH-Z19 sensor
uart = UART(1, baudrate=9600, tx=Pin(17), rx=Pin(16))

# Initialize OLED display
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C(128, 64, i2c)

def connect_wifi():
    oled.fill(0)
    oled.text("Connecting to WiFi", 0, 0)
    oled.show()
    
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(SSID, PASSWORD)
    
    while not sta_if.isconnected():
        oled.text(".", 120, 0)  # Show progress dots on the OLED
        oled.show()
        time.sleep(0.1)
    
    oled.fill(0)
    oled.text("WiFi Connected!", 0, 0)
    oled.show()
    print("Connected to WiFi:", sta_if.ifconfig())
    time.sleep(2)

def read_mhz19():
    uart.write(b"\xFF\x01\x86\x00\x00\x00\x00\x00\x79")
    time.sleep(0.1)
    response = uart.read(9)
    if response and len(response) == 9 and response[0] == 0xFF and response[1] == 0x86:
        high = response[2]
        low = response[3]
        co2 = (high * 256) + low
        return co2
    else:
        return None

def display_data(temperature, humidity, co2):
    oled.fill(0)
    oled.text("Temp: {:.1f}C".format(temperature), 0, 0)
    oled.text("Hum: {:.1f}%".format(humidity), 0, 10)
    if co2 is not None:
        oled.text("CO2: {:.1f}ppm".format(co2), 0, 20)
    else:
        oled.text("CO2: Error", 0, 20)
    oled.show()

def create_payload(sensor_id, temperature, humidity, co2):
    timestamp = int(time.time())
    payload = {
        'sensor_id': sensor_id,
        'timestamp': timestamp,
        'temperature': temperature,
        'humidity': humidity,
        'co2': co2 if co2 is not None else "N/A"
    }
    return ujson.dumps(payload)

def send_data(payload):
    oled.fill(0)
    oled.text("Sending data to AWS...", 0, 0)
    oled.show()
    
    try:
        client = MQTTClient(CLIENT_ID, MQTT_BROKER, port=8883, keepalive=60, ssl=True, ssl_params={
            'certfile': CLIENT_CERT,
            'keyfile': PRIVATE_KEY,
            'ca_certs': ROOT_CA
        })
        client.connect()
        client.publish(TOPIC, payload)
        client.disconnect()
        
        oled.fill(0)
        oled.text("Data sent to AWS!", 0, 0)
        oled.show()
        time.sleep(2)
    except Exception as e:
        print("Error sending data:", e)
        oled.fill(0)
        oled.text("Error sending data!", 0, 0)
        oled.show()
        time.sleep(2)

# Connect to WiFi
connect_wifi()

# Main loop
while True:
    try:
        # Read DHT22 sensor data
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()

        # Read MH-Z19 CO2 sensor data
        co2 = read_mhz19()

        # Print values to console
        print("Temperature:", temperature)
        print("Humidity:", humidity)
        print("CO2:", co2)

        # Display values on OLED
        display_data(temperature, humidity, co2)

        # Create payload and send data to AWS IoT Core
        payload = create_payload("sensor_02", temperature, humidity, co2)
        send_data(payload)

    except Exception as e:
        print("Error:", e)
        oled.fill(0)
        oled.text("Error occurred!", 0, 0)
        oled.show()

    time.sleep(10)  # Update every 10 seconds
