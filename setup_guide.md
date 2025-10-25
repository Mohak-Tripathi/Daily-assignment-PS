# Python Virtual Environment Setup Guide

This guide will help you understand and set up Python virtual environments for your Agentic AI assignments. Virtual environments are essential for managing dependencies and keeping your projects isolated.

## 📖 What is a Virtual Environment?

A virtual environment is an isolated Python environment that allows you to:
- Install packages without affecting your system Python
- Use different package versions for different projects
- Keep your project dependencies organized and reproducible
- Avoid conflicts between project requirements

Think of it as a separate "workspace" for each project!

## 🎯 Two Approaches for This Repository

### Option 1: Global Virtual Environment (Recommended for Beginners)

**Pros:**
- Simpler to manage
- One environment for all assignments
- Less disk space used

**Cons:**
- All assignments share the same package versions
- Potential for dependency conflicts if assignments need different versions

### Option 2: Per-Assignment Virtual Environments

**Pros:**
- Complete isolation between assignments
- Each assignment has its own dependencies
- No conflicts between different package versions

**Cons:**
- More disk space used
- Need to activate different environments for different assignments

## 🚀 Step-by-Step Setup

### Option 1: Global Virtual Environment

#### 1. Create the Virtual Environment

Open your terminal (Git Bash or Command Prompt) in the project root:

```bash
# Navigate to project root
cd C:\AgenticAIDevelopment

# Create virtual environment
python -m venv .venv
```

This creates a `.venv` folder containing your isolated Python environment.

#### 2. Activate the Virtual Environment

**On Windows (Command Prompt):**
```bash
.venv\Scripts\activate
```

**On Windows (Git Bash):**
```bash
source .venv/Scripts/activate
```

**On Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

You'll see `(.venv)` appear at the start of your command prompt, indicating the environment is active.

#### 3. Install Dependencies for an Assignment

```bash
# Navigate to an assignment folder
cd day01_assignment_name

# Install its dependencies
pip install -r requirements.txt
```

#### 4. Run Your Streamlit App

```bash
streamlit run streamlit_app.py
```

#### 5. Deactivate When Done

```bash
deactivate
```

---

### Option 2: Per-Assignment Virtual Environments

#### 1. Navigate to an Assignment Folder

```bash
cd C:\AgenticAIDevelopment\day01_assignment_name
```

#### 2. Create Virtual Environment

```bash
python -m venv venv
```

This creates a `venv` folder inside the assignment directory.

#### 3. Activate the Virtual Environment

**On Windows (Command Prompt):**
```bash
venv\Scripts\activate
```

**On Windows (Git Bash):**
```bash
source venv/Scripts/activate
```

You'll see `(venv)` at the start of your prompt.

#### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 5. Run Your App

```bash
streamlit run streamlit_app.py
```

#### 6. Deactivate When Done

```bash
deactivate
```

## 🔄 Daily Workflow

### When Starting Work:

1. Open terminal in project root (or assignment folder)
2. Activate virtual environment
3. Navigate to assignment folder (if using global venv)
4. Start coding!

### When Installing New Packages:

```bash
# Make sure virtual environment is activated
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt
```

### When Finishing Work:

```bash
# Save your requirements
pip freeze > requirements.txt

# Deactivate virtual environment
deactivate

# Commit your changes
git add .
git commit -m "Completed day01 assignment"
git push
```

## 🛠️ Useful Commands

### Check if Virtual Environment is Active
```bash
# Your prompt should show (venv) or (.venv)
# Or check Python location:
which python    # Git Bash
where python    # Command Prompt
```

### List Installed Packages
```bash
pip list
```

### Install Specific Package Version
```bash
pip install package-name==1.2.3
```

### Upgrade a Package
```bash
pip install --upgrade package-name
```

### Uninstall a Package
```bash
pip uninstall package-name
```

### Create requirements.txt
```bash
pip freeze > requirements.txt
```

### Install from requirements.txt
```bash
pip install -r requirements.txt
```

## ❗ Troubleshooting

### Problem: "python: command not found"

**Solution:** Make sure Python is installed and added to PATH
```bash
# Check Python installation
python --version
# or
python3 --version
```

### Problem: "Scripts\activate: Permission denied" (PowerShell)

**Solution:** Run PowerShell as Administrator and execute:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Problem: Virtual environment not activating

**Solution:** 
1. Make sure you're in the correct directory
2. Check the path to activate script
3. Try using the full path:
   ```bash
   C:\AgenticAIDevelopment\.venv\Scripts\activate
   ```

### Problem: Wrong Python version in virtual environment

**Solution:** Specify Python version when creating venv:
```bash
python3.11 -m venv .venv
```

### Problem: Packages not found after activation

**Solution:** Make sure you're installing in the activated environment:
```bash
# Check pip location
which pip    # Should point to your venv

# Reinstall packages
pip install -r requirements.txt
```

## 🎓 Best Practices

1. **Always activate before working**: Get in the habit of activating your virtual environment first thing
2. **Keep requirements.txt updated**: Run `pip freeze > requirements.txt` after installing new packages
3. **Don't commit virtual environments**: The `.gitignore` file excludes venv folders
4. **Use meaningful names**: If creating multiple venvs, use descriptive names
5. **Document dependencies**: Add comments in requirements.txt for complex packages
6. **Test in clean environment**: Occasionally create a fresh venv to test your requirements.txt

## 📦 Common Packages for Agentic AI

Here are packages you'll likely use across assignments:

```txt
# Core
streamlit>=1.30.0
python-dotenv>=1.0.0

# LLM Frameworks
langchain>=0.1.0
langchain-community>=0.0.10
langgraph>=0.0.20
langchain-openai>=0.0.5

# LLM APIs
openai>=1.0.0
anthropic>=0.8.0

# Data & Utilities
pandas>=2.0.0
numpy>=1.24.0
requests>=2.31.0

# Vector Stores (as needed)
chromadb>=0.4.0
faiss-cpu>=1.7.4
```

## 🚢 Deployment Considerations

When deploying to Streamlit Community Cloud:
- You **don't** need to include the virtual environment
- Only `requirements.txt` is needed
- Streamlit Cloud creates its own environment
- Make sure all dependencies are in `requirements.txt`

## 🔐 Managing Secrets

### Local Development

Create `.streamlit/secrets.toml` in your assignment folder:

```toml
# .streamlit/secrets.toml
OPENAI_API_KEY = "sk-..."
ANTHROPIC_API_KEY = "sk-ant-..."
```

Access in your code:
```python
import streamlit as st

api_key = st.secrets["OPENAI_API_KEY"]
```

### Streamlit Cloud

1. Deploy your app
2. Go to app settings
3. Click "Secrets"
4. Paste your secrets in TOML format
5. Save

## 📚 Additional Resources

- [Python venv documentation](https://docs.python.org/3/library/venv.html)
- [pip documentation](https://pip.pypa.io/en/stable/)
- [Streamlit deployment guide](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app)
- [Python packaging guide](https://packaging.python.org/en/latest/tutorials/installing-packages/)

---

**Need Help?** Open an issue in this repository or check the official Python documentation!

