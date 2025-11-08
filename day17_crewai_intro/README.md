# 🤖 CrewAI Content Workflow - Streamlit App

A collaborative AI content generation system using CrewAI with 4 specialized agents working in sequence.

## 🌟 Features

- **4 AI Agents Working in Sequence:**
  - 🔍 **Researcher**: Finds 5 credible, up-to-date facts using Tavily search
  - ✍️ **Drafter**: Writes an initial paragraph based on facts
  - 🔎 **Critic**: Provides constructive feedback on the draft
  - ✨ **Finalizer**: Polishes the content based on feedback

- **Interactive UI:**
  - Toggle verbose mode to see detailed execution logs
  - 3-tab interface showing results, process details, and logs
  - Download final content as text file
  - Real-time progress indicators

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd day17_crewai_intro
pip install -r requirements.txt
```

### 2. Configure API Keys

The app uses `.streamlit/secrets.toml` for secure API key storage (already configured with your keys).

Alternatively, you can enter keys directly in the UI when prompted.

### 3. Run the App

```bash
streamlit run streamlit_app.py
```

The app will open in your default browser at `http://localhost:8501`

## 🎯 How to Use

1. **Enter a Topic**: Type any topic you want researched and written about
2. **Toggle Verbose Mode** (optional): Enable in sidebar to see detailed logs
3. **Click "Generate Content"**: Watch as 4 agents collaborate to create polished content
4. **View Results**:
   - **Final Result Tab**: See the polished output and download it
   - **Process Details Tab**: Review each agent's contribution
   - **Execution Logs Tab**: View detailed execution logs (if verbose enabled)

## 📋 API Keys Required

- **Gemini API Key**: For the LLM (Google's Gemini 2.5 Flash)
- **Tavily API Key**: For web search functionality

## 🛠️ Technology Stack

- **CrewAI**: Multi-agent orchestration framework
- **Streamlit**: Web interface
- **Google Gemini**: Language model
- **Tavily**: Web search API

## 📝 Example Topics

- "What is Artificial General Intelligence?"
- "Latest developments in quantum computing"
- "Climate change solutions in 2025"
- "Future of electric vehicles"

## 🔒 Security

- API keys are stored in `.streamlit/secrets.toml` (gitignored)
- Keys can also be entered securely via the UI
- Never commit secrets.toml to version control

## 📄 Project Structure

```
day17_crewai_intro/
├── streamlit_app.py                    # Main application
├── .streamlit/
│   ├── secrets.toml                    # API keys (gitignored)
│   └── config.toml                     # Streamlit configuration
├── requirements.txt                    # Python dependencies
├── .gitignore                         # Git ignore rules
└── README.md                          # This file
```

## 🤝 Contributing

This is a learning project. Feel free to experiment and extend functionality!

## 📜 License

Educational project - free to use and modify.

