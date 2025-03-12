import numpy as np
import wave
import struct

# Paramètres du signal
frequency = 440  # Fréquence en Hz
duration = 15  # Durée en secondes
sampling_rate = 44100  # Fréquence d'échantillonnage en Hz
amplitude = 32767  # Amplitude max pour une quantification sur 16 bits

# Génération des échantillons
t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
signal = amplitude * np.sin(2 * np.pi * frequency * t)

# Conversion en entiers 16 bits
signal = signal.astype(np.int16)

# Création du fichier WAV
output_file = "sine_440Hz.wav"
with wave.open(output_file, 'w') as wav_file:
    wav_file.setnchannels(1)  # Mono
    wav_file.setsampwidth(2)  # 16 bits = 2 octets
    wav_file.setframerate(sampling_rate)
    
    # Encodage et écriture des échantillons
    for sample in signal:
        wav_file.writeframes(struct.pack('<h', sample))

print(f"Fichier WAV généré: {output_file}")
