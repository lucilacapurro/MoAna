import serial
import math
import time

#####################################################################################################################

# FUNCTIONS:

# Function to open the serial port
def open_serial_port(serial_port = 'COM6', baud_rate = 230400):
    ser = serial.Serial(serial_port, baud_rate)
    return ser


# Function to send a message from PC to board
def send_message(ser, hex_bytes):
    data_to_send = bytes(hex_bytes)
    ser.write(data_to_send)


# Function to read a message sent from board to PC
def read_message(ser, n_bytes):
    response = ser.read(n_bytes)
    return response

# Function to write a register 
def write_register(ser, address, data): # address = 0x12 = [0x31, 0x32]     data = 0x456789 = [0x34 0x35 0x36 0x37 0x38 0x39]
    # SPI_READ register bit must be enabled before attempting a serial readout from the AFE
    #enable_spi_read(ser)
    # PC to EVM: 0x02 < 2 bytes of ASCII addr with MSB first> < 6 bytes of ASCII data with MSB first> 0x0D
    message = [0x02, address[0], address[1], data[0], data[1], data[2], data[3], data[4], data[5], 0x0D]
    send_message(ser, message)


# Function to read a register 
def read_register(ser, address): # address = 0x12 = [0x31, 0x32]
    # SPI_READ register bit must be disabled before attempting a serial readout from the AFE
    #disable_spi_read(ser)

    # PC to EVM: 0x03 < 2 bytes of ASCII addr with MSB first> 0x0D
    message = [0x03, address[0], address[1], 0x0D]
    send_message(ser, message)

    # EVM to PC: 0x03 0x02 <3 bytes of raw data with LSB first> 0x03 0x0D
    data_bytes = read_message(ser, n_bytes = 7)
    raw_data = data_bytes[2:5] 

    # Convertir los bytes a un valor decimal (LSB primero)
    decimal_value = int.from_bytes(raw_data, byteorder='little') # considerando LSB first (invierte)
    #decimal_value = int.from_bytes(raw_data, byteorder='big')

    #print("Valor decimal:", decimal_value)
    return decimal_value



#####################################################################################################################
'''
data = []

try:
    # Open the serial port
    ser = open_serial_port()

    for j in range(1):
        for i in range(1000): 
            #new_data = read_register(ser, address = [0x32, 0x41]) # address = LED2VAL = 0x2A = 0x32 0x41  RED
            new_data = read_register(ser, address = [0x32, 0x43]) # address = LED1VAL = 0x2C = 0x32 0x43   IR
            #new_data = read_register(ser, address = [0x32, 0x45]) # address = LED2VAL - ALED2VAL = 0x2E = 0x32 0x45
            #new_data = read_register(ser, address = [0x32, 0x46]) # address = LED1VAL - ALED1VAL = 0x2F = 0x32 0x46 
            data.append(new_data)
            time.sleep(0.005) 
    print(data)

    # Close the serial port
    ser.close()

except serial.SerialException as e:
    print("Error:", e)
'''