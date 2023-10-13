import numpy as np
from scipy.io.wavfile import write
import pygame

# Parámetros pulso de alarma técnica de media prioridad
frecuencia_pulso_MP = 800 #np.random.uniform(150, 1000)  # Frecuencia del pulso entre 150 y 1000 Hz

# Parámetros pulso de alarma técnica de baja prioridad 
frecuencia_pulso_LP = 600 #np.random.uniform(150, 1000)  # Frecuencia del pulso entre 150 y 1000 Hz

# Parámetros genéricos para ambos casos
num_componentes = 4
duracion_efectiva = 0.15 # Duración efectiva del pulso en segundos entre 125 y 250 ms
rise_time = 0.1 * duracion_efectiva # Rise time en segundos entre 10% y 40% de la duración efectiva del pulso
fall_time = 0.05  # Fall time menor a intervalo entre pulsos menos rise time 
sample_rate = 44100

# Defijo la cantidad de muestras de rise y fall teniendo en cuenta el tiempo y la frecuencia de muestreo
rise_samples = int(rise_time * sample_rate) 
fall_samples = int(fall_time * sample_rate)

# Crear una forma de onda de pulso
t = np.linspace(0, duracion_efectiva, int(44100 * duracion_efectiva), endpoint=False)  # 44100 Hz es una frecuencia de muestreo común
pulso_MP = np.zeros_like(t)
pulso_LP = np.zeros_like(t)

# Alarma técnica de media prioridad --> tiene 3 pulsos por norma 
for j in range(3): 
    # Crear una forma de onda de pulso para un ciclo
    pulso_ciclo = np.zeros_like(t)
    for i in range(1, num_componentes + 1):
        componente = np.sin(2 * np.pi * i * frecuencia_pulso_MP * t) / i
        pulso_ciclo += componente

    # Aplico rise y fall time a cada pulso
    pulso_ciclo[:rise_samples] *= np.linspace(0, 1, rise_samples)
    pulso_ciclo[-fall_samples:] *= np.linspace(1, 0, fall_samples)

    # Agrego el pulso del ciclo al pulso MP con un espacio de silencio entre ellos
    espacio_silencio = np.zeros(int(sample_rate * 0.2))  # 200 ms de silencio, la norma pide entre 125 ms y 250 ms
    pulso_MP = np.concatenate((pulso_MP, pulso_ciclo, espacio_silencio))

# Alarma técnica de baja prioridad --> tiene 1 sólo pulso porque la norma tiene 1 o 2 --> elijo 2 para favorecer la diferenciación de prioridad de ambas 
for i in range(1, num_componentes + 1):
    componente = np.sin(2 * np.pi * i * frecuencia_pulso_LP * t) / i
    pulso_LP += componente

# Aplico rise y fall time a la alarma de baja prioridad
pulso_LP[:rise_samples] *= np.linspace(0, 1, rise_samples)
pulso_LP[-fall_samples:] *= np.linspace(1, 0, fall_samples)

# Normalizar la amplitud
pulso_MP /= np.max(np.abs(pulso_MP))
pulso_LP /= np.max(np.abs(pulso_LP))

# Guardar el pulso como un archivo WAV
write("C:/Users/Zakie Assad/Proyecto Final/Git/MoAna/Codigos/Windows/pulso_personalizado_MP.wav", sample_rate, pulso_MP)
write("C:/Users/Zakie Assad/Proyecto Final/Git/MoAna/Codigos/Windows/pulso_personalizado_LP.wav", sample_rate, pulso_LP)


# Reproducir el archivo de audio con pygame
pygame.mixer.init()
pygame.mixer.music.load("C:/Users/Zakie Assad/Proyecto Final/Git/MoAna/Codigos/Windows/pulso_personalizado_LP.wav")
pygame.mixer.music.play()

# Esperar hasta que se termine de reproducir
pygame.time.wait(int(1000))  # Esperar según la duración del pulso en milisegundos

# Detener la reproducción (opcional)
pygame.mixer.music.stop()
