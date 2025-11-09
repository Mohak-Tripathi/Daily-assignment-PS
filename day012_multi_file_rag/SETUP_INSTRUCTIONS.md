# 🛠️ Setup Instructions for Multi-File RAG ChatBot

This guide will walk you through setting up the Multi-File RAG ChatBot application.

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- PostgreSQL database with pgvector extension (or Neon account)
- API keys for Google Gemini and Tavily

## 🚀 Step-by-Step Setup

### Step 1: Install Python Dependencies

Navigate to the project directory and install required packages:

```bash
cd day012_multi_file_rag
pip install -r requirements.txt
```

**Installed packages include:**
- `streamlit` - Web application framework
- `langchain` - RAG orchestration (includes langchain_core)
- `langchain-community` - Community integrations
- `langchain-google-genai` - Google Gemini integration
- `langchain-tavily` - Tavily search integration
- `langchain-postgres` - PostgreSQL vector store
- `sqlalchemy` - Database toolkit
- `psycopg2-binary` - PostgreSQL adapter
- `pymupdf` - PDF processing
- `pgvector` - Vector similarity search
- `asyncpg` - Async PostgreSQL driver
- `google-generativeai` - Google AI SDK
- `tavily-python` - Tavily search SDK

### Step 2: Set Up PostgreSQL with pgvector

You have two options:

#### Option A: Use Neon (Recommended for Beginners) ✨

Neon provides free PostgreSQL with pgvector built-in:

1. **Sign up**: Go to [neon.tech](https://neon.tech) and create a free account
2. **Create Project**: Click "Create Project"
3. **Get Connection Details**:
   - Go to your project dashboard
   - Click "Connection Details"
   - Copy the connection string
4. **Extract Information**: From the connection string like:
   ```
   postgresql://user:password@host:5432/dbname
   ```
   Extract:
   - User: `user`
   - Password: `password`
   - Host: `host`
   - Port: `5432`
   - Database: `dbname`

#### Option B: Use Local PostgreSQL

If you have PostgreSQL installed locally:

```bash
# Install PostgreSQL (if not already installed)
# Windows: Download from postgresql.org
# Mac: brew install postgresql
# Linux: sudo apt-get install postgresql

# Install pgvector extension
# Follow instructions at: https://github.com/pgvector/pgvector

# Create database and enable extension
psql -U postgres
CREATE DATABASE multifile_rag;
\c multifile_rag
CREATE EXTENSION vector;
\q
```

### Step 3: Get API Keys

#### Google Gemini API Key 🔑

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key

#### Tavily API Key 🔍

1. Visit [Tavily](https://tavily.com/)
2. Sign up for a free account
3. Navigate to API Keys section
4. Copy your API key

### Step 4: Configure Secrets

Create a secrets file for your API keys:

```bash
# Copy the example file
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Edit `.streamlit/secrets.toml` with your actual credentials:

```toml
# API Keys
GEMINI_API_KEY = "your-actual-gemini-api-key"
TAVILY_API_KEY = "your-actual-tavily-api-key"

# PostgreSQL Configuration
PG_USER = "your_pg_user"
PG_PASSWORD = "your_pg_password"
PG_HOST = "your_pg_host"
PG_PORT = "5432"
PG_DATABASE = "your_database_name"
```

**⚠️ Important Security Notes:**
- Never commit `secrets.toml` to version control (it's in `.gitignore`)
- Keep your API keys private
- Don't share screenshots containing your secrets

### Step 5: Run the Application

Start the Streamlit app:

```bash
streamlit run streamlit_app.py
```

The application will automatically open in your default browser at `http://localhost:8501`

## 🎯 Usage Guide

### First-Time Usage

1. **Upload Documents**:
   - Click the file upload area
   - Select PDF, CSV, or TXT files
   - You can upload multiple files at once

2. **Initialize Agent**:
   - Click "Process Files & Initialize Agent"
   - Wait for document processing (may take 30-60 seconds)
   - You'll see a success message when ready

3. **Start Chatting**:
   - Type your question in the chat input
   - Press Enter to submit
   - View responses with source indicators

### Understanding Sources

The chatbot will indicate where answers come from:

- **📄 Green Badge (From Documents)**: Answer found in your uploaded documents
- **🌐 Blue Badge (From Web Search)**: Documents didn't contain the answer, so it searched the web

### Managing Your Session

- **Clear Chat**: Click "Clear Chat History" in the sidebar
- **View Files**: Expand "View Files" in sidebar to see loaded documents
- **Change Collection**: Update collection name in sidebar (requires re-initialization)

## 🔧 Troubleshooting

### Issue: "API keys not found in secrets.toml"

**Solution:**
- Verify `.streamlit/secrets.toml` exists
- Check file has correct formatting (valid TOML syntax)
- Alternatively, enter keys in the UI when prompted

### Issue: "Error connecting to PostgreSQL"

**Solutions:**
- Verify PostgreSQL credentials are correct
- Check if database is running and accessible
- Ensure pgvector extension is installed:
  ```sql
  SELECT * FROM pg_extension WHERE extname = 'vector';
  ```
- For Neon: Verify connection string includes `?ssl=require`

### Issue: "Module not found" errors

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Issue: "Unsupported file type"

**Solution:**
- Only PDF, CSV, and TXT files are supported
- Check file extension is correct (lowercase)
- Verify files are not corrupted

### Issue: Agent initialization fails

**Common causes:**
- Invalid API keys - double-check they're correct
- Database connection issues - verify PostgreSQL is accessible
- Insufficient permissions - ensure database user has CREATE privileges
- Network issues - check internet connectivity for API calls

**Debug steps:**
1. Enable error details expander in the app
2. Check the full error message
3. Verify each credential individually
4. Try with a smaller file first

### Issue: Slow performance

**Solutions:**
- Reduce number of documents
- Use smaller files
- Check database connection latency
- Verify internet speed for API calls

## 📊 Configuration Options

### Adjusting Chunk Parameters

Edit `streamlit_app.py` to modify document chunking:

```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Increase for more context per chunk
    chunk_overlap=200      # Increase for better continuity
)
```

### Changing Retrieval Count

Modify the number of chunks retrieved:

```python
retriever = vector_store.as_retriever(search_kwargs={"k": 3})  # Change 3 to desired number
```

### Adjusting Model Temperature

Control response randomness:

```python
llm = GoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,  # 0 = deterministic, 1 = creative
    google_api_key=gemini_key
)
```

## 🔄 Updating the Application

To update dependencies:

```bash
pip install -r requirements.txt --upgrade
```

To get latest changes from the repository:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

## 📁 Project Structure Explained

```
day012_multi_file_rag/
├── streamlit_app.py              # Main application code
├── MultiFileRagChatBot.ipynb    # Original notebook (reference)
├── requirements.txt              # Python dependencies
├── README.md                     # User documentation
├── SETUP_INSTRUCTIONS.md         # This file
├── .gitignore                    # Git ignore rules
└── .streamlit/
    ├── config.toml               # Streamlit UI configuration
    ├── secrets.toml              # Your API keys (DO NOT COMMIT)
    └── secrets.toml.example      # Template for secrets
```

## 🎓 Learning Resources

### Understanding RAG (Retrieval-Augmented Generation)

- [LangChain RAG Tutorial](https://python.langchain.com/docs/use_cases/question_answering/)
- [Vector Databases Explained](https://www.pinecone.io/learn/vector-database/)

### Working with pgvector

- [pgvector GitHub](https://github.com/pgvector/pgvector)
- [PostgreSQL Vector Operations](https://www.postgresql.org/docs/current/)

### Streamlit Best Practices

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Session State Guide](https://docs.streamlit.io/library/advanced-features/session-state)

## 🤝 Getting Help

If you encounter issues:

1. **Check Error Messages**: Expand error details in the app
2. **Review Logs**: Look at terminal output where Streamlit is running
3. **Verify Setup**: Go through this guide step-by-step
4. **Test Components**: Try each API key/connection individually
5. **Simplify**: Start with a single small file

## 📝 Common Workflows

### Workflow 1: Research Paper Analysis

```
1. Upload: Multiple PDF research papers
2. Ask: "What are the main findings across all papers?"
3. Ask: "Compare the methodologies used"
4. Ask: "What are the key conclusions?"
```

### Workflow 2: Document Q&A

```
1. Upload: Company documentation, manuals
2. Ask: "How do I configure X?"
3. Ask: "What are the prerequisites for Y?"
4. Ask: "Explain the process for Z"
```

### Workflow 3: Data Analysis

```
1. Upload: CSV files with data
2. Ask: "Summarize the data trends"
3. Ask: "What patterns do you see?"
4. Ask: "Compare values between categories"
```

## 🚀 Next Steps

After successful setup:

1. **Test with Sample Documents**: Try with a few small files first
2. **Explore Features**: Test both document-based and web-search responses
3. **Customize**: Adjust parameters for your use case
4. **Scale Up**: Gradually add more documents
5. **Integrate**: Consider integrating with your workflows

## 📞 Support

For technical issues with:
- **Streamlit**: [Streamlit Community](https://discuss.streamlit.io/)
- **LangChain**: [LangChain Documentation](https://python.langchain.com/)
- **Google Gemini**: [Google AI Studio](https://aistudio.google.com/)
- **PostgreSQL/Neon**: [Neon Documentation](https://neon.tech/docs)

---

**Happy Document Chatting! 📚🤖**

