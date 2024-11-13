import wave
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd

# Fonction pour charger un fichier WAV et extraire ses métadonnées
def charger_fichier_wav(chemin_fichier):
    try:
        with wave.open(chemin_fichier, 'rb') as fichier_audio:
            nb_canaux = fichier_audio.getnchannels()
            taux_echantillonnage = fichier_audio.getframerate()
            nb_frames = fichier_audio.getnframes()
            largeur_echantillon = fichier_audio.getsampwidth()
            duree = nb_frames / taux_echantillonnage
            
            print("Métadonnées du fichier WAV:")
            print(f"Nombre de canaux: {nb_canaux}")
            print(f"Taux d'échantillonnage: {taux_echantillonnage} Hz")
            print(f"Largeur d'échantillon: {largeur_echantillon * 8} bits")
            print(f"Durée: {duree:.2f} secondes")

            # Lecture des données brutes
            donnees_brutes = fichier_audio.readframes(nb_frames)
            donnees_audio = np.frombuffer(donnees_brutes, dtype=np.int16)

            # Si l'audio est stéréo, le convertir en tableau 2D
            if nb_canaux == 2:
                donnees_audio = np.reshape(donnees_audio, (nb_frames, nb_canaux))
            
            return donnees_audio, taux_echantillonnage, nb_canaux
    except FileNotFoundError:
        print("Erreur: Fichier non trouvé. Assurez-vous que le chemin est correct.")
        return None, None, None

# Fonction pour afficher un oscillographe
def afficher_oscillographe(donnees_audio, taux_echantillonnage, nb_canaux):
    plt.figure(figsize=(12, 6))
    temps = np.linspace(0, len(donnees_audio) / taux_echantillonnage, num=len(donnees_audio))
    
    if nb_canaux == 1:
        plt.plot(temps, donnees_audio, label='Mono', color='blue')
    else:
        plt.plot(temps, donnees_audio[:, 0], label='Canal gauche', color='green')
        plt.plot(temps, donnees_audio[:, 1], label='Canal droit', color='red')

    plt.xlabel('Temps (secondes)')
    plt.ylabel('Amplitude')
    plt.title('Oscillographe du fichier WAV')
    plt.legend()
    plt.grid()
    plt.show()

# Fonction pour créer un signal déphasé et le sommer avec le signal original
def somme_dephasee(donnees_audio, decalage):
    # Assurez-vous que le décalage est valide
    if decalage <= 0 or decalage >= len(donnees_audio):
        print("Erreur: Le décalage est trop grand ou invalide.")
        return donnees_audio
    
    # Créer un signal déphasé en décalant de `decalage` échantillons
    signal_dephase = np.zeros_like(donnees_audio)
    if donnees_audio.ndim == 1:  # Mono
        signal_dephase[decalage:] = donnees_audio[:-decalage]
    else:  # Stéréo
        signal_dephase[decalage:, :] = donnees_audio[:-decalage, :]

    # Somme des deux signaux
    signal_somme = (donnees_audio + signal_dephase) * 0.5

    # Normalisation pour éviter les saturations
    max_val = np.max(np.abs(signal_somme))
    if max_val > 0:
        signal_somme = signal_somme / max_val * np.iinfo(donnees_audio.dtype).max

    return signal_somme.astype(donnees_audio.dtype)

# Fonction pour lire l'audio
def lire_audio(donnees_audio, taux_echantillonnage):
    print("Lecture de l'audio...")
    sd.play(donnees_audio, taux_echantillonnage)
    sd.wait()  # Attend que la lecture soit terminée
    print("Lecture terminée.")

# Boucle principale pour interagir avec l'utilisateur
while True:
    chemin_fichier = input("Entrez le chemin du fichier WAV (ou 'q' pour quitter) : ")
    
    if chemin_fichier.lower() == 'q':
        print("Programme terminé.")
        break
    
    donnees_audio, taux_echantillonnage, nb_canaux = charger_fichier_wav(chemin_fichier)
    
    if donnees_audio is not None:
        afficher_oscillographe(donnees_audio, taux_echantillonnage, nb_canaux)
        
        # Appliquer le traitement de déphasage et somme
        decalage = int(input("Entrez le décalage en échantillons pour le déphasage : "))
        donnees_traitees = somme_dephasee(donnees_audio, decalage)
        
        # Afficher l'oscillographe du signal traité
        afficher_oscillographe(donnees_traitees, taux_echantillonnage, nb_canaux)
        
        # Lire le signal traité
        lire_audio(donnees_traitees, taux_echantillonnage)
