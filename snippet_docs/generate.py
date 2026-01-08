import os
import commentjson as json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from dataclasses import dataclass
from typing import List
from pathlib import Path

import shutil

def copy_static_files(output_dir):
    static_dir = Path("static")
    if not static_dir.exists():
        return

    for file in static_dir.iterdir():
        if file.is_file():
            shutil.copy(file, output_dir / file.name)

@dataclass
class Snippet:
    name: str
    scope: str
    prefix: str
    description: str
    body: List[str]

def get_all_files(root_dir="example"):
    all_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for file in filenames:
            if(file.endswith(".code-snippets")):
                file_path = os.path.join(dirpath, file)
                all_files.append(file_path)
    if len(all_files) == 0:
        print("No existen snippets")
    return all_files

def slugify(text: str) -> str:
    return (
        text.lower()
        .replace(" ", "-")
        .replace("/", "-")
        .replace("\\", "-")
    )


def generate_docs(snippets_dir="example", output_dir="dist"):
    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=select_autoescape(["html"])
    )

    index_template = env.get_template("index.html")
    snippet_template = env.get_template("snippet.html")

    output_dir = Path(output_dir)
    snippets_html_dir = output_dir / "snippets"
    snippets_html_dir.mkdir(parents=True, exist_ok=True)

    # Árbol completo: carpeta → archivo → snippets
    tree = {}

    base_path = Path(snippets_dir).resolve()

    for snippet_file in get_all_files(snippets_dir):
        snippet_file = Path(snippet_file).resolve()

        # Ruta relativa (carpetas internas)
        relative_parts = snippet_file.relative_to(base_path).parts
        folders = relative_parts[:-1]           # carpetas
        file_name = relative_parts[-1]           # archivo .code-snippets

        current_level = tree

        # Crear carpetas en el árbol
        for folder in folders:
            current_level = current_level.setdefault(folder, {})

        # Crear nodo del archivo
        if file_name not in current_level:
            current_level[file_name] = []

        # Leer snippets
        with open(snippet_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        for name, snippet in data.items():
            snippet_obj = Snippet(
                name=name,
                scope=snippet.get("scope", ""),
                prefix=snippet.get("prefix", ""),
                description=snippet.get("description", ""),
                body="\n".join(snippet.get("body", []))
            )

            html_name = slugify(name) + ".html"
            html_path = snippets_html_dir / html_name

            # HTML del snippet
            rendered = snippet_template.render(snippet=snippet_obj)
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(rendered)

            current_level[file_name].append({
                "name": snippet_obj.name,
                "file": f"snippets/{html_name}"
            })

    # Render del índice
    rendered_index = index_template.render(tree=tree)
    with open(output_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(rendered_index)
    copy_static_files(output_dir)
    print(f"📄 Documentación generada en: {output_dir.resolve()}")

generate_docs()
