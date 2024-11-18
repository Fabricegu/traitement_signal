import numpy as np
import matplotlib.pyplot as plt

# Paramètres communs
fs = 48000  # Fréquence d'échantillonnage en Hz
duration = 0.01  # Durée de la sinusoïde en secondes (par exemple, 10 ms)
t = np.linspace(0, duration, int(fs * duration), endpoint=False)

# Fonction pour générer une sinusoïde avec une fréquence et une phase spécifiée
def generate_sine_wave(frequency, phase_degree, sampling_rate, duration):
    phase_radians = np.deg2rad(phase_degree)
    return np.sin(2 * np.pi * frequency * t + phase_radians)

# Caractéristiques des sinusoïdes
sinusoids = [(120, 0),
    (260, 45),
    (1080, 10),
    (4120, 0),
    (440, 90),
    (2080, 30)
]

# Tracé des sinusoïdes
plt.figure(figsize=(12, 10))

for i, (freq, phase) in enumerate(sinusoids, 1):
    y = generate_sine_wave(freq, phase, fs, duration)
    plt.subplot(6, 1, i)
    plt.plot(t, y)
    plt.title(f"Sinusoïde à {freq} Hz avec une phase de {phase}°")
    plt.xlabel("Temps (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)

plt.tight_layout()
plt.show()
