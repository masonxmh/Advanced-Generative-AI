# Crafting an AI-Powered HR Assistant

This project builds an HR assistant that answers questions about the Nestle HR policy document.

## Contents

- `HR_assistant.ipynb`: main notebook with Azure OpenAI, embeddings, retrieval, and Gradio UI
- `hr_assistant_notebook.ipynb`: alternate notebook version
- `app.py`: Python app entry point
- `data/`: source HR policy PDF and related files

## Features

- loads and splits the HR policy PDF
- creates embeddings with Azure OpenAI
- stores vectors in Chroma DB
- retrieves relevant policy chunks
- answers user questions with a Gradio interface

## Requirements

Install dependencies from:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file with:

```env
AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_API_VERSION=your_api_version
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_CHAT_DEPLOYMENT=your_chat_deployment
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=your_embedding_deployment
```
