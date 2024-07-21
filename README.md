![openplexity-pages](https://github.com/user-attachments/assets/4fb6dfa2-fda9-421d-a30d-8026c300a0c1)

# OpenPlexity: Open Source AI-Powered Content Creation

## Introducing OpenPlexity

OpenPlexity is an open-source alternative to Perplexity Pages, designed to transform your research into visually stunning, comprehensive content. Whether you're crafting in-depth articles, detailed reports, or informative guides, OpenPlexity streamlines the process so you can focus on what matters most: sharing your knowledge with the world.

## What sets OpenPlexity apart?

- **Open Source**: Unlike Perplexity Pages, OpenPlexity is fully open source, allowing for community contributions and customizations.
- **Privacy-Focused**: Your data stays with you. OpenPlexity runs locally, ensuring your research and content remain private.
- **Customizable**: Tailor the tone of your content to resonate with your target audience, from general readers to subject matter experts.
- **Adaptable**: Easily modify the structure of your articles—add, rearrange, or remove sections to best suit your material.
- **Visual**: Enhance your articles with AI-generated visuals or integrate your own images.

## Features That Matter

- **Local LLM Support**: Harness the power of Llama3 and Mixtral using Ollama for content generation.
- **Seamless Creation**: Transform your research into well-structured, beautifully formatted articles with ease.
- **Always Current**: Unlike static embedding-based tools, OpenPlexity uses real-time search results, ensuring your content is up-to-date.

## A Tool for Everyone

OpenPlexity empowers creators in any field to share knowledge:

- **Educators**: Develop comprehensive study guides, breaking down complex topics into digestible content.
- **Researchers**: Create detailed reports on your findings, making your work more accessible.
- **Hobbyists**: Share your passions by creating engaging guides that inspire others.
- **Content Creators**: Produce well-researched, visually appealing articles on any topic.

# Getting Started

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
echo "pplx_api=<your-pplx-api-key>
VERTEX_AI_API_KEY=<your-vertex-ai-api-key>
GROQ_API_KEY=<your-groq-api-key>
BASE_URL=https://rentry.co
SERPER_API_KEY=<your-serper-api-key>" > .env
```

## Running the Application

To run the application, use the following command:

```bash
poetry run streamlit run openplexity_pages/app.py
```

And that's it! Your application should now be up and running. Enjoy exploring OpenPlexity!

---

## Contribute

OpenPlexity thrives on community contributions. Whether you're fixing bugs, adding features, or improving docs, we welcome your input! Check out our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Support the Project

Love OpenPlexity? Here's how you can help:

- Star us on GitHub

## The Power of Open Source

While Perplexity Pages offers a polished, hosted solution, OpenPlexity brings the power of AI-driven content creation to the open-source community. We believe in the potential of collaborative development and the importance of data privacy.

With OpenPlexity, you have the freedom to host your own instance, contribute to its development, and create content that educates, inspires, and engages your audience—all while maintaining full control over your data and the tool itself.

**Let's see what we can create together.**
