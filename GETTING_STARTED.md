# 🎯 Getting Started - Your First 30 Minutes

Welcome! This guide will get you up and running in 30 minutes or less.

## ✅ Pre-Flight Checklist

Before you begin, make sure you have:
- [ ] Python 3.8+ installed (`python --version`)
- [ ] Git installed (`git --version`)
- [ ] A code editor (VS Code recommended)
- [ ] A GitHub account
- [ ] Terminal/Command Prompt access

## 🚀 30-Minute Setup

### Step 1: Verify Your Setup (2 minutes)

Open your terminal and run:

```bash
# Check Python
python --version
# Should show: Python 3.8.x or higher

# Check pip
pip --version
# Should show pip version

# Check Git
git --version
# Should show git version
```

✅ **All working?** Continue to Step 2!
❌ **Something missing?** Install the missing tool first.

### Step 2: Initialize Git Repository (3 minutes)

```bash
# Navigate to your project folder
cd C:\AgenticAIDevelopment

# Initialize git
git init

# Add all files
git add .

# First commit
git commit -m "Initial project setup with complete structure"
```

### Step 3: Create GitHub Repository (5 minutes)

1. Go to [github.com](https://github.com)
2. Click "+" → "New repository"
3. Name it: `AgenticAIDevelopment`
4. Keep it **Public** (or Private if you prefer)
5. **Don't** initialize with README (we already have one)
6. Click "Create repository"

Then in your terminal:

```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/AgenticAIDevelopment.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 4: Set Up Virtual Environment (5 minutes)

**Choose your approach:**

#### Option A: Global Virtual Environment (Recommended)

```bash
# From project root
cd C:\AgenticAIDevelopment

# Create virtual environment
python -m venv .venv

# Activate it
.venv\Scripts\activate

# You should see (.venv) in your prompt
```

#### Option B: Per-Assignment Virtual Environment

```bash
# Navigate to template
cd C:\AgenticAIDevelopment\day00_template

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# You should see (venv) in your prompt
```

### Step 5: Test the Template (10 minutes)

```bash
# Make sure you're in day00_template and venv is activated
cd day00_template

# Install dependencies
pip install -r requirements.txt

# This will install Streamlit and other packages
# Should take 2-3 minutes

# Run the template app
streamlit run streamlit_app.py

# Your browser should open automatically to http://localhost:8501
```

**Explore the template:**
- ✅ Click buttons and test interactions
- ✅ Try the sidebar settings
- ✅ Check the metrics display
- ✅ Test the text input

**Stop the app:**
- Press `Ctrl+C` in terminal

### Step 6: Create Your First Assignment (5 minutes)

```bash
# Go back to project root
cd ..

# Copy template to new assignment
cp -r day00_template day01_hello_world

# Navigate to new assignment
cd day01_hello_world

# Open in your editor
code streamlit_app.py
# Or: notepad streamlit_app.py
```

**Make a simple change:**

Replace the title in `streamlit_app.py` (around line 41):

```python
# Change from:
st.title("🤖 Agentic AI Assignment Template")

# To:
st.title("👋 Hello World - My First Assignment")
```

**Test your change:**

```bash
# Make sure venv is activated
streamlit run streamlit_app.py
```

You should see your new title! 🎉

## 🎓 What You've Accomplished

In 30 minutes, you've:
- ✅ Set up Git and GitHub
- ✅ Created a virtual environment
- ✅ Tested the template
- ✅ Created your first assignment
- ✅ Made your first modification

## 📚 Next Steps

### Immediate (Today)

1. **Read the documentation:**
   - [ ] [QUICK_START.md](QUICK_START.md) - Fast reference
   - [ ] [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md) - Complete workflow

2. **Customize your first assignment:**
   - [ ] Update `day01_hello_world/README.md`
   - [ ] Add your own features to the app
   - [ ] Test thoroughly

3. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Create day01: Hello World assignment"
   git push
   ```

### This Week

1. **Complete 3-5 simple assignments:**
   - Day 01: Hello World (done!)
   - Day 02: Simple calculator
   - Day 03: Text analyzer
   - Day 04: Data display
   - Day 05: User input forms

2. **Learn Streamlit basics:**
   - Widgets (buttons, inputs, sliders)
   - Layout (columns, sidebar, containers)
   - Session state
   - File uploads

3. **Deploy your first app:**
   - Follow [deployment guide](setup_guide.md#deployment)
   - Share your live demo link!

### This Month

1. **Integrate LLM APIs:**
   - Get OpenAI API key
   - Build a simple chatbot
   - Experiment with prompts

2. **Learn LangChain:**
   - Chains and prompts
   - Memory systems
   - Document loaders

3. **Build RAG system:**
   - Vector databases
   - Embeddings
   - Retrieval

## 🆘 Troubleshooting

### Virtual Environment Won't Activate

**Problem:** `activate` command not found

**Solution:**
```bash
# Try full path
C:\AgenticAIDevelopment\.venv\Scripts\activate

# Or use forward slashes
C:/AgenticAIDevelopment/.venv/Scripts/activate
```

### Streamlit Won't Install

**Problem:** `pip install streamlit` fails

**Solution:**
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Then try again
pip install streamlit
```

### Port Already in Use

**Problem:** "Address already in use" error

**Solution:**
```bash
# Use different port
streamlit run streamlit_app.py --server.port 8502
```

### Can't Push to GitHub

**Problem:** Authentication failed

**Solution:**
1. Use Personal Access Token instead of password
2. Go to GitHub → Settings → Developer settings → Personal access tokens
3. Generate new token with `repo` scope
4. Use token as password when pushing

## 📖 Learning Resources

### Essential Reading
- [Streamlit Docs](https://docs.streamlit.io/) - Official documentation
- [Streamlit Cheat Sheet](https://docs.streamlit.io/library/cheatsheet) - Quick reference
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html) - Official guide

### Video Tutorials
- [Streamlit in 6 Minutes](https://www.youtube.com/watch?v=_9WiB2PDO7k)
- [Streamlit Crash Course](https://www.youtube.com/watch?v=JwSS70SZdyM)

### Community
- [Streamlit Forum](https://discuss.streamlit.io/) - Ask questions
- [Streamlit Gallery](https://streamlit.io/gallery) - Get inspired

## 💡 Pro Tips

1. **Use the template:** Always start by copying `day00_template`
2. **Commit often:** Small commits are easier to manage
3. **Test locally first:** Always test before deploying
4. **Read error messages:** They usually tell you what's wrong
5. **Use the docs:** Streamlit docs are excellent
6. **Start simple:** Build basic version first, then add features
7. **Document as you go:** Write notes while coding
8. **Have fun:** Enjoy the learning process!

## ✅ Daily Checklist

Use this checklist for each assignment:

```markdown
### Day XX: [Assignment Name]

Setup:
- [ ] Copy template to new folder
- [ ] Activate virtual environment
- [ ] Install dependencies

Development:
- [ ] Update app title and description
- [ ] Implement core functionality
- [ ] Add error handling
- [ ] Test all features

Documentation:
- [ ] Update assignment README
- [ ] Add comments to code
- [ ] Document learnings

Git:
- [ ] Commit changes
- [ ] Push to GitHub
- [ ] Update main README

Deployment (optional):
- [ ] Deploy to Streamlit Cloud
- [ ] Test deployed version
- [ ] Add live demo link
```

## 🎯 Your First Week Goals

By the end of Week 1, you should:
- [ ] Complete 5 basic assignments
- [ ] Understand virtual environments
- [ ] Be comfortable with Git workflow
- [ ] Know Streamlit basics
- [ ] Have deployed at least 1 app

## 🎉 Congratulations!

You're all set up and ready to start your Agentic AI learning journey!

**Remember:**
- Take it one day at a time
- Don't worry about perfection
- Learn from mistakes
- Ask for help when needed
- Celebrate small wins

**Now go build something amazing! 🚀**

---

**Need help?** Check:
1. [QUICK_START.md](QUICK_START.md) - Fast reference
2. [setup_guide.md](setup_guide.md) - Detailed setup
3. [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md) - Complete workflow
4. [Streamlit Forum](https://discuss.streamlit.io/) - Community help

