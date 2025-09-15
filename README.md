#   New Manga Reader Project, the REST api for project will be based in this repository

This project will be the quintessence of all my knowledge

## Setup and installation


###    ~1.Installation with docker(recommended)~**(on progress)**

_instructions for build docker container and run it_


###    2. Installation on local system

for run this project you need `uv` package manager

To install UV on Windows you need to type this in cmd or powershell.
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

for macOS and linux
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

if you haven't curl you can use wget

```bash
wget -qO- https://astral.sh/uv/install.sh | sh
```

then run `uv sync` for install all project dependencies




## How to run project

for run installed app you must type
'''bash
uv run main.py
'''


