# Tela Client

A Python client library for interacting with the Tela API.

## Installation

You can install the Tela Client using pip:

```
pip install git+https://github.com/yourusername/tela-client.git
```

## Usage

Here's a basic example of how to use the Tela Client:

```python
from tela_client import TelaClient, file

TELA_API_KEY = "Your API KEY"
tela_client = TelaClient(TELA_API_KEY)

canvas_id = "your-canvas-id"
canvas = tela_client.newCanvas(canvas_id, expected_input=['document'])

FILE_NAME = "./your_document.pdf"
result = canvas.run(document=file(FILE_NAME))
print(result)
```

## License