```bash
pip install poetry
```

```bash
poetry install
```

Create a `.env` file in the main directory. 

```bash
echo "pplx_api=<your-key>" > .env
```

The `.env` file should contain your `pplx_api` key in the following format: `pplx_api=<your-key>`.

```bash
poetry run streamlit run openplexity_pages/app.py
```