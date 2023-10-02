import numpy as np
from scipy.io.wavfile import write
import pygame

# Parámetros pulso de alarma técnica 
frecuencia_pulso_tecnica = 900 #np.random.uniform(150, 1000)  # Frecuencia del pulso entre 150 y 1000 Hz

# Parámetros pulso de alarma fisiológica 
frecuencia_pulso_fisiologica = 600 #np.random.uniform(150, 1000)  # Frecuencia del pulso entre 150 y 1000 Hz

# Parámetros genéricos para ambos casos
num_componentes = 7
duracion_efectiva = 0.2 #np.random.uniform(0.125, 0.25)  # Duración efectiva del pulso en segundos entre 125 y 250 ms
rise_time = 0.1 * duracion_efectiva #np.random.uniform(0.01 * duracion_efectiva, 0.4 * duracion_efectiva)  # Rise time en segundos entre 10% y 40% de la duración efectiva del pulso
fall_time = 0.05  # Fall time de 50 ms (0.05 segundos)

# Crear una forma de onda de pulso
t = np.linspace(0, duracion_efectiva, int(44100 * duracion_efectiva), endpoint=False)  # 44100 Hz es una frecuencia de muestreo común
pulso_tecnica = np.zeros_like(t)
pulso_fisiologica = np.zeros_like(t)

#Alarma tecnica
for i in range(1, num_componentes + 1):
    componente = np.sin(2 * np.pi * i * frecuencia_pulso_tecnica * t) / i
    pulso_tecnica += componente

#Alarma fisiologica
for i in range(1, num_componentes + 1):
    componente = np.sin(2 * np.pi * i * frecuencia_pulso_fisiologica * t) / i
    pulso_fisiologica += componente

# Aplicar rise time
rise_samples = int(44100 * rise_time)
pulso_tecnica[:rise_samples] *= np.linspace(0, 1, rise_samples)
pulso_fisiologica[:rise_samples] *= np.linspace(0, 1, rise_samples)

# Aplicar fall time
fall_samples = int(44100 * fall_time)
pulso_tecnica[-fall_samples:] *= np.linspace(1, 0, fall_samples)
pulso_fisiologica[-fall_samples:] *= np.linspace(1, 0, fall_samples)

# Normalizar la amplitud
pulso_tecnica /= np.max(np.abs(pulso_tecnica))
pulso_fisiologica /= np.max(np.abs(pulso_fisiologica))

# Guardar el pulso como un archivo WAV
write("C:/Users/Zakie Assad/Proyecto Final/Git/MoAna/Codigos/Windows/pulso_personalizado_tecnica.wav", 44100, pulso_tecnica)
write("C:/Users/Zakie Assad/Proyecto Final/Git/MoAna/Codigos/Windows/pulso_personalizado_fisiologica.wav", 44100, pulso_fisiologica)


# Reproducir el archivo de audio con pygame
pygame.mixer.init()
pygame.mixer.music.load("C:/Users/Zakie Assad/Proyecto Final/Git/MoAna/Codigos/Windows/pulso_personalizado_fisiologica.wav")
pygame.mixer.music.play()

# Esperar hasta que se termine de reproducir
pygame.time.wait(int(duracion_efectiva * 1000))  # Esperar según la duración del pulso en milisegundos

# Detener la reproducción (opcional)
pygame.mixer.music.stop()
