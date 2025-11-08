# 🧮 LangGraph ReAct Agent - Streamlit App

A conversational math assistant built with LangGraph that uses the ReAct (Reasoning + Acting) pattern to solve arithmetic problems using tools.

## 🌟 Features

- **Interactive Chat Interface**: Natural conversation flow with memory
- **Smart Tool Usage**: Agent decides when to use tools (add, multiply, divide)
- **ReAct Pattern**: Combines reasoning and action-taking
- **Conversation Memory**: Remembers context across multiple turns
- **Tool Call Visibility**: Toggle to see when and how tools are used
- **Thread Management**: Start new conversations anytime

## 🧮 Available Math Tools

- ➕ **Add**: Add two integers
- ✖️ **Multiply**: Multiply two integers  
- ➗ **Divide**: Divide two integers (with zero-check)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd day016_langgrapg_react_agent
pip install -r requirements.txt
```

### 2. Configure API Keys

The app uses `.streamlit/secrets.toml` for secure API key storage (already configured).

### 3. Run the App

```bash
streamlit run streamlit_app.py
```

The app will open in your default browser at `http://localhost:8501`

## 🎯 How to Use

1. **Ask a Math Question**: Type any arithmetic query
2. **Multi-Step Problems**: "Add 5 and 10, then multiply by 3"
3. **Follow-Up Questions**: "Now divide that by 5"
4. **View Tool Calls**: Toggle "Show Tool Calls" to see agent thinking
5. **New Conversation**: Click "New Conversation" to start fresh

## 💬 Example Queries

```
"Add 15 and 27"
"What is 8 multiplied by 9?"
"Add 5 and 10, then multiply the result by 3"
"Divide 100 by 4"
"What was the last result?" (uses conversation memory)
```

## 🧠 How It Works

This app implements the **ReAct (Reasoning + Acting)** pattern:

1. **User Query** → Agent receives math question
2. **Reasoning** → Agent decides which tool(s) to use
3. **Action** → Agent calls appropriate tool(s)
4. **Response** → Agent provides natural language answer

### Architecture

```
User Input → LangGraph ReAct Agent → Tool Selection → Tool Execution → Response
                     ↓
              Conversation Memory (maintains context)
```

## 📋 Technical Details

- **Framework**: LangGraph for agent orchestration
- **LLM**: Google Gemini 2.5 Flash
- **Memory**: MemorySaver for conversation persistence
- **UI**: Streamlit chat interface
- **Tools**: LangChain @tool decorator

## 🔑 API Keys Required

- **Gemini API Key**: For the language model

## 🛠️ Project Structure

```
day016_langgrapg_react_agent/
├── streamlit_app.py              # Main application
├── .streamlit/
│   ├── secrets.toml              # API keys (gitignored)
│   └── config.toml               # Streamlit configuration
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

## 🎨 Features Breakdown

### Chat Interface
- Clean message bubbles for user and assistant
- Persistent conversation history
- Thread ID display for debugging

### Tool Call Display
- Expandable sections showing tool usage
- Display tool name, arguments, and results
- Helps understand agent's decision-making

### Session Management
- Conversation memory across messages
- New conversation button to reset context
- Thread IDs for conversation tracking

## 🔒 Security

- API keys stored in `.streamlit/secrets.toml` (gitignored)
- No hardcoded credentials in code
- Secure key input via password field fallback

## 🐛 Troubleshooting

**Agent not using tools:**
- Check if query is clear and mathematical
- Try more explicit instructions: "Use the add tool to calculate..."

**Memory not working:**
- Ensure you're in the same thread (check thread ID)
- Click "New Conversation" if you want to reset

**Tool call errors:**
- Division by zero is caught and handled
- Ensure inputs are integers for add/multiply

## 🤝 Contributing

This is a learning project. Feel free to experiment and extend functionality!

## 📜 License

Educational project - free to use and modify.

