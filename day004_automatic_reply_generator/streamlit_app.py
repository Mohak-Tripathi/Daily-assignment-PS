import streamlit as st
import os
import re
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnableLambda, RunnablePassthrough, RunnableBranch

# Page config
st.set_page_config(
    page_title="Automated Customer Review Insight & Reply Generator",
    page_icon="💬",
    layout="wide"
)

# # Custom CSS for better styling
# st.markdown("""
#     <style>
#     .stExpander {
#         border: 1px solid #f0f2f6;
#         border-radius: 5px;
#         margin-bottom: 10px;
#     }
#     .review-box {
#         background-color: #f8f9fa;
#         padding: 15px;
#         border-radius: 5px;
#         border-left: 4px solid #1f77b4;
#         margin: 10px 0;
#     }
#     </style>
# """, unsafe_allow_html=True)




# Custom CSS for better styling
st.markdown("""
    <style>
    .stExpander {
        border: 1px solid #f0f2f6;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .review-box {
        background-color: #f8f9fa;
        color: #262730;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #1f77b4;
        margin: 10px 0;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)


# Get API key from secrets with fallback to UI input
google_api_key = None

try:
    google_api_key = st.secrets["GOOGLE_API_KEY"]
    st.success("✅ API key loaded from secrets.toml")
except KeyError:
    st.warning("⚠️ API key not found in secrets.toml. Please enter it below:")
    google_api_key = st.text_input("Google Gemini API Key", type="password")

# Set environment variable if key is available
if google_api_key:
    os.environ["GOOGLE_API_KEY"] = google_api_key
else:
    st.error("Please provide your Google Gemini API key!")
    st.stop()

# Sidebar for configuration
st.sidebar.title("⚙️ Configuration")
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.1, step=0.1, 
                                help="Controls randomness in responses")
st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info("""
This app analyzes customer reviews and generates:
- 📊 Sentiment analysis
- ⭐ Star rating
- ✅ Pros and Cons
- 📝 Summary bullets
- 💬 Auto-generated reply
""")

# Initialize LLM
@st.cache_resource
def initialize_llm(temperature):
    """Initialize the LLM with caching"""
    return ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=temperature)

llm = initialize_llm(temperature)
parser = StrOutputParser()

# Output contract schema
OUTPUT_CONTRACT_TEXT = """{
  "sentiment": "Positive|Negative|Mixed|Neutral",
  "reason": "string",
  "pros": ["string"],
  "cons": ["string"],
  "rating": { "stars": 1, "out_of": 5, "why": "string" },
  "summary_bullets": ["string", "string", "string", "string"],
  "auto_reply": "string"
}"""

# Helper function to coerce JSON from strings
def coerce_json(s: str):
    """Accepts strings with code fences or extra prose; returns parsed JSON obj/array."""
    if not isinstance(s, str):
        raise TypeError("coerce_json expected a string")
    txt = s.strip()
    # stripn ... ``` or ``` ...     txt = re.sub(r"^```(?:json)?\s*|\s*```$", "", txt, flags=re.I | re.M)
    # grab the first JSON object or array
    m = re.search(r"(\{.*?\}|\[.*?\])", txt, flags=re.S)
    if not m:
        raise ValueError(f"No JSON object/array found in: {s[:80]}...")
    return json.loads(m.group(1))

# Initialize chains
@st.cache_resource
def initialize_chains(_llm, _parser):
    """Initialize all LangChain chains"""
    
    # Sentiment chain
    sentiment_pt = PromptTemplate.from_template(
        """You are a precise information extractor.
- Obey this OUTPUT_CONTRACT strictly:
{schema}
- Be terse. No extra words or headings unless asked.

Task: Return the overall sentiment for the REVIEW as one of: Positive, Negative, Mixed, or Neutral.
Output: ONE WORD ONLY (no punctuation).
REVIEW: {review}
"""
    ).partial(schema=OUTPUT_CONTRACT_TEXT)
    sentiment_chain = sentiment_pt | _llm | _parser

    # Reason chain
    reason_pt = PromptTemplate.from_template(
        """You are a precise information extractor.
- Obey this OUTPUT_CONTRACT strictly:
{schema}
- Be terse. No extra words or headings unless asked.

Task: Give a one-line reason for the sentiment (what tipped the balance).
Output: One short sentence, no lists.
REVIEW: {review}
"""
    ).partial(schema=OUTPUT_CONTRACT_TEXT)
    reason_chain = reason_pt | _llm | _parser

    # Pros chain
    pros_pt = PromptTemplate.from_template(
        """You are a precise information extractor.
- Obey this OUTPUT_CONTRACT strictly:
{schema}
- Be terse. No extra words or headings unless asked.

Task: Extract clear Pros from the REVIEW.
Output: JSON array of short phrases only.
REVIEW: {review}
"""
    ).partial(schema=OUTPUT_CONTRACT_TEXT)
    pros_chain = pros_pt | _llm | _parser

    # Cons chain
    cons_pt = PromptTemplate.from_template(
        """You are a precise information extractor.
- Obey this OUTPUT_CONTRACT strictly:
{schema}
- Be terse. No extra words or headings unless asked.

Task: Extract clear Cons from the REVIEW.
Output: JSON array of short phrases only.
REVIEW: {review}
"""
    ).partial(schema=OUTPUT_CONTRACT_TEXT)
    cons_chain = cons_pt | _llm | _parser

    # Rating chain
    RATING_EXAMPLE = '{"stars": <int 1-5>, "out_of": 5, "why": "<short reason>"}'
    rating_pt = PromptTemplate.from_template(
        """You are a precise information extractor.
- Obey this OUTPUT_CONTRACT strictly:
{schema}
- Be terse. No extra words or headings unless asked.

Task: Infer a star rating (1–5) and a brief justification.
Output: JSON object exactly like:
{rating_example}
Rules: Output JSON only. No code fences/backticks.
REVIEW: {review}
"""
    ).partial(schema=OUTPUT_CONTRACT_TEXT, rating_example=RATING_EXAMPLE)
    rating_chain = rating_pt | _llm | _parser

    # Summary chain
    summary_pt = PromptTemplate.from_template(
        """You are a precise information extractor.
- Obey this OUTPUT_CONTRACT strictly:
{schema}
- Be terse. No extra words or headings unless asked.

Task: Produce 3–4 bullet summary points.
Output: JSON array of 3 or 4 short strings (bullets).
REVIEW: {review}
"""
    ).partial(schema=OUTPUT_CONTRACT_TEXT)
    summary_chain = summary_pt | _llm | _parser

    # Fan-out parallel execution
    fanout = RunnableParallel({
        "sentiment": sentiment_chain,
        "reason": reason_chain,
        "pros_raw": pros_chain,
        "cons_raw": cons_chain,
        "rating_raw": rating_chain,
        "summary_raw": summary_chain,
        "review": RunnablePassthrough()
    })

    # Assemble function
    def assemble(d):
        return {
            "sentiment": d["sentiment"].strip(),
            "reason": d["reason"].strip(),
            "pros": coerce_json(d["pros_raw"]),
            "cons": coerce_json(d["cons_raw"]),
            "rating": coerce_json(d["rating_raw"]),
            "summary_bullets": coerce_json(d["summary_raw"]),
            "review": d["review"]["review"] if isinstance(d["review"], dict) else d["review"]
        }

    assembled = fanout | RunnableLambda(assemble)

    # Reply chains
    reply_positive = (PromptTemplate.from_template(
        "You are a polite brand rep.\nREVIEW: {review}\nWrite a brief warm thank-you replying to a positive review."
    ) | _llm | _parser)

    reply_negative = (PromptTemplate.from_template(
        "You are a polite brand rep.\nREVIEW: {review}\nWrite a brief empathetic apology and ask for details to fix issues."
    ) | _llm | _parser)

    reply_mixed = (PromptTemplate.from_template(
        "You are a polite brand rep.\nREVIEW: {review}\nWrite a brief balanced reply: thank for positives, apologise for issues, ask for 1–2 specifics."
    ) | _llm | _parser)

    reply_neutral = (PromptTemplate.from_template(
        "You are a polite brand rep.\nREVIEW: {review}\nWrite a brief neutral professional acknowledgment."
    ) | _llm | _parser)

    # Branch by sentiment
    reply_branch = RunnableBranch(
        (lambda x: "positive" in x["sentiment"].lower(), reply_positive),
        (lambda x: "negative" in x["sentiment"].lower(), reply_negative),
        (lambda x: "mixed" in x["sentiment"].lower(), reply_mixed),
        (lambda x: "neutral" in x["sentiment"].lower(), reply_neutral),
        reply_neutral
    )

    # Final pipeline
    final_pipeline = (assembled | RunnableParallel({
        "sentiment": RunnableLambda(lambda x: x["sentiment"]),
        "reason": RunnableLambda(lambda x: x["reason"]),
        "pros": RunnableLambda(lambda x: x["pros"]),
        "cons": RunnableLambda(lambda x: x["cons"]),
        "rating": RunnableLambda(lambda x: x["rating"]),
        "summary_bullets": RunnableLambda(lambda x: x["summary_bullets"]),
        "auto_reply": (RunnableParallel({
            "review": RunnableLambda(lambda x: x["review"]),
            "sentiment": RunnableLambda(lambda x: x["sentiment"]),
        }) | reply_branch),
    }))

    return final_pipeline

# Initialize chains
pipeline = initialize_chains(llm, parser)

# Main UI
st.title("💬 Automated Customer Review Insight & Reply Generator")
st.markdown("Analyze customer reviews and generate professional responses automatically.")

# Review input
review = st.text_area(
    "Enter customer review:",
    value="I love the battery life and display quality, but the camera is disappointing and the app keeps crashing.",
    height=150,
    help="Paste the customer review you want to analyze"
)

# Generate button
if st.button("🚀 Analyze Review & Generate Reply", type="primary"):
    if not review.strip():
        st.error("Please enter a customer review!")
    else:
        with st.spinner("🔄 Analyzing review and generating insights..."):
            try:
                # Process the review
                result = pipeline.invoke({"review": review})
                
                # Display results
                st.success("✅ Analysis completed!")
                
                # Create tabs for organized output
                tab1, tab2, tab3 = st.tabs(["📊 Analysis Results", "💬 Auto Reply", "📋 Full Details"])
                
                with tab1:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("### 📊 Sentiment Analysis")
                        sentiment = result["sentiment"]
                        sentiment_color = {
                            "Positive": "🟢",
                            "Negative": "🔴",
                            "Mixed": "🟡",
                            "Neutral": "⚪"
                        }.get(sentiment, "⚪")
                        st.markdown(f"**Sentiment:** {sentiment_color} {sentiment}")
                        st.markdown(f"**Reason:** {result['reason']}")
                        
                        st.markdown("### ⭐ Rating")
                        rating = result["rating"]
                        stars = "⭐" * rating.get("stars", 0)
                        st.markdown(f"**{stars} {rating.get('stars', 0)}/5**")
                        st.markdown(f"*{rating.get('why', '')}*")
                    
                    with col2:
                        st.markdown("### ✅ Pros")
                        if result["pros"]:
                            for pro in result["pros"]:
                                st.markdown(f"- ✅ {pro}")
                        else:
                            st.info("No pros identified")
                        
                        st.markdown("### ❌ Cons")
                        if result["cons"]:
                            for con in result["cons"]:
                                st.markdown(f"- ❌ {con}")
                        else:
                            st.info("No cons identified")
                    
                    st.markdown("### 📝 Summary")
                    if result["summary_bullets"]:
                        for bullet in result["summary_bullets"]:
                            st.markdown(f"- {bullet}")
                
                with tab2:
                    st.markdown("### 💬 Auto-Generated Reply")
                    st.markdown("---")
                    st.markdown(f'<div class="review-box">{result["auto_reply"]}</div>', unsafe_allow_html=True)
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Reply",
                        data=result["auto_reply"],
                        file_name="auto_reply.txt",
                        mime="text/plain"
                    )
                
                with tab3:
                    st.markdown("### 📋 Full Analysis Details")
                    
                    with st.expander("📝 Original Review", expanded=False):
                        st.write(review)
                    
                    with st.expander("📊 Complete Analysis JSON", expanded=False):
                        st.json(result)
                    
                    # Copy JSON button
                    st.download_button(
                        label="📥 Download Full Analysis (JSON)",
                        data=json.dumps(result, indent=2),
                        file_name="review_analysis.json",
                        mime="application/json"
                    )
                
            except Exception as e:
                st.error(f"❌ Error analyzing review: {str(e)}")
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