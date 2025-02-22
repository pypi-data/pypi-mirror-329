# Markdown renderer - Markdown to HTML Converter

Author : Orhan Cavus  
Date   : 20.02.2025  

`markdown_renderer_lite` is a simple command-line tool that converts Markdown into HTML with syntax highlighting.

## Features

- Supports **fenced code blocks** and **syntax highlighting** (`codehilite`)
- Outputs clean, well-structured HTML
- Customizable CSS for styling
- Lightweight and easy to use

## Installation

### Install Locally

Clone the repository and install the package:

```sh
git clone https://github.com/yourusername/markdown_renderer_lite.git
cd markdown_renderer_lite
pip install -e .
```

or

```sh
pip install markdown-renderer-lite
```

### Usage

```sh
echo "# Hello World" | markdown_renderer_lite > output.html
```

or create bash script to view the markdown file directly in Safari

```sh
% markdown_html_view README.md
```

```sh
python -m markdown_renderer_lite README.md
```
