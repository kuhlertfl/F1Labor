import numpy as np 
import matplotlib.pyplot as plt 

# Widerstand [Ohm]
R_1 = 560
R_2 = 560

# Kapazitaet [F]
C_1 = 150e-9
C_2 = 150e-9

# Frequenzachse 
f = np.arange(10,50e3,10)
omega = 2 * np.pi * f 


# Werte die Uebertragungsfunktion aus 
H = (R_2/(1 + 1j*omega*R_2*C_2)) / (R_1 + 1/(1j*omega*C_1) + R_2/(1 + 1j*omega*R_2*C_2))

# Plotte Betrag und Phase 
fig, (ax1,ax2) = plt.subplots(2,1)
fig.set_tight_layout(True)

ax1.set_title("Betrag der Uebertragsfunktion")
ax1.set_xlabel("f [kHz]")
ax1.set_ylabel("[H]")
ax1.grid(True)
ax1.plot(f / 1e3 , np.abs(H))

ax2.set_title("Phase der Uebertragsfunktion")
ax2.set_xlabel("f [kHz]")
ax2.set_ylabel("arg(H) [rad]")
ax2.grid(True)
ax2.plot(f / 1e3 , np.angle(H , deg=True))

plt.show()