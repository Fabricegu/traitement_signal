import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, freqz

def plot_bode(b, a, fs=1.0):
    """
    Trace uniquement la magnitude du diagramme de Bode d'un filtre numérique.

    Paramètres :
    - b : coefficients du numérateur du filtre.
    - a : coefficients du dénominateur du filtre.
    - fs : fréquence d'échantillonnage en Hz (par défaut 1.0).
    """
    # Calcul de la réponse en fréquence avec une meilleure résolution
    w, h = freqz(b, a, worN=16000)

    # Conversion des pulsations en fréquence (Hz)
    freqs = w * fs / (2 * np.pi)

    # Calcul du gain en décibels
    magnitude = 20 * np.log10(abs(h))

    # Tracé de la magnitude avec une échelle logarithmique pour l'axe des fréquences
    plt.figure(figsize=(12, 6))
    plt.semilogx(freqs, magnitude, linewidth=1.5)
    plt.title("Diagramme de Bode (Magnitude)")
    plt.xlabel("Fréquence (Hz)")
    plt.ylabel("Gain (dB)")
    plt.grid(which="both", linestyle="--", linewidth=0.5)
    plt.tight_layout()
    plt.show()

def filter_example():
    """
    Exemple de démonstration d'un filtre passe-bas Butterworth du quatrième ordre.
    """
    # Paramètres du filtre
    fs = 5000  # Fréquence d'échantillonnage en Hz
    fc = 60   # Fréquence de coupure en Hz
    order = 4  # Ordre du filtre

    # Conception du filtre Butterworth
    b, a = butter(order, fc / (fs / 2), btype='low')

    # Affichage des coefficients du filtre
    print("Coefficients du numérateur (b):", b)
    print("Coefficients du dénominateur (a):", a)

    # Affichage du diagramme de Bode
    plot_bode(b, a, fs)

    # Génération d'un signal d'entrée avec une meilleure résolution temporelle
    n = 1000  # Plus de points pour une meilleure résolution
    t = np.arange(n) / fs
    x = np.sin(2 * np.pi * 50 * t) + np.sin(2 * np.pi * 200 * t)  # Signal mixte (50 Hz et 200 Hz)

    # Application du filtre avec l'équation de récurrence
    y = [0] * len(x)  # Initialisation du signal de sortie
    for n in range(len(x)):
        # Partie liée à l'entrée
        y[n] += sum(b[k] * x[n - k] for k in range(len(b)) if n - k >= 0)
        # Partie liée à la rétroaction
        y[n] -= sum(a[k] * y[n - k] for k in range(1, len(a)) if n - k >= 0)

    # Tracé du signal d'entrée et de sortie avec des lignes plus lisses
    plt.figure(figsize=(12, 6))
    plt.plot(t, x, label="Signal d'entrée (non filtré)", linewidth=1.5)
    plt.plot(t, y, label="Signal de sortie (filtré)", linestyle='--', linewidth=1.5)
    plt.title("Signal avant et après filtrage")
    plt.xlabel("Temps (s)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid()
    plt.show()

# Exemple avec un filtre passe-bas Butterworth du quatrième ordre
filter_example()
