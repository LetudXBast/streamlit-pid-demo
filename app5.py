import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import random

import plotly.graph_objects as go # Pour les graphiques interactifs (zoom...)

import streamlit.components.v1 as components
import streamlit as st

if st.runtime.scriptrunner.script_run_context.is_running_with_streamlit:
    is_mobile = st.runtime.scriptrunner.script_run_context.user_info.device_info.screen_width < 500
else:
    is_mobile = False

# ensuite adapter width :
plot_width = 350 if is_mobile else 700


# --- Configuration Streamlit ---
st.set_page_config(page_title="Devine la fonction", layout="centered")
st.title("🎯 Devine la fonction cachée")


with st.expander("ℹ️ Comment proposer une fonction ?", expanded=False):
    st.markdown(r"""
    Voici quelques règles pour écrire correctement une fonction :

    - Utilise `x` comme variable.
    - Les opérations doivent suivre la syntaxe Python :
        - Multiplication : `*` → exemple : `3*x`
        - Puissance : `**` → exemple : `x**2` pour \(x^2\)
        - Division : `/` → exemple : `1/x`
        - Parenthèses : `()` pour grouper les expressions
    - Fonctions usuelles disponibles :
        - `sin(x)` : sinus
        - `cos(x)` : cosinus
        - `exp(x)` : exponentielle \(e^x\)
        - `log(x)` : logarithme népérien
        - `sqrt(x)` : racine carrée
        - `abs(x)` : valeur absolue
    - ⚠️ Évite d’écrire `e^x`, préfère `exp(x)`
    - Exemple valide : `exp(-x**2) + sin(x)`

    Essaie de proposer une fonction continue et définie sur \[-6 ; 6\].
    """)


# --- Définition des fonctions cibles disponibles ---
x = sp.Symbol('x')
easy_functions = [
    x,
    2*x,
    -x,
    x + 3,
    x - 2,
    x**2,
    -x**2,
    x**2 + 2,
    x**2 - 3*x + 1,
    -x**2 + 4*x - 1,
    x**3,
    -x**3 + x,
    x**3 - 3*x,
    sp.Abs(x),
    sp.sqrt(x + 6),  # définie sur [-6; 6]
    sp.exp(x),
    sp.exp(-x),
    sp.log(x + 7),   # définie sur [-6; 6]
    sp.sin(x),
    sp.cos(x)
]

hard_functions = [
    x**3 - x,
    sp.Abs(x),
    x**2 + sp.sin(x),
    sp.sin(x),
    sp.cos(x) + 1,
    sp.sqrt(sp.Abs(x)),
    sp.exp(-x**2),
    x * sp.exp(-x**2),
    sp.sin(x**2),
    sp.log(x**2 + 1),
    x**2 * sp.cos(x),
    sp.cos(x) / (x + 0.01)
]

# --- Choix du niveau ---
niveau = st.radio("Choisis ton niveau :", ["Facile", "Difficile"], horizontal=True)

# --- Génération de la fonction cible ---
if "target_expr" not in st.session_state:
    st.session_state["niveau"] = niveau
    st.session_state["target_expr"] = random.choice(easy_functions if niveau == "Facile" else hard_functions)

# --- Changement de fonction si clic sur bouton ---
if st.button("🔄 Nouvelle fonction"):
    st.session_state["niveau"] = niveau
    st.session_state["target_expr"] = random.choice(easy_functions if niveau == "Facile" else hard_functions)


# --- Fonction cible courante ---
target_expr = st.session_state["target_expr"]
target_func = sp.lambdify(x, target_expr, 'numpy')

# --- Saisie utilisateur ---
user_input = st.text_input("Propose une fonction en x :", value="x")

# --- Tracé des courbes ---
x_vals = np.linspace(-6, 6, 500)
try:
    user_expr = sp.sympify(user_input)
    user_func = sp.lambdify(x, user_expr, 'numpy')

    y_target = target_func(x_vals)
    y_user = user_func(x_vals)

    # Calcul de l'écart
    score = np.mean(np.abs(y_target - y_user))

    # --- Tracé interactif Plotly ---
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x_vals, y=y_target,
        mode='lines',
        name='Fonction cible',
        line=dict(color='blue')
    ))

    fig.add_trace(go.Scatter(
        x=x_vals, y=y_user,
        mode='lines',
        name='Ta fonction',
        line=dict(color='red', dash='dash')
    ))

    fig.update_layout(
        title="Comparaison des courbes",
        xaxis_title="x",
        yaxis_title="y",
        legend=dict(x=0.02, y=0.98),
        height=500
    )

    fig.update_xaxes(
    showgrid=True,
    zeroline=True,
    zerolinewidth=2,
    zerolinecolor='black',
    linecolor='black',
    linewidth=2,
    mirror=True,
    title_font=dict(size=16, color='black', family='Arial',),
    tickfont=dict(size=14, color='black')
)

    fig.update_yaxes(
    showgrid=True,
    zeroline=True,
    zerolinewidth=2,
    zerolinecolor='black',
    linecolor='black',
    linewidth=2,
    mirror=True,
    title_font=dict(size=16, color='black', family='Arial',),
    tickfont=dict(size=14, color='black')
)


    st.plotly_chart(fig, use_container_width=False, width=360, height=400)

    # --- Feedback ---
    if score < 0.1:
        st.success("🎉 Bravo, tu as trouvé la bonne fonction !")
    elif score < 1:
        st.info("🧐 Tu t'en rapproches.")
    else:
        st.warning("❌ Essaie encore.")

    st.write(f"Écart moyen entre les courbes : {score:.3f}")

except Exception as e:
    st.error(f"Erreur dans la fonction saisie : {e}")
