# barre

<div align="center">

[![PyPI version](https://badge.fury.io/py/barre.svg)](https://badge.fury.io/py/barre)
[![CI](https://github.com/FeelTheFonk/barre/workflows/CI/badge.svg)](https://github.com/FeelTheFonk/barre/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight progress bar. One line, zero config, zero dependencies.

![Demo](demo.gif)

</div>

## Install

```bash
pip install barre
```

## Usage

Simple and intuitive:

```python
from barre import b
from time import sleep

# Simple iteration
for x in b(range(100)):
    sleep(0.1)  # your work here

# With any iterable
items = ["item1", "item2", "item3"]
for x in b(items):
    process(x)
```

Output:
```
[||||||||||||||||||||||||||||||||||||||||] 50/100
```

## Real-world Examples

### Processing Files
```python
from barre import b
import os

# Process all images in a directory
image_files = [f for f in os.listdir("images/") if f.endswith((".jpg", ".png"))]
for file in b(image_files):
    with open(f"images/{file}", "rb") as img:
        # Your image processing here
        pass
```

### API Requests
```python
from barre import b
import requests

# Download multiple URLs with progress
urls = [
    "https://api.example.com/data1",
    "https://api.example.com/data2",
    "https://api.example.com/data3",
]
responses = []
for url in b(urls):
    response = requests.get(url)
    responses.append(response.json())
```

### Data Processing
```python
from barre import b
import pandas as pd

# Process chunks of a large DataFrame
df = pd.read_csv("large_file.csv")
chunk_size = 1000
chunks = [df[i:i+chunk_size] for i in range(0, len(df), chunk_size)]

results = []
for chunk in b(chunks):
    result = chunk.groupby('category').sum()
    results.append(result)
```

### Long Computations
```python
from barre import b
import numpy as np

# Heavy computations with visual feedback
matrices = []
for i in b(range(100)):
    matrix = np.random.rand(100, 100)
    result = np.linalg.eig(matrix)
    matrices.append(result)
```

### Training ML Models
```python
from barre import b

# Training epochs with progress
epochs = 100
for epoch in b(range(epochs)):
    model.train_epoch()
    loss = model.evaluate()
```

## Features

- **Minimal**: Single file (<1KB)
- **Fast**: Zero dependencies
- **Simple**: No configuration needed
- **Clean**: Professional ASCII output
- **Universal**: Works with any iterable

## License

[MIT](LICENSE)

---