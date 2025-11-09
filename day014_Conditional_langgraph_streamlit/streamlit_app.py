import streamlit as st
import os
from langgraph.graph import START, END, StateGraph
from typing import TypedDict, Literal, Dict, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
import re
import sys
from io import StringIO
import contextlib

# Page config
st.set_page_config(
    page_title="LangGraph Conditional Routing",
    page_icon="🔀",
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
    .path-badge {
        padding: 5px 10px;
        border-radius: 5px;
        font-weight: bold;
        display: inline-block;
        margin: 5px 0;
    }
    .kb-path {
        background-color: #d4edda;
        color: #155724;
    }
    .llm-path {
        background-color: #d1ecf1;
        color: #0c5460;
    }
    </style>
""", unsafe_allow_html=True)

# Get API key from secrets with fallback to UI input
gemini_api_key = None

try:
    gemini_api_key = st.secrets["GEMINI_API_KEY"]
    st.success("✅ API key loaded from secrets.toml")
except KeyError:
    st.warning("⚠️ API key not found in secrets.toml. Please enter it below:")
    gemini_api_key = st.text_input("Gemini API Key", type="password")

# Set environment variable if key is available
if gemini_api_key:
    os.environ["GEMINI_API_KEY"] = gemini_api_key
else:
    st.error("Please provide Gemini API key!")
    st.stop()

# Initialize Knowledge Base
knowledge_base: Dict[str, str] = {
    "ada lovelace": "Ada Lovelace (1815–1852) is considered the first computer programmer.",
    "python": "Python is a high-level programming language known for readability and broad library support.",
    "langchain": "LangChain is a Python framework for developing applications powered by large language models.",
    "langgraph": "LangGraph is a library for building stateful, multi-agent applications with LLMs using graph-based workflows.",
    "artificial intelligence": "Artificial Intelligence (AI) is the simulation of human intelligence by machines, especially computer systems.",
}

# Sidebar for configuration
st.sidebar.title("⚙️ Configuration")

# Knowledge base editor
st.sidebar.markdown("### 📚 Knowledge Base")
with st.sidebar.expander("View/Edit Knowledge Base", expanded=False):
    st.markdown("Current entries:")
    for key, value in knowledge_base.items():
        st.markdown(f"- **{key}**: {value[:50]}...")

verbose_mode = st.sidebar.toggle("Verbose Mode", value=False, help="Show detailed execution logs")
show_graph = st.sidebar.toggle("Show Graph Visualization", value=True, help="Display the workflow graph")

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info("""
This app uses LangGraph with conditional routing:
- 📚 **Knowledge Base Path**: Answers from predefined facts
- 🤖 **LLM Path**: Uses Gemini for dynamic responses

The graph automatically routes questions based on content!
""")

# Helper function to capture stdout
@contextlib.contextmanager
def capture_stdout():
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()
    try:
        yield captured_output
    finally:
        sys.stdout = old_stdout

# Define State
class State(TypedDict):
    question: str
    path: Literal["knowledge_base", "llm"]
    interim: str
    final_answer: str

# Helper functions
def _canonicalise(text: str) -> str:
    """Canonicalize text for matching"""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def _kb_lookup(q: str) -> Optional[str]:
    """Look up question in knowledge base"""
    cq = _canonicalise(q)
    for key, val in knowledge_base.items():
        if key in cq:  # substring match
            return val
    return None

# Node functions
def get_question(state: State) -> dict:
    """Process and clean the input question"""
    if verbose_mode:
        st.write("🔍 Processing question...")
    return {"question": state["question"].strip()}

def decide_path(state: State) -> dict:
    """Decide which path to take based on knowledge base lookup"""
    path = "knowledge_base" if _kb_lookup(state["question"]) else "llm"
    if verbose_mode:
        st.write(f"🔀 Routing to: **{path}**")
    return {"path": path}

def answer_from_knowledge_base(state: State) -> dict:
    """Get answer from knowledge base"""
    fact = _kb_lookup(state["question"]) or ""
    if verbose_mode:
        st.write("📚 Retrieving from knowledge base...")
    return {"interim": fact}

def answer_from_llm(state: State, llm) -> dict:
    """Get answer from LLM"""
    prompt = (
        "Answer the user's question clearly and concisely.\n\n"
        f"Question: {state['question']}\n"
    )
    if verbose_mode:
        st.write("🤖 Querying Gemini LLM...")
    resp = llm.invoke(prompt)
    text = getattr(resp, "content", str(resp))
    return {"interim": text}

def get_answer(state: State) -> dict:
    """Format the final answer with metadata"""
    tag = "[knowledge_base]" if state["path"] == "knowledge_base" else "[llm]"
    final = f"{tag} Q: {state['question']}\nA: {state['interim']}"
    return {"final_answer": final}

def initialize_graph(llm, verbose=False):
    """Initialize the LangGraph workflow"""
    
    # Create wrapper functions with LLM
    def answer_from_llm_wrapper(state: State) -> dict:
        return answer_from_llm(state, llm)
    
    # Build the graph
    builder = StateGraph(State)
    
    builder.add_node("get_question", get_question)
    builder.add_node("decide_path", decide_path)
    builder.add_node("answer_from_knowledge_base", answer_from_knowledge_base)
    builder.add_node("answer_from_llm", answer_from_llm_wrapper)
    builder.add_node("get_answer", get_answer)
    
    builder.add_edge(START, "get_question")
    builder.add_edge("get_question", "decide_path")
    
    # Conditional branch based on state["path"]
    builder.add_conditional_edges(
        "decide_path",
        lambda s: s["path"],
        {
            "knowledge_base": "answer_from_knowledge_base",
            "llm": "answer_from_llm",
        },
    )
    
    builder.add_edge("answer_from_knowledge_base", "get_answer")
    builder.add_edge("answer_from_llm", "get_answer")
    builder.add_edge("get_answer", END)
    
    return builder.compile()

# Main UI
st.title("🔀 LangGraph Conditional Routing")
st.markdown("Ask questions and watch the graph automatically route between Knowledge Base and LLM!")

# Question input
question = st.text_area(
    "Enter your question:",
    value="Who is Ada Lovelace?",
    height=100,
    help="Try questions about Ada Lovelace, Python, LangChain, or anything else!"
)

# Example questions
st.markdown("**💡 Try these examples:**")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📚 Ada Lovelace"):
        question = "Who is Ada Lovelace?"
        st.rerun()
with col2:
    if st.button("🐍 Python"):
        question = "What is Python?"
        st.rerun()
with col3:
    if st.button("🤔 General Question"):
        question = "What is the capital of France?"
        st.rerun()

# Process button
if st.button("🚀 Process Question", type="primary"):
    if not question.strip():
        st.error("Please enter a question!")
    else:
        with st.spinner("🔄 Processing your question..."):
            try:
                # Initialize LLM
                llm = ChatGoogleGenerativeAI(
                    model="gemini-2.0-flash-exp",
                    google_api_key=gemini_api_key
                )
                
                # Initialize graph
                graph = initialize_graph(llm, verbose=verbose_mode)
                
                # Execute graph
                if verbose_mode:
                    st.markdown("### 🔍 Execution Trace")
                    with st.container():
                        result = graph.invoke({"question": question})
                else:
                    result = graph.invoke({"question": question})
                
                # Display results
                st.success("✅ Question processed successfully!")
                
                # Create tabs for organized output
                tab1, tab2, tab3 = st.tabs(["📝 Result", "🔍 Process Details", "📊 Graph Visualization"])
                
                with tab1:
                    st.markdown("### ✨ Answer")
                    
                    # Display path badge
                    path = result.get("path", "unknown")
                    path_class = "kb-path" if path == "knowledge_base" else "llm-path"
                    path_emoji = "📚" if path == "knowledge_base" else "🤖"
                    
                    st.markdown(
                        f'<div class="path-badge {path_class}">{path_emoji} Source: {path.replace("_", " ").title()}</div>',
                        unsafe_allow_html=True
                    )
                    
                    st.markdown("---")
                    
                    # Display question and answer
                    st.markdown(f"**Question:** {result.get('question', question)}")
                    st.markdown(f"**Answer:** {result.get('interim', 'No answer available')}")
                    
                    # Download button
                    download_text = f"Question: {result.get('question', question)}\n\nAnswer: {result.get('interim', 'No answer available')}\n\nSource: {path}"
                    st.download_button(
                        label="📥 Download Answer",
                        data=download_text,
                        file_name="langgraph_answer.txt",
                        mime="text/plain"
                    )
                
                with tab2:
                    st.markdown("### 🔍 Step-by-Step Process")
                    
                    # Step 1: Question Processing
                    with st.expander("🔍 Step 1: Question Processing", expanded=True):
                        st.write(f"**Original Question:** {question}")
                        st.write(f"**Processed Question:** {result.get('question', question)}")
                    
                    # Step 2: Path Decision
                    with st.expander("🔀 Step 2: Path Decision", expanded=True):
                        path = result.get("path", "unknown")
                        st.write(f"**Selected Path:** {path}")
                        
                        # Show why this path was chosen
                        if path == "knowledge_base":
                            kb_match = _kb_lookup(question)
                            st.success("✅ Found match in knowledge base!")
                            st.write(f"**Matched Entry:** {kb_match}")
                        else:
                            st.info("ℹ️ No knowledge base match found, routing to LLM")
                    
                    # Step 3: Answer Generation
                    with st.expander("💬 Step 3: Answer Generation", expanded=True):
                        if path == "knowledge_base":
                            st.write("**Method:** Retrieved from Knowledge Base")
                        else:
                            st.write("**Method:** Generated by Gemini LLM")
                        st.write(f"**Answer:** {result.get('interim', 'No answer')}")
                    
                    # Step 4: Final Formatting
                    with st.expander("✨ Step 4: Final Formatting", expanded=True):
                        st.write("**Formatted Output:**")
                        st.code(result.get('final_answer', 'No final answer'), language="text")
                
                with tab3:
                    if show_graph:
                        st.markdown("### 📊 Workflow Graph")
                        try:
                            # Try to display the graph
                            graph_png = graph.get_graph().draw_mermaid_png()
                            st.image(graph_png, caption="LangGraph Conditional Workflow")
                        except Exception as e:
                            st.warning("Graph visualization requires additional dependencies.")
                            st.markdown("""
                            **Workflow Structure:**
                            ```
                            START → get_question → decide_path
                                                        ↓
                                        ┌───────────────┴───────────────┐
                                        ↓                               ↓
                            answer_from_knowledge_base    answer_from_llm
                                        ↓                               ↓
                                        └───────────────┬───────────────┘
                                                        ↓
                                                  get_answer → END
                            ```
                            """)
                    else:
                        st.info("Graph visualization is disabled. Enable it in the sidebar.")
                
            except Exception as e:
                st.error(f"❌ Error processing question: {str(e)}")
                with st.expander("🔍 Error Details"):
                    st.exception(e)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Powered by LangGraph & Gemini | Built with Streamlit"
    "</div>",
    unsafe_allow_html=True
)

