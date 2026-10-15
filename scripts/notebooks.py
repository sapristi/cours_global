"""Maintient les notebooks d'un cours dans un état propre.

Commandes :

- ``extract`` : déplace les pièces jointes markdown (``attachments``) des
  notebooks vers ``<td>/assets/`` et remplace les références ``attachment:<uuid>``
  par ``assets/<nom>``.
- ``clear`` : supprime les sorties (``outputs``, ``execution_count``) des
  cellules de code.
- ``prune`` : supprime les fichiers de ``<td>/assets/`` non référencés par un
  notebook (orphelins).

Usage :
    python scripts/notebooks.py --td machine_learning/td extract [notebooks...]
    python scripts/notebooks.py --td machine_learning/td clear [notebooks...]
    python scripts/notebooks.py --td machine_learning/td prune
"""
from __future__ import annotations

import argparse
import base64
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TD = "machine_learning/td"


def source_text(cell: dict) -> str:
    src = cell.get("source", "")
    if isinstance(src, list):
        return "".join(src)
    return src


def resolve(td: str) -> tuple[Path, Path]:
    nb_dir = (ROOT / td).resolve()
    assets_dir = nb_dir / "assets"
    return nb_dir, assets_dir


def iter_notebooks(nb_dir: Path, paths: list[str]) -> list[Path]:
    if paths:
        seen: dict[Path, None] = {}
        out: list[Path] = []
        for p in paths:
            path = Path(p)
            if path.is_file() and path not in seen:
                seen[path] = None
                out.append(path)
        return out
    out = []
    for nb in sorted(nb_dir.glob("*.ipynb")):
        if ".ipynb_checkpoints" in nb.parts:
            continue
        out.append(nb)
    return out


def sanitize(name: str) -> str:
    name = Path(name).name
    name = re.sub(r"[^A-Za-z0-9._-]+", "-", name).strip("-")
    return name or "image"


def decode(data: str) -> bytes:
    if isinstance(data, list):
        data = "".join(data)
    return base64.b64decode("".join(data.split()))


def unique_asset_path(assets_dir: Path, filename: str, data: bytes) -> Path:
    """Renvoie un chemin libre dans assets_dir (contenu identique = réutilisé)."""
    target = assets_dir / filename
    if not target.exists() or target.read_bytes() == data:
        return target
    stem, suffix = target.stem, target.suffix
    n = 2
    while True:
        candidate = assets_dir / f"{stem}-{n}{suffix}"
        if not candidate.exists() or candidate.read_bytes() == data:
            return candidate
        n += 1


DISPLAY_RE = re.compile(r"!\[([^\]]*)\]\(attachment:([^)]+)\)")


def extract_cell_attachments(cell: dict, stem: str, assets_dir: Path) -> list[str]:
    """Extrait les pièces jointes d'une cellule markdown, réécrit la source."""
    attachments = cell.get("attachments")
    if not attachments or cell.get("cell_type") != "markdown":
        return []
    names = {key: name for name, key in DISPLAY_RE.findall(source_text(cell))}
    logs: list[str] = []
    mapping: dict[str, str] = {}
    removed: list[str] = []
    for key, mimes in list(attachments.items()):
        for mime, payload in mimes.items():
            if not mime.startswith("image/"):
                continue
            data = decode(payload)
            filename = sanitize(f"{stem}-{names.get(key, Path(key).name)}")
            dest = unique_asset_path(assets_dir, filename, data)
            assets_dir.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            mapping[key] = dest.name
            removed.append(key)
            logs.append(f"  {key} -> assets/{dest.name}")
            break  # une seule mime image par clé suffit
    if mapping:
        src = cell.get("source", "")
        is_list = isinstance(src, list)
        lines = list(src) if is_list else src.splitlines(keepends=True)
        for key, name in mapping.items():
            lines = [ln.replace(f"attachment:{key}", f"assets/{name}") for ln in lines]
        cell["source"] = lines if is_list else "".join(lines)
        for key in removed:
            attachments.pop(key, None)
        if not attachments:
            del cell["attachments"]
    return logs


def extract(nb_dir: Path, assets_dir: Path, notebooks: list[str]) -> int:
    paths = iter_notebooks(nb_dir, notebooks)
    changed = 0
    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        stem = path.stem
        logs: list[str] = []
        for cell in data.get("cells", []):
            logs.extend(extract_cell_attachments(cell, stem, assets_dir))
        if logs:
            path.write_text(
                json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8"
            )
            changed += 1
            print(f"extracted from {path}")
            for line in logs:
                print(line)
    if not changed:
        print("nothing to extract")
    return 0


def clear(nb_dir: Path, notebooks: list[str]) -> int:
    paths = iter_notebooks(nb_dir, notebooks)
    changed = 0
    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        touched = 0
        for cell in data.get("cells", []):
            if cell.get("cell_type") != "code":
                continue
            has_outputs = bool(cell.get("outputs"))
            has_count = "execution_count" in cell and cell.get("execution_count") is not None
            if has_outputs or has_count:
                cell["outputs"] = []
                if "execution_count" in cell:
                    cell["execution_count"] = None
                touched += 1
        if touched:
            path.write_text(
                json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8"
            )
            changed += 1
            print(f"cleared {touched} cell(s) from {path}")
    if not changed:
        print("nothing to clear")
    return 0


def referenced_names(nb_dir: Path, assets_dir: Path) -> set[str]:
    text = "".join(
        source_text(cell)
        for nb in nb_dir.glob("*.ipynb")
        if ".ipynb_checkpoints" not in nb.parts
        for cell in json.loads(nb.read_text(encoding="utf-8")).get("cells", [])
    )
    return {f.name for f in assets_dir.glob("*") if f.is_file() and f.name in text}


def prune(nb_dir: Path, assets_dir: Path) -> int:
    if not assets_dir.is_dir():
        print("nothing to prune")
        return 0
    kept = referenced_names(nb_dir, assets_dir)
    removed = 0
    for f in sorted(assets_dir.iterdir()):
        if f.is_file() and f.name not in kept:
            f.unlink()
            removed += 1
            print(f"deleted orphan {f.relative_to(ROOT)}")
    if not removed:
        print("nothing to prune")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Extrait les images embarquées des notebooks et nettoie les orphelines."
    )
    p.add_argument("--td", default=DEFAULT_TD, help=f"dossier des notebooks (défaut : {DEFAULT_TD})")
    sub = p.add_subparsers(dest="command", required=True)
    pe = sub.add_parser("extract", help="déplace les attachments vers <td>/assets/")
    pe.add_argument("notebooks", nargs="*", help="notebooks à traiter (tous par défaut)")
    pc = sub.add_parser("clear", help="supprime les sorties des cellules de code")
    pc.add_argument("notebooks", nargs="*", help="notebooks à traiter (tous par défaut)")
    sub.add_parser("prune", help="supprime les images orphelines de <td>/assets/")
    args = p.parse_args(argv)

    nb_dir, assets_dir = resolve(args.td)

    if args.command == "extract":
        return extract(nb_dir, assets_dir, args.notebooks)
    if args.command == "clear":
        return clear(nb_dir, args.notebooks)
    if args.command == "prune":
        return prune(nb_dir, assets_dir)
    p.print_usage(sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
