import streamlit as st
import os
import requests
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
import sys
from io import StringIO
import contextlib

# Page config
st.set_page_config(
    page_title="AI Currency Converter",
    page_icon="💱",
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
    .conversion-result {
        font-size: 24px;
        font-weight: bold;
        padding: 20px;
        background-color: #f0f9ff;
        color: #1e293b;
        border-radius: 10px;
        border-left: 5px solid #0ea5e9;
        margin: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Currency codes list (major currencies)
CURRENCY_CODES = [
    "USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY", 
    "INR", "MXN", "BRL", "ZAR", "KRW", "SGD", "HKD", "NOK", 
    "SEK", "DKK", "PLN", "THB", "IDR", "MYR", "PHP", "NZD",
    "TRY", "RUB", "AED", "SAR", "QAR", "KWD", "EGP", "PKR"
]

# Get API keys from secrets with fallback to UI input
gemini_api_key = None
exchangerate_api_key = None

try:
    gemini_api_key = st.secrets["GEMINI_API_KEY"]
    exchangerate_api_key = st.secrets["EXCHANGERATE_API_KEY"]
    st.success("✅ API keys loaded from secrets.toml")
except (KeyError, FileNotFoundError):
    st.warning("⚠️ API keys not found in secrets.toml. Please enter them below:")
    
    col1, col2 = st.columns(2)
    with col1:
        gemini_api_key = st.text_input(
            "Gemini API Key", 
            type="password",
            help="Get your API key from https://makersuite.google.com/app/apikey"
        )
    with col2:
        exchangerate_api_key = st.text_input(
            "ExchangeRate API Key", 
            type="password",
            help="Get your API key from https://www.exchangerate-api.com/"
        )

# Sidebar for configuration
st.sidebar.title("⚙️ Configuration")
verbose_mode = st.sidebar.toggle("Verbose Mode", value=False, help="Show detailed execution logs")
st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info("""
This app uses an AI-powered currency converter with:
- 💱 **Real-time Exchange Rates**: Live data from ExchangeRate API
- 🤖 **AI Agent**: Google Gemini AI for natural language queries
- 🔧 **LangChain Tools**: Intelligent function calling
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### Example Queries")
st.sidebar.markdown("""
- "Convert 100 USD to EUR"
- "How much is 50 GBP in INR?"
- "What's 1000 JPY in USD?"
- "Convert 250 EUR to CAD"
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

# Currency converter tool
def create_currency_converter_tool(api_key):
    """Create the currency converter tool with the API key"""
    
    @tool
    def currency_converter(amount: float, base: str, target: str) -> str:
        """Converts amount from base currency to target currency using real-time ExchangeRate API.
        
        Args:
            amount: The amount to convert
            base: The base currency code (e.g., USD, EUR, INR)
            target: The target currency code (e.g., USD, EUR, INR)
        
        Returns:
            A string with the conversion result
        """
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{base}/{target}/{amount}"
        
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if data.get("result") == "success":
                converted = data["conversion_result"]
                rate = data.get("conversion_rate", "N/A")
                return f"{amount} {base} = {converted:.2f} {target} (Rate: 1 {base} = {rate:.4f} {target})"
            else:
                return f"Conversion failed: {data.get('error-type', 'Unknown error')}"
        except requests.exceptions.RequestException as e:
            return f"API request failed: {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    return currency_converter

# Initialize agent
def initialize_agent(gemini_key, exchange_key, verbose=False):
    """Initialize the LangChain agent with currency converter tool"""
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        google_api_key=gemini_key,
        temperature=0.2
    )
    
    converter_tool = create_currency_converter_tool(exchange_key)
    
    agent = create_agent(
        model=llm,
        tools=[converter_tool],
        system_prompt="""You are a helpful currency conversion assistant. 
        Use the currency_converter tool to answer user questions about currency rates.
        Always extract the amount, base currency, and target currency from the user's query.
        Be helpful and provide clear, formatted responses."""
    )
    
    return agent

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Main UI
st.title("💱 AI-Powered Currency Converter")
st.markdown("Convert currencies using AI-powered natural language queries with real-time exchange rates.")

# Check if API keys are available
if not gemini_api_key or not exchangerate_api_key:
    st.error("❌ Please provide both API keys to continue!")
    st.stop()

# Main content tabs
tab1, tab2, tab3 = st.tabs(["💬 Chat Converter", "📊 Quick Convert", "📜 Chat History"])

with tab1:
    st.markdown("### Natural Language Currency Conversion")
    st.markdown("Ask me anything about currency conversion in natural language!")
    
    # Chat input
    user_query = st.text_input(
        "Your question:",
        placeholder="e.g., How much is 100 USD in Indian Rupees?",
        key="chat_input"
    )
    
    col1, col2 = st.columns([1, 5])
    with col1:
        convert_button = st.button("🔄 Convert", type="primary", use_container_width=True)
    with col2:
        clear_button = st.button("🗑️ Clear History", use_container_width=True)
    
    if clear_button:
        st.session_state.messages = []
        st.rerun()
    
    if convert_button and user_query:
        with st.spinner("🤖 AI Agent is processing your query..."):
            try:
                # Initialize agent
                agent = initialize_agent(gemini_api_key, exchangerate_api_key, verbose_mode)
                
                # Capture output if verbose
                if verbose_mode:
                    with capture_stdout() as captured:
                        response = agent.invoke({
                            "messages": [
                                {"role": "user", "content": user_query}
                            ]
                        })
                    verbose_output = captured.getvalue()
                else:
                    response = agent.invoke({
                        "messages": [
                            {"role": "user", "content": user_query}
                        ]
                    })
                    verbose_output = None
                
                # Extract final answer
                final_answer = "No answer found."
                for msg in reversed(response["messages"]):
                    if hasattr(msg, "content") and msg.content:
                        if msg.__class__.__name__ == "AIMessage":
                            final_answer = msg.content
                            break
                
                # Store in chat history
                st.session_state.messages.append({
                    "query": user_query,
                    "response": final_answer,
                    "verbose": verbose_output
                })
                
                # Display result
                st.markdown("### ✨ Result")
                st.info(f"**{final_answer}**")  # Changed from st.markdown with custom CSS
                
                # Show verbose logs if enabled
                if verbose_mode and verbose_output:
                    with st.expander("🔍 Detailed Execution Logs"):
                        st.code(verbose_output, language="text")
                
            except Exception as e:
                st.error(f"❌ Error processing query: {str(e)}")
                with st.expander("🔍 Error Details"):
                    st.exception(e)

with tab2:
    st.markdown("### Quick Currency Conversion")
    st.markdown("Use the form below for a quick conversion")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        amount = st.number_input("Amount", min_value=0.01, value=100.0, step=10.0)
    
    with col2:
        base_currency = st.selectbox("From Currency", CURRENCY_CODES, index=0)
    
    with col3:
        target_currency = st.selectbox("To Currency", CURRENCY_CODES, index=8)  # INR by default
    
    if st.button("🔄 Quick Convert", type="primary", use_container_width=True):
        query = f"Convert {amount} {base_currency} to {target_currency}"
        
        with st.spinner("🤖 Converting..."):
            try:
                agent = initialize_agent(gemini_api_key, exchangerate_api_key, verbose=False)
                
                response = agent.invoke({
                    "messages": [
                        {"role": "user", "content": query}
                    ]
                })
                
                # Extract final answer
                final_answer = "No answer found."
                for msg in reversed(response["messages"]):
                    if hasattr(msg, "content") and msg.content:
                        if msg.__class__.__name__ == "AIMessage":
                            final_answer = msg.content
                            break
                
                # Display result
                st.markdown("### ✨ Conversion Result")
                st.info(f"**{final_answer}**")  # Changed from st.markdown with custom CSS
                
                # Store in chat history
                st.session_state.messages.append({
                    "query": query,
                    "response": final_answer,
                    "verbose": None
                })
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

with tab3:
    st.markdown("### 📜 Conversion History")
    
    if not st.session_state.messages:
        st.info("No conversion history yet. Start converting currencies in the other tabs!")
    else:
        for idx, msg in enumerate(reversed(st.session_state.messages), 1):
            with st.expander(f"Query {len(st.session_state.messages) - idx + 1}: {msg['query']}", expanded=(idx == 1)):
                st.markdown("**Query:**")
                st.write(msg['query'])
                st.markdown("**Response:**")
                st.success(msg['response'])
                
                if msg.get('verbose'):
                    with st.expander("🔍 Execution Logs"):
                        st.code(msg['verbose'], language="text")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Powered by Google Gemini & ExchangeRate API | Built with LangChain & Streamlit"
    "</div>",
    unsafe_allow_html=True
)

