import streamlit as st
import os
from crewai import Agent, Process, Crew, Task
from crewai_tools import TavilySearchTool
import sys
from io import StringIO
import contextlib

# Page config
st.set_page_config(
    page_title="CrewAI Content Workflow",
    page_icon="🤖",
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
tavily_api_key = None

try:
    gemini_api_key = st.secrets["GEMINI_API_KEY"]
    tavily_api_key = st.secrets["TAVILY_API_KEY"]
    st.success("✅ API keys loaded from secrets.toml")
except KeyError:
    st.warning("⚠️ API keys not found in secrets.toml. Please enter them below:")
    
    col1, col2 = st.columns(2)
    with col1:
        gemini_api_key = st.text_input("Gemini API Key", type="password")
    with col2:
        tavily_api_key = st.text_input("Tavily API Key", type="password")

# Set environment variables if keys are available
if gemini_api_key and tavily_api_key:
    os.environ["GEMINI_API_KEY"] = gemini_api_key
else:
    st.error("Please provide both API keys!")
    st.stop()

# Sidebar for configuration
st.sidebar.title("⚙️ Configuration")
verbose_mode = st.sidebar.toggle("Verbose Mode", value=False, help="Show detailed execution logs")
st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info("""
This app uses CrewAI with 4 agents working sequentially:
- 🔍 **Researcher**: Finds credible facts
- ✍️ **Drafter**: Writes initial paragraph
- 🔎 **Critic**: Provides feedback
- ✨ **Finalizer**: Polishes the content
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

# Initialize CrewAI components
def initialize_crew(verbose=False):
    """Initialize all agents, tasks, and crew"""
    
    # Initialize search tool
    search_tool = TavilySearchTool(api_key=tavily_api_key)
    
    # Define Agents
    researcher = Agent(
        role="Researcher",
        goal="Find 5 up-to-date, credible facts.",
        backstory="Expert at finding trustworthy information online.",
        tools=[search_tool],
        llm="gemini/gemini-2.5-flash",
        verbose=verbose
    )
    
    drafter = Agent(
        role="Drafter",
        goal="Write a draft paragraph using these facts.",
        backstory="Transforms facts into a readable, draft paragraph for beginners.",
        llm="gemini/gemini-2.5-flash",
        verbose=verbose
    )
    
    critic = Agent(
        role="Critic",
        goal="Provide actionable, constructive feedback.",
        backstory="Professional editor who always helps writers improve.",
        llm="gemini/gemini-2.5-flash",
        verbose=verbose
    )
    
    finalizer = Agent(
        role="Finalizer",
        goal="Rewrite the draft as per the critic's feedback.",
        backstory="Polishes text into their best versions.",
        llm="gemini/gemini-2.5-flash",
        verbose=verbose
    )
    
    # Define Tasks
    research_task = Task(
        description="""
        Using web search, find and list exactly 5 distinct, recent (2024-2025),
        and credible facts about: {topic}. Respond only with 5 bullet points.
        """,
        expected_output="Exactly 5 factual bullet points with clear sources.",
        agent=researcher,
        output_key="facts"
    )
    
    draft_task = Task(
        description="""
        Using only the facts provided in context from the researcher task,
        write one concise, beginner friendly draft paragraph. Do not invent facts.
        """,
        expected_output="One beginner friendly draft paragraph.",
        agent=drafter,
        output_key="paragraph",
        context=[research_task]
    )
    
    critique_task = Task(
        description="""
        Given the draft paragraph in context, provide 2-3 constructive, actionable suggestions to improve
        clarity, accuracy and the flow of the writing.
        """,
        expected_output="A short list of 2 to 3 actionable suggestions.",
        agent=critic,
        output_key="critique",
        context=[draft_task]
    )
    
    final_task = Task(
        description="""
        Rewrite the draft paragraph in context according to the critic's suggestions provided in the context.
        Return the final polished paragraph.
        """,
        expected_output="A polished and improved final paragraph.",
        agent=finalizer,
        context=[draft_task, critique_task]
    )
    
    # Create Crew
    crew = Crew(
        agents=[researcher, drafter, critic, finalizer],
        tasks=[research_task, draft_task, critique_task, final_task],
        process=Process.sequential,
        verbose=verbose
    )
    
    return crew

# Main UI
st.title("🤖 CrewAI Content Workflow")
st.markdown("Generate well-researched, critiqued, and polished content on any topic using AI agents.")

# Topic input
topic = st.text_area(
    "Enter your topic:",
    value="What is Artificial General Intelligence?",
    height=100,
    help="Enter any topic you want researched and written about"
)

# Generate button
if st.button("🚀 Generate Content", type="primary"):
    if not topic.strip():
        st.error("Please enter a topic!")
    else:
        with st.spinner("🔄 Agents are working on your content..."):
            try:
                # Initialize crew
                crew = initialize_crew(verbose=verbose_mode)
                
                # Capture output if verbose
                if verbose_mode:
                    with capture_stdout() as captured:
                        result = crew.kickoff(inputs={"topic": topic})
                    verbose_output = captured.getvalue()
                else:
                    result = crew.kickoff(inputs={"topic": topic})
                    verbose_output = None
                
                # Display results
                st.success("✅ Content generation completed!")
                
                # Create tabs for organized output
                tab1, tab2, tab3 = st.tabs(["📝 Final Result", "🔍 Process Details", "📊 Execution Logs"])
                
                with tab1:
                    st.markdown("### ✨ Final Polished Content")
                    st.markdown(f"**Topic:** {topic}")
                    st.markdown("---")
                    
                    # Extract and display only the final paragraph
                    final_content = result.raw if hasattr(result, 'raw') else str(result)
                    st.write(final_content)
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Final Content",
                        data=final_content,
                        file_name="crewai_output.txt",
                        mime="text/plain"
                    )
                
                with tab2:
                    st.markdown("### 🔍 Agent Workflow Details")
                    
                    # Get task outputs if available
                    try:
                        # Research Facts
                        with st.expander("🔍 Step 1: Research Facts", expanded=True):
                            if hasattr(result, 'tasks_output') and len(result.tasks_output) > 0:
                                st.write(result.tasks_output[0].raw)
                            else:
                                st.info("Research output not available separately")
                        
                        # Draft Paragraph
                        with st.expander("✍️ Step 2: Draft Paragraph", expanded=True):
                            if hasattr(result, 'tasks_output') and len(result.tasks_output) > 1:
                                st.write(result.tasks_output[1].raw)
                            else:
                                st.info("Draft output not available separately")
                        
                        # Critic Feedback
                        with st.expander("🔎 Step 3: Critic's Feedback", expanded=True):
                            if hasattr(result, 'tasks_output') and len(result.tasks_output) > 2:
                                st.write(result.tasks_output[2].raw)
                            else:
                                st.info("Critique output not available separately")
                        
                        # Final Result
                        with st.expander("✨ Step 4: Final Polished Content", expanded=True):
                            final_content = result.raw if hasattr(result, 'raw') else str(result)
                            st.write(final_content)
                    
                    except Exception as e:
                        st.warning("Individual task outputs not available. Final result shown in first tab.")
                
                with tab3:
                    if verbose_mode and verbose_output:
                        st.markdown("### 📊 Detailed Execution Logs")
                        st.code(verbose_output, language="text")
                    else:
                        st.info("Enable 'Verbose Mode' in the sidebar to see detailed execution logs.")
                
            except Exception as e:
                st.error(f"❌ Error generating content: {str(e)}")
                with st.expander("🔍 Error Details"):
                    st.exception(e)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Powered by CrewAI & Gemini | Built with Streamlit"
    "</div>",
    unsafe_allow_html=True
)

