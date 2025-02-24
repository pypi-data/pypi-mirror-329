# Meterviewer

Meter Data viewer, not only to view multiple dataset via notebook.

## Features

1. Meter Image generation.
2. Generate jsondb for meter dataset.
3. Generate sqlite.db for meter dataset.
4. View the dataset with streamlit.

## Install

`pip install meterviewer`

## Development

We use [pdm](https://pdm-project.org/) to manage the project.

- To install pdm, run `python3 -m pip install pdm`.
- To install the dependencies, run `pdm install`.

## Documentation

We use [sphinx](https://www.sphinx-doc.org/en/master/) for documentation.

## Notes

1. Pure functional is critial. Less things to worry about.


## For Developer

`pdm run pip install -r ./requirements/dev.txt -r /requirements/docs.txt`
