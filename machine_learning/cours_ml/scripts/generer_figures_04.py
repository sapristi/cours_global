"""Génère les figures de la partie 04 - Données non linéairement séparables.
Usage: uv run --with matplotlib --with numpy python scripts/generer_figures_04.py
Sorties: assets/04-*.png
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

# 1. Deux cas non séparables : XOR + cercles concentriques
fig, axes = plt.subplots(1, 2, figsize=(9, 4))
# XOR
ax = axes[0]
xor_pts = np.array([[0, 0], [1, 1], [0, 1], [1, 0]])
xor_lab = np.array([-1, -1, 1, 1])
pos = xor_pts[xor_lab == 1]; neg = xor_pts[xor_lab == -1]
ax.scatter(pos[:, 0], pos[:, 1], s=140, marker="o", edgecolors="k",
           color="#e67e22", label="classe +1", zorder=3)
ax.scatter(neg[:, 0], neg[:, 1], s=140, marker="s", edgecolors="k",
           color="#3498db", label="classe −1", zorder=3)
for (x1, x2) in xor_pts:
    ax.text(x1 + 0.05, x2 + 0.05, f"({x1},{x2})", fontsize=8)
xs = np.linspace(-0.4, 1.4, 100)
ax.plot(xs, 0.5 * xs + 0.25, "k--", linewidth=1.5, label="droite en échec")
ax.plot(xs, -xs + 0.5, "k:", linewidth=1.5)
xx, yy = np.meshgrid(np.linspace(-0.4, 1.4, 200), np.linspace(-0.4, 1.4, 200))
ax.contourf(xx, yy, xx + yy - 1.0, levels=[-10, 0, 10],
            colors=["#cfe0ff", "#ffd9c9"], alpha=0.25)
ax.set_xlim(-0.4, 1.4); ax.set_ylim(-0.4, 1.4)
ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")
ax.set_title("XOR : aucune droite ne sépare")
ax.legend(fontsize=8)
ax.set_aspect("equal")

# Cercles concentriques
ax = axes[1]
rng = np.random.default_rng(0)
n_in, n_out = 40, 60
theta_in = rng.uniform(0, 2 * np.pi, n_in)
r_in = rng.uniform(0, 0.35, n_in)
theta_out = rng.uniform(0, 2 * np.pi, n_out)
r_out = rng.uniform(0.8, 1.15, n_out)
xin = np.c_[r_in * np.cos(theta_in), r_in * np.sin(theta_in)]
xout = np.c_[r_out * np.cos(theta_out), r_out * np.sin(theta_out)]
ax.scatter(xin[:, 0], xin[:, 1], s=30, marker="s", edgecolors="k",
           color="#3498db", label="classe −1 (centre)", zorder=3)
ax.scatter(xout[:, 0], xout[:, 1], s=30, marker="o", edgecolors="k",
           color="#e67e22", label="classe +1 (anneau)", zorder=3)
circle = plt.Circle((0, 0), 0.55, color="k", fill=False, linestyle="--",
                    linewidth=1.5, label="droite ? non : cercle")
ax.add_patch(circle)
ax.set_xlim(-1.4, 1.4); ax.set_ylim(-1.4, 1.4)
ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")
ax.set_title("Cercles concentriques : pas de droite non plus")
ax.legend(fontsize=8)
ax.set_aspect("equal")

fig.suptitle("Deux échecs du séparateur linéaire")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "04-non-separables-exemples.png"), dpi=150)
print("ok 04-non-separables-exemples.png")

# 2. XOR relevé en 3D via x3 = (x1 - x2)^2 : séparable par plan horizontal
fig = plt.figure(figsize=(8.5, 4))
ax1 = fig.add_subplot(1, 2, 1)
ax1.scatter(pos[:, 0], pos[:, 1], s=140, marker="o", edgecolors="k",
            color="#e67e22", label="+1", zorder=3)
ax1.scatter(neg[:, 0], neg[:, 1], s=140, marker="s", edgecolors="k",
            color="#3498db", label="−1", zorder=3)
ax1.set_xlim(-0.4, 1.4); ax1.set_ylim(-0.4, 1.4)
ax1.set_xlabel("$x_1$"); ax1.set_ylabel("$x_2$")
ax1.set_title("Avant : $\\Phi(x)=x$ (2D)")
ax1.legend(fontsize=8)
ax1.set_aspect("equal")

ax2 = fig.add_subplot(1, 2, 2, projection="3d")
phi = lambda p: (p[0], p[1], (p[0] - p[1]) ** 2)
for (x1, x2), y in zip(xor_pts, xor_lab):
    _, _, x3 = phi((x1, x2))
    ax2.scatter(x1, x2, x3, s=100,
                color="#e67e22" if y == 1 else "#3498db",
                edgecolors="k", depthshade=True)
    ax2.plot([x1, x1], [x2, x2], [0, x3], "k:", linewidth=1)
xx, yy = np.meshgrid(np.linspace(-0.2, 1.2, 10), np.linspace(-0.2, 1.2, 10))
zz = np.full_like(xx, 0.5)
ax2.plot_surface(xx, yy, zz, alpha=0.3, color="green")
ax2.set_xlabel("$x_1$"); ax2.set_ylabel("$x_2$"); ax2.set_zlabel("$x_3=(x_1-x_2)^2$")
ax2.set_title("Après : plan $x_3=0.5$ sépare")
ax2.set_zlim(0, 1.2)
fig.suptitle("XOR devient linéairement séparable en 3D")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "04-phi-XOR-3D.png"), dpi=150)
print("ok 04-phi-XOR-3D.png")

# 3. Cercles relevés via r = x1^2 + x2^2
fig = plt.figure(figsize=(8.5, 4))
ax1 = fig.add_subplot(1, 2, 1)
ax1.scatter(xin[:, 0], xin[:, 1], s=25, marker="s", edgecolors="k",
            color="#3498db", label="−1")
ax1.scatter(xout[:, 0], xout[:, 1], s=25, marker="o", edgecolors="k",
            color="#e67e22", label="+1")
ax1.set_xlabel("$x_1$"); ax1.set_ylabel("$x_2$")
ax1.set_title("Avant : anneau en 2D")
ax1.legend(fontsize=8)
ax1.set_aspect("equal")

ax2 = fig.add_subplot(1, 2, 2, projection="3d")
rin = np.sum(xin ** 2, axis=1)
rout = np.sum(xout ** 2, axis=1)
ax2.scatter(xin[:, 0], xin[:, 1], rin, s=20, color="#3498db", edgecolors="k")
ax2.scatter(xout[:, 0], xout[:, 1], rout, s=20, color="#e67e22", edgecolors="k")
xx, yy = np.meshgrid(np.linspace(-1.2, 1.2, 10), np.linspace(-1.2, 1.2, 10))
zz = np.full_like(xx, 0.35)
ax2.plot_surface(xx, yy, zz, alpha=0.3, color="green")
ax2.set_xlabel("$x_1$"); ax2.set_ylabel("$x_2$"); ax2.set_zlabel("$r=x_1^2+x_2^2$")
ax2.set_title("Après : plan $r=0.35$ sépare")
fig.suptitle("Cercles concentriques relevés : paraboloïde")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "04-phi-cercles-3D.png"), dpi=150)
print("ok 04-phi-cercles-3D.png")

# 4. Complexité : erreur train qui chute, erreur test en U
fig, ax = plt.subplots(figsize=(6, 4))
cplx = np.linspace(0, 10, 200)
err_train = 0.45 * np.exp(-0.55 * cplx) + 0.02
err_test = 0.45 * np.exp(-0.55 * cplx) + 0.015 * (cplx - 3.5) ** 2 + 0.02
ax.plot(cplx, err_train, "b-", linewidth=2, label="erreur train (empirique)")
ax.plot(cplx, err_test, "r-", linewidth=2, label="erreur test (généralisation)")
ax.axvline(3.5, color="k", linestyle="--", linewidth=1.5)
ax.text(3.55, 0.5, "bonne\ncomplexité", fontsize=9, va="top")
ax.text(0.5, 0.35, "sous-\napprentissage", fontsize=9, ha="center")
ax.text(8.0, 0.4, "sur-\napprentissage", fontsize=9, ha="center")
ax.set_xlabel("complexité du modèle (dim. de $\\Phi$, degré, nb. neurones...)")
ax.set_ylabel("erreur")
ax.set_title("Plus complexe ≠ meilleur : courbe en U sur le test")
ax.set_ylim(0, 0.6)
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "04-complexite-generalisation.png"), dpi=150)
print("ok 04-complexite-generalisation.png")
