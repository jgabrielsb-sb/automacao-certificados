### Introduction ###

This project is an automation that encapsulates:
    
    * the download of documents from several sources;
    * the extraction of the relevant information on those documents;
    * the insertion of those informations on database via API;

### How to run on development ###

Note: This project uses uv as the Python project manager.
Install it first using:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh

```

Install the dependencies:
```
uv sync
```


Define .env variables by checking the .env.sample:
```bash
cp .env.sample .env # create your .env by copying .env sample
```

To run locally, go to the project root and run:
```bash
uv run python src/automacao_certificados/main.py
```

To run the tests: 
```bash
uv run pytest
```

### How to run on production ###

To run on production, set the docker environement variable that are defined on .env.sample.

Then, run:

```bash
docker compose up --build
```




