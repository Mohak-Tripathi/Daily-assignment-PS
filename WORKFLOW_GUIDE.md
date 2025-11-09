# 📋 Assignment Workflow Guide

This guide walks you through the complete workflow for each daily assignment, from creation to deployment.

## 📊 Workflow Overview

```
Create → Develop → Test → Document → Commit → Deploy
```

## Step-by-Step Workflow

### Step 1: Create New Assignment 📁

```bash
# Navigate to project root
cd C:\AgenticAIDevelopment

# Copy template to new assignment folder
cp -r day00_template day01_chatbot_basic

# Navigate to new assignment
cd day01_chatbot_basic
```

**Naming Convention:** `dayXX_descriptive_name`
- `day01_chatbot_basic`
- `day02_langchain_rag`
- `day03_agent_with_tools`

### Step 2: Setup Environment 🔧

**Option A: Using Global Virtual Environment**
```bash
# From project root
cd C:\AgenticAIDevelopment
.venv\Scripts\activate

# Navigate to assignment
cd day01_chatbot_basic
```

**Option B: Using Per-Assignment Virtual Environment**
```bash
# From assignment folder
cd day01_chatbot_basic

# Create venv
python -m venv venv

# Activate
venv\Scripts\activate
```

### Step 3: Install Dependencies 📦

```bash
# Install base dependencies
pip install -r requirements.txt

# Install additional packages as needed
pip install langchain openai

# Update requirements.txt
pip freeze > requirements.txt
```

### Step 4: Configure Secrets 🔐

Create `.streamlit/secrets.toml`:

```toml
# .streamlit/secrets.toml
OPENAI_API_KEY = "sk-your-actual-key"
ANTHROPIC_API_KEY = "sk-ant-your-actual-key"
```

**Important:** This file is gitignored and won't be committed!

### Step 5: Develop Your App 💻

Edit `streamlit_app.py`:

```python
import streamlit as st

st.set_page_config(
    page_title="Day 01 - Chatbot",
    page_icon="💬",
    layout="wide"
)

def main():
    st.title("💬 My Chatbot")
    
    # Your code here
    user_input = st.text_input("Ask me anything:")
    
    if st.button("Send"):
        # Process input
        st.write(f"You said: {user_input}")

if __name__ == "__main__":
    main()
```

### Step 6: Test Locally 🧪

```bash
# Run the app
streamlit run streamlit_app.py

# Open browser to http://localhost:8501
# Test all functionality
# Check for errors in terminal
```

**Testing Checklist:**
- [ ] App loads without errors
- [ ] All buttons work
- [ ] Input validation works
- [ ] Error messages display correctly
- [ ] Secrets load properly
- [ ] UI looks good on different screen sizes

### Step 7: Document Your Work 📝

Update `README.md` in your assignment folder:

```markdown
# Day 01 - Chatbot Basic

## Description
A simple chatbot using OpenAI API...

## Features
- Feature 1
- Feature 2

## What I Learned
- Learned about...
- Discovered that...

## Challenges
- Challenge 1 and how I solved it
- Challenge 2 and solution
```

### Step 8: Commit to Git 💾

```bash
# Check what changed
git status

# Add all files
git add .

# Commit with descriptive message
git commit -m "Complete day01: Basic chatbot with OpenAI"

# Push to GitHub
git push origin main
```

**Good Commit Messages:**
- `Complete day01: Basic chatbot with OpenAI`
- `Add day02: RAG system with LangChain`
- `Update day03: Fix API key handling`

### Step 9: Deploy to Streamlit Cloud ☁️

1. **Go to Streamlit Cloud:**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub

2. **Create New App:**
   - Click "New app" button
   - Select your repository: `AgenticAIDevelopment`
   - Set branch: `main`
   - Set main file path: `day01_chatbot_basic/streamlit_app.py`

3. **Configure Secrets:**
   - Click "Advanced settings"
   - Go to "Secrets" section
   - Paste your secrets:
   ```toml
   OPENAI_API_KEY = "sk-your-key"
   ```

4. **Deploy:**
   - Click "Deploy"!
   - Wait 2-3 minutes for deployment
   - Your app will be live at: `https://your-app-name.streamlit.app`

### Step 10: Update Main README 📋

Update the main `README.md` with your new assignment:

```markdown
| Day | Assignment | Description | Status | Live Demo |
|-----|-----------|-------------|--------|-----------|
| 01  | [Chatbot Basic](day01_chatbot_basic/) | Simple OpenAI chatbot | ✅ Complete | [Live](https://your-app.streamlit.app) |
```

### Step 11: Clean Up 🧹

```bash
# Deactivate virtual environment
deactivate

# Final commit
git add README.md
git commit -m "Update main README with day01 link"
git push
```

## 🔄 Daily Routine

### Morning Routine
```bash
# 1. Navigate to project
cd C:\AgenticAIDevelopment

# 2. Pull latest changes (if working from multiple machines)
git pull

# 3. Activate virtual environment
.venv\Scripts\activate

# 4. Start working on assignment
cd day01_chatbot_basic
streamlit run streamlit_app.py
```

### Evening Routine
```bash
# 1. Save dependencies
pip freeze > requirements.txt

# 2. Update documentation
# Edit README.md with learnings

# 3. Commit progress
git add .
git commit -m "Day01: Work in progress"
git push

# 4. Deactivate environment
deactivate
```

## 🎯 Best Practices

### Code Organization
```python
# Good structure
# 1. Imports
import streamlit as st
from utils import helper_function

# 2. Constants
API_ENDPOINT = "https://api.example.com"

# 3. Helper functions
def process_input(text):
    return text.upper()

# 4. Main function
def main():
    st.title("My App")
    # App logic here

# 5. Entry point
if __name__ == "__main__":
    main()
```

### Error Handling
```python
try:
    result = api_call()
    st.success("Success!")
except Exception as e:
    st.error(f"Error: {str(e)}")
    st.exception(e)  # Show full traceback in development
```

### Session State
```python
# Initialize once
if "messages" not in st.session_state:
    st.session_state.messages = []

# Use throughout app
st.session_state.messages.append(new_message)
```

### Secrets Management
```python
# Always check if secret exists
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except (KeyError, FileNotFoundError):
    st.error("Please configure your API key!")
    st.stop()
```

## 📊 Progress Tracking

Create a simple progress tracker in your main README:

```markdown
## Learning Progress

### Week 1: Fundamentals
- [x] Day 01: Basic Streamlit app
- [x] Day 02: API integration
- [ ] Day 03: Session state
- [ ] Day 04: File uploads
- [ ] Day 05: Database integration

### Week 2: LangChain
- [ ] Day 06: LangChain basics
- [ ] Day 07: RAG system
...
```

## 🐛 Common Issues & Solutions

### Issue: Virtual environment not activating
```bash
# Solution: Use full path
C:\AgenticAIDevelopment\.venv\Scripts\activate
```

### Issue: Import errors
```bash
# Solution: Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Issue: Streamlit port in use
```bash
# Solution: Use different port
streamlit run streamlit_app.py --server.port 8502
```

### Issue: Secrets not loading
```bash
# Solution: Check file location
# Should be: day01_folder/.streamlit/secrets.toml
# Not: day01_folder/streamlit/secrets.toml
```

### Issue: Deployment fails
```bash
# Solution: Check these:
# 1. requirements.txt is up to date
# 2. All imports are in requirements.txt
# 3. File path in Streamlit Cloud is correct
# 4. Secrets are configured in cloud dashboard
```

## 📚 Resources

- **Streamlit:** https://docs.streamlit.io/
- **LangChain:** https://python.langchain.com/
- **OpenAI:** https://platform.openai.com/docs
- **Git:** https://git-scm.com/doc

## 💡 Tips for Success

1. **Start Simple:** Begin with basic functionality, then add features
2. **Test Often:** Run your app frequently during development
3. **Document as You Go:** Write notes while coding, not after
4. **Commit Frequently:** Small, frequent commits are better than large ones
5. **Learn from Errors:** Every error is a learning opportunity
6. **Ask for Help:** Use GitHub issues or community forums
7. **Stay Consistent:** Try to code a little bit every day
8. **Have Fun:** Enjoy the learning process! 🎉

---

**Remember:** The goal is learning, not perfection. Make mistakes, experiment, and grow! 🚀



<!-- 
cd /c/AgenticAIDevelopment/day17_crewai_intro
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
streamlit run streamlit_app.py -->

