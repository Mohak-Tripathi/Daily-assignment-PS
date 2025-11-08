import streamlit as st
import uuid
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage, ToolMessage
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode
from langgraph.checkpoint.memory import MemorySaver

# Page config
st.set_page_config(
    page_title="LangGraph ReAct Agent",
    page_icon="🧮",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .stChatMessage {
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .tool-call {
        background-color: #f0f2f6;
        border-left: 3px solid #FF4B4B;
        padding: 10px;
        margin: 10px 0;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Get API keys from secrets with fallback to UI input
gemini_api_key = None

try:
    gemini_api_key = st.secrets["GEMINI_API_KEY"]
    st.success("✅ API key loaded from secrets.toml")
except KeyError:
    st.warning("⚠️ API key not found in secrets.toml. Please enter it below:")
    gemini_api_key = st.text_input("Gemini API Key", type="password")

# Set environment variables if keys are available
if not gemini_api_key:
    st.error("Please provide Gemini API key!")
    st.stop()

# Sidebar for configuration
st.sidebar.title("⚙️ Configuration")
verbose_mode = st.sidebar.toggle("Show Tool Calls", value=True, help="Display when tools are being used")

if st.sidebar.button("🔄 New Conversation"):
    # Clear session state to start fresh
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### 🧮 Available Tools")
st.sidebar.info("""
**Math Operations:**
- ➕ **Add**: Add two numbers
- ✖️ **Multiply**: Multiply two numbers
- ➗ **Divide**: Divide two numbers

Try: *"Add 5 and 10, then multiply by 3"*
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info("""
This is a **ReAct Agent** built with LangGraph that can:
- Solve arithmetic problems
- Use tools when needed
- Remember conversation context
- Handle multi-step queries
""")

# Define tools
@tool
def multiply(a: int, b: int) -> int:
    """
    Multiplies two integers together.
    
    Args:
        a: The first integer.
        b: The second integer.
    
    Returns:
        The product of the two integers.
    """
    return a * b

@tool
def add(a: int, b: int) -> int:
    """
    Add two integers together.
    
    Args:
        a: The first integer.
        b: The second integer.
    
    Returns:
        The sum of the two integers.
    """
    return a + b

@tool
def divide(a: int, b: int) -> float:
    """
    Divide the first integer by the second integer.
    
    Args:
        a: The numerator.
        b: The denominator.
    
    Returns:
        The quotient of the two integers.
    """
    if b == 0:
        return "Error: Division by zero is not allowed"
    return a / b

# Initialize LLM and tools
@st.cache_resource
def initialize_agent(api_key):
    """Initialize the LangGraph ReAct agent"""
    
    # Create LLM
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)
    
    # Bind tools
    tools_list = [add, multiply, divide]
    llm_with_tools = llm.bind_tools(tools_list)
    
    # Define assistant node
    def assistant_node(state: MessagesState):
        system_message = SystemMessage(
            content="You are a helpful assistant. You are responsible to provide correct answer of user arithmetic queries using tools at your disposal."
        )
        messages = [system_message] + state["messages"]
        return {"messages": [llm_with_tools.invoke(messages)]}
    
    # Build graph
    builder = StateGraph(MessagesState)
    builder.add_node("assistant_node", assistant_node)
    builder.add_node("tools", ToolNode(tools_list))
    
    # Add edges
    builder.add_edge(START, "assistant_node")
    builder.add_conditional_edges("assistant_node", tools_condition, {"tools": "tools", END: END})
    builder.add_edge("tools", "assistant_node")
    
    # Compile with memory
    memory = MemorySaver()
    graph = builder.compile(checkpointer=memory)
    
    return graph

# Initialize agent
agent = initialize_agent(gemini_api_key)

# Initialize session state for conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = f"chat-{uuid.uuid4().hex[:6]}"

# Main UI
st.title("🧮 LangGraph ReAct Agent")
st.markdown("Ask me to solve arithmetic problems! I can add, multiply, and divide numbers.")

# Display thread ID
st.caption(f"🔗 Thread ID: `{st.session_state.thread_id}`")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Show tool calls if in verbose mode
        if verbose_mode and "tool_calls" in message and message["tool_calls"]:
            with st.expander("🔧 Tool Calls", expanded=False):
                for tool_call in message["tool_calls"]:
                    st.markdown(f"""
                    <div class="tool-call">
                    <strong>🔧 {tool_call['name']}</strong><br>
                    <strong>Args:</strong> {tool_call['args']}<br>
                    <strong>Result:</strong> {tool_call.get('result', 'Processing...')}
                    </div>
                    """, unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Ask me to solve a math problem..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get agent response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        with st.spinner("Thinking..."):
            try:
                # Prepare config
                config = {"configurable": {"thread_id": st.session_state.thread_id}}
                
                # Invoke agent
                result = agent.invoke({"messages": [HumanMessage(content=prompt)]}, config)
                
                # Extract response and tool calls
                ai_messages = [m for m in result["messages"] if isinstance(m, AIMessage)]
                tool_messages = [m for m in result["messages"] if isinstance(m, ToolMessage)]
                
                if ai_messages:
                    # Get the last AI message
                    last_ai_msg = ai_messages[-1]
                    
                    # Extract text content
                    if hasattr(last_ai_msg, 'content'):
                        if isinstance(last_ai_msg.content, str):
                            response_text = last_ai_msg.content
                        elif isinstance(last_ai_msg.content, list):
                            # Handle list content (mixed text and tool calls)
                            text_parts = [part.get('text', '') for part in last_ai_msg.content if isinstance(part, dict) and 'text' in part]
                            response_text = ' '.join(text_parts) if text_parts else "Task completed."
                        else:
                            response_text = str(last_ai_msg.content)
                    else:
                        response_text = "Task completed."
                    
                    # Extract tool calls
                    tool_calls_info = []
                    if hasattr(last_ai_msg, 'tool_calls') and last_ai_msg.tool_calls:
                        for tool_call in last_ai_msg.tool_calls:
                            tool_info = {
                                'name': tool_call.get('name', 'unknown'),
                                'args': tool_call.get('args', {}),
                                'id': tool_call.get('id', '')
                            }
                            
                            # Find corresponding tool result
                            for tool_msg in tool_messages:
                                if hasattr(tool_msg, 'tool_call_id') and tool_msg.tool_call_id == tool_info['id']:
                                    tool_info['result'] = tool_msg.content
                                    break
                            
                            tool_calls_info.append(tool_info)
                    
                    # Display response
                    message_placeholder.markdown(response_text)
                    
                    # Display tool calls if verbose
                    if verbose_mode and tool_calls_info:
                        with st.expander("🔧 Tool Calls", expanded=False):
                            for tool_call in tool_calls_info:
                                st.markdown(f"""
                                <div class="tool-call">
                                <strong>🔧 {tool_call['name']}</strong><br>
                                <strong>Args:</strong> {tool_call['args']}<br>
                                <strong>Result:</strong> {tool_call.get('result', 'N/A')}
                                </div>
                                """, unsafe_allow_html=True)
                    
                    # Add to session state
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response_text,
                        "tool_calls": tool_calls_info
                    })
                else:
                    # Fallback if no AI message
                    message_placeholder.markdown("I processed your request.")
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": "I processed your request.",
                        "tool_calls": []
                    })
                
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                message_placeholder.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                    "tool_calls": []
                })
                st.exception(e)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Powered by LangGraph & Gemini | Built with Streamlit"
    "</div>",
    unsafe_allow_html=True
)

