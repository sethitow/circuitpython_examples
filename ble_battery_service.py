import analogio
import bleio
import board
import time

# Create an analog input for the battery voltage
voltage_monitor = analogio.AnalogIn(board.VOLTAGE_MONITOR)

# Create a characteristic for publishing battery level.
# 0x2919 is the characteristic UUID for a device to publish batery level percentage.
# UUIDs for common characteristics are defined by Bluetooth SIG.
# https://www.bluetooth.com/specifications/gatt/characteristics/
battery_level_chara = bleio.Characteristic(bleio.UUID(0x2919), read=True, notify=True)

# Create a service for battery information
# 0x180F is the service UUID for publishing characteristics related to the battery.
# UUIDs for common services are defined by Bluetooth SIG.
# https://www.bluetooth.com/specifications/gatt/services/
battery_service = bleio.Service(bleio.UUID(0x180F), [battery_level_chara])

# Create a peripherial with our service and start it
periph = bleio.Peripheral([battery_service])

while True:
    # Start advertising when not connected.
    periph.start_advertising()
    #  Wait for a connection
    while not periph.connected:
        pass

    while periph.connected:
        # Do some math to turn the analog value into a percentage.
        battery_voltage = (voltage_monitor.value * 3.3) / 65536 * 2
        # We assume the battery has a voltage between 3.0 and 4.2 volts.
        battery_percent = 250 * (battery_voltage - 3) / 3

        # Characteristic values must be Bytes. The Battery Level characteristic
        # specification says the value should be an unsigned 8-bit integer, so
        # we encode the integer as a single byte.
        battery_level_chara.value = int(battery_percent).to_bytes(1, "big")
