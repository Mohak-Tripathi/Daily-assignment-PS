# 🚀 Quick Start Guide

This is a quick reference for getting started with your daily assignments. For detailed information, see [setup_guide.md](setup_guide.md).

## First Time Setup

### 1. Install Python
Make sure you have Python 3.8 or higher installed:
```bash
python --version
```

### 2. Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/AgenticAIDevelopment.git
cd AgenticAIDevelopment
```

### 3. Choose Your Virtual Environment Strategy

#### Option A: Global Virtual Environment (Easier)
```bash
# Create virtual environment at project root
python -m venv .venv

# Activate it
.venv\Scripts\activate  # Windows Command Prompt
# OR
source .venv/Scripts/activate  # Git Bash
```

#### Option B: Per-Assignment Virtual Environment (More Isolated)
```bash
# Navigate to assignment folder
cd day01_assignment_name

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate  # Windows Command Prompt
```

## Daily Workflow

### Starting a New Assignment

1. **Copy the template:**
   ```bash
   # From project root
   cp -r day00_template day01_my_new_assignment
   cd day01_my_new_assignment
   ```

2. **Activate virtual environment:**
   ```bash
   # If using global venv (from project root)
   .venv\Scripts\activate
   
   # If using per-assignment venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start coding:**
   - Edit `streamlit_app.py`
   - Add any new packages you need:
     ```bash
     pip install package-name
     pip freeze > requirements.txt
     ```

5. **Run your app:**
   ```bash
   streamlit run streamlit_app.py
   ```

### Working on Existing Assignment

```bash
# 1. Navigate to assignment
cd day01_assignment_name

# 2. Activate virtual environment
.venv\Scripts\activate  # or venv\Scripts\activate

# 3. Run the app
streamlit run streamlit_app.py
```

### Finishing Up

```bash
# 1. Save dependencies
pip freeze > requirements.txt

# 2. Deactivate virtual environment
deactivate

# 3. Commit your work
git add .
git commit -m "Complete day01 assignment"
git push
```

## Common Commands Cheat Sheet

### Virtual Environment
```bash
# Create
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Deactivate
deactivate

# Check if active (should show venv path)
where python
```

### Package Management
```bash
# Install package
pip install package-name

# Install specific version
pip install package-name==1.2.3

# Install from requirements.txt
pip install -r requirements.txt

# List installed packages
pip list

# Save current packages
pip freeze > requirements.txt

# Uninstall package
pip uninstall package-name
```

### Streamlit
```bash
# Run app
streamlit run streamlit_app.py

# Run on different port
streamlit run streamlit_app.py --server.port 8502

# Clear cache
streamlit cache clear
```

### Git
```bash
# Check status
git status

# Add files
git add .

# Commit
git commit -m "Your message"

# Push to GitHub
git push

# Pull latest changes
git pull
```

## Deployment to Streamlit Cloud

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Ready to deploy"
   git push
   ```

2. **Deploy:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository
   - Set main file path: `dayXX_assignment_name/streamlit_app.py`
   - Add secrets if needed (Settings → Secrets)
   - Click "Deploy"!

## Managing Secrets

### Local Development
Create `.streamlit/secrets.toml` in your assignment folder:
```toml
OPENAI_API_KEY = "sk-your-key-here"
```

### Streamlit Cloud
Add secrets in the app dashboard:
1. Go to your deployed app
2. Click "Settings" → "Secrets"
3. Paste your secrets in TOML format
4. Save

## Troubleshooting

### Virtual environment not activating
```bash
# Try full path
C:\AgenticAIDevelopment\.venv\Scripts\activate
```

### Package not found
```bash
# Make sure venv is activated (you should see (.venv) or (venv) in prompt)
# Then reinstall
pip install -r requirements.txt
```

### Port already in use
```bash
# Use different port
streamlit run streamlit_app.py --server.port 8502
```

### Import errors
```bash
# Upgrade all packages
pip install --upgrade -r requirements.txt
```

## Need More Help?

- **Detailed Setup:** See [setup_guide.md](setup_guide.md)
- **Project Structure:** See [README.md](README.md)
- **Template Example:** Check `day00_template/` folder
- **Streamlit Docs:** https://docs.streamlit.io/

---

**Remember:** Always activate your virtual environment before working! 🎯

