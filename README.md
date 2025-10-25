# Agentic AI Development - Daily Assignments

Welcome to my Agentic AI learning journey! This repository contains my daily assignments as I explore and build various AI agents using Python, Streamlit, LangChain, and LangGraph.

## 📚 About This Repository

This is a structured collection of daily assignments where each assignment is:
- **Independent**: Each folder is a standalone project
- **Deployable**: Can be deployed separately to Streamlit Community Cloud
- **Well-documented**: Includes its own README and dependencies

## 🗂️ Project Structure

```
AgenticAIDevelopment/
├── .gitignore                    # Git ignore rules
├── README.md                     # This file
├── setup_guide.md               # Virtual environment setup guide
├── day00_template/              # Template for new assignments
├── day01_assignment_name/       # First assignment
├── day02_assignment_name/       # Second assignment
└── ...                          # More assignments
```

Each assignment folder contains:
```
dayXX_assignment_name/
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── requirements.txt         # Python dependencies
├── streamlit_app.py         # Main application
├── README.md                # Assignment documentation
├── utils/                   # Helper modules (optional)
└── tests/                   # Tests (optional)
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Git
- A code editor (VS Code recommended)

### Setup Instructions

1. **Clone this repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/AgenticAIDevelopment.git
   cd AgenticAIDevelopment
   ```

2. **Set up virtual environment** (see [setup_guide.md](setup_guide.md) for detailed instructions)
   ```bash
   # Option 1: Global virtual environment (recommended for beginners)
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   
   # Option 2: Per-assignment virtual environment
   cd day01_assignment_name
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies for an assignment**
   ```bash
   cd day01_assignment_name
   pip install -r requirements.txt
   ```

4. **Run the Streamlit app**
   ```bash
   streamlit run streamlit_app.py
   ```

## 📋 Daily Assignments

| Day | Assignment | Description | Status | Live Demo |
|-----|-----------|-------------|--------|-----------|
| 00  | [Template](day00_template/) | Project template and example | ✅ Complete | - |
| 01  | Coming soon... | - | 🔄 In Progress | - |

## 🛠️ Technologies Used

- **Python**: Core programming language
- **Streamlit**: Web app framework for AI/ML projects
- **LangChain**: Framework for LLM applications
- **LangGraph**: Framework for building stateful agents
- **OpenAI API**: LLM integration (when needed)
- **Other libraries**: As required per assignment

## 📖 Learning Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Python Virtual Environments Guide](setup_guide.md)

## 🚢 Deployment

Each assignment can be deployed independently to Streamlit Community Cloud:

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Select your repository
5. Set the main file path to `dayXX_assignment_name/streamlit_app.py`
6. Click "Deploy"!

For detailed deployment instructions, see [setup_guide.md](setup_guide.md#deployment).

## 🔐 Managing Secrets

For API keys and sensitive information:

**Local Development:**
- Create `.streamlit/secrets.toml` in your assignment folder
- Add your secrets (this file is gitignored)
```toml
OPENAI_API_KEY = "your-key-here"
ANTHROPIC_API_KEY = "your-key-here"
```

**Streamlit Cloud:**
- Add secrets in the Streamlit Cloud dashboard
- Settings → Secrets → Paste your secrets in TOML format

## 🤝 Contributing

This is a personal learning repository, but feel free to:
- Open issues for suggestions
- Fork and experiment with the code
- Share your own learning journey

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 📧 Contact

Feel free to reach out if you have questions or want to discuss Agentic AI!

---

**Happy Learning! 🎉**

