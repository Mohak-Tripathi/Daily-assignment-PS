import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
import sys
from io import StringIO, BytesIO
import contextlib

# Page config
st.set_page_config(
    page_title="LangGraph Math Agent",
    page_icon="🧮",
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
    .message-box {
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
        color: #1f1f1f !important;
    }
    .message-box * {
        color: #1f1f1f !important;
    }
    .human-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196F3;
    }
    .ai-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .tool-message {
        background-color: #e8f5e9;
        border-left: 4px solid #4caf50;
    }
    </style>
""", unsafe_allow_html=True)

# Get API keys from secrets with fallback to UI input
gemini_api_key = None

try:
    gemini_api_key = st.secrets["GEMINI_API_KEY"]
    st.success("✅ API key loaded from secrets.toml")
except (KeyError, FileNotFoundError):
    st.warning("⚠️ API key not found in secrets.toml. Please enter it below:")
    gemini_api_key = st.text_input("Gemini API Key", type="password")

# Set environment variable if key is available
if gemini_api_key:
    os.environ["GEMINI_API_KEY"] = gemini_api_key
else:
    st.error("Please provide your Gemini API key!")
    st.stop()

# Sidebar for configuration
st.sidebar.title("⚙️ Configuration")
show_graph = st.sidebar.toggle("Show Graph Visualization", value=True, help="Display the LangGraph workflow diagram")
st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info("""
This app uses LangGraph to create a math agent with tools:
- ➗ **Divide**: Divides two numbers
- ✖️ **Multiply**: Multiplies two numbers

The agent uses Gemini to understand your question and call the appropriate tool.
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### Example Queries")
st.sidebar.code("""
- What is 10 divided by 2?
- Multiply 5 by 7
- Calculate 100 / 4
- What's 12 times 8?
- Divide 50 by 5 and tell me
""")

# Define tools
@tool
def divide(a: float, b: float) -> float:
    """Divide a by b."""
    if b == 0:
        return "Error: Cannot divide by zero"
    return a / b

@tool
def multiply(a: float, b: float) -> float:
    """Multiply a by b."""
    if a == 0 or b == 0:
        return 0
    return a * b

# Initialize LLM and bind tools
@st.cache_resource
def initialize_agent():
    """Initialize the LangGraph agent with tools"""
    
    # Create LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        google_api_key=gemini_api_key
    )
    
    # Bind tools to LLM
    tools = [divide, multiply]
    llm_with_tools = llm.bind_tools(tools)
    
    # Define the LLM node
    def llm_node(state: MessagesState):
        messages = state["messages"]
        
        # Add system message to guide the LLM's behavior
        system_msg = SystemMessage(
            content="""You are a helpful AI assistant with access to mathematical tools (divide and multiply).

For math questions involving division or multiplication, use the appropriate tools.
For all other questions, answer them directly using your knowledge.

Examples:
- "What is 10 divided by 2?" → Use the divide tool
- "Multiply 5 by 7" → Use the multiply tool  
- "Who is the PM of India?" → Answer directly without tools
- "What is AI?" → Answer directly without tools"""
        )
        
        # Prepend system message if it's not already there
        if not messages or not isinstance(messages[0], SystemMessage):
            messages = [system_msg] + messages
        
        return {
            "messages": [llm_with_tools.invoke(messages)]
        }
    
    # Build the graph
    builder = StateGraph(MessagesState)
    
    builder.add_node("llm_node", llm_node)
    builder.add_node("tools", ToolNode([divide, multiply]))
    
    builder.add_edge(START, "llm_node")
    builder.add_conditional_edges(
        "llm_node",
        tools_condition,
        {"tools": "tools", END: END}
    )
    builder.add_edge("tools", END)
    
    graph = builder.compile()
    
    return graph

# Function to format messages
def format_message(msg):
    """Format different message types for display"""
    if isinstance(msg, HumanMessage):
        return {
            "type": "human",
            "content": msg.content,
            "icon": "👤"
        }
    elif isinstance(msg, AIMessage):
        content = msg.content if msg.content else ""
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            tool_info = []
            for tc in msg.tool_calls:
                tool_info.append(f"**Tool Call:** {tc['name']}")
                tool_info.append(f"**Arguments:** {tc['args']}")
            content = "\n\n".join(tool_info) if not content else content + "\n\n" + "\n\n".join(tool_info)
        return {
            "type": "ai",
            "content": content,
            "icon": "🤖",
            "tool_calls": getattr(msg, 'tool_calls', None)
        }
    elif isinstance(msg, ToolMessage):
        return {
            "type": "tool",
            "content": f"**Result:** {msg.content}",
            "icon": "🔧",
            "name": msg.name
        }
    else:
        return {
            "type": "unknown",
            "content": str(msg),
            "icon": "📝"
        }

# Main UI
st.title("🧮 LangGraph Math Agent")
st.markdown("Ask math questions and watch the agent use tools to solve them!")

# Query input
query = st.text_area(
    "Enter your math question:",
    value="What is 10 divided by 2?",
    height=100,
    help="Ask any question involving multiplication or division"
)

# Execute button
if st.button("🚀 Execute Query", type="primary"):
    if not query.strip():
        st.error("Please enter a query!")
    else:
        with st.spinner("🔄 Agent is processing your query..."):
            try:
                # Initialize agent
                graph = initialize_agent()
                
                # Execute the graph
                messages = [HumanMessage(content=query)]
                result = graph.invoke({"messages": messages})
                
                # Display results
                st.success("✅ Query executed successfully!")
                
                # Create tabs for organized output
                tabs = ["💬 Conversation Flow", "🔍 Detailed View"]
                if show_graph:
                    tabs.append("📊 Graph Visualization")
                
                tab_objects = st.tabs(tabs)
                
                with tab_objects[0]:
                    st.markdown("### 💬 Conversation Flow")
                    st.markdown("---")
                    
                    # Display all messages in order
                    for i, msg in enumerate(result["messages"]):
                        formatted = format_message(msg)
                        
                        with st.container():
                            if formatted["type"] == "human":
                                st.markdown(f"""
                                <div class="message-box human-message">
                                    <strong style="color: #1f1f1f;">{formatted["icon"]} Human</strong><br>
                                    <span style="color: #1f1f1f;">{formatted["content"]}</span>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            elif formatted["type"] == "ai":
                                if formatted["tool_calls"]:
                                    st.markdown(f"""
                                    <div class="message-box ai-message">
                                        <strong>{formatted["icon"]} AI Assistant</strong><br>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    for tc in formatted["tool_calls"]:
                                        st.info(f"🔧 **Calling tool:** `{tc['name']}`")
                                        st.json(tc['args'])
                                else:
                                    content = formatted["content"] if formatted["content"] else "(No content)"
                                    st.markdown(f"""
                                    <div class="message-box ai-message">
                                        <strong>{formatted["icon"]} AI Assistant</strong><br>
                                        <span style="color: #1f1f1f;">{content}</span>
                                    </div>
                                    """, unsafe_allow_html=True)
                            
                            elif formatted["type"] == "tool":
                                st.markdown(f"""
                                <div class="message-box tool-message">
                                    <strong style="color: #1f1f1f;">{formatted["icon"]} Tool: {formatted.get("name", "Unknown")}</strong><br>
                                    <span style="color: #1f1f1f;">{formatted["content"]}</span>
                                </div>
                                """, unsafe_allow_html=True)
                
                with tab_objects[1]:
                    st.markdown("### 🔍 Detailed Message Analysis")
                    
                    for i, msg in enumerate(result["messages"]):
                        with st.expander(f"Message {i+1}: {type(msg).__name__}", expanded=False):
                            st.write("**Type:**", type(msg).__name__)
                            
                            if hasattr(msg, 'content'):
                                st.write("**Content:**")
                                st.code(msg.content if msg.content else "(empty)")
                            
                            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                                st.write("**Tool Calls:**")
                                for tc in msg.tool_calls:
                                    st.json(tc)
                            
                            if hasattr(msg, 'name'):
                                st.write("**Tool Name:**", msg.name)
                            
                            st.write("**Full Message Object:**")
                            st.json(msg.dict() if hasattr(msg, 'dict') else str(msg))
                
                if show_graph and len(tab_objects) > 2:
                    with tab_objects[2]:
                        st.markdown("### 📊 LangGraph Workflow Visualization")
                        try:
                            graph_image = graph.get_graph().draw_mermaid_png()
                            st.image(graph_image, caption="Agent Workflow Graph")
                        except Exception as e:
                            st.warning(f"Could not generate graph visualization: {str(e)}")
                            st.info("Make sure you have the required dependencies installed (pygraphviz or mermaid)")
                
            except Exception as e:
                st.error(f"❌ Error executing query: {str(e)}")
                with st.expander("🔍 Error Details"):
                    st.exception(e)

# Session history (optional enhancement)
st.markdown("---")
with st.expander("📚 Session History"):
    if 'history' not in st.session_state:
        st.session_state.history = []
    
    if st.session_state.history:
        for i, item in enumerate(st.session_state.history[-5:]):  # Show last 5
            st.text(f"{i+1}. {item}")
    else:
        st.info("No queries executed yet in this session")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Powered by LangGraph & Gemini | Built with Streamlit"
    "</div>",
    unsafe_allow_html=True
)

