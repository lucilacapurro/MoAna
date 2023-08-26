import serial
import math
import time

#####################################################################################################################

# FUNCTIONS:


# Function to open the serial port
def open_serial_port(serial_port = '/dev/cu.usbmodem1101', baud_rate = 230400):
    ser = serial.Serial(serial_port, baud_rate)
    return ser


# Function to send a message from PC to board
def send_message(hex_bytes):
    data_to_send = bytes(hex_bytes)
    ser.write(data_to_send)


# Function to read a message sent from board to PC
def read_message(n_bytes):
    response = ser.read(n_bytes)
    return response


'''
# Function to reset the software
def reset(ser):
    disable_spi_read()
    # CONTROL0 D3 (SW_RST) = 1
    address = [0x30, 0x30] # address = 0x00 = 0x30 0x30   
    data = [0x30, 0x30, 0x30, 0x30, 0x30, 0x38] #  data = 0x000008 = [0x30 0x30 0x30 0x30 0x30 0x38]
    message = [0x02, address[0], address[1], data[0], data[1], data[2], data[3], data[4], data[5], 0x0D]
    send_message(message)
'''

# Function to enable the SPI read
def enable_spi_read():
    # Enables SPI read: sets D0 to 1
    address = [0x30, 0x30] # address = 0x00 = 0x30 0x30   
    data = [0x30, 0x30, 0x30, 0x30, 0x30, 0x31] #  data = 0x000001 = [0x30 0x30 0x30 0x30 0x30 0x31]
    message = [0x02, address[0], address[1], data[0], data[1], data[2], data[3], data[4], data[5], 0x0D]
    send_message(message)


# Function to disable the SPI read
def disable_spi_read():
    # Disables SPI read: sets D0 to 0
    address = [0x30, 0x30] # address = 0x00 = 0x30 0x30   
    data = [0x30, 0x30, 0x30, 0x30, 0x30, 0x30] #  data = 0x000000 = [0x30 0x30 0x30 0x30 0x30 0x30]
    message = [0x02, address[0], address[1], data[0], data[1], data[2], data[3], data[4], data[5], 0x0D]
    send_message(message)


# Function to get the device ID 
def get_device_id():
    send_message([0x04, 0x0D])
    response = read_message(n_bytes = 8)  # response = b'\x04\x024490\x03\r'
    device_response = str(response[2:6])[2:-1]
    print("Device:", device_response)  # response = 4490


# Function to get the firmware version of the board
def get_firmware_revision():
    send_message([0x07, 0x0D])
    response = read_message(n_bytes = 6)
    fw_major = response[2]
    fw_minor = response[3]
    version_response = f"{fw_major}.{fw_minor}"
    print("Version:", version_response)


# Function to write a register 
def write_register(address, data): # address = 0x12 = [0x31, 0x32]     data = 0x456789 = [0x34 0x35 0x36 0x37 0x38 0x39]
    # SPI_READ register bit must be enabled before attempting a serial readout from the AFE
    #enable_spi_read()
    # PC to EVM: 0x02 < 2 bytes of ASCII addr with MSB first> < 6 bytes of ASCII data with MSB first> 0x0D
    message = [0x02, address[0], address[1], data[0], data[1], data[2], data[3], data[4], data[5], 0x0D]
    send_message(message)


# Function to read a register 
def read_register(address): # address = 0x12 = [0x31, 0x32]
    # SPI_READ register bit must be disabled before attempting a serial readout from the AFE
    #disable_spi_read()

    # PC to EVM: 0x03 < 2 bytes of ASCII addr with MSB first> 0x0D
    message = [0x03, address[0], address[1], 0x0D]
    send_message(message)

    # EVM to PC: 0x03 0x02 <3 bytes of raw data with LSB first> 0x03 0x0D
    data_bytes = read_message(n_bytes = 7)
    raw_data = data_bytes[2:5] 

    # Convertir los bytes a un valor decimal (LSB primero)
    decimal_value = int.from_bytes(raw_data, byteorder='little') # considerando LSB first (invierte)
    #decimal_value = int.from_bytes(raw_data, byteorder='big')

    #print("Valor decimal:", decimal_value)
    return decimal_value


# Function to start the ADC read
def start_adc_read_packet(packet_count):
    # PC to EVM: 0x01 0x2A < 2 ASCII bytes of N packets expressed as log base 2 with MSB first> 0x0D 
    # Example: to capture 1024 packets (log base 2 of 1024 is 0x0A), PC sends: “0x01 0x2A 0x30 0x61 0x0D”
    decimal_log_2 = int(math.log(packet_count, 2))
    hex_log_2 = "0x{:02X}".format(decimal_log_2)
    charMSB = hex_log_2[2]
    asciiMSB = ord(charMSB)
    hexaMSB = hex(asciiMSB)
    charLSB = hex_log_2[3]
    asciiLSB = ord(charLSB)
    hexaLSB = hex(asciiLSB)
    message = [0x01, 0x2A, int(hexaMSB, 16), int(hexaLSB, 16), 0x0D]
    send_message(message)

    # EVM sends N packets with each packet in following format: 0x01 0x02 <18 bytes of 6 channel data with LSB first> 0x03 0x0D
    channel_arrays = [[] for _ in range(6)]
    for i in range(packet_count):
        response = read_message(n_bytes=22)
        channel_data = response[2:20]                                                                                               # TODO: chequeo de errores de mensaje (recibir efectivamente tanto bytes)
        channel_values = [int.from_bytes(channel_data[i:i+2], byteorder='little') for i in range(0, len(channel_data), 3)] 
        for channel_index, value in enumerate(channel_values):
            channel_arrays[channel_index].append(value)

    for channel_index, values in enumerate(channel_arrays):
        print(f"Valores del canal {channel_index}:", values)


# Function to stop the ADC read
def stop_adc_read():
    # Clear the USB/ COM port buffer before a Start Read ADC Register command is issued
    send_message([0x06, 0x0D])



#####################################################################################################################

'''
data = []

try:
    # Open the serial port
    ser = open_serial_port()

    # Gets device ID
    get_device_id()
    
    # Gets firmware version
    get_firmware_revision()


    # Read register
    start_adc_read_packet(packet_count = 4000)
    stop_adc_read()


    for j in range(1):
        for i in range(1000): 
            #new_data = read_register(address = [0x32, 0x41]) # address = LED2VAL = 0x2A = 0x32 0x41  
            new_data = read_register(address = [0x32, 0x43]) # address = LED1VAL = 0x2C = 0x32 0x43 
            #new_data = read_register(address = [0x32, 0x45]) # address = LED2VAL - ALED2VAL = 0x2E = 0x32 0x45
            #new_data = read_register(address = [0x32, 0x46]) # address = LED1VAL - ALED1VAL = 0x2F = 0x32 0x46 
            data.append(new_data)
            print(len(data))
            time.sleep(0.005) 
    print(data)

    # Close the serial port
    ser.close()

except serial.SerialException as e:
    print("Error:", e)

'''