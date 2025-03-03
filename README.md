# Personal LLM Hub

A local web interface for interacting with different LLM providers using customizable instruction sets.

## Features

- **Provider Selection**: Choose from multiple LLM API providers (OpenAI, Anthropic, etc.)
- **Custom Instructions**: Apply different system prompts and instruction sets to any provider
- **Simple Chat Interface**: Interact with your selected configuration
- **Local Deployment**: Run completely locally for privacy and personal use

## Planned Features

- Save and continue conversations
- Manage and edit custom instruction sets through the UI
- Support for more LLM providers

## Project Structure

```
personal-llm-hub/
├── .env                    # API keys (ignored by git)
├── .env.example            # Template for required environment variables
├── .gitignore              # Git ignore file
├── README.md               # Project documentation
├── config/
│   ├── providers.json      # Available LLM API providers
│   └── instructions.json   # Custom instruction sets
├── backend/
│   ├── app.py              # FastAPI application
│   ├── llm_providers/      # Provider implementations
│   │   ├── __init__.py
│   │   ├── anthropic.py    # Anthropic Claude API
│   │   ├── openai.py       # OpenAI API
│   │   └── base.py         # Common interface
│   └── requirements.txt    # Python dependencies
└── frontend/
    ├── index.html          # Main HTML file
    ├── style.css           # CSS styles
    └── script.js           # Frontend JavaScript
```

## Development Status

🚧 **Early Development** 🚧

This project is starting with a minimal implementation focused on separating provider selection from custom instruction sets.