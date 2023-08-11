import csv
import time
import serial

####################################################################################################################################

# Puerto y baudrate del Arduino
puerto = '/dev/cu.usbmodem1101'
baudrate = 115200
arduinoData = serial.Serial(puerto, baudrate)

time.sleep(1)

# CAMBIAR EL NOMBRE DEL ARCHIVO DE DATOS A GUARDAR:
archivo_data = 'data.csv'

# Campos de datos 
fieldnames=["Tiempo","redVal","irVal"]

# Escribe los campos en el csv 
with open(archivo_data, 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()


# Levanta los datos, los decodifica y los guarda
while True:
    while (arduinoData.inWaiting()==0):
            pass
    dataPacket=arduinoData.readline()
    dataPacket=str(dataPacket,'utf-8')
    dataPacket=dataPacket.strip('\r\n')
    splitPacket=dataPacket.split(",")
    
    tiempo=splitPacket[0].replace(" ","")
    redVal=splitPacket[1].replace(" ","")
    irVal=splitPacket[2].replace(" ","")
    
    tiempo=int(tiempo)
    redVal=int(redVal)
    irVal=int(irVal)

    with open(archivo_data, 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        info = {
            "Tiempo": tiempo,
            "redVal": redVal,
            "irVal": irVal,
        }

        csv_writer.writerow(info)
        print(tiempo, redVal, irVal)
        



