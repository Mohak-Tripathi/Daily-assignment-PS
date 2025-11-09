# 📚 Multi-File RAG ChatBot - Streamlit App

An intelligent document chatbot that uses Retrieval-Augmented Generation (RAG) to answer questions from your documents, with automatic fallback to web search when needed.

## 🌟 Features

- **📄 Multi-Format Support:**
  - PDF documents (via PyMuPDF)
  - CSV files
  - Text files (.txt)

- **🧠 Smart RAG System:**
  - Document chunking with overlap for better context
  - Vector embeddings using Google Gemini
  - PostgreSQL + pgvector for efficient similarity search
  - Intelligent retrieval of top 3 relevant chunks

- **🔍 Hybrid Search:**
  - Primary: Answer from your documents
  - Fallback: Automatic web search via Tavily when documents don't contain the answer
  - Clear source indication (documents vs web)

- **💬 Interactive Chat Interface:**
  - Real-time chat with conversation history
  - Visual distinction between user and assistant messages
  - Source badges showing where answers came from
  - Persistent chat across interactions

- **⚙️ Flexible Configuration:**
  - Secure API key management via secrets.toml
  - Alternative UI-based configuration
  - Custom collection naming
  - File upload status tracking

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd day012_multi_file_rag
pip install -r requirements.txt
```

### 2. Configure API Keys and Database

Create `.streamlit/secrets.toml` with your credentials:

```toml
# API Keys
GEMINI_API_KEY = "your-gemini-api-key"
TAVILY_API_KEY = "your-tavily-api-key"

# PostgreSQL Configuration
PG_USER = "your_pg_user"
PG_PASSWORD = "your_pg_password"
PG_HOST = "your_pg_host"
PG_PORT = "5432"
PG_DATABASE = "your_pg_database"
```

**Alternative:** Enter credentials directly in the UI when prompted.

### 3. Set Up PostgreSQL with pgvector

You need a PostgreSQL database with pgvector extension. Options:

**Option A: Neon (Recommended - Free Tier Available)**
1. Sign up at [neon.tech](https://neon.tech)
2. Create a new project
3. Copy connection details to secrets.toml

**Option B: Local PostgreSQL**
```bash
# Install PostgreSQL and pgvector extension
# Then create a database and enable pgvector:
CREATE EXTENSION vector;
```

### 4. Run the App

```bash
streamlit run streamlit_app.py
```

The app will open in your default browser at `http://localhost:8501`

## 🎯 How to Use

### Step 1: Upload Documents
1. Click the file upload area
2. Select one or more files (PDF, CSV, or TXT)
3. Click "Process Files & Initialize Agent"
4. Wait for documents to be processed and embedded

### Step 2: Chat with Your Documents
1. Type your question in the chat input
2. Press Enter or click Send
3. View the response with source indicator:
   - 📄 **Green badge**: Answer from your documents
   - 🌐 **Blue badge**: Answer from web search (fallback)

### Step 3: Continue the Conversation
- Ask follow-up questions
- Chat history persists during your session
- Click "Clear Chat History" in sidebar to start fresh

## 📋 Configuration Options

### Sidebar Settings

- **Collection Name**: Name for your vector store collection (default: "multi_file_rag_docs")
- **System Status**: Shows agent status and uploaded files
- **Clear Chat History**: Reset conversation

### Document Processing

- **Chunk Size**: 1000 characters (configurable in code)
- **Chunk Overlap**: 200 characters (configurable in code)
- **Retrieval**: Top 3 most relevant chunks

## 🛠️ Technology Stack

- **Streamlit**: Web interface
- **LangChain**: RAG orchestration
- **Google Gemini**: 
  - `gemini-embedding-001`: Document embeddings
  - `gemini-2.5-flash`: Question answering
- **PostgreSQL + pgvector**: Vector database
- **Tavily**: Web search fallback
- **PyMuPDF**: PDF processing

## 💡 Example Use Cases

### Personal Knowledge Base
```
Upload: Research papers, notes, documentation
Ask: "What are the key findings about X?"
```

### Resume Assistant
```
Upload: Your resume (PDF)
Ask: "Summarize my work experience"
Ask: "What programming languages do I know?"
```

### Document Analysis
```
Upload: Reports, articles, CSV data
Ask: "What trends are mentioned?"
Ask: "Compare the data between months"
```

### Mixed Queries
```
Ask: "What's in my documents about AI?" → Searches documents
Ask: "What's the latest news on quantum computing?" → Falls back to web
```

## 🔒 Security & Privacy

- **API Keys**: Stored in `.streamlit/secrets.toml` (gitignored by default)
- **Database**: Uses SSL for PostgreSQL connections
- **Local Processing**: Document processing happens locally
- **Session Isolation**: Each session has isolated chat history

## 📁 Project Structure

```
day012_multi_file_rag/
├── streamlit_app.py                    # Main application
├── MultiFileRagChatBot.ipynb         # Original notebook (reference)
├── .streamlit/
│   ├── secrets.toml                   # API keys & DB config (gitignored)
│   └── config.toml                    # Streamlit configuration
├── requirements.txt                   # Python dependencies
├── .gitignore                        # Git ignore rules
└── README.md                         # This file
```

## 🐛 Troubleshooting

### "API keys not found"
- Create `.streamlit/secrets.toml` with your credentials
- Or enter them in the UI when prompted

### "Error connecting to PostgreSQL"
- Verify your PostgreSQL credentials
- Ensure pgvector extension is installed
- Check if database allows SSL connections
- Verify network connectivity

### "Unsupported file type"
- Only PDF, CSV, and TXT files are supported
- Check file extension is correct

### "No documents could be loaded"
- Verify files are not corrupted
- Check file permissions
- Try uploading files one at a time

### Agent Initialization Fails
- Check all API keys are valid
- Ensure PostgreSQL is accessible
- Verify sufficient database storage
- Check error details in expander

## 🔄 Comparison with Notebook

**Notebook Version:**
- Manual file upload in Colab
- One-time setup
- Terminal-based chat loop
- No session persistence

**Streamlit Version:**
- Web-based file upload
- Reusable across sessions
- Visual chat interface
- Source indicators
- Better UX with progress indicators

## 🚧 Future Enhancements

- [ ] Support for more file types (DOCX, XLSX)
- [ ] Document preview before processing
- [ ] Advanced search filters
- [ ] Export chat history
- [ ] Multiple collection management
- [ ] Document deletion/update
- [ ] Conversation memory across sessions
- [ ] Custom prompt templates

## 🤝 Contributing

This is a learning project. Feel free to experiment and extend functionality!

## 📜 License

Educational project - free to use and modify.

## 🙏 Acknowledgments

- Built with LangChain and Streamlit
- Uses Google Gemini for AI capabilities
- Vector storage powered by pgvector
- Web search via Tavily

---

**Need Help?** Check the error details in the app or review the original notebook for reference.


Multi-File RAG ChatBot is an intelligent document question-answering system built with Streamlit that allows users to upload multiple documents (PDF, CSV, TXT) and interact with them through natural language conversations. The system implements Retrieval-Augmented Generation (RAG) architecture using LangChain for orchestration, Google Gemini for embeddings and language understanding, and PostgreSQL with pgvector extension for efficient vector similarity search. A key feature is the hybrid search approach—when documents don't contain sufficient information to answer a query, the system automatically falls back to web search via Tavily API, ensuring comprehensive responses. Through this project, I gained hands-on experience with vector databases, document chunking strategies, semantic search implementation, and building production-ready conversational AI interfaces with proper error handling and session management.