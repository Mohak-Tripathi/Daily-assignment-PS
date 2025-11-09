# LangGraph Math Agent - Streamlit App

A Streamlit application that demonstrates LangGraph's agent capabilities with mathematical tools.

## Features

- 🧮 **Math Tools**: Divide and multiply operations
- 🤖 **AI Agent**: Uses Google's Gemini to understand queries and call tools
- 📊 **Visualization**: Shows the LangGraph workflow diagram
- 💬 **Conversation Flow**: Displays the full agent reasoning process
- 🔍 **Detailed Analysis**: Inspect all messages and tool calls

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.streamlit/secrets.toml` with your API key:
```toml
GEMINI_API_KEY = "your-gemini-api-key"
```

Or enter it directly in the UI when prompted.

3. Run the app:
```bash
streamlit run streamlit_app.py
```

## Usage

1. Enter a mathematical question (e.g., "What is 10 divided by 2?")
2. Click "Execute Query"
3. View the conversation flow, detailed analysis, and graph visualization

## Example Queries

- What is 10 divided by 2?
- Multiply 5 by 7
- Calculate 100 / 4
- What's 12 times 8?
- Divide 50 by 5

## Technology Stack

- **LangGraph**: For agent workflow orchestration
- **LangChain**: For LLM integration
- **Google Gemini**: As the language model
- **Streamlit**: For the web interface

