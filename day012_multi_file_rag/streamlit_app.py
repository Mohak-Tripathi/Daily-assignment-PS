import streamlit as st
import os
import tempfile
from langchain_community.document_loaders import CSVLoader, PyMuPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, GoogleGenerativeAI
from langchain_postgres import PGVector
from langchain_tavily import TavilySearch
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from urllib.parse import quote_plus
import uuid

# Page config
st.set_page_config(
    page_title="Multi-File RAG ChatBot",
    page_icon="📚",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .stExpander {
        border: 1px solid #f0f2f6;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #e3f2fd;
    }
    .assistant-message {
        background-color: #f5f5f5;
    }
    .source-badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.75rem;
        font-weight: bold;
        margin-top: 0.5rem;
    }
    .doc-source {
        background-color: #4caf50;
        color: white;
    }
    .web-source {
        background-color: #2196f3;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = None
if 'agent_initialized' not in st.session_state:
    st.session_state.agent_initialized = False
if 'uploaded_file_names' not in st.session_state:
    st.session_state.uploaded_file_names = []

# Get API keys from secrets with fallback to UI input
gemini_api_key = None
tavily_api_key = None
pg_connection_string = None

try:
    gemini_api_key = st.secrets["GEMINI_API_KEY"]
    tavily_api_key = st.secrets["TAVILY_API_KEY"]
    
    # Build PostgreSQL connection string from secrets
    pg_user = st.secrets["PG_USER"]
    pg_password = quote_plus(st.secrets["PG_PASSWORD"])
    pg_host = st.secrets["PG_HOST"]
    pg_port = st.secrets["PG_PORT"]
    pg_db = st.secrets["PG_DATABASE"]
    pg_connection_string = f"postgresql+psycopg://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}?sslmode=require"
    
    st.success("✅ Configuration loaded from secrets.toml")
except KeyError:
    st.warning("⚠️ Configuration not found in secrets.toml. Please enter them below:")
    
    with st.expander("🔑 API Configuration", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            gemini_api_key = st.text_input("Gemini API Key", type="password")
            tavily_api_key = st.text_input("Tavily API Key", type="password")
        
        with col2:
            st.markdown("**PostgreSQL Configuration**")
            pg_user = st.text_input("PG User", value="neondb_owner")
            pg_password = st.text_input("PG Password", type="password")
            pg_host = st.text_input("PG Host")
            pg_port = st.text_input("PG Port", value="5432")
            pg_db = st.text_input("PG Database", value="neondb")
            
            if pg_password and pg_host:
                pg_connection_string = f"postgresql+psycopg://{pg_user}:{quote_plus(pg_password)}@{pg_host}:{pg_port}/{pg_db}?sslmode=require"

# Sidebar for configuration
st.sidebar.title("⚙️ Configuration")

# Collection name input
collection_name = st.sidebar.text_input(
    "Collection Name",
    value="multi_file_rag_docs",
    help="Name for the vector store collection in PostgreSQL"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 System Status")

if st.session_state.agent_initialized:
    st.sidebar.success("✅ Agent Ready")
    if st.session_state.uploaded_file_names:
        st.sidebar.info(f"📁 {len(st.session_state.uploaded_file_names)} file(s) loaded")
        with st.sidebar.expander("View Files"):
            for fname in st.session_state.uploaded_file_names:
                st.sidebar.text(f"• {fname}")
else:
    st.sidebar.warning("⏳ Upload files to initialize")

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info("""
This app uses a multi-file RAG system with:
- 📄 **Document Support**: PDF, CSV, TXT
- 🧠 **Smart Retrieval**: PostgreSQL + pgvector
- 🤖 **AI Models**: Google Gemini
- 🔍 **Fallback**: Web search via Tavily
""")

# Clear chat button
if st.sidebar.button("🗑️ Clear Chat History"):
    st.session_state.chat_history = []
    st.rerun()

# Helper functions
def load_documents(uploaded_files):
    """Load documents from uploaded files"""
    docs = []
    
    for uploaded_file in uploaded_files:
        ext = uploaded_file.name.split(".")[-1].lower()
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
        
        try:
            if ext == "pdf":
                loader = PyMuPDFLoader(tmp_path)
            elif ext == "csv":
                loader = CSVLoader(tmp_path)
            elif ext == "txt":
                loader = TextLoader(tmp_path)
            else:
                st.warning(f"⚠️ Unsupported file type: {uploaded_file.name}")
                continue
            
            file_docs = loader.load()
            docs.extend(file_docs)
        finally:
            # Clean up temp file
            os.unlink(tmp_path)
    
    return docs

def format_chunks(relevant_chunks):
    """Format retrieved chunks into a single string"""
    return "\n\n".join(chunk.page_content for chunk in relevant_chunks)

def initialize_agent(documents, gemini_key, tavily_key, connection_string, collection):
    """Initialize the RAG agent with vector store"""
    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(documents)
    
    # Initialize embedding model
    embedding_model = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=gemini_key
    )
    
    # Create vector store
    vector_store = PGVector.from_documents(
        documents=chunks,
        embedding=embedding_model,
        connection=connection_string,
        collection_name=collection,
    )
    
    # Initialize LLM and tools
    llm = GoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        google_api_key=gemini_key
    )
    
    search_tool = TavilySearch(
        max_results=3,
        topic="general",
        tavily_api_key=tavily_key
    )
    
    # Create retriever
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    
    # Define prompts
    answer_prompt = PromptTemplate.from_template("""
You are a helpful assistant. Answer using ONLY the context below:

Content:
{context}

Question:
{question}

If the context is enough, answer accurately.
If not, respond only and exactly with this tag: [NEED_WEB_SEARCH], do not
provide any extra stuff just return the tag if the context is not enough
for answering the question.
""")
    
    web_prompt = PromptTemplate.from_template("""
User Question: {question}

Web search results:
{web_results}

Based on the web results, provide a complete and helpful answer to the question asked by the user.
Provide citations as well, if available.
""")
    
    # Create chains
    determination_chain = (
        {
            "context": retriever | format_chunks,
            "question": RunnablePassthrough()
        }
        | answer_prompt
        | llm
        | StrOutputParser()
    )
    
    web_search_chain = (
        {
            "question": RunnablePassthrough(),
            "web_results": lambda x: search_tool.invoke({"query": x})
        }
        | web_prompt
        | llm
        | StrOutputParser()
    )
    
    return determination_chain, web_search_chain, vector_store, len(chunks)

def get_agent_response(question, determination_chain, web_search_chain):
    """Get response from agent, with fallback to web search"""
    response = determination_chain.invoke(question)
    
    if "[NEED_WEB_SEARCH]" in response:
        return web_search_chain.invoke(question), "web"
    else:
        return response, "documents"

# Main UI
st.title("📚 Multi-File RAG ChatBot")
st.markdown("Upload documents and chat with an AI that understands your files!")

# File upload section
with st.container():
    st.markdown("### 📤 Upload Documents")
    uploaded_files = st.file_uploader(
        "Choose files (PDF, CSV, TXT)",
        type=["pdf", "csv", "txt"],
        accept_multiple_files=True,
        help="Upload one or more documents to create a knowledge base"
    )
    
    if uploaded_files and not st.session_state.agent_initialized:
        if st.button("🚀 Process Files & Initialize Agent", type="primary"):
            if not gemini_api_key or not tavily_api_key or not pg_connection_string:
                st.error("❌ Please provide all required API keys and database configuration!")
            else:
                with st.spinner("📊 Processing documents and creating embeddings..."):
                    try:
                        # Load documents
                        documents = load_documents(uploaded_files)
                        
                        if not documents:
                            st.error("❌ No documents could be loaded!")
                        else:
                            # Initialize agent
                            determination_chain, web_search_chain, vector_store, num_chunks = initialize_agent(
                                documents,
                                gemini_api_key,
                                tavily_api_key,
                                pg_connection_string,
                                collection_name
                            )
                            
                            # Store in session state
                            st.session_state.determination_chain = determination_chain
                            st.session_state.web_search_chain = web_search_chain
                            st.session_state.vector_store = vector_store
                            st.session_state.agent_initialized = True
                            st.session_state.uploaded_file_names = [f.name for f in uploaded_files]
                            
                            st.success(f"✅ Successfully processed {len(documents)} documents into {num_chunks} chunks!")
                            st.rerun()
                    
                    except Exception as e:
                        st.error(f"❌ Error initializing agent: {str(e)}")
                        with st.expander("🔍 Error Details"):
                            st.exception(e)

# Chat interface
if st.session_state.agent_initialized:
    st.markdown("---")
    st.markdown("### 💬 Chat with Your Documents")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>🙋 You:</strong><br>
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                source_badge = f'<span class="source-badge {"doc-source" if message["source"] == "documents" else "web-source"}">{"📄 From Documents" if message["source"] == "documents" else "🌐 From Web Search"}</span>'
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <strong>🤖 Assistant:</strong><br>
                    {message["content"]}<br>
                    {source_badge}
                </div>
                """, unsafe_allow_html=True)
    
    # Chat input
    user_question = st.chat_input("Ask a question about your documents...")
    
    if user_question:
        # Add user message to history
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_question
        })
        
        # Get agent response
        with st.spinner("🤔 Thinking..."):
            try:
                response, source = get_agent_response(
                    user_question,
                    st.session_state.determination_chain,
                    st.session_state.web_search_chain
                )
                
                # Add assistant message to history
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response,
                    "source": source
                })
                
                st.rerun()
            
            except Exception as e:
                st.error(f"❌ Error getting response: {str(e)}")
                with st.expander("🔍 Error Details"):
                    st.exception(e)

else:
    st.info("👆 Please upload files and initialize the agent to start chatting!")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Powered by LangChain, Google Gemini & PostgreSQL pgvector | Built with Streamlit"
    "</div>",
    unsafe_allow_html=True
)

