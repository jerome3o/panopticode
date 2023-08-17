# Panopticode

This is a project to leverage self monitoring and social/brain hacks to help motivate me to achieve my goals

## Setup

### Env vars

Set up env files and fill in blanks:

```sh
cp .env.example .env
```

`PANOPTICODE_API_KEYS` is a placeholder for an eventual api key system for these projects.

### Python environment

Each project will have it's own python environment defined by a `requirements.txt` file, but I will be developing in a superset environment and worry about isolating deps when making images

```sh
python -m venv venv
source ./venv/bin/activate

# and then something like:
pip install -r ./services/daily/requirements.txt -r ./services/processes/requirements.txt
```

Note that as this repo evolves more projects will be added and names may be changed, so you might have to craft your dev environment by hand for now (very open to good python monorepo tooling).
