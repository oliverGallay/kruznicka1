import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from datetime import datetime

st.set_page_config(page_title="Kružnica – body", page_icon="⚪", layout="centered")
st.title("Kružnica – rovnomerné body")

# Bočný panel – info o autorovi a technológiách (bod 3)
st.sidebar.header("Informácie")
name = st.sidebar.text_input("Tvoje meno", value="Meno Priezvisko")
email = st.sidebar.text_input("Email", value="tvoj@email.com")
st.sidebar.text_area("Použité technológie", value="Python, Streamlit, matplotlib")

# Vstupy (bod 1)
st.subheader("Vstupné parametre")
col1, col2 = st.columns(2)
with col1:
    x0 = st.number_input("Stred X", value=0.0, step=0.1, format="%.2f")
    r  = st.number_input("Polomer r", value=5.0, min_value=0.0, step=0.1, format="%.2f")
    unit = st.text_input("Jednotka na osiach", value="m")
with col2:
    y0 = st.number_input("Stred Y", value=0.0, step=0.1, format="%.2f")
    n  = st.number_input("Počet bodov", min_value=1, max_value=360, value=12)
    color = st.color_picker("Farba bodov", value="#1f77b4")

# Výpočet bodov na kružnici
angles = np.linspace(0, 2*np.pi, int(n), endpoint=False)
xs = x0 + r*np.cos(angles)
ys = y0 + r*np.sin(angles)

# Vykreslenie s osami a jednotkami (bod 2)
fig, ax = plt.subplots(figsize=(6, 6))
ax.plot(x0, y0, marker="x")                  # stred
ax.scatter(xs, ys, s=50, c=color)           # body
circle = plt.Circle((x0, y0), r, fill=False, linestyle="--")
ax.add_artist(circle)

# Očíslovanie bodov
for i, (xi, yi) in enumerate(zip(xs, ys), start=1):
    ax.annotate(str(i), (xi, yi), textcoords="offset points", xytext=(5, 5), fontsize=8)

ax.set_aspect("equal", adjustable="box")
ax.set_xlabel(f"X [{unit}]")
ax.set_ylabel(f"Y [{unit}]")
ax.grid(True, linewidth=0.5, alpha=0.6)
ax.set_title("Body na kružnici")

# Text s parametrami priamo do obrázka (bod 4)
param_text = (
    f"Stred=({x0:.2f}, {y0:.2f}) | r={r:.2f} {unit} | n={n} | farba={color}\n"
    f"Autor: {name} | {email} | {datetime.now():%Y-%m-%d %H:%M}"
)
fig.text(0.02, 0.02, param_text, fontsize=8)

# Zobrazenie v appke
st.pyplot(fig, use_container_width=True)

# Export do PDF (bod 4)
buf = BytesIO()
fig.savefig(buf, format="pdf", bbox_inches="tight")
st.download_button(
    "Stiahnuť PDF s grafom a parametrami",
    data=buf.getvalue(),
    file_name="kruznica.pdf",
    mime="application/pdf",
)
