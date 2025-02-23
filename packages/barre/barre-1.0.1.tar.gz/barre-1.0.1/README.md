# barre

<div align="center">

[![PyPI version](https://badge.fury.io/py/barre.svg)](https://badge.fury.io/py/barre)
[![CI](https://github.com/FeelTheFonk/barre/workflows/CI/badge.svg)](https://github.com/FeelTheFonk/barre/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight progress bar. One line, zero config, zero dependencies.
</div>

## Install
```bash
pip install barre
```

## Usage
```python
from barre import b

# Simple iteration
for x in b(range(100)):
    process(x)

# With any iterable
items = ["item1", "item2", "item3"]
for x in b(items):
    process(x)
```

Output:
```
[||||||||||||||||||||||||||||||||||||||||] 100/100
```

## Features
- Single file (<1KB)
- Zero dependencies
- No configuration needed
- Clean ASCII progress display

## License
MIT

---
Built with minimalism in France 🇫🇷