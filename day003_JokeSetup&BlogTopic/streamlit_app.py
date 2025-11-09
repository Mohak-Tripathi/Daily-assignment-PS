import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough, RunnableParallel
from operator import itemgetter

# Page config
st.set_page_config(
    page_title="Blog Topic Generator",
    page_icon="📝",
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
    </style>
""", unsafe_allow_html=True)

# Get API key from secrets with fallback to UI input
gemini_api_key = None

try:
    gemini_api_key = st.secrets["GOOGLE_API_KEY"]
    st.success("✅ API key loaded from secrets.toml")
except KeyError:
    st.warning("⚠️ API key not found in secrets.toml. Please enter it below:")
    gemini_api_key = st.text_input("Google Gemini API Key", type="password")

# Set environment variable if key is available
if gemini_api_key:
    os.environ["GOOGLE_API_KEY"] = gemini_api_key
else:
    st.error("Please provide the API key!")
    st.stop()

# Sidebar for configuration
st.sidebar.title("⚙️ Configuration")
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.4, step=0.1, 
                                help="Controls randomness in output")
st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info("""
This app generates blog content in 3 steps:
- 📌 **Topic**: Generates a niche blog topic
- ✍️ **Title**: Creates a catchy title
- 📄 **Summary**: Writes a comprehensive summary
""")

# Initialize LLM
@st.cache_resource
def initialize_llm(temperature=0.4):
    """Initialize the LLM with caching"""
    return ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=temperature)

# Initialize chains
@st.cache_resource
def initialize_chains(_llm):
    """Initialize all chains for the blog generation pipeline"""
    
    # Step 1: Topic generator
    topic_prompt = PromptTemplate.from_template(
        "Given the broad domain: {domain}\n"
        "Propose one specific, fresh **niche blog topic** (max 12 words). Return only the topic text."
    )
    topic_chain = topic_prompt | _llm | StrOutputParser()
    
    # Bridge: str -> {"topic": str}
    to_topic_dict = RunnableLambda(lambda s: {"topic": s})
    
    # Step 2: Title generator
    title_prompt = PromptTemplate.from_template(
        "Given this blog topic: {topic}\n"
        "Write a catchy blog **title** (≤ 12 words). Return only the title."
    )
    title_chain = title_prompt | _llm | StrOutputParser()
    
    # Bridge: str -> {"title": str}
    to_title_dict = RunnableLambda(lambda s: {"title": s})
    
    # Step 3: Summary generator
    summary_prompt = PromptTemplate.from_template(
        "Based on this blog title: {title}\n"
        "Write a single-paragraph blog summary (4–6 sentences). Return only the paragraph."
    )
    summary_chain = summary_prompt | _llm | StrOutputParser()
    
    # Compose full pipeline
    full_pipeline = RunnableParallel({
        "domain": RunnablePassthrough() | RunnableLambda(itemgetter("domain")),
        "topic": topic_chain,  # expects {"domain"}
        "title": topic_chain | to_topic_dict | title_chain,
        "summary": topic_chain | to_topic_dict | title_chain | to_title_dict | summary_chain,
    })
    
    return full_pipeline

# Helper function to format markdown
def to_markdown(res: dict) -> str:
    """Convert result dictionary to markdown format"""
    return f"""# Blog Draft

**Domain:** {res['domain']}

## {res['title']}

### Topic
{res['topic']}

### Summary
{res['summary']}
"""

# Main UI
st.title("📝 Blog Topic → Title → Summary Generator")
st.markdown("Generate a complete blog outline from a domain using AI-powered chains.")

# Domain input
domain = st.text_input(
    "Enter your domain:",
    value="Productivity",
    help="Enter a broad domain (e.g., Productivity, Technology, Health, etc.)"
)

# Generate button
if st.button("🚀 Generate Blog Content", type="primary"):
    if not domain.strip():
        st.error("Please enter a domain!")
    else:
        with st.spinner("🔄 Generating blog content..."):
            try:
                # Initialize LLM and chains
                llm = initialize_llm(temperature=temperature)
                pipeline = initialize_chains(llm)
                
                # Run the pipeline
                result = pipeline.invoke({"domain": domain})
                
                # Display results
                st.success("✅ Blog content generation completed!")
                
                # Create tabs for organized output
                tab1, tab2, tab3 = st.tabs(["📄 Formatted Output", "📊 Individual Components", "📝 Markdown View"])
                
                with tab1:
                    st.markdown("### ✨ Complete Blog Draft")
                    st.markdown(to_markdown(result))
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Blog Draft",
                        data=to_markdown(result),
                        file_name="blog_draft.md",
                        mime="text/markdown"
                    )
                
                with tab2:
                    st.markdown("### 📊 Step-by-Step Results")
                    
                    with st.expander("📌 Step 1: Domain", expanded=True):
                        st.info(f"**Input Domain:** {result['domain']}")
                    
                    with st.expander("📌 Step 2: Generated Topic", expanded=True):
                        st.write(result['topic'])
                    
                    with st.expander("✍️ Step 3: Generated Title", expanded=True):
                        st.write(result['title'])
                    
                    with st.expander("📄 Step 4: Generated Summary", expanded=True):
                        st.write(result['summary'])
                
                with tab3:
                    st.markdown("### 📝 Raw Markdown")
                    st.code(to_markdown(result), language="markdown")
                    
                    # Copy to clipboard button
                    st.code(to_markdown(result), language="markdown")
                
            except Exception as e:
                st.error(f"❌ Error generating content: {str(e)}")
                with st.expander("🔍 Error Details"):
                    st.exception(e)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Powered by LangChain & Gemini | Built with Streamlit"
    "</div>",
    unsafe_allow_html=True
)
