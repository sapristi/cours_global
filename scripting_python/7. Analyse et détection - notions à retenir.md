# Module 7 — Notions à retenir

Détecter des hôtes compromis dans des journaux de connexions sortantes avec `pandas`.

## Les trois signaux

| signal | principe | notion pandas | piège / contre-mesure |
| --- | --- | --- | --- |
| **1. Beaconing** | intervalle régulier vers un C2 | `groupby` + `diff` + CV | mises à jour légitimes (whitelist), jitter |
| **2. Fast-flux** | destination (IP/domaine) qui tourne | `groupby().nunique()` | destinations « populaires » (partagées) |
| **3. Plage d'IP** | timing aléatoire, plage d'IP rare | `map` + `agg` sur le préfixe | — |

## 1. Beaconing : le coefficient de variation

Un implant contacte son C2 à intervalle régulier. On mesure les **temps
inter-arrivées** puis leur **coefficient de variation** `CV = std / moyenne` :

```python
df = df.sort_values("timestamp")
df["dt"] = df.groupby(["src_ip", "domain"])["timestamp"].diff().dt.total_seconds()

stats = (df.dropna(subset=["dt"])
           .groupby(["src_ip", "domain"])["dt"]
           .agg(n="count", moyenne="mean", ecart_type="std"))
stats["cv"] = stats["ecart_type"] / stats["moyenne"]
```

- `cv ≈ 0` → intervalle quasi constant : **beacon**… ou tâche planifiée.
- `cv` élevé → trafic humain, irrégulier.

> [!warning] Piège : les mises à jour légitimes
> `windowsupdate.com`, `ntp.org`, antivirus sont *aussi* périodiques (`cv = 0`).
> On les écarte avec une **liste blanche** de domaines connus, et on croise avec
> la **stabilité du payload** (un beacon envoie toujours la même taille).

## 2. Fast-flux : compter les destinations

Le C2 change d'IP et de domaine à chaque connexion : grouper par domaine ne
donne plus rien. On regarde l'hôte **source** :

```python
df.groupby("src_ip")["dst_ip"].nunique()
```

- destination **populaire** : contactée par beaucoup d'hôtes (CDN, Microsoft…).
- destination **rare** : contactée par *une seule* source — signature C2.

## 3. Plage d'IP : quand il n'y a plus de rythme

Timing totalement aléatoire → aucun CV exploitable. Mais le C2 vit dans un `/24`
que personne d'autre ne touche. On réduit chaque IP à son préfixe, puis on
cherche les préfixes **rares** (1 source) **et** massivement contactés :

```python
def prefixe(ip: str) -> str:
    return ".".join(ip.split(".")[:3]) + ".0/24"
```

## Fonctions pandas à retenir

| fonction | usage |
| --- | --- |
| `pd.read_csv(..., parse_dates=[...])` | charger un CSV, convertir les dates |
| `df.sort_values("col")` | trier |
| `df.groupby([...])["col"].diff()` | écart entre valeurs successives d'un groupe |
| `.dt.total_seconds()` | passer d'un écart de temps à des secondes |
| `.groupby(...).agg(n="count", moyenne="mean", ecart_type="std")` | résumer par groupe |
| `.groupby(...).nunique()` | nombre de valeurs distinctes par groupe |
| `.map(f)` / `.str` | transformer une colonne |
| `.isin(...)` | filtrer par appartenance (liste blanche) |
| `.idxmin()` / `.idxmax()` | libellé de la ligne min/max |

## À retenir

- La détection de C2 est **heuristique** : on croise plusieurs signaux, aucun ne
  suffit seul.
- Chaque contre-mesure de l'attaquant casse un signal mais en laisse un autre :
  *jitter* (ex 1), *fast-flux* (ex 2), *timing aléatoire* (ex 3).
- Les **faux positifs** (mises à jour, tâches planifiées) se gèrent par liste
  blanche, plage de destinations connues, stabilité du payload.
- Références : RITA (`github.com/activecm/rita`), `river-io/sloth`
  (`docs/wiki/beacon-detection.md`), Yilmaz et al. *« Beaconing detection via
  timing-based flow metadata analysis »* (Springer, 2026).

> [!danger] Cadre légal
> Données simulées uniquement. Toute analyse sur un vrai réseau exige un **labo
> isolé** et une **autorisation écrite**. Art. 323-1 Code pénal.
