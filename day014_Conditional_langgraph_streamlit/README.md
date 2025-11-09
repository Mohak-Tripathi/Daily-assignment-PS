# 🔀 LangGraph Conditional Routing - Streamlit App

An intelligent question-answering system using LangGraph with conditional routing between a knowledge base and an LLM.

## 🌟 Features

- **Conditional Routing:**
  - 📚 **Knowledge Base Path**: Instantly retrieves answers from predefined facts
  - 🤖 **LLM Path**: Uses Google Gemini for dynamic, AI-generated responses
  
- **Automatic Decision Making:**
  - Graph automatically determines the best path based on question content
  - No manual selection needed!

- **Interactive UI:**
  - Toggle verbose mode to see detailed execution logs
  - 3-tab interface showing results, process details, and graph visualization
  - Download answers as text files
  - Real-time progress indicators
  - Example questions to get started

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd day014_Conditional_langgraph_streamlit
pip install -r requirements.txt
```

### 2. Configure API Key

Create a `.streamlit/secrets.toml` file:

```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
```

Alternatively, you can enter the key directly in the UI when prompted.

### 3. Run the App

```bash
streamlit run streamlit_app.py
```

The app will open in your default browser at `http://localhost:8501`

## 🎯 How to Use

1. **Enter a Question**: Type any question in the text area
2. **Use Example Questions**: Click the example buttons to try predefined questions
3. **Toggle Verbose Mode** (optional): Enable in sidebar to see step-by-step execution
4. **Click "Process Question"**: Watch as the graph routes and answers your question
5. **View Results**:
   - **Result Tab**: See the answer and which path was used (KB or LLM)
   - **Process Details Tab**: Review each step of the workflow
   - **Graph Visualization Tab**: View the workflow structure

## 📚 Knowledge Base

The app comes pre-loaded with facts about:
- Ada Lovelace
- Python programming language
- LangChain framework
- LangGraph library
- Artificial Intelligence

Questions matching these topics will be answered from the knowledge base. All other questions will be routed to the LLM.

## 🔑 API Key Required

- **Gemini API Key**: Get yours at [Google AI Studio](https://makersuite.google.com/app/apikey)

## 🛠️ Technology Stack

- **LangGraph**: State machine and graph-based workflow orchestration
- **LangChain**: LLM framework
- **Streamlit**: Web interface
- **Google Gemini**: Language model (gemini-2.0-flash-exp)

## 💡 Example Questions

**Knowledge Base Questions:**
- "Who is Ada Lovelace?"
- "What is Python?"
- "Tell me about LangChain"
- "What is LangGraph?"

**LLM Questions:**
- "What is the capital of France?"
- "How does photosynthesis work?"
- "Explain quantum computing"

## 🔒 Security

- API keys are stored in `.streamlit/secrets.toml` (gitignored)
- Keys can also be entered securely via the UI
- Never commit secrets.toml to version control

## 📄 Project Structure

```
day014_Conditional_langgraph_streamlit/
├── streamlit_app.py              # Main application
├── .streamlit/
│   └── secrets.toml              # API keys (gitignored)
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

## 🎓 Learning Objectives

This app demonstrates:
- Conditional routing in LangGraph
- State management in graph-based workflows
- Integration of knowledge bases with LLMs
- Building interactive AI applications with Streamlit

## 🤝 Contributing

This is a learning project. Feel free to experiment and extend functionality!

## 📜 License

Educational project - free to use and modify.

