# aquarium_monitoring


Connect the pins of tft (st7735) with the esp32 board
_____________________________
| Display Pin  | ESP32 Pin  |
|--------------|------------|
| LED          | 3.3V       |
| SCK          | D18        |
| SDA (MOSI)   | D23        |
| A0 (DC)      | D5         |
| Reset        | D19        |
| CS           | D21        |
| GND          | GND        |
| VCC          | 3.3V       |
|___________________________|

Clone the repository 
git clone https://github.com/Sabbbir/aquarium_monitoring.git


cd aquarium_monitoring

esptool.py --port /dev/ttyUSB0 erase_flash

esptool.py --port /dev/ttyUSB0 write_flash -z 0x1000 bin/ESP32_GENERIC-20241025-v1.24.0.bin

