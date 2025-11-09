import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Page config
st.set_page_config(
    page_title="Sequential Chain Report Generator",
    page_icon="📊",
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
    st.error("Please provide your Google Gemini API key!")
    st.stop()

# Sidebar for configuration
st.sidebar.title("⚙️ Configuration")
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.3, 0.1, help="Controls randomness in the output")
model_name = st.sidebar.selectbox(
    "Model",
    ["gemini-2.5-flash", "gemini-1.5-pro", "gemini-1.5-flash"],
    index=0,
    help="Select the Gemini model to use"
)
st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info("""
This app uses LangChain Sequential Chain:
- 📝 **Report Chain**: Generates a detailed markdown report
- 📋 **Summary Chain**: Creates a 5-point summary
- 🔗 **Sequential**: Chains them together automatically
""")

# Initialize LLM
@st.cache_resource
def initialize_llm(model: str, temperature: float):
    """Initialize the LLM with caching"""
    return ChatGoogleGenerativeAI(model=model, temperature=temperature)

# Initialize chains
@st.cache_resource
def initialize_chains(_llm):
    """Initialize the report and summary chains"""
    
    # Report prompt
    report_prompt = PromptTemplate.from_template(
        """You are a public-health analyst.
Write a detailed, well-structured **markdown report** on the topic: "{topic}".

Requirements:
- Audience: intelligent non-experts (10th–12th grade clarity)
- Sections (use H2/H3): Introduction, Prevalence & Trends, Key Drivers, Health & Economic Impact, Policy & City-Level Interventions, Case Snapshots, Data Gaps, Conclusion
- Include India-urban context (income strata, food environment, sedentary work, women & children, metros vs tier-2)
- Be balanced, evidence-informed (no citations needed), ~800–1000 words
- End with a short "Key Terms" glossary

Return only markdown text."""
    )
    
    # Summary prompt
    summary_prompt = PromptTemplate.from_template(
        """You are a senior editor.
Summarize the following report into exactly **5 numbered points (1–5)** in markdown.
Each point should be one crisp sentence focusing on the most decision-relevant insights.

Report:
========
{report}
========

Return only the 5 numbered lines."""
    )
    
    # Assemble chains
    report_chain = report_prompt | _llm | StrOutputParser()
    summary_chain = summary_prompt | _llm | StrOutputParser()
    
    # Sequential chain
    final_chain = report_chain | summary_chain
    
    return report_chain, summary_chain, final_chain

# Main UI
st.title("📊 Sequential Chain Report Generator")
st.markdown("Generate detailed reports and summaries using LangChain Sequential Chains.")

# Topic input
topic = st.text_area(
    "Enter your topic:",
    value="Obesity in Urban India",
    height=100,
    help="Enter any topic you want a detailed report and summary for"
)

# Generate button
if st.button("🚀 Generate Report & Summary", type="primary"):
    if not topic.strip():
        st.error("Please enter a topic!")
    else:
        with st.spinner("🔄 Generating report and summary..."):
            try:
                # Initialize LLM
                llm = initialize_llm(model_name, temperature)
                
                # Initialize chains
                report_chain, summary_chain, final_chain = initialize_chains(llm)
                
                # Execute the sequential chain
                result = final_chain.invoke({"topic": topic})
                
                # Also get the intermediate report for display
                with st.spinner("📝 Generating detailed report..."):
                    report_result = report_chain.invoke({"topic": topic})
                
                # Display results
                st.success("✅ Report and summary generation completed!")
                
                # Create tabs for organized output
                tab1, tab2, tab3 = st.tabs(["📋 Summary (5 Points)", "📝 Full Report", "🔍 Both Results"])
                
                with tab1:
                    st.markdown("### 📋 5-Point Summary")
                    st.markdown(f"**Topic:** {topic}")
                    st.markdown("---")
                    st.markdown(result)
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Summary",
                        data=result,
                        file_name="summary.txt",
                        mime="text/plain"
                    )
                
                with tab2:
                    st.markdown("### 📝 Detailed Report")
                    st.markdown(f"**Topic:** {topic}")
                    st.markdown("---")
                    st.markdown(report_result)
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Full Report",
                        data=report_result,
                        file_name="report.md",
                        mime="text/markdown"
                    )
                
                with tab3:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("### 📋 Summary")
                        st.markdown(result)
                    
                    with col2:
                        st.markdown("### 📝 Full Report")
                        st.markdown(report_result)
                
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