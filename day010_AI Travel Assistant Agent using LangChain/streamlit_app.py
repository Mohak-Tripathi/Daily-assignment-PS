import streamlit as st
import os
import requests
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_community.tools import DuckDuckGoSearchRun
import sys
from io import StringIO
import contextlib

# Page config
st.set_page_config(
    page_title="AI Travel Assistant",
    page_icon="✈️",
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

# Get API keys from secrets with fallback to UI input
gemini_api_key = None
weather_api_key = None
aviation_api_key = None

try:
    gemini_api_key = st.secrets["GEMINI_API_KEY"]
    weather_api_key = st.secrets["WEATHER_API_KEY"]
    aviation_api_key = st.secrets["AVIATION_API_KEY"]
    st.success("✅ API keys loaded from secrets.toml")
except KeyError:
    st.warning("⚠️ API keys not found in secrets.toml. Please enter them below:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        gemini_api_key = st.text_input("Gemini API Key", type="password")
    with col2:
        weather_api_key = st.text_input("WeatherStack API Key", type="password")
    with col3:
        aviation_api_key = st.text_input("AviationStack API Key", type="password")

# Sidebar for configuration
st.sidebar.title("⚙️ Configuration")
verbose_mode = st.sidebar.toggle("Verbose Mode", value=False, help="Show detailed execution logs")
st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info("""
This AI Travel Assistant can help you with:
- 🌤️ **Weather Information**: Get current weather for any city
- ✈️ **Flight Information**: Find flights from Delhi to major Indian cities
- 🔍 **Web Search**: Search for travel-related information
- ➕ **Calculations**: Perform basic calculations
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### Example Queries")
st.sidebar.markdown("""
- "Tell me weather of Kanpur and Delhi right now and add the temperature of both cities"
- "Find the capital of Madhya Pradesh, then find its current weather condition"
- "What flights are available from Delhi to Mumbai on 2025-12-25?"
- "Search for best travel destinations in India"
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

# Initialize tools
def create_tools(weather_key, aviation_key):
    """Create all tools for the travel assistant"""
    
    # Search tool
    search_tool = DuckDuckGoSearchRun()
    
    # Weather tool
    @tool
    def get_weather_data(city: str) -> str:
        """
        This function fetches the current weather data for a given city
        
        Args:
            city: The name of the city to get weather for
        """
        url = f'https://api.weatherstack.com/current?access_key={weather_key}&query={city}'
        try:
            response = requests.get(url, timeout=10)
            return response.json()
        except Exception as e:
            return f"Error fetching weather: {str(e)}"
    
    # Addition tool
    @tool
    def addition(a: str, b: str) -> str:
        """
        This function adds two numbers
        
        Args:
            a: First number as string
            b: Second number as string
        """
        try:
            return str(int(a) + int(b))
        except ValueError:
            return "Error: Invalid numbers provided"
    
    # Flight info tool
    @tool
    def flight_info_tool(arg_city_name: str, my_date: str) -> str:
        """
        This function suggests available flights from Delhi to the destination only if a travel date is provided.
        
        Args:
            arg_city_name: The destination city name
            my_date: The travel date in YYYY-MM-DD format
        """
        # Normalize the input
        name = arg_city_name.strip().lower()
        city_to_iata = {
            "delhi": "DEL",
            "mumbai": "BOM",
            "chennai": "MAA",
            "bengaluru": "BLR",
            "bangalore": "BLR",
            "hyderabad": "HYD",
            "kolkata": "CCU",
            "ahmedabad": "AMD"
        }
        
        if name not in city_to_iata:
            return "Invalid city name. Supported cities: Delhi, Mumbai, Chennai, Bengaluru, Bangalore, Hyderabad, Kolkata, Ahmedabad"
        
        city_iata = city_to_iata[name]
        
        url = f'http://api.aviationstack.com/v1/flights?access_key={aviation_key}&dep_iata=DEL&arr_iata={city_iata}&flight_date={my_date}'
        try:
            response = requests.get(url, timeout=10)
            return response.json()
        except Exception as e:
            return f"Error fetching flight information: {str(e)}"
    
    return [search_tool, get_weather_data, flight_info_tool, addition]

# Initialize agent
def initialize_agent(gemini_key, weather_key, aviation_key, verbose=False):
    """Initialize the LangChain agent with all tools"""
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=gemini_key,
        temperature=0.7
    )
    
    tools = create_tools(weather_key, aviation_key)
    
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt="You are a helpful travel assistant. Use the available tools to help users with weather information, flight searches, web searches, and calculations. Always provide clear and helpful responses."
    )
    
    return agent

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Main UI
st.title("✈️ AI-Powered Travel Assistant")
st.markdown("Get weather information, flight details, and travel assistance using natural language queries.")

# Check if API keys are available
if not gemini_api_key or not weather_api_key or not aviation_api_key:
    st.error("❌ Please provide all API keys to continue!")
    st.stop()

# Main content
st.markdown("### 💬 Ask Your Travel Question")
user_query = st.text_area(
    "Your question:",
    placeholder="e.g., Tell me weather of Kanpur and Delhi right now and add the temperature of both cities",
    height=100,
    key="query_input"
)

col1, col2 = st.columns([1, 5])
with col1:
    submit_button = st.button("🚀 Ask Assistant", type="primary", use_container_width=True)
with col2:
    clear_button = st.button("🗑️ Clear History", use_container_width=True)

if clear_button:
    st.session_state.messages = []
    st.rerun()

if submit_button and user_query:
    with st.spinner("🤖 AI Assistant is processing your query..."):
        try:
            # Initialize agent
            agent = initialize_agent(gemini_api_key, weather_api_key, aviation_api_key, verbose_mode)
            
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
            st.markdown("### ✨ Response")
            st.info(f"**{final_answer}**")
            
            # Show verbose logs if enabled
            if verbose_mode and verbose_output:
                with st.expander("🔍 Detailed Execution Logs"):
                    st.code(verbose_output, language="text")
            
        except Exception as e:
            st.error(f"❌ Error processing query: {str(e)}")
            with st.expander("🔍 Error Details"):
                st.exception(e)

# Chat History Section
if st.session_state.messages:
    st.markdown("---")
    st.markdown("### 📜 Conversation History")
    
    for idx, msg in enumerate(reversed(st.session_state.messages), 1):
        with st.expander(f"Query {len(st.session_state.messages) - idx + 1}: {msg['query'][:50]}...", expanded=(idx == 1)):
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
    "Powered by Google Gemini & LangChain | Built with Streamlit"
    "</div>",
    unsafe_allow_html=True
)
