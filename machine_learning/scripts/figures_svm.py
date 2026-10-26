"""Figures du chapitre 5 (SVM) -> assets/05-svm-*.png.

Usage : uv run python machine_learning/scripts/figures_svm.py
Notation : cibles t in {-1,+1}, score z = w.x + b.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ASSETS = Path(__file__).resolve().parent.parent / "assets"
C_POS, C_NEG, C_SVM = "#d55e00", "#0072b2", "#009e73"


def donnees_separables(seed=3, n=10):
    """Deux nuages gaussiens, ecartes de force pour garantir une marge."""
    rng = np.random.default_rng(seed)
    X = np.vstack([rng.normal([-1.6, -1.0], 0.65, (n, 2)),
                   rng.normal([1.6, 1.0], 0.65, (n, 2))])
    t = np.r_[-np.ones(n), np.ones(n)]
    u = np.array([2.0, 1.0]) / np.sqrt(5)
    X = X + 0.5 * t[:, None] * u  # ecarte les classes le long de l'axe u
    return X, t


def svm_hinge(X, t, lam=1e-4, lr=0.05, epochs=40000):
    """Descente de gradient (sous-gradient) sur
    E = lam/2 ||w||^2 + 1/N sum max(0, 1 - t z). Renvoie (w, b)."""
    N = len(t)
    w, b = np.zeros(2), 0.0
    for k in range(epochs):
        z = X @ w + b
        viol = t * z < 1
        gw = lam * w - (t[viol, None] * X[viol]).sum(0) / N
        gb = -t[viol].sum() / N
        eta = lr / np.sqrt(1 + k / 100)
        w, b = w - eta * gw, b - eta * gb
    return w, b


def droite(w, b, xs, c=0.0):
    """Points de la droite w.x + b = c, parametree par x1."""
    return xs, (c - b - w[0] * xs) / w[1]


def nuage(ax, X, t):
    ax.scatter(*X[t > 0].T, c=C_POS, marker="+", s=70, label="classe $t=+1$")
    ax.scatter(*X[t < 0].T, c=C_NEG, marker="o", s=35, label="classe $t=-1$")


def style(ax, lim=(-3.6, 3.6)):
    ax.set_xlim(lim)
    ax.set_ylim(lim)
    ax.set_aspect("equal")
    ax.set_xlabel("$x_1$")
    ax.set_ylabel("$x_2$")


def fig_separateurs(X, t, w, b):
    fig, ax = plt.subplots(figsize=(6, 5.5))
    nuage(ax, X, t)
    xs = np.linspace(-3.6, 3.6, 2)
    # droite proche de la max-marge, tournee/decalee ; on garde celles qui separent
    sep = []
    for ang in (0.35, -0.35):
        c, s = np.cos(ang), np.sin(ang)
        R = np.array([[c, -s], [s, c]])
        w2 = R @ w
        # decale pour passer au milieu des projections extremes
        p = X @ w2
        b2 = -(p[t > 0].min() + p[t < 0].max()) / 2
        sep.append((w2, b2, "#888888", "--"))
    # droite qui frole un point : parallele a w, collee au point + le plus proche
    p = X @ w
    b3 = -(p[t > 0].min() - 0.03 * np.linalg.norm(w))
    sep.append((w, b3, "#888888", ":"))
    for w2, b2, col, ls in sep:
        ok = np.all(t * (X @ w2 + b2) > 0)
        assert ok, "un separateur ne separe pas"
        ax.plot(*droite(w2, b2, xs), color=col, ls=ls, lw=1.8)
    ax.plot(*droite(w, b, xs), color=C_SVM, lw=2.8, label="marge maximale")
    ax.plot([], [], color="#888888", ls="--", label="autres séparateurs")
    ax.plot([], [], color="#888888", ls=":", label="séparateur « limite »")
    style(ax)
    ax.set_title("Plusieurs droites séparent parfaitement les données")
    ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    fig.savefig(ASSETS / "05-svm-separateurs.png", dpi=150)
    plt.close(fig)


def fig_marge(X, t, w, b):
    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    nuage(ax, X, t)
    xs = np.linspace(-3.6, 3.6, 2)
    ax.plot(*droite(w, b, xs), color=C_SVM, lw=2.5, label="$z=0$")
    for c in (-1, 1):
        ax.plot(*droite(w, b, xs, c), color=C_SVM, ls="--", lw=1.4)
    z = X @ w + b
    sv = np.abs(np.abs(z) - 1) < 0.05
    ax.scatter(*X[sv].T, s=260, facecolors="none", edgecolors="k", lw=1.5,
               label="vecteurs de support")
    n = np.linalg.norm(w)
    u = w / n
    x0 = -b * w / n**2  # point de z=0 le plus proche de l'origine
    # largeur 2/||w|| : fleche entre z=-1 et z=+1, decalee le long de la droite
    d = np.array([-u[1], u[0]])
    base = x0 + 0.5 * d
    p1, p2 = base - u / n, base + u / n
    ax.annotate("", xy=p2, xytext=p1,
                arrowprops=dict(arrowstyle="<->", color="k", lw=1.3))
    ax.text(*(base + 0.25 * d), "$2/\\|w\\|$", fontsize=12,
            va="center", bbox=dict(fc="white", ec="none", pad=1))
    # vecteur w (normal), longueur d'affichage fixe
    o = x0 - 1.5 * d
    ax.annotate("", xy=o + 0.9 * u, xytext=o,
                arrowprops=dict(arrowstyle="->", color="k", lw=2))
    ax.text(*(o + 0.9 * u + 0.1 * u + 0.25 * d), "$w$", fontsize=13)
    ax.text(*(x0 + 2.9 * d + 1.3 * u + 0.15 * u), "$z=+1$", color=C_SVM, ha="left")
    ax.text(*(x0 + 2.9 * d - 1.3 * u - 0.15 * u), "$z=-1$", color=C_SVM, ha="right")
    style(ax)
    ax.set_title("Marge maximale : largeur $2/\\|w\\|$")
    ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    fig.savefig(ASSETS / "05-svm-marge.png", dpi=150)
    plt.close(fig)


def fig_marge_souple():
    X, t = donnees_separables(seed=5, n=12)
    # 3 points fautifs : (A) classe - dans la marge mais bien classe,
    # (B) classe + du mauvais cote, (C) classe - du mauvais cote
    X = X.copy()
    X[3] = [-0.5, -0.4]       # A : classe -, entre z=-1 et z=0
    X[15] = [-0.9, -1.2]      # B : classe +, franchement cote z<0
    X[8] = [0.4, 0.9]         # C : classe -, franchement cote z>0
    w, b = svm_hinge(X, t, lam=0.02, lr=0.1, epochs=20000)
    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    nuage(ax, X, t)
    xs = np.linspace(-3.6, 3.6, 2)
    ax.plot(*droite(w, b, xs), color=C_SVM, lw=2.5, label="$z=0$")
    for c in (-1, 1):
        ax.plot(*droite(w, b, xs, c), color=C_SVM, ls="--", lw=1.4)
    z = X @ w + b
    xi = np.maximum(0, 1 - t * z)
    n2 = w @ w
    d = np.array([-w[1], w[0]]) / np.sqrt(n2)
    viol = np.where(xi > 0.2)[0]
    for k, i in enumerate(viol):
        col = C_POS if t[i] > 0 else C_NEG
        # projection sur la droite t z = 1 : distance xi/||w||
        proj = X[i] + (xi[i] * t[i] / n2) * w
        ax.scatter(*X[i], s=260, facecolors="none", edgecolors=col, lw=1.5)
        ax.annotate("", xy=proj, xytext=X[i],
                    arrowprops=dict(arrowstyle="->", color=col, lw=1.6))
        mid = (X[i] + proj) / 2
        ax.text(*(mid + 0.3 * d), f"$\\xi_{{{k + 1}}}$", fontsize=13,
                color=col, ha="center", va="center",
                bbox=dict(fc="white", ec="none", pad=0.5, alpha=0.8))
    style(ax)
    ax.set_title("Marge souple : variables d'écart $\\xi_i = \\max(0, 1-t_iz_i)$")
    ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    fig.savefig(ASSETS / "05-svm-marge-souple.png", dpi=150)
    plt.close(fig)
    return xi


def fig_pertes():
    tz = np.linspace(-3, 3, 601)
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    ax.plot(tz, (tz < 0).astype(float), color="#999999", lw=1.5,
            label="perte 0-1 (erreur)")
    ax.plot(tz, np.maximum(0, -tz), color=C_POS, lw=2.2,
            label="perceptron : $\\max(0,-tz)$")
    ax.plot(tz, np.maximum(0, 1 - tz), color=C_SVM, lw=2.2,
            label="hinge (SVM) : $\\max(0,1-tz)$")
    ax.axvline(1, color="k", ls=":", lw=1)
    ax.text(1.05, 3.0, "$tz=1$ : marge", fontsize=9)
    ax.set_xlim(-3, 3)
    ax.set_ylim(-0.1, 4)
    ax.set_xlabel("$t\\cdot z$  (positif = bien classé)")
    ax.set_ylabel("perte")
    ax.set_title("Perte du perceptron vs perte hinge")
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    fig.savefig(ASSETS / "05-svm-pertes.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    X, t = donnees_separables()
    w, b = svm_hinge(X, t)
    print("min t z =", (t * (X @ w + b)).min(), " marge 2/||w|| =", 2 / np.linalg.norm(w))
    fig_separateurs(X, t, w, b)
    fig_marge(X, t, w, b)
    print("xi =", np.round(fig_marge_souple(), 2))
    fig_pertes()
