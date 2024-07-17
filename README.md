# OpenPlexity Setup Guide

Follow these instructions to set up and run OpenPlexity using Poetry.

## Installation

First, ensure you have Poetry installed. If not, install it via pip:

```bash
pip install poetry
```

Once Poetry is installed, navigate to your project directory and install the dependencies:

```bash
poetry install
```

## Configuration

Next, you need to create a `.env` file in the root directory of the project. This file will store your `pplx_api` key. Use the following command to create and add your API key to the `.env` file:

```bash
echo "pplx_api=<your-key>" > .env
```

Ensure your `.env` file contains your `pplx_api` key in this format:

```plaintext
pplx_api=<your-key>
```

## Running the Application

To run the application, use the following command:

```bash
poetry run streamlit run openplexity_pages/app.py
```

And that's it! Your application should now be up and running. Enjoy exploring OpenPlexity!
