import argparse
import shutil
import commentjson as json

from importlib.resources import files
from jinja2 import Environment, PackageLoader, FileSystemLoader, select_autoescape
from dataclasses import dataclass
from typing import List
from pathlib import Path
from .logger import log

@dataclass
class Snippet:
    name: str
    scope: List[str]
    is_file_template: bool
    prefix: str
    description: str
    body: str

    def __init__(self, name, snippet_aux):
        self.name=name
        
        self.scope = [x.strip() for x in snippet_aux.get("scope", "").split(",") if x]

        is_file_template_aux = snippet_aux.get("isFileTemplate", False)
        self.is_file_template = is_file_template_aux if isinstance(is_file_template_aux, bool) else is_file_template_aux.strip().lower() == "true"

        prefix_aux = snippet_aux.get("prefix", "")
        prefix_aux = prefix_aux if isinstance(prefix_aux, list) else prefix_aux.split(",")
        self.prefix = [x.strip() for x in prefix_aux if x]
        
        self.description=snippet_aux.get("description", "")
        
        body_aux = snippet_aux.get("body", [])
        self.body= body_aux if isinstance(body_aux, str) else "\n".join(body_aux)

def copy_static_files(output_dir):
    static_dir = files("snippet_docs").joinpath("static")
    if not static_dir.exists():
        return

    for file in static_dir.iterdir():
        if file.is_file():
            shutil.copy(file, output_dir / file.name)

def get_all_files(root_dir):
    log.info("Analyzing snippets...")
    root_path = Path(root_dir)
    all_files = list(root_path.rglob("*.code-snippets"))  # busca recursivamente
    if all_files:
        for f in all_files:
            log.info(f"Code Snippet file: {f}")
    else:
        log.warning("No snippets exist")
    return all_files

def slugify(text: str) -> str:
    return (
        text.replace(" ", "-")
            .replace("/", "-")
            .replace("\\", "-")
    )


def generate_docs(input_dir=None, output_dir="dist"):
    input_dir = Path.cwd() if input_dir is None else Path(input_dir)
    output_dir = Path(output_dir)
    
    env = Environment(
        loader=PackageLoader("snippet_docs", "templates"),
        autoescape=select_autoescape(["html"])
    )

    index_template = env.get_template("index.html")
    snippet_template = env.get_template("snippet.html")

    if not output_dir.is_absolute():
        output_dir = Path.cwd() / output_dir

    snippets_html_dir = output_dir / "snippets"
    snippets_html_dir.mkdir(parents=True, exist_ok=True)

    # Árbol completo: carpeta → archivo → snippets
    tree = {}

    base_path = Path(input_dir).resolve()

    for snippet_file in get_all_files(input_dir):
        snippet_file = Path(snippet_file).resolve()

        # Ruta relativa (carpetas internas)
        relative_parts = snippet_file.relative_to(base_path).parts
        folders = relative_parts[:-1]                                  # carpetas
        file_name = relative_parts[-1].removesuffix(".code-snippets")  # archivo .code-snippets

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
            snippet_obj = Snippet(name, snippet)

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

    log.info(f"Documentation generated in: {output_dir.resolve()}")

def main():
    parser = argparse.ArgumentParser(description="Generates HTML documentation for snippet files")
    parser.add_argument("-i", "--input", default=None, help="Folder containing .code-snippets files")
    parser.add_argument("-o", "--output", default="dist", help="Output folder for HTML files")
    args = parser.parse_args()

    snippets_dir = args.input
    output_dir = args.output

    generate_docs(snippets_dir, output_dir)