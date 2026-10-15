"""Fonctions partagées de préparation des notebooks (strip solutions, sorties, images, bouton clear).

Module commun utilisé par ``collect_lite_content.py`` (pipeline CI) et
``prepare_notebooks.py`` (aperçu local) pour ne pas dupliquer la logique
d'export. La logique provient des deux cours fusionnés :

- machine_learning : ``prepare_notebooks.py`` (marqueurs ``# BEGIN``/``# END``,
  corps du TODO dérivé des commentaires, inline des images ``assets/`` en
  base64, bouton « Clear notebook » simple).
- scripting_python : ``collect_lite_content.py`` (marqueurs ``#BEGIN``/``#END``,
  bouton « Clear notebook » robuste via ``indexedDB.databases()``).

Les deux conventions de marqueurs sont supportées (espace optionnel).
"""
from __future__ import annotations

import base64
import html
import json
import re
import sys
from pathlib import Path

# Les deux cours utilisent des formes différentes : ``# BEGIN``/``# END``
# (machine_learning) et ``#BEGIN``/``#END`` (scripting_python). La regex
# tolère l'espace optionnel après le ``#``.
BEGIN_RE = re.compile(r"#\s*BEGIN\b")
END_RE = re.compile(r"#\s*END\b")

TODO = "# TODO"

MIME_BY_SUFFIX = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".svg": "image/svg+xml",
    ".webp": "image/webp",
}

INLINE_RE = re.compile(r"!\[([^\]]*)\]\(assets/([^)]+)\)")

MARQUEUR_CLEAR = "indexedDB"

DELETE_MARQUEUR = "DELETE"


def is_delete_cell(cell: dict) -> bool:
    """Vrai si la cellule code doit être supprimée (1ère ligne = commentaire avec DELETE).

    Seules les cellules ``code`` sont concernées. La 1ère ligne non vide,
    une fois les espaces de tête retirés, doit commencer par ``#`` et
    contenir ``DELETE`` n'importe où.
    """
    if cell.get("cell_type") != "code":
        return False
    for line in as_lines(cell):
        if not line.strip():
            continue
        stripped = line.lstrip()
        return stripped.startswith("#") and DELETE_MARQUEUR in stripped
    return False


def drop_delete_cells(nb: dict) -> int:
    """Supprime les cellules code marquées DELETE (en place). Renvoie leur nombre."""
    cells = nb.get("cells", [])
    kept = [c for c in cells if not is_delete_cell(c)]
    removed = len(cells) - len(kept)
    if removed:
        nb["cells"] = kept
    return removed


def source_text(cell: dict) -> str:
    src = cell.get("source", "")
    if isinstance(src, list):
        return "".join(src)
    return src


def as_lines(cell: dict) -> list[str]:
    src = cell.get("source", "")
    if isinstance(src, list):
        return list(src)
    return src.splitlines(keepends=True)


def uncomment_line(line: str) -> tuple[str, bool]:
    """Transforme une ligne de commentaire du corps du TODO.

    ``# code`` -> ``code`` (dé-commenté, devient du code) ; ``## indice`` ->
    ``# indice`` (conserve un ``#``). Renvoie ``(ligne, est_du_code)``.
    """
    indent = line[: len(line) - len(line.lstrip())]
    content = line[len(indent) :]
    if content.startswith("##"):
        return indent + content[1:], False
    body = content[1:]
    if body.startswith(" "):
        body = body[1:]
    return indent + body, True


def truncate_blocks(lines: list[str]) -> list[str]:
    """Remplace chaque bloc ``# BEGIN`` … ``# END`` par ``# TODO`` (+ corps/hint).

    Les commentaires écrits juste après le marqueur deviennent le corps du TODO
    (voir ``uncomment_line``). Sans commentaire, un ``pass`` est ajouté.
    """
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not BEGIN_RE.search(line):
            out.append(line)
            i += 1
            continue
        indent = line[: len(line) - len(line.lstrip())]
        newline = "\n" if line.endswith("\n") else ""
        out.append(indent + TODO + newline)
        i += 1
        has_code = False
        while i < len(lines):
            nxt = lines[i]
            if not nxt.lstrip().startswith("#") or END_RE.search(nxt):
                break
            emitted, is_code = uncomment_line(nxt)
            out.append(emitted)
            has_code = has_code or is_code
            i += 1
        if not has_code:
            out.append(indent + "pass" + newline)
        while i < len(lines) and not END_RE.search(lines[i]):
            i += 1
        if i < len(lines):
            i += 1
    return out


def clear_cell(cell: dict) -> None:
    cell["outputs"] = []
    if "execution_count" in cell:
        cell["execution_count"] = None


def strip_solutions(nb: dict) -> int:
    """Retire les solutions (blocs BEGIN/END) et vide les sorties des cellules code.

    Supprime aussi les cellules code dont la 1ère ligne est un commentaire
    contenant ``DELETE`` (voir ``drop_delete_cells``).

    Opère en place sur le dict notebook. Renvoie le nombre de blocs retirés.
    """
    drop_delete_cells(nb)
    count = 0
    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        lines = as_lines(cell)
        stripped = truncate_blocks(lines)
        if stripped != lines:
            count += 1
        cell["source"] = stripped
        clear_cell(cell)
    return count


def inline_images(nb: dict, assets_dir: Path) -> int:
    """Remplace ``![..](assets/<nom>)`` par un data URI base64 inline.

    Renvoie le nombre d'images inlinées. Une image sans mime connu ou
    introuvable est signalée sur stderr et laissée telle quelle.
    """
    count = 0

    def replace(m: re.Match) -> str:
        nonlocal count
        alt, name = m.group(1), m.group(2)
        mime = MIME_BY_SUFFIX.get(Path(name).suffix.lower())
        if mime is None:
            print(f"  image sans mime connu, ignorée: {name}", file=sys.stderr)
            return m.group(0)
        image = assets_dir / name
        if not image.is_file():
            print(f"  image introuvable: {image}", file=sys.stderr)
            return m.group(0)
        data = base64.b64encode(image.read_bytes()).decode("ascii")
        count += 1
        return f"![{alt}](data:{mime};base64,{data})"

    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "markdown":
            continue
        src = cell.get("source", "")
        is_list = isinstance(src, list)
        text = "".join(src) if is_list else src
        new_text = INLINE_RE.sub(replace, text)
        if new_text != text:
            cell["source"] = new_text.splitlines(keepends=True) if is_list else new_text
    return count


def cle_js(cle: str) -> str:
    return cle.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"')


def make_clear_cell(cle: str) -> dict:
    """Première cellule : bouton qui purge l'état du notebook dans IndexedDB.

    Version robuste (scripting_python) : énumère les bases ``indexedDB`` dont le
    nom contient « JupyterLite Storage » et efface la clé ``cle`` des tables
    « checkpoints » et « files ».
    """
    libelle = html.escape(f"Clear notebook {cle}")
    jk = cle_js(cle)
    source = (
        "from IPython.display import display, HTML\n"
        f'display(HTML("""<button type="button" id="button_for_indexeddb">{libelle}</button>'
        "    <script>"
        "    window.button_for_indexeddb.onclick = function(e) {"
        "        function clearFrom(dbName) {"
        "            let req;"
        "            try { req = window.indexedDB.open(dbName); }"
        '            catch (err) { console.warn("Skipping " + dbName + ": " + err); return; }'
        "            req.onerror = function(ev) {"
        '                console.warn("Cannot open " + dbName + ": " + (ev.target.error || ev));'
        "            };"
        "            req.onsuccess = function(e) {"
        "                let db = e.target.result;"
        '                for (let tablename of ["checkpoints", "files"]) {'
        "                    try {"
        "                        if (!db.objectStoreNames.contains(tablename)) continue;"
        '                        let t = db.transaction(tablename, "readwrite");'
        "                        t.onerror = function(ev) {};"
        f"                    let del; try {{ del = t.objectStore(tablename).delete('{jk}'); }} catch (err) {{ continue; }}"
        "                        del.onerror = function(ev) {};"
        "                        del.onsuccess = function(ev) {"
        f'                            console.log("Deleted {jk} state in " + dbName + "/" + tablename + " (" + ev.target.result + ")");'
        "                        };"
        "                    }"
        '                    catch (err) { console.warn("Skipping " + dbName + "/" + tablename + ": " + err); }'
        "                }"
        "            };"
        "        };"
        "        if (window.indexedDB.databases) {"
        "            window.indexedDB.databases().then(dbs => {"
        "                let names = dbs.map(d => d.name).filter(n => n && n.includes('JupyterLite Storage'));"
        "                if (!names.length) names = ['JupyterLite Storage'];"
        "                names.forEach(clearFrom);"
        "            });"
        "        } else {"
        "            clearFrom('JupyterLite Storage');"
        "        }"
        "    };"
        '    </script>"""))'
    )
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": "clear-local-storage",
        "metadata": {},
        "outputs": [],
        "source": [source],
    }


def is_clear_cell(cell: dict) -> bool:
    if cell.get("cell_type") != "code":
        return False
    return MARQUEUR_CLEAR in source_text(cell)


def has_clear_cell(nb: dict) -> bool:
    cells = nb.get("cells", [])
    return bool(cells) and is_clear_cell(cells[0])


def inject_clear_button(nb: dict, rel: str) -> None:
    """Retire une éventuelle cellule clear existante puis insère la nouvelle en tête."""
    nb["cells"] = [c for c in nb.get("cells", []) if not is_clear_cell(c)]
    nb["cells"].insert(0, make_clear_cell(rel))


def load_notebook(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_notebook(nb: dict, path: Path) -> None:
    path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
