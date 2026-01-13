# SnippetDocs

SnippetDocs is a Python library that automatically generates a dynamic, interactive documentation website for your VS Code snippets. It scans directories for `.code-snippets` files, parses their JSON content (including comments), and creates an HTML site with a hierarchical navigation structure and detailed snippet pages.

## Features

- **Recursive Scanning**: Automatically discovers `.code-snippets` files in subdirectories.
- **JSON with Comments Support**: Parses snippet files using `commentjson` to handle comments in JSON.
- **Hierarchical Documentation**: Organizes snippets in a tree structure (folders > files > snippets).
- **Interactive UI**: Expandable navigation with details/summary elements.
- **Dynamic Scope Coloring**: Assigns unique colors to scope badges based on a hash function for better visual distinction.
- **Individual Snippet Pages**: Each snippet gets its own HTML page with detailed information including description, prefixes, scopes, and code body.
- **Static Assets**: Includes CSS for styling and JavaScript for interactive elements.

## How It Works

1. **Input Processing**: The tool recursively searches for `.code-snippets` files in the specified input directory (or current directory if not specified).

2. **Snippet Parsing**: Each `.code-snippets` file is parsed as JSON (supporting comments). Snippets are extracted and converted into `Snippet` objects containing:
   - Name
   - Scope (list of applicable scopes)
   - File template flag
   - Prefix(es)
   - Description
   - Body (code content)

3. **HTML Generation**:
   - An index page (`index.html`) is created with a collapsible tree navigation showing the folder/file/snippet hierarchy.
   - Individual pages for each snippet are generated in the `snippets/` subdirectory.
   - Static assets (CSS, JS) are copied to the output directory.

4. **Templating**: Uses Jinja2 templates to render HTML pages dynamically.

5. **Output**: All generated files are placed in the specified output directory (default: `dist/`).

## Installation

Install SnippetDocs via pip:

```bash
pip install git+https://github.com/luchersol/SnippetDocs
```

Or clone the repository and install locally:

```bash
git clone https://github.com/luchersol/SnippetDocs.git
cd SnippetDocs
pip install .
```

## Dependencies

- Python >= 3.7
- Jinja2: For HTML templating
- commentjson: For parsing JSON files with comments

## Usage

After installation, use the command-line tool:

```bash
generate-snippet-docs [OPTIONS]
```

### Options

- `-i, --input DIR`: Directory containing `.code-snippets` files (default: current directory)
- `-o, --output DIR`: Output directory for generated HTML files (default: `dist`)

### Example

Generate documentation for snippets in the `example/` directory and output to `docs/`:

```bash
generate-snippet-docs -i example -o docs
```

This will create a `docs/` folder with:
- `index.html`: Main navigation page
- `snippets/`: Individual snippet pages
- `static/`: CSS and JavaScript files
- `scripts/`: Additional scripts

## Snippet File Format

SnippetDocs expects `.code-snippets` files in the standard VS Code format. Example:

```json
{
  "Print to console": {
    "scope": "javascript,typescript",
    "prefix": "log",
    "body": [
      "console.log('$1');",
      "$2"
    ],
    "description": "Log output to console"
  }
}
```

Comments are supported using `commentjson` syntax:

```json
{
  // This is a comment
  "Snippet Name": {
    "scope": "python",
    "prefix": "if",
    "body": "if ${1:condition}:\n\t${2:pass}",
    "description": "Basic if statement"
  }
}
```

## Project Structure

After generation, the output directory contains:

```
output_dir/
├── index.html          # Main index page
├── snippets/           # Individual snippet pages
│   ├── snippet1.html
│   └── snippet2.html
├── static/
│   └── styles.css      # Styling
└── scripts/
    └── scopes-color.js # Dynamic coloring for scopes
```

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
