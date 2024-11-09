import numpy as np
import matplotlib.pyplot as plt

# Die normierte Übertragungsfunktion
def transfer_function(omega, delta, omega_0):
    """
    Berechnet die normierte Übertragungsfunktion H(omega).

    Args:
        omega (array): Kreisfrequenz [rad/s].
        delta (float): Dämpfungsfaktor.
        omega_0 (float): Eigenkreisfrequenz [rad/s].

    Returns:
        array: Betrag der normierten Übertragungsfunktion H(omega).
    """
    denominator = -omega**2 + 2j * delta * omega + omega_0**2
    numerator = omega_0**2  # Normierung auf H(0)
    return numerator / denominator

# Parameter
omega = np.linspace(-10, 10, 1000)  # Frequenzen [rad/s]
delta = 0.00001  # Dämpfungsfaktor
omega_0 = 2 * np.pi * 0.6  # Eigenkreisfrequenz für f0 = 1 Hz

# Übertragungsfunktion berechnen
H = transfer_function(omega, delta, omega_0)

# Betrag und Phase berechnen
H_magnitude = np.abs(H)  # Betrag korrekt berechnet
H_phase = np.angle(H)    # Phase korrekt berechnet

# Plot der Ergebnisse
plt.figure(figsize=(12, 6))

# Betrag der Übertragungsfunktion
plt.subplot(2, 1, 1)
plt.plot(omega, H_magnitude, label=f"$\delta={delta}$, $\\omega_0={omega_0/(2*np.pi):.2f}$ Hz")
plt.title("Betrag der normierten Übertragungsfunktion")
plt.xlabel("Kreisfrequenz $\\omega$ [rad/s]")
plt.ylabel("$|H(\\omega)|$")
plt.ylim(0, 1.2)  # Begrenzung auf sinnvolle Werte
plt.grid()
plt.legend()

# Phase der Übertragungsfunktion
plt.subplot(2, 1, 2)
plt.plot(omega, H_phase, label=f"$\delta={delta}$, $\\omega_0={omega_0/(2*np.pi):.2f}$ Hz")
plt.title("Phase der normierten Übertragungsfunktion")
plt.xlabel("Kreisfrequenz $\\omega$ [rad/s]")
plt.ylabel("Phase $\\arg(H(\\omega))$ [rad]")
plt.grid()
plt.legend()

plt.tight_layout()
plt.show()
