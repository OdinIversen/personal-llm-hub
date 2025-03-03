# Personal LLM Hub

A local web interface for interacting with different LLM providers using customizable instruction sets.

## Features

- **Provider Selection**: Choose from multiple LLM API providers (OpenAI, Anthropic, etc.)
- **Custom Instructions**: Apply different system prompts and instruction sets to any provider
- **Simple Chat Interface**: Interact with your selected configuration
- **Local Deployment**: Run completely locally for privacy and personal use

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

## Setup Instructions

### Prerequisites

- Python 3.8+
- API keys for providers you wish to use (OpenAI, Anthropic, etc.)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/personal-llm-hub.git
   cd personal-llm-hub
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install fastapi uvicorn python-dotenv anthropic openai
   ```

4. Create a `.env` file in the root directory:
   ```
   ANTHROPIC_API_KEY=your_anthropic_key_here
   OPENAI_API_KEY=your_openai_key_here
   HOST=localhost
   PORT=8000
   ```

### Running the Application

1. Start the server:
   ```bash
   cd backend
   python app.py
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

3. Select a provider and instruction set from the dropdowns, then start chatting!

## Using the App

1. **Select a Provider**: Choose which LLM API to use (e.g., "Anthropic Claude 3.5 Sonnet")
2. **Select Instructions**: Choose a set of system instructions (e.g., "Coding Expert")
3. **Chat**: Type messages and receive responses based on your selected configuration

## Planned Features

- Save and continue conversations
- Manage and edit custom instruction sets through the UI
- Support for more LLM providers
- Conversation history persistence

## Development Status

🚧 **Early Development** 🚧

This project is a personal tool for interacting with various LLM APIs through a unified interface.