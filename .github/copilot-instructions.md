# AI Coding Assistant Instructions

## Project Context
This is a Python Flask-based notetaking application. Its core features include creating, managing, translating, and generating notes using AI.

- **Backend:** Python, Flask, SQLAlchemy
- **Database:** Supabase (PostgreSQL)
- **AI Integration:** OpenAI SDK is used to call the `gpt-4o-mini` model for translation and note generation.

## Core Instructions

### 1. API Keys and Secrets
**NEVER** hardcode API keys, database URLs, or any other secrets directly in the code. Always load them from environment variables using `os.getenv()`.

*Correct Example:*
```python
import os
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
database_url = os.getenv("DATABASE_URL")
```

*Incorrect Example:*
```python
openai_api_key = "sk-..."
database_url = "postgresql://..."
```

### 2. Database Schema
The primary database is a Supabase PostgreSQL instance. The main table for notes is structured as follows:

- **Table Name:** `notes`
- **Columns:**
    - `id`: `SERIAL PRIMARY KEY`
    - `title`: `TEXT NOT NULL`
    - `notes`: `TEXT`
    - `tags`: `TEXT` (e.g., comma-separated values)
    - `language`: `TEXT` (e.g., 'en', 'zh')
    - `date`: `TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP`

When generating database-related code (e.g., SQLAlchemy models or raw SQL queries), adhere strictly to this schema.

### 3. AI Model Usage
The project uses the OpenAI Python SDK to interact with the `gpt-4o-mini` model for AI-powered features like translation and note generation. Ensure that all calls to the OpenAI API are properly authenticated using the API key loaded from environment variables.

### 4. Commit Messages
All commit messages **MUST** follow the Conventional Commits specification. This helps maintain a clear and automated version history.

- `feat:` for new features.
- `fix:` for bug fixes.
- `refactor:` for code changes that neither fix a bug nor add a feature.
- `docs:` for documentation changes.
- `style:` for code style changes (e.g., formatting).
- `test:` for adding or improving tests.
- `chore:` for build process or auxiliary tool changes.

*Example Commit Message:*
```
feat: add note translation feature

Implement a new API endpoint `/notes/<id>/translate` that uses the OpenAI API to translate note content to a specified language.
```

## Goal
The purpose of these instructions is to align all generated code with the project's standards, ensure security best practices are followed, and prevent the AI from "hallucinating" or deviating from the established architecture.