# galactica

all the resources for a future paper :)

```
├── config.py -- configuration file
├── generate_symbols.py -- main file for generating all symbols. run python3 generate_symbols.py --help for instructions
├── generator
│   ├── cache.py
│   ├── generate_map.py
│   ├── generate_shapes.py
│   ├── generate_vectors.py
│   ├── __init__.py
│   └── normalize_vectors.py
├── .gitignore
├── Makefile
├── trainer
│   ├── flask -- the backend for the web trainer
│   │   ├── main.py
│   │   ├── read.py
│   │   └── resize.py
│   └── web -- the frontend for the web trainer: can be run with python3 -m http.server
│       ├── app.js
│       └── index.html
├── words_300.txt
└── words_45.txt
```
