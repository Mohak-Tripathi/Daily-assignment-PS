import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_tavily import TavilySearch
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel

# Page config
st.set_page_config(
    page_title="Social Media Content Generator",
    page_icon="📱",
    layout="wide"
)

# Get API keys from secrets with fallback to UI input
google_api_key = None
tavily_api_key = None

try:
    google_api_key = st.secrets["GOOGLE_API_KEY"]
    tavily_api_key = st.secrets["TAVILY_API_KEY"]
    st.success("✅ API keys loaded from secrets.toml")
except KeyError:
    st.warning("⚠️ API keys not found in secrets.toml. Please enter them below:")
    
    col1, col2 = st.columns(2)
    with col1:
        google_api_key = st.text_input("Google API Key", type="password")
    with col2:
        tavily_api_key = st.text_input("Tavily API Key", type="password")

# Set environment variables if keys are available
if google_api_key and tavily_api_key:
    os.environ["GOOGLE_API_KEY"] = google_api_key
    os.environ["TAVILY_API_KEY"] = tavily_api_key
else:
    st.error("Please provide both API keys!")
    st.stop()

# Initialize components
parser = StrOutputParser()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.4)

# Tavily setup
tool = TavilySearch(
    max_results=10,
    topic="general",
)

def tavilyResult(query: str) -> str:
    response = tool.invoke({"query": query})
    content = ""
    for result in response.get("results", []):
        content += result.get("content", "") + "\n\n"
    return content.strip()

# Social media templates
linkedIn_template = PromptTemplate.from_template("""
From the {search_result}, create a LinkedIn style post.
""")

twitter_template = PromptTemplate.from_template("""
From the {search_result}, create a twitter style post.
""")

instagram_template = PromptTemplate.from_template("""
From the {search_result}, create a instagram style post.
""")

# Create chains
linkedIn_chain = linkedIn_template | llm | parser
twitter_chain = twitter_template | llm | parser
instagram_chain = instagram_template | llm | parser

# Parallel chain
parallel_chain = RunnableParallel({
    "linkedin": linkedIn_chain,
    "twitter": twitter_chain,
    "instagram": instagram_chain
})

# Streamlit UI
st.title("📱 Social Media Content Generator")

# Search query
search_query = st.text_input("Enter your search query:", "What happened at the last IPL 2025")

if st.button("Generate Social Media Posts"):
    with st.spinner("Searching and generating content..."):
        try:
            # Get search results
            search_result = tavilyResult(search_query)
            
            # Generate social media posts
            draft = parallel_chain.invoke({"search_result": search_result})
            
            # Display results
            for platform, content in draft.items():
                with st.expander(f"📱 {platform.title()} Post"):
                    st.write(content)
        except Exception as e:
            st.error(f"Error generating content: {str(e)}")
            st.exception(e)