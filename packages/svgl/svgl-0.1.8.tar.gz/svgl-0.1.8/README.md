# svgl

A simple SVG library for interact with https://svgl.app/.

Based on the API documentation: https://svgl.app/api.

## Installation

### Using setup.py

```bash
python -m pip install svgl
```

## Usage

```python
from svgl import SVGL

svgl = SVGL()

## Get information about the SVG
coursera = svgl.svgs.search("coursera").get()

## Download the SVG
### Download the SVG to the current search
svgl.svgs.search("poper").route.download()

### Download the specific SVG to a specific output
svgl.library("discord").output("archive/").download()

### Get categories of the SVG
categories = svgl.categories.get()
```


