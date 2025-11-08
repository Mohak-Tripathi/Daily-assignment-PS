# Day 00 - Streamlit Template

## 📝 Description

This is a template project for Agentic AI assignments. It demonstrates the basic structure and best practices for building Streamlit applications.

## 🎯 Learning Objectives

- Understand Streamlit app structure
- Learn session state management
- Practice proper error handling
- Implement secrets management
- Create clean, user-friendly interfaces

## 🚀 Features

- Clean, organized code structure
- Session state management
- API key configuration (UI + secrets)
- Responsive layout with sidebar
- Example components (buttons, inputs, metrics)
- Error handling
- Professional UI/UX

## 📦 Dependencies

See `requirements.txt` for the full list. Main dependencies:
- `streamlit>=1.30.0`
- `python-dotenv>=1.0.0`

## 🛠️ Setup

### 1. Create Virtual Environment

```bash
# Navigate to this folder
cd day00_template

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows (Command Prompt):
venv\Scripts\activate
# On Windows (Git Bash):
source venv/Scripts/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Secrets (Optional)

Create `.streamlit/secrets.toml`:

```toml
OPENAI_API_KEY = "your-api-key-here"
ANTHROPIC_API_KEY = "your-api-key-here"
```

**Note:** This file is gitignored and won't be committed.

### 4. Run the App

```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
day00_template/
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── utils/
│   └── __init__.py          # Helper functions (add as needed)
├── tests/
│   └── test_app.py          # Tests (optional)
├── requirements.txt         # Python dependencies
├── streamlit_app.py         # Main application
└── README.md               # This file
```

## 🎨 Customization

### Modify Theme

Edit `.streamlit/config.toml` to change colors and appearance:

```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

### Add New Features

1. Create helper functions in `utils/` folder
2. Import them in `streamlit_app.py`
3. Add new UI components in the main function

## 🚢 Deployment

### Deploy to Streamlit Community Cloud

1. Push this folder to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Select your repository
5. Set main file path: `day00_template/streamlit_app.py`
6. Add secrets in the Streamlit Cloud dashboard (if needed)
7. Click "Deploy"!

## 📚 Key Concepts Demonstrated

### 1. Page Configuration
```python
st.set_page_config(
    page_title="My App",
    page_icon="🤖",
    layout="wide"
)
```

### 2. Session State
```python
if "counter" not in st.session_state:
    st.session_state.counter = 0
```

### 3. Secrets Management
```python
api_key = st.secrets["OPENAI_API_KEY"]
```

### 4. Layout
```python
col1, col2 = st.columns([2, 1])
with col1:
    st.write("Main content")
```

### 5. Error Handling
```python
try:
    main()
except Exception as e:
    st.error(f"Error: {str(e)}")
```

## 🐛 Troubleshooting

### App won't start
- Make sure virtual environment is activated
- Check that all dependencies are installed: `pip list`
- Verify Python version: `python --version` (should be 3.8+)

### Import errors
```bash
pip install --upgrade -r requirements.txt
```

### Port already in use
```bash
streamlit run streamlit_app.py --server.port 8502
```

## 📖 Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit API Reference](https://docs.streamlit.io/library/api-reference)
- [Streamlit Gallery](https://streamlit.io/gallery)

## ✅ Checklist for New Assignments

When creating a new assignment based on this template:

- [ ] Copy this folder and rename it (e.g., `day01_my_assignment`)
- [ ] Update this README with assignment-specific information
- [ ] Modify `streamlit_app.py` with your logic
- [ ] Update `requirements.txt` with needed packages
- [ ] Test locally before deploying
- [ ] Update main repository README with assignment link
- [ ] Deploy to Streamlit Cloud
- [ ] Add live demo link to main README

## 📝 Notes

Add your personal notes and learnings here as you work through the assignment.

---

**Happy Coding! 🎉**



# Then for day02
# 1. Navigate to assignment
cd day00_chains

# 2. Create virtual environment
python -m venv venv

# 3. Activate (Git Bash syntax)
source venv/Scripts/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run your app
streamlit run streamlit_app.py


# Upgrade pip first (recommended)
pip install --upgrade pip

# Install the packages for day007
pip install langchain-community langchain-google-genai pypdf wikipedia beautifulsoup4 lxml jupyter

