# aquarium_monitoring

git clone https://github.com/Sabbbir/aquarium_monitoring.git

cd aquarium_monitoring

esptool.py --port /dev/ttyUSB0 erase_flash

esptool.py --port /dev/ttyUSB0 write_flash -z 0x1000 bin/ESP32_GENERIC-20241025-v1.24.0.bin

