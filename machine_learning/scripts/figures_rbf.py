"""Figures du chapitre 7 (k-NN et reseaux RBF) -> assets/07-rbf-*.png.

Usage : uv run python machine_learning/scripts/figures_rbf.py
Notation : cibles t in {0, 1}, phi(x) = exp(-||x - c||^2 / 2 sigma^2).
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ASSETS = Path(__file__).resolve().parent.parent / "assets"
C0, C1 = "tab:red", "tab:blue"


def lunes(n=150, noise=0.25, seed=1):
    """Deux demi-lunes entrelacees (meme generateur que les TD)."""
    rng = np.random.default_rng(seed)
    a = rng.uniform(0.0, np.pi, size=n)
    lab = rng.integers(0, 2, size=n)
    x = np.where(lab == 0, np.cos(a), 1.0 - np.cos(a))
    y = np.where(lab == 0, np.sin(a), 0.5 - np.sin(a))
    return np.c_[x, y] + rng.normal(0.0, noise, size=(n, 2)), lab.astype(float)


def phi(X, c, sigma):
    return np.exp(-((X - c) ** 2).sum(-1) / (2 * sigma ** 2))


def knn(X, t, Xq, k):
    d = ((Xq[:, None, :] - X[None, :, :]) ** 2).sum(2)
    idx = np.argsort(d, axis=1)[:, :k]
    return (t[idx].mean(1) >= 0.5).astype(float)


def points(ax, X, t):
    for k, color in ((0, C0), (1, C1)):
        m = t == k
        ax.scatter(X[m, 0], X[m, 1], color=color, edgecolors="w", linewidths=0.5,
                   s=22, zorder=3, label=f"classe {k}")


def fig_knn():
    X, t = lunes()
    xx, yy = np.meshgrid(np.linspace(-1.6, 2.6, 250), np.linspace(-1.3, 1.8, 250))
    G = np.c_[xx.ravel(), yy.ravel()]
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for ax, k in zip(axes, (1, 15)):
        Z = knn(X, t, G, k).reshape(xx.shape)
        ax.contourf(xx, yy, Z, levels=[-0.5, 0.5, 1.5], colors=[C0, C1], alpha=0.25)
        ax.contour(xx, yy, Z, levels=[0.5], colors="k", linewidths=1.5)
        points(ax, X, t)
        ax.set_title(f"k = {k}")
        ax.set_aspect("equal")
        ax.set_xlabel("x1")
        ax.set_ylabel("x2")
    axes[0].legend(loc="upper right")
    fig.suptitle("k plus proches voisins : frontière de décision")
    fig.tight_layout()
    fig.savefig(ASSETS / "07-rbf-knn.png", dpi=130)
    plt.close(fig)


def fig_bosses_1d():
    x = np.linspace(-5, 5, 400)
    fig, ax = plt.subplots(figsize=(7, 3.8))
    for s in (0.3, 1.0, 2.0):
        ax.plot(x, np.exp(-x ** 2 / (2 * s ** 2)), lw=2, label=f"σ = {s}")
    ax.axvline(0, color="gray", ls=":", lw=1)
    ax.text(0.1, 1.03, "centre c = 0", color="gray")
    ax.set_xlabel("x")
    ax.set_ylabel("φ(x)")
    ax.set_ylim(0, 1.12)
    ax.set_title("φ(x) = exp(−(x − c)² / 2σ²)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(ASSETS / "07-rbf-bosses-1d.png", dpi=130)
    plt.close(fig)


def fig_bosse_2d():
    xx, yy = np.meshgrid(np.linspace(-2, 2, 200), np.linspace(-2, 2, 200))
    c = np.array([0.3, -0.2])
    Z = phi(np.stack([xx, yy], -1), c, 0.6)
    fig, ax = plt.subplots(figsize=(5, 4.3))
    im = ax.contourf(xx, yy, Z, levels=20, cmap="viridis")
    fig.colorbar(im, ax=ax, label="φ(x)")
    ax.plot(*c, "w+", ms=14, mew=2)
    ax.annotate("centre c", c, xytext=(c[0] + 0.4, c[1] + 0.9), color="w",
                arrowprops=dict(arrowstyle="->", color="w"))
    ax.set_aspect("equal")
    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
    ax.set_title("Neurone RBF en 2D (σ = 0.6)")
    fig.tight_layout()
    fig.savefig(ASSETS / "07-rbf-bosse-2d.png", dpi=130)
    plt.close(fig)


def fig_sigmoide_vs_rbf():
    xx, yy = np.meshgrid(np.linspace(-3, 3, 200), np.linspace(-3, 3, 200))
    G = np.stack([xx, yy], -1)
    w, b = np.array([1.5, 1.0]), -0.5
    S = 1 / (1 + np.exp(-(G @ w + b)))
    R = phi(G, np.array([0.5, 0.5]), 0.8)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.3))
    for ax, Z, title in ((axes[0], S, "Neurone sigmoïde : sigmoid(w·x + b)\nréponse globale (demi-plan)"),
                         (axes[1], R, "Neurone RBF : φ(‖x − c‖)\nréponse locale (bosse)")):
        im = ax.contourf(xx, yy, Z, levels=np.linspace(0, 1, 21), cmap="viridis")
        ax.contour(xx, yy, Z, levels=[0.5], colors="w", linewidths=1.5)
        ax.set_aspect("equal")
        ax.set_xlabel("x1")
        ax.set_ylabel("x2")
        ax.set_title(title)
    axes[1].plot(0.5, 0.5, "w+", ms=14, mew=2)
    fig.colorbar(im, ax=axes, label="activation", shrink=0.9)
    fig.savefig(ASSETS / "07-rbf-sigmoide-vs-rbf.png", dpi=130, bbox_inches="tight")
    plt.close(fig)


def fig_architecture():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    entrees = [(1, 4), (1, 2)]
    caches = [(5, 5.0), (5, 3.5), (5, 1.0)]
    sortie = (8.7, 3)

    def noeud(p, txt, color):
        ax.add_patch(plt.Circle(p, 0.42, color=color, zorder=3))
        ax.text(*p, txt, ha="center", va="center", fontsize=12, zorder=4, color="k")

    for e in entrees:
        for c in caches:
            ax.plot([e[0], c[0]], [e[1], c[1]], color="gray", lw=0.8, zorder=1)
    for c in caches:
        ax.plot([c[0], sortie[0]], [c[1], sortie[1]], color="k", lw=1.2, zorder=1)
    for e, txt in zip(entrees, ("x1", "x2")):
        noeud(e, txt, "#cfe2f3")
    for c, txt in zip(caches, ("φ1", "φ2", "φK")):
        noeud(c, txt, "#fde9b8")
    ax.text(5, 2.25, "⋮", ha="center", va="center", fontsize=18)
    noeud(sortie, "y", "#d9ead3")
    ax.text(7.0, 4.6, "w1", fontsize=11)
    ax.text(7.0, 1.2, "wK", fontsize=11)
    ax.text(1, 0.3, "entrée", ha="center", fontsize=11)
    ax.text(5, -0.15, "K neurones RBF\n(centres c_k, largeur σ)", ha="center", fontsize=11)
    ax.text(sortie[0], 1.6, "sortie\ny = sigmoid(Σ w_k φ_k + b)", ha="center", fontsize=11)
    ax.text(3.0, 5.6, "distances ‖x − c_k‖\n(pas de poids appris)", ha="center", fontsize=10, color="gray")
    fig.tight_layout()
    fig.savefig(ASSETS / "07-rbf-architecture.png", dpi=130)
    plt.close(fig)


def fig_somme_bosses():
    x = np.linspace(-1, 7, 400)
    cible = np.sin(x) + 0.3 * x
    centres = np.linspace(-0.5, 6.5, 8)
    sigma = 0.6
    P = np.exp(-(x[:, None] - centres[None]) ** 2 / (2 * sigma ** 2))
    w = np.linalg.lstsq(P, cible, rcond=None)[0]
    fig, ax = plt.subplots(figsize=(8, 4))
    for k in range(len(centres)):
        ax.plot(x, w[k] * P[:, k], ls="--", lw=1, color="gray", label="w_k φ_k(x)" if k == 0 else None)
    ax.plot(x, cible, color="tab:orange", lw=4, alpha=0.5, label="fonction à approcher")
    ax.plot(x, P @ w, color="k", lw=1.8, label="Σ_k w_k φ_k(x)")
    ax.plot(centres, np.zeros_like(centres), "k^", ms=7, label="centres c_k")
    ax.set_xlabel("x")
    ax.set_title("Une somme pondérée de bosses approche une fonction")
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(ASSETS / "07-rbf-somme-bosses.png", dpi=130)
    plt.close(fig)


def main():
    ASSETS.mkdir(exist_ok=True)
    fig_knn()
    fig_bosses_1d()
    fig_bosse_2d()
    fig_sigmoide_vs_rbf()
    fig_architecture()
    fig_somme_bosses()


if __name__ == "__main__":
    main()
