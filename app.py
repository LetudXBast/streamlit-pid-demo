import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("Simulation de la hauteur d'eau dans une bassine avec correcteur proportionnel")

# 📈 Temps de simulation
time = np.linspace(0, T_max, 500)
dt = time[1] - time[0]
setpoint = 1.0  # m
A = 1.0  # surface en m²

# 🧮 Simulation
height = np.zeros_like(time)
height[0] = initial_height
empty_flag = False  # Pour détecter si la bassine se vide

for i in range(1, len(time)):
    error = setpoint - height[i-1]

    if Kp > 0:
        Q_in = max(Kp * error, 0)
    else:
        Q_in = Q_in_manual

    dh = ((Q_in - Q_out) / A) * dt
    height[i] = height[i-1] + dh

    # ✅ Empêcher une hauteur négative
    if height[i] < 0:
        empty_flag = True
        height[i] = 0

# 📢 Affichage d'une alerte si la bassine s’est vidée
if empty_flag:
    st.warning("⚠️ La bassine s’est complètement vidée pendant la simulation. Vérifiez vos paramètres.")

# 🎨 Tracé du graphique
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(time, height, label="Hauteur d'eau", color='blue')
ax.axhline(setpoint, color='red', linestyle='--', label='Consigne (1 m)')

# Axes personnalisés
ax.spines['left'].set_position('zero')
ax.spines['bottom'].set_position('zero')
ax.spines['left'].set_linewidth(1.5)
ax.spines['bottom'].set_linewidth(1.5)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.tick_params(width=1.5)

# Flèches pour les axes
ax.annotate('', xy=(T_max, 0), xytext=(0, 0),
            arrowprops=dict(facecolor='black', arrowstyle='->', lw=1.5))
ax.annotate('', xy=(0, max(height) + 0.1), xytext=(0, 0),
            arrowprops=dict(facecolor='black', arrowstyle='->', lw=1.5))

ax.set_xlim(0, T_max)
ax.set_ylim(-0.1, max(height) + 0.1)
ax.set_xlabel("Temps (min)", weight='bold')
ax.set_ylabel("Hauteur d'eau (m)", weight='bold')
ax.set_title("Remplissage d'une bassine avec ou sans régulation", weight='bold')
ax.legend()
ax.grid(True)

st.pyplot(fig)
