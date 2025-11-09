import streamlit as st
import os
from typing import TypedDict
from langgraph.graph import START, END, StateGraph
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import sys
from io import StringIO, BytesIO
import contextlib

# Page config
st.set_page_config(
    page_title="LangGraph DAG Workflow",
    page_icon="🔄",
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
    .workflow-step {
        padding: 15px;
        background-color: #f0f2f6;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Define the state
class State(TypedDict):
    question: str
    search: str
    summerize: str

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
    os.environ["GOOGLE_API_KEY"] = gemini_api_key
else:
    st.error("Please provide your Gemini API key!")
    st.stop()

# Sidebar for configuration
st.sidebar.title("⚙️ Configuration")
model_name = st.sidebar.selectbox(
    "Model",
    ["gemini-2.0-flash-exp", "gemini-1.5-flash", "gemini-1.5-pro"],
    help="Select the Gemini model to use"
)
show_graph = st.sidebar.toggle("Show Graph Visualization", value=True, help="Display the workflow graph")
st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info("""
This app uses LangGraph with a DAG workflow:
- 📝 **Get Question**: Normalizes the input question
- 🔍 **Search**: Researches the topic using LLM
- 📊 **Summarize**: Creates bullet point summary
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

# Initialize LangGraph workflow
@st.cache_resource
def initialize_graph(_api_key, model):
    """Initialize the LangGraph workflow"""
    
    # Create LLM
    llm = ChatGoogleGenerativeAI(model=model, google_api_key=_api_key)
    
    # Define the functions
    def get_question(state: State) -> dict:
        """Normalize the question"""
        q = state["question"].strip()
        return {"question": q}
    
    # Build search chain
    search_prompt = PromptTemplate.from_template(
        "Research the user's question and provide detailed research on this topic.\n\n"
        "Question: {q}"
    )
    search_chain = search_prompt | llm | StrOutputParser()
    
    def search(state: State) -> dict:
        """Search and research the question"""
        q = state["question"]
        search_result = search_chain.invoke({"q": q})
        return {"search": search_result}
    
    # Build summary chain
    summary_prompt = PromptTemplate.from_template("""
        Provide 3-5 bullet points summary on this topic.\n\n
        Search Result: {user_search}
    """)
    summary_chain = summary_prompt | llm | StrOutputParser()
    
    def summerize(state: State) -> dict:
        """Summarize the search results"""
        user_search = state["search"]
        user_search_chain = summary_chain.invoke({"user_search": user_search})
        return {"summerize": user_search_chain}
    
    # Build the graph
    builder = StateGraph(State)
    builder.add_node("get_question", get_question)
    builder.add_node("search", search)
    builder.add_node("summerize", summerize)
    
    builder.add_edge(START, "get_question")
    builder.add_edge("get_question", "search")
    builder.add_edge("search", "summerize")
    builder.add_edge("summerize", END)
    
    graph = builder.compile()
    
    return graph

# Function to get graph visualization
def get_graph_visualization(graph):
    """Get the Mermaid graph visualization as PNG"""
    try:
        png_data = graph.get_graph().draw_mermaid_png()
        return png_data
    except Exception as e:
        st.warning(f"Could not generate graph visualization: {str(e)}")
        return None

# Main UI
st.title("🔄 LangGraph DAG Workflow")
st.markdown("Research and summarize any topic using a directed acyclic graph (DAG) workflow powered by LangGraph.")

# Question input
question = st.text_area(
    "Enter your question:",
    value="What is LangGraph?",
    height=100,
    help="Enter any question you want researched and summarized"
)

# Generate button
if st.button("🚀 Execute Workflow", type="primary"):
    if not question.strip():
        st.error("Please enter a question!")
    else:
        with st.spinner("🔄 Executing LangGraph workflow..."):
            try:
                # Initialize graph
                graph = initialize_graph(gemini_api_key, model_name)
                
                # Show graph visualization if enabled
                if show_graph:
                    with st.expander("📊 Workflow Graph", expanded=False):
                        graph_png = get_graph_visualization(graph)
                        if graph_png:
                            st.image(graph_png, caption="LangGraph DAG Workflow")
                
                # Execute the workflow
                result = graph.invoke({"question": question})
                
                # Display results
                st.success("✅ Workflow execution completed!")
                
                # Create tabs for organized output
                tab1, tab2 = st.tabs(["📝 Summary", "🔍 Detailed Steps"])
                
                with tab1:
                    st.markdown("### ✨ Summary")
                    st.markdown(f"**Question:** {question}")
                    st.markdown("---")
                    
                    # Display the summary
                    summary_content = result.get("summerize", "No summary generated")
                    st.markdown(summary_content)
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Summary",
                        data=summary_content,
                        file_name="langgraph_summary.txt",
                        mime="text/plain"
                    )
                
                with tab2:
                    st.markdown("### 🔍 Workflow Execution Steps")
                    
                    # Step 1: Get Question
                    with st.expander("📝 Step 1: Get Question (Normalization)", expanded=True):
                        normalized_q = result.get("question", question)
                        st.write(f"**Normalized Question:** {normalized_q}")
                    
                    # Step 2: Search
                    with st.expander("🔍 Step 2: Search (Research)", expanded=True):
                        search_result = result.get("search", "No search results")
                        st.write(search_result)
                    
                    # Step 3: Summarize
                    with st.expander("📊 Step 3: Summarize (Bullet Points)", expanded=True):
                        summary_result = result.get("summerize", "No summary generated")
                        st.write(summary_result)
                
            except Exception as e:
                st.error(f"❌ Error executing workflow: {str(e)}")
                with st.expander("🔍 Error Details"):
                    st.exception(e)

# Example questions
with st.expander("💡 Example Questions"):
    example_questions = [
        "What is LangGraph?",
        "Explain Artificial General Intelligence",
        "What are the benefits of using directed acyclic graphs in workflows?",
        "How does state management work in LangGraph?",
        "What is the difference between LangChain and LangGraph?"
    ]
    
    st.markdown("Try these example questions:")
    for i, eq in enumerate(example_questions, 1):
        st.markdown(f"{i}. {eq}")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Powered by LangGraph & Google Gemini | Built with Streamlit"
    "</div>",
    unsafe_allow_html=True
)

