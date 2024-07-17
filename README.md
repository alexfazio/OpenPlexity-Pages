# Installation
  poetry install

# ENV
Set manually, in app.py, the following variables. In this example the api are for oobabooga Text Generation Webui API
  API_ENDPOINT = "http://localhost:5000/v1"
  API_KEY = "na"
Be sure to provide the correct API_KEY, if the endpoint you specify requires authentication.
TODO: add this variables in .env file

# Run project 
  poetry run streamlit run python app.py