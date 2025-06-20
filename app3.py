import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# 🔧 Widgets Streamlit
st.title("Simulation PID sur système du 1er ordre")
with st.expander("📘 Afficher / masquer l'introduction pédagogique", expanded=True):
    st.markdown(r"""
    ## 🧪 Objectif pédagogique

    Ce simulateur interactif permet de comprendre l'effet des différents termes d'un **correcteur PID** sur la réponse d’un système du premier ordre.

    Vous pouvez :
    - Modifier les gains **proportionnel** (`Kp`), **intégral** (`Ki`) et **dérivatif** (`Kd`)
    - Visualiser la réponse du système \( y(t) \)
    - Observer la commande envoyée \( u(t) \)

    ---

    ## 🎯 Objectif de la régulation

    Le système doit atteindre la **consigne** (ici : 1) **rapidement**, **sans dépassement excessif**, **sans oscillations**, et **avec une erreur finale nulle**.

    ---

    ## 📌 Consigne : interpréter

    Après chaque réglage :
    - Identifiez l’effet des variations de chaque paramètre.
    - Essayez de régler le système pour qu’il atteigne la consigne dans un délai court avec une réponse stable.

    ---
    """)

# 🔧 Curseurs interactifs
Kp = st.slider("Gain proportionnel Kp", 0.0, 10.0, 2.0, step=0.1)
Ki = st.slider("Gain intégral Ki", 0.0, 2.0, 0.0, step=0.05)
Kd = st.slider("Gain dérivatif Kd", 0.0, 5.0, 0.0, step=0.05)
t_max = st.slider("Durée de simulation", 10, 100, 50, step=5)

# 📈 Modèle du système
def process_model(y, t, u, K_process=1.0, tau=5.0):
    dydt = (-y + K_process * u) / tau
    return dydt

# 🔁 Simulation
def pid_simulation(Kp, Ki, Kd, setpoint=1.0, t_max=50, dt=0.1):
    t = np.arange(0, t_max, dt)
    y = np.zeros_like(t)
    u = np.zeros_like(t)
    e = np.zeros_like(t)
    integral = 0
    prev_error = 0

    for i in range(1, len(t)):
        e[i] = setpoint - y[i-1]
        integral += e[i] * dt
        derivative = (e[i] - prev_error) / dt
        u[i] = Kp * e[i] + Ki * integral + Kd * derivative
        y[i] = odeint(process_model, y[i-1], [t[i-1], t[i]], args=(u[i],))[-1]
        prev_error = e[i]

    return t, y, u

# ▶️ Exécution
t, y, u = pid_simulation(Kp, Ki, Kd, t_max=t_max)

# 🎨 Affichage des courbes
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Courbe y(t)
ax1.plot(t, y, label='Sortie $y(t)$', linewidth=2)
ax1.axhline(1.0, color='gray', linestyle='--', linewidth=1)
ax1.axhline(0.95, color='red', linestyle='--', linewidth=1)
ax1.axhline(1.05, color='red', linestyle='--', linewidth=1)
ax1.set_title('Réponse du système', weight='bold')
ax1.set_xlabel('Temps (s)', weight='bold')
ax1.set_ylabel('Sortie', weight='bold')
ax1.legend()
ax1.grid(True)

# Courbe u(t)
ax2.plot(t, u, label='Commande $u(t)$', color='orange', linewidth=2)
ax2.set_title('Commande envoyée', weight='bold')
ax2.set_xlabel('Temps (s)', weight='bold')
ax2.set_ylabel('Commande', weight='bold')
ax2.legend()
ax2.grid(True)

# Axes en gras avec flèches
for ax in [ax1, ax2]:
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_linewidth(1.5)
    ax.spines['bottom'].set_linewidth(1.5)
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.tick_params(width=1.5)
    ax.annotate('', xy=(t[-1], 0), xytext=(0, 0),
                arrowprops=dict(facecolor='black', arrowstyle='->', lw=1.5))
    ax.annotate('', xy=(0, max(ax.get_ylim())), xytext=(0, 0),
                arrowprops=dict(facecolor='black', arrowstyle='->', lw=1.5))

# 🎯 Affichage Streamlit
st.pyplot(fig)
