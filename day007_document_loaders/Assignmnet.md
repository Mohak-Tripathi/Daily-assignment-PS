# Document Insights App

## 📘 Assignment: Document Insights App Using LangChain

### 🎯 Objective

Build a **simple, non-chatbot app** that allows users to:

- Load documents from different sources
- Use an LLM to **summarize** or **answer questions** based on the content
- View metadata
- Get a session summary of all loaded documents

## ✅ Core Features

The app should offer the following functionality:

- **Load Documents** from:
    - Local files: `.txt`, `.csv`, `.pdf`
    - Web URLs
    - Wikipedia articles
- **Display Metadata** for each loaded document (e.g., file name, source URL, title)
- **Use LLM** to:
    - Summarize the document
    - Answer user-provided questions based on document content
- **Session Summary** at the end:
    - List of documents loaded
    - Source and loader used for each

## 🧑💻 Implementation Instructions

- Use **LangChain’s document loaders**:
    - `TextLoader`, `CSVLoader`, `PyPDFLoader`, `WebBaseLoader`, `WikipediaLoader`*(from `langchain_community.document_loaders`)*
- Use an **LLM from LangChain’s integrations** (e.g., Google Gemini via `ChatGoogleGenerativeAI`, or OpenAI/GPT-4)
- App Format:
    - **CLI (terminal-based)** or **basic UI** is sufficient
    - No chatbot or dialogue memory needed
- Keep documents in memory during the session to allow multiple operations on them
- Handle exceptions gracefully (e.g., file not found, invalid URL)