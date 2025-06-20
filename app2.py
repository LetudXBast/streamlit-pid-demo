import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("Simulation d'une bassine avec correcteur proportionnel")

# 🔧 Curseurs interactifs
T_max = st.slider("Durée de la simulation (minutes)", 10, 200, 50)
Kp = st.slider("Gain proportionnel Kp", 0.0, 2.0, 0.2, step=0.05)
Q_in_manual = st.slider("Débit d'entrée Q_in (m³/min) si Kp = 0", 0.0, 1.0, 0.2, step=0.01)
Q_out = st.slider("Débit de sortie Q_out (m³/min)", 0.0, 1.0, 0.1, step=0.01)
initial_height = st.slider("Hauteur initiale h_init (m)", 0.0, 2.0, 0.0, step=0.05)

# 📈 Temps de simulation
time = np.linspace(0, T_max, 500)
dt = time[1] - time[0]
setpoint = 1.0  # m
A = 1.0  # surface en m²

# 🧮 Simulation
height = np.zeros_like(time)
height[0] = initial_height

for i in range(1, len(time)):
    error = setpoint - height[i-1]
    if Kp > 0:
        Q_in = Kp * error
        Q_in = max(Q_in, 0)  # pas de débit négatif
    else:
        Q_in = Q_in_manual
    height[i] = height[i-1] + ((Q_in - Q_out) / A) * dt

# 🎨 Affichage
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(time, height, label="Hauteur d'eau", color='blue')
ax.axhline(setpoint, color='red', linestyle='--', label='Consigne (1 m)')
ax.set_xlabel("Temps (min)")
ax.set_ylabel("Hauteur d'eau (m)")
ax.set_title("Remplissage d'une bassine avec ou sans régulation")
ax.legend()
ax.grid(True)

st.pyplot(fig)
