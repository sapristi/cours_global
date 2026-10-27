"""Figures du chapitre 6 (Évaluer un modèle) -> assets/06-eval-*.png.

Usage : uv run python machine_learning/scripts/figures_evaluation.py
Générateurs, MLP et réglages copiés du TD 07 (mêmes graines : mêmes chiffres).
Notation : cible t, sortie y, lr = eta, élan mu.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle

ASSETS = Path(__file__).resolve().parent.parent / "assets"
C_TRAIN, C_VAL, C_TEST = "#0072b2", "#d55e00", "#009e73"
C_GRIS = "#888888"


# ---------------------------------------------------------------- TD 07
def make_blobs_imbalanced(n, noise=0.6, pos_frac=0.1, seed=1):
    rng = np.random.default_rng(seed)
    lab = (rng.uniform(size=n) < pos_frac).astype(float)
    centers = np.where(lab[:, None] == 1, [1.0, 1.0], [0.0, 0.0])
    X = centers + rng.normal(0.0, noise, size=(n, 2))
    return X, lab[:, None]


def make_moons(n, noise=0.3, seed=1):
    rng = np.random.default_rng(seed)
    a = rng.uniform(0.0, np.pi, size=n)
    lab = rng.integers(0, 2, size=n)
    x = np.where(lab == 0, np.cos(a), 1.0 - np.cos(a))
    y = np.where(lab == 0, np.sin(a), 0.5 - np.sin(a))
    X = np.c_[x, y] + rng.normal(0.0, noise, size=(n, 2))
    return X, lab[:, None].astype(float)


def split_train_val_test(X, t, n_train, n_val, seed=0):
    perm = np.random.default_rng(seed).permutation(len(X))
    X, t = X[perm], t[perm]
    a, b = n_train, n_train + n_val
    return X[:a], t[:a], X[a:b], t[a:b], X[b:], t[b:]


class MLP:
    """tanh cachée, sigmoïde en sortie, coût 0.5 * mean ; élan optionnel."""

    def __init__(self, sizes, seed=0, momentum=0.0):
        rng = np.random.default_rng(seed)
        self.Ws = [rng.normal(0.0, 0.5, size=(o, i)) for i, o in zip(sizes[:-1], sizes[1:])]
        self.bs = [np.zeros(o) for o in sizes[1:]]
        self.momentum = momentum
        self.vWs = [np.zeros_like(W) for W in self.Ws]
        self.vbs = [np.zeros_like(b) for b in self.bs]

    def forward(self, X):
        A, As, Zs = X, [X], []
        for l, (W, b) in enumerate(zip(self.Ws, self.bs)):
            Z = A @ W.T + b
            Zs.append(Z)
            A = 1.0 / (1.0 + np.exp(-Z)) if l == len(self.Ws) - 1 else np.tanh(Z)
            As.append(A)
        return As, Zs

    def backward(self, X, t):
        As, Zs = self.forward(X)
        N, Y = X.shape[0], As[-1]
        delta = (Y - t) * Y * (1.0 - Y)
        grads = []
        for l in reversed(range(len(self.Ws))):
            grads.append((delta.T @ As[l] / N, delta.mean(axis=0)))
            if l > 0:
                delta = (delta @ self.Ws[l]) * (1.0 - np.tanh(Zs[l - 1]) ** 2)
        grads.reverse()
        return grads

    def step(self, X, t, lr):
        for l, (dW, db) in enumerate(self.backward(X, t)):
            self.vWs[l] = self.momentum * self.vWs[l] + lr * dW
            self.vbs[l] = self.momentum * self.vbs[l] + lr * db
            self.Ws[l] = self.Ws[l] - self.vWs[l]
            self.bs[l] = self.bs[l] - self.vbs[l]

    def predict(self, X):
        return self.forward(X)[0][-1]

    def loss(self, X, t):
        return 0.5 * float(np.mean(np.sum((self.predict(X) - t) ** 2, axis=1)))

    def error_rate(self, X, t, threshold=0.5):
        return float(np.mean((self.predict(X) >= threshold) != (t > 0.5)))

    def fit(self, X, t, lr, epochs, X_val=None, t_val=None):
        h = {"train": [], "val": [], "err_train": [], "err_val": []}
        for _ in range(epochs):
            self.step(X, t, lr)
            h["train"].append(self.loss(X, t))
            h["err_train"].append(self.error_rate(X, t))
            if X_val is not None:
                h["val"].append(self.loss(X_val, t_val))
                h["err_val"].append(self.error_rate(X_val, t_val))
        return h


def confusion(t, y):
    t, y = t.ravel(), y.ravel()
    return (int(np.sum((t == 1) & (y == 1))), int(np.sum((t == 0) & (y == 1))),
            int(np.sum((t == 0) & (y == 0))), int(np.sum((t == 1) & (y == 0))))


def metriques(tp, fp, tn, fn):
    acc = (tp + tn) / (tp + fp + tn + fn)
    prec = tp / (tp + fp) if tp + fp else 0.0
    rap = tp / (tp + fn) if tp + fn else 0.0
    return acc, prec, rap


# ---------------------------------------------------------------- figures
def matrice(ax, tp, fp, tn, fn, titre):
    cells = [[tp, fn], [fp, tn]]
    noms = [["TP", "FN"], ["FP", "TN"]]
    bon = [[True, False], [False, True]]
    for i in range(2):
        for j in range(2):
            ax.add_patch(Rectangle((j, 1 - i), 1, 1, fc="#cfe8d8" if bon[i][j] else "#f6d5c3",
                                   ec="white", lw=3))
            ax.text(j + 0.5, 1.5 - i, f"{noms[i][j]}\n{cells[i][j]}", ha="center",
                    va="center", fontsize=14)
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 2)
    ax.set_xticks([0.5, 1.5], ["prédit +", "prédit −"])
    ax.set_yticks([1.5, 0.5], ["réel +", "réel −"])
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    acc, prec, rap = metriques(tp, fp, tn, fn)
    ax.set_title(f"{titre}\naccuracy = {acc:.3f}   précision = {prec:.3f}   rappel = {rap:.3f}",
                 fontsize=11)


def fig_confusion():
    X_tr, t_tr = make_blobs_imbalanced(100, seed=1)
    X_val, t_val = make_blobs_imbalanced(1000, seed=2)
    mlp = MLP([2, 16, 1], seed=0)
    mlp.fit(X_tr, t_tr, lr=1.0, epochs=2000)
    y_mlp = (mlp.predict(X_val).ravel() >= 0.5).astype(float)
    y_zero = np.zeros(len(t_val))
    c0, c1 = confusion(t_val, y_zero), confusion(t_val, y_mlp)
    print("confusion zero", c0, metriques(*c0))
    print("confusion mlp ", c1, metriques(*c1))
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))
    matrice(axes[0], *c0, "« toujours négatif »")
    matrice(axes[1], *c1, "MLP [2, 16, 1]")
    fig.suptitle("Gaussiennes déséquilibrées, jeu de test (1000 points, 80 positifs)", y=1.0)
    fig.tight_layout()
    fig.savefig(ASSETS / "06-eval-confusion.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def fig_train_val_test():
    fig, ax = plt.subplots(figsize=(10, 3.4))
    blocs = [(0.0, 0.5, C_TRAIN, "train", "entraîne\n(calcule les gradients)"),
             (0.5, 0.25, C_VAL, "validation", "règle\n($\\eta$, $\\mu$, époque d'arrêt)"),
             (0.75, 0.25, C_TEST, "test", "juge, une seule fois\n(verrouillé)")]
    for x, w, c, nom, role in blocs:
        ax.add_patch(FancyBboxPatch((x + 0.005, 0.45), w - 0.01, 0.35,
                                    boxstyle="round,pad=0,rounding_size=0.02",
                                    fc=c, ec="none", alpha=0.9))
        ax.text(x + w / 2, 0.625, nom, ha="center", va="center", color="white",
                fontsize=16, weight="bold")
        ax.text(x + w / 2, 0.30, role, ha="center", va="center", fontsize=11)
    ax.add_patch(FancyBboxPatch((0.755, 0.45), 0.24, 0.35, boxstyle="round,pad=0,rounding_size=0.02",
                                fc="none", ec="black", lw=2, ls="--"))
    ax.text(0.875, 0.86, "à ne pas toucher avant la fin", ha="center",
            fontsize=10, style="italic")
    ax.annotate("", xy=(1.0, 0.12), xytext=(0.0, 0.12),
                arrowprops=dict(arrowstyle="->", color=C_GRIS))
    ax.text(0.5, 0.04, "temps : on règle sur la validation, on juge sur le test", ha="center",
            fontsize=10, color=C_GRIS)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 0.95)
    ax.axis("off")
    fig.savefig(ASSETS / "06-eval-train-val-test.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def donnees_lunes():
    X, t = make_moons(1060, noise=0.3, seed=1)
    return split_train_val_test(X, t, n_train=60, n_val=500)


SIZES, LR, EPOCHS = [2, 32, 32, 1], 0.5, 4000


def entrainer(mu, data):
    X_tr, t_tr, X_va, t_va, _, _ = data
    return MLP(SIZES, seed=0, momentum=mu).fit(X_tr, t_tr, lr=LR, epochs=EPOCHS,
                                               X_val=X_va, t_val=t_va)


def fig_courbe(h):
    b = int(np.argmin(h["val"]))
    x = np.arange(1, EPOCHS + 1)
    print(f"mu=0 : min val {h['val'][b]:.4f} indice {b} (apres {b + 1} etapes), "
          f"train au min {h['train'][b]:.4f}, fin train {h['train'][-1]:.4f} val {h['val'][-1]:.4f}")
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.axvspan(1, 10, color="#f0c9c9", alpha=0.7, lw=0)
    ax.axvspan(10, b + 1, color="#cfe8d8", alpha=0.7, lw=0)
    ax.axvspan(b + 1, EPOCHS, color="#f6e3b8", alpha=0.7, lw=0)
    ax.plot(x, h["train"], color=C_TRAIN, ls="--", label="entraînement")
    ax.plot(x, h["val"], color=C_VAL, label="test")
    ax.plot(b + 1, h["val"][b], "o", color=C_VAL, mec="k", ms=9, zorder=5)
    ax.axvline(b + 1, color="k", lw=1, ls=":")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1, EPOCHS)
    ax.set_ylim(0.008, 0.3)
    ax.set_xlabel("époque (échelle log)")
    ax.set_ylabel("coût (échelle log)")
    ax.annotate(f"minimum du coût de test\nà l'époque {b + 1} : {h['val'][b]:.3f}",
                xy=(b + 1, h["val"][b]), xytext=(60, 0.012), fontsize=10,
                arrowprops=dict(arrowstyle="->"))
    top = 0.22
    ax.text(3.2, 0.0095, "sous-\napprentissage", ha="center", va="bottom", fontsize=10)
    ax.text(np.sqrt(10 * (b + 1)), top, "bon régime", ha="center", va="top", fontsize=11)
    ax.text(np.sqrt((b + 1) * EPOCHS), top, "surapprentissage\n(l'écart se creuse)",
            ha="center", va="top", fontsize=11)
    ax.legend(loc="lower left", bbox_to_anchor=(0.27, 0.02))
    ax.set_title("Courbe d'apprentissage, lunes, 60 points d'entraînement, $\\mu = 0$")
    fig.tight_layout()
    fig.savefig(ASSETS / "06-eval-courbe-apprentissage.png", dpi=150)
    plt.close(fig)


def fig_elan(h0, h9):
    fig, ax = plt.subplots(figsize=(9, 5))
    x = np.arange(1, EPOCHS + 1)
    for h, c, nom in ((h0, C_TRAIN, "$\\mu = 0$"), (h9, C_VAL, "$\\mu = 0.9$")):
        b = int(np.argmin(h["val"]))
        ax.plot(x, h["train"], color=c, ls="--", lw=1)
        ax.plot(x, h["val"], color=c, label=f"{nom}")
        ax.plot(b + 1, h["val"][b], "o", color=c, mec="k", ms=9, zorder=5)
        ax.vlines(b + 1, 0.0095, h["val"][b], color=c, lw=1, ls=":")
        ax.text(b + 1, 0.0092, f"{nom}\nmin après {b + 1} étapes\n= {h['val'][b]:.4f}",
                ha="left" if c == C_TRAIN else "right", va="top", fontsize=10, color=c)
        print(f"mu={nom}: min val {h['val'][b]:.4f} apres {b + 1} etapes ; fin val {h['val'][-1]:.4f}")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_ylim(0.0045, 0.3)
    ax.set_xlabel("époque (échelle log)")
    ax.set_ylabel("coût (échelle log)")
    ax.legend(loc="upper right", fontsize=9)
    ax.set_title("Lunes : même graine, même $\\eta$, mêmes données (trait plein : test, tirets : entraînement)", fontsize=10)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(ASSETS / "06-eval-elan-lunes.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    fig_confusion()
    fig_train_val_test()
    data = donnees_lunes()
    h0, h9 = entrainer(0.0, data), entrainer(0.9, data)
    fig_courbe(h0)
    fig_elan(h0, h9)
