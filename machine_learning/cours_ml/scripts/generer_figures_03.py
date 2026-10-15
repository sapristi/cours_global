"""Génère les figures de la partie 03 - Classification et séparations linéaires.
Usage: uv run --with matplotlib --with numpy python scripts/generer_figures_03.py
Sorties: assets/03-*.png
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "assets")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({"font.size": 10, "axes.grid": True, "grid.alpha": 0.3})

# 1. Lecture géométrique : hyperplan, w normal, exemple (2,0)
fig, ax = plt.subplots(figsize=(5.5, 4.5))
xs = np.linspace(-0.5, 2.5, 100)
ax.plot(xs, xs, "k-", linewidth=2, label="frontière $w^Tx+b=0$")
xx, yy = np.meshgrid(np.linspace(-0.5, 2.5, 200), np.linspace(-0.5, 2.5, 200))
Z = 1 * xx - 1 * yy
ax.contourf(xx, yy, Z, levels=[-10, 0, 10], colors=["#cfe0ff", "#ffd9c9"], alpha=0.5)
ax.text(0.0, 1.9, "côté −1\n($h<0$)", fontsize=9)
ax.text(1.7, 0.55, "côté +1\n($h>0$)", fontsize=9)
ax.annotate("", xy=(1.5, 0.8), xytext=(1.15, 1.15),
            arrowprops=dict(facecolor="black", shrink=0.05, width=1.5, headwidth=7))
ax.text(1.55, 0.65, "$w$ (normal)", fontsize=10)
ax.plot(2.0, 0.0, "o", color="red", markersize=8)
ax.text(1.55, -0.3, "$(2,0)$ → +1", fontsize=9)
ax.set_xlim(-0.5, 2.5)
ax.set_ylim(-0.5, 2.5)
ax.set_xlabel("$x_1$")
ax.set_ylabel("$x_2$")
ax.set_title("Séparation linéaire : $w=(1,-1)$, $b=0$")
ax.legend(loc="upper left", fontsize=8)
ax.set_aspect("equal")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "03-geometrie-hyperplan.png"), dpi=150)
print("ok 03-geometrie-hyperplan.png")


def plot_logic(points, labels, w, b, title, fname, note=""):
    fig, ax = plt.subplots(figsize=(4.8, 4.2))
    pts = np.array(points)
    labs = np.array(labels)
    pos = pts[labs == 1]
    neg = pts[labs == -1]
    ax.scatter(pos[:, 0], pos[:, 1], s=120, marker="o", label="classe +1",
               edgecolors="k", color="#e67e22", zorder=3)
    ax.scatter(neg[:, 0], neg[:, 1], s=120, marker="s", label="classe −1",
               edgecolors="k", color="#3498db", zorder=3)
    for (x1, x2), y in zip(points, labels):
        ax.text(x1 + 0.06, x2 + 0.06, f"({x1},{x2})", fontsize=8)
    xs = np.linspace(-0.6, 1.6, 100)
    if abs(w[1]) > 1e-9:
        ys = -(w[0] * xs + b) / w[1]
        ax.plot(xs, ys, "k--", linewidth=2, label=f"frontière $w={tuple(w)}, b={b}$")
    xx, yy = np.meshgrid(np.linspace(-0.6, 1.6, 200), np.linspace(-0.6, 1.6, 200))
    Z = w[0] * xx + w[1] * yy + b
    ax.contourf(xx, yy, Z, levels=[-10, 0, 10], colors=["#cfe0ff", "#ffd9c9"], alpha=0.35)
    ax.set_xlim(-0.6, 1.6)
    ax.set_ylim(-0.6, 1.6)
    ax.set_xlabel("$x_1$")
    ax.set_ylabel("$x_2$")
    ax.set_title(title)
    if note:
        ax.text(0.5, -0.35, note, ha="center", fontsize=8, style="italic")
    ax.legend(fontsize=8, loc="best")
    ax.set_aspect("equal")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, fname), dpi=150)
    print("ok", fname)


plot_logic([(0, 0), (0, 1), (1, 0), (1, 1)], [-1, 1, 1, 1],
           w=(1, 1), b=-0.5, title="OU logique : séparable",
           fname="03-exemple-OU.png")
plot_logic([(0, 0), (0, 1), (1, 0), (1, 1)], [-1, -1, -1, 1],
           w=(1, 1), b=-1.5, title="ET logique : séparable",
           fname="03-exemple-ET.png")
plot_logic([(0, 0), (1, 1), (0, 1), (1, 0)], [-1, -1, 1, 1],
           w=(1, 1), b=-0.5, title="XOR : non séparable (droite en échec)",
           fname="03-exemple-XOR.png",
           note="aucune droite ne sépare ○ et ■")

# 2. Rosenblatt avant/après : une seule correction qui fait basculer le point raté
neg_pts = np.array([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0]])
pos_pts = np.array([[3.0, 3.0], [2.5, 2.5], [2.0, 2.0]])
w_before = np.array([1.0, 1.0]); b_before = -4.8
eta_demo = 0.5
x_err = np.array([2.0, 2.0]); y_err = 1  # seul mal classé avant
w_after = w_before + eta_demo * y_err * x_err
b_after = b_before + eta_demo * y_err

fig, axes = plt.subplots(1, 2, figsize=(9, 4), sharex=True, sharey=True)
for axi, w, b, title in [
    (axes[0], w_before, b_before, "Avant : (2,2) +1 mal classé"),
    (axes[1], w_after, b_after, "Après : correction, 0 erreur"),
]:
    xx, yy = np.meshgrid(np.linspace(-0.5, 3.5, 200), np.linspace(-0.5, 3.5, 200))
    Z = w[0] * xx + w[1] * yy + b
    axi.contourf(xx, yy, Z, levels=[-10, 0, 10], colors=["#cfe0ff", "#ffd9c9"], alpha=0.35)
    xs = np.linspace(-0.5, 3.5, 100)
    ys = -(w[0] * xs + b) / w[1]
    axi.plot(xs, ys, "k-", linewidth=2)
    axi.scatter(neg_pts[:, 0], neg_pts[:, 1], s=110, marker="s",
                edgecolors="k", color="#3498db", label="classe −1", zorder=3)
    axi.scatter(pos_pts[:, 0], pos_pts[:, 1], s=110, marker="o",
                edgecolors="k", color="#e67e22", label="classe +1", zorder=3)
    axi.set_xlim(-0.5, 3.5); axi.set_ylim(-0.5, 3.5)
    axi.set_xlabel("$x_1$"); axi.set_title(title, fontsize=10)
    axi.set_aspect("equal")
axes[0].set_ylabel("$x_2$")
# mise en évidence du point corrigé
axes[0].plot(2.0, 2.0, "o", ms=18, mfc="none", mec="red", mew=2)
axes[0].text(2.05, 1.55, "raté", color="red", fontsize=9)
axes[1].plot(2.0, 2.0, "o", ms=18, mfc="none", mec="green", mew=2)
axes[1].text(2.05, 1.55, "corrigé", color="green", fontsize=9)
fig.suptitle("Rosenblatt : $w \\leftarrow w + \\eta y x$, $b \\leftarrow b + \\eta y$ sur le seul point raté ($\\eta=0.5$)")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "03-rosenblatt-correction.png"), dpi=150)
print("ok 03-rosenblatt-correction.png")

# 3. Hebb vs Rosenblatt sur OU : erreurs et norme de w par époque
X_ou = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y_ou = np.array([-1, 1, 1, 1])
eta = 1.0
EPOCHS = 15

def run(rule):
    w = np.zeros(2); b = 0.0
    errs, norms = [], []
    for _ in range(EPOCHS):
        for xi, yi in zip(X_ou, y_ou):
            h = w.dot(xi) + b
            if rule == "rosenblatt":
                if yi * h <= 0:
                    w = w + eta * yi * xi; b = b + eta * yi
            else:  # hebb : toujours renforcer
                w = w + eta * yi * xi; b = b + eta * yi
        pred = np.where(X_ou.dot(w) + b >= 0, 1, -1)
        errs.append(int(np.sum(pred != y_ou)))
        norms.append(float(np.linalg.norm(w)))
    return np.array(errs), np.array(norms)

# 4. Pas-à-pas : données OU + poids initial + frontières après chaque époque
X_OU_PTS = [(0, 0), (0, 1), (1, 0), (1, 1)]
Y_OU = [-1, 1, 1, 1]

def draw_state(ax, w, b, title, sub=""):
    pts = np.array(X_OU_PTS); labs = np.array(Y_OU)
    pos = pts[labs == 1]; neg = pts[labs == -1]
    xx, yy = np.meshgrid(np.linspace(-0.6, 1.6, 200), np.linspace(-0.6, 1.6, 200))
    if np.linalg.norm(w) < 1e-9:
        ax.set_facecolor("#f0f0f0")
        if abs(b) < 1e-9:
            txt = "w=0, b=0 : pas de frontière\nh=0 partout, 4 erreurs (y·h≤0)"
        else:
            verdict = "tout classé +1" if b >= 0 else "tout classé −1"
            txt = f"w=0 : pas de frontière\n({verdict})"
        ax.text(0.5, 0.5, txt,
                ha="center", va="center", transform=ax.transAxes, fontsize=9)
    else:
        Z = w[0] * xx + w[1] * yy + b
        ax.contourf(xx, yy, Z, levels=[-1e9, 0, 1e9], colors=["#cfe0ff", "#ffd9c9"], alpha=0.35)
        xs = np.linspace(-0.6, 1.6, 100)
        if abs(w[1]) > 1e-9:
            ax.plot(xs, -(w[0] * xs + b) / w[1], "k-", linewidth=2)
        elif abs(w[0]) > 1e-9:
            ax.axvline(-b / w[0], color="k", linewidth=2)
    # points avec halo rouge si erreur au sens Rosenblatt (y*h <= 0, inclut h=0)
    H = pts.dot(np.array(w, dtype=float)) + b
    for (x1, x2), yi, hi in zip(X_OU_PTS, Y_OU, H):
        ax.scatter([x1], [x2], s=140, marker="o" if yi == 1 else "s",
                   edgecolors="k", color="#e67e22" if yi == 1 else "#3498db", zorder=3)
        if yi * hi <= 0:
            ax.plot(x1, x2, "o", ms=20, mfc="none", mec="red", mew=2)
    ax.set_xlim(-0.6, 1.6); ax.set_ylim(-0.6, 1.6)
    ax.set_xlabel("$x_1$"); ax.set_title(title, fontsize=9)
    if sub:
        ax.text(0.5, -0.38, sub, ha="center", fontsize=7, style="italic", transform=ax.transAxes)
    ax.set_aspect("equal")

# Rosenblatt : init -> fin E1 (1,1,1) -> fin E2 (1,1,0) -> final E5 (2,2,-1)
fig, axes = plt.subplots(2, 2, figsize=(8.5, 7))
states_r = [
    ((0, 0), 0.0, "Init : w=(0,0), b=0", "tout classé +1, (0,0) raté"),
    ((1, 1), 1.0, "Fin époque 1 : w=(1,1), b=1", "(0,0) encore raté"),
    ((1, 1), 0.0, "Fin époque 2 : w=(1,1), b=0", "1 erreur restante"),
    ((2, 2), -1.0, "Final (ép.5) : w=(2,2), b=-1", "0 erreur, convergé"),
]
for axi, (w, b, t, s) in zip(axes.flat, states_r):
    draw_state(axi, w, b, t, s)
axes[0, 0].set_ylabel("$x_2$"); axes[1, 0].set_ylabel("$x_2$")
fig.suptitle("Rosenblatt sur OU ($\\eta=1$) : la frontière bascule à chaque erreur")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "03-rosenblatt-pasapas.png"), dpi=150)
print("ok 03-rosenblatt-pasapas.png")

# Hebb : init -> fin E1 (2,2,2) -> fin E2 (4,4,4) : dérive, (0,0) toujours raté
fig, axes = plt.subplots(1, 3, figsize=(10, 3.6))
states_h = [
    ((0, 0), 0.0, "Init : w=(0,0), b=0", ""),
    ((2, 2), 2.0, "Fin époque 1 : w=(2,2), b=2", "(0,0) raté, mais on a renforcé quand même"),
    ((4, 4), 4.0, "Fin époque 2 : w=(4,4), b=4", "dérive : même frontière, norme x2"),
]
for axi, (w, b, t, s) in zip(axes, states_h):
    draw_state(axi, w, b, t, s)
axes[0].set_ylabel("$x_2$")
fig.suptitle("Hebb sur OU ($\\eta=1$) : renforce même quand c'est juste → dérive")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "03-hebb-pasapas.png"), dpi=150)
print("ok 03-hebb-pasapas.png")

err_r, norm_r = run("rosenblatt")
err_h, norm_h = run("hebb")

fig, axes = plt.subplots(1, 2, figsize=(9, 3.8))
ep = np.arange(1, EPOCHS + 1)
axes[0].plot(ep, err_r, "o-", label="Rosenblatt (si erreur)")
axes[0].plot(ep, err_h, "s--", label="Hebb (toujours)")
axes[0].set_xlabel("époque"); axes[0].set_ylabel("nb erreurs sur OU")
axes[0].set_title("Erreurs : Rosenblatt → 0, Hebb stagne")
axes[0].set_xticks(ep[::2]); axes[0].legend(fontsize=8)
axes[1].plot(ep, norm_r, "o-", label="Rosenblatt")
axes[1].plot(ep, norm_h, "s--", label="Hebb")
axes[1].set_xlabel("époque"); axes[1].set_ylabel("$||w||$")
axes[1].set_title("Norme : Hebb dérive, Rosenblatt se stabilise")
axes[1].set_xticks(ep[::2]); axes[1].legend(fontsize=8)
fig.suptitle("OU logique, $\\eta=1$, $w=0$ init : Hebb renforce même quand c'est juste")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "03-hebb-vs-rosenblatt.png"), dpi=150)
print("ok 03-hebb-vs-rosenblatt.png")

# 5. Intra-époque 1 Rosenblatt : variations de pente pas à pas
# Époque 1 OU, eta=1 : init (0,0,0) -> après (0,0) : (0,0,-1) ->
# après (0,1) : (0,1,0), pente 0 -> après (1,0) : (1,1,1), pente -1
fig, axes = plt.subplots(1, 4, figsize=(12, 3.4))
states_intra = [
    ((0, 0), 0.0, "Init\nw=(0,0), b=0", "pas de frontière"),
    ((0, 0), -1.0, "Après (0,0)→-1\nw=(0,0), b=-1", "translation seule\n(pas de pivot)"),
    ((0, 1), 0.0, "Après (0,1)→+1\nw=(0,1), b=0", "pente 0 : $x_2=0$"),
    ((1, 1), 1.0, "Après (1,0)→+1\nw=(1,1), b=1", "pente -1 : $x_2=-x_1-1$"),
]
for axi, (w, b, t, s) in zip(axes, states_intra):
    draw_state(axi, w, b, t, s)
axes[0].set_ylabel("$x_2$")
fig.suptitle("Intra-époque 1 (Rosenblatt, OU) : la pente change à chaque exemple")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "03-intra-epoque1.png"), dpi=150)
print("ok 03-intra-epoque1.png")
