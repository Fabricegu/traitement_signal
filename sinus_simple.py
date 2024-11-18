import numpy as np
import matplotlib.pyplot as plt

# Paramètres
f = 120  # Fréquence de la sinusoïde en Hz
fs = 48000  # Fréquence d'échantillonnage en Hz
duration = 0.05  # Durée de la sinusoïde en secondes (par exemple, 50 ms)

# Génération de l'axe temporel
t = np.linspace(0, duration, int(fs * duration), endpoint=False)

# Génération de la sinusoïde
y = np.sin(2 * np.pi * f * t)

# Affichage du signal
plt.figure(figsize=(10, 4))
plt.plot(t, y)
plt.title(f"Sinusoïde à {f} Hz avec une fréquence d'échantillonnage de {fs} Hz")
plt.xlabel("Temps (s)")
plt.ylabel("Amplitude")
plt.grid(True)
plt.show()
