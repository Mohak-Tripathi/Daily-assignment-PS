# 🔧 Setup Instructions for AI Currency Converter

This guide will help you set up and run the AI-powered Currency Converter application.

## 📋 Prerequisites

- **Python 3.8+** installed on your system
- **pip** (Python package installer)
- **Internet connection** for API calls
- **API Keys** (free to obtain):
  - Google Gemini API key
  - ExchangeRate API key

---

## 🔑 Step 1: Get Your API Keys

### 1.1 Google Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key (starts with `AIza...`)
5. Save it securely

**Note**: Gemini API has a free tier with generous limits for testing.

### 1.2 ExchangeRate API Key

1. Visit [ExchangeRate-API](https://www.exchangerate-api.com/)
2. Click "Get Free Key" or "Sign Up"
3. Enter your email and create an account
4. Copy your API key from the dashboard
5. Save it securely

**Free Tier**: 1,500 requests/month (plenty for testing)

---

## 🛠️ Step 2: Install Dependencies

### Option A: Using Virtual Environment (Recommended)

**Windows:**
```bash
# Navigate to project directory
cd day011_AI_BASED_CURRENCY_CONVERTOR

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Mac/Linux:**
```bash
# Navigate to project directory
cd day011_AI_BASED_CURRENCY_CONVERTOR

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Option B: System-wide Installation
```bash
cd day011_AI_BASED_CURRENCY_CONVERTOR
pip install -r requirements.txt
```

---

## ⚙️ Step 3: Configure API Keys

### Method A: Using secrets.toml (Recommended for Security)

1. **Create the secrets file**:
   ```bash
   # The .streamlit folder should already exist
   # If not, create it:
   mkdir .streamlit
   ```

2. **Copy the example file**:
   ```bash
   # Windows
   copy .streamlit\secrets.toml.example .streamlit\secrets.toml
   
   # Mac/Linux
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```

3. **Edit `.streamlit/secrets.toml`** with your actual API keys:
   ```toml
   GEMINI_API_KEY = "AIzaSy..."
   EXCHANGERATE_API_KEY = "7055bf..."
   ```

4. **Save the file**

**Important**: `.streamlit/secrets.toml` is in `.gitignore` and will NOT be committed to Git.

### Method B: Enter Keys in the UI

If you don't create `secrets.toml`, the app will prompt you to enter your API keys in the web interface when you run it.

---

## 🚀 Step 4: Run the Application

1. **Make sure you're in the project directory**:
   ```bash
   cd day011_AI_BASED_CURRENCY_CONVERTOR
   ```

2. **Activate virtual environment** (if using one):
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Run Streamlit**:
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Access the app**:
   - Your default browser should open automatically
   - If not, navigate to: `http://localhost:8501`

---

## 🎯 Step 5: Using the Application

### Chat Converter (Natural Language)

1. Go to the "💬 Chat Converter" tab
2. Type your query naturally:
   - "Convert 100 USD to EUR"
   - "How much is 50 GBP in Indian Rupees?"
3. Click "🔄 Convert"
4. View the AI-generated response

### Quick Convert (Form-based)

1. Go to the "📊 Quick Convert" tab
2. Enter amount (e.g., 100)
3. Select source currency (e.g., USD)
4. Select target currency (e.g., INR)
5. Click "🔄 Quick Convert"
6. View instant results

### Chat History

- View all your previous conversions in the "📜 Chat History" tab
- Clear history anytime with the "🗑️ Clear History" button

---

## 🔍 Troubleshooting

### Issue: "API keys not found"
**Solution**: Make sure you've created `.streamlit/secrets.toml` with valid keys, or enter them in the UI.

### Issue: "ModuleNotFoundError"
**Solution**: 
```bash
pip install -r requirements.txt --upgrade
```

### Issue: "Conversion failed"
**Solution**: 
- Check your ExchangeRate API key is valid
- Verify you haven't exceeded free tier limits
- Check internet connection

### Issue: "Invalid API key" for Gemini
**Solution**:
- Verify your Gemini API key is correct
- Make sure you've enabled the Gemini API in Google AI Studio
- Check for extra spaces in the secrets.toml file

### Issue: App is slow
**Solution**:
- This is normal for first request (cold start)
- Subsequent requests should be faster
- Enable "Verbose Mode" to see detailed logs

---

## 🎨 Features to Try

1. **Natural Language Queries**:
   - "What's 1000 Japanese Yen in US Dollars?"
   - "Convert 250 euros to Canadian dollars"
   
2. **Multiple Currencies**:
   - Try different currency pairs
   - App supports 30+ major currencies

3. **Verbose Mode**:
   - Toggle in sidebar
   - See detailed execution logs
   - Useful for debugging

4. **Chat History**:
   - Review past conversions
   - Compare rates over time

---

## 📦 Package Information

### Required Packages:
- `streamlit` - Web interface
- `langchain` - Agent framework
- `langchain-google-genai` - Gemini AI integration
- `langchain-community` - Community tools
- `requests` - HTTP requests
- `google-generativeai` - Google AI SDK

### Package Compatibility:
All packages are compatible and tested. No `langchain_core` is directly installed (it's a dependency that will be auto-installed if needed).

---

## 🔐 Security Notes

1. **Never commit** `.streamlit/secrets.toml` to Git (it's in `.gitignore`)
2. **Never share** your API keys publicly
3. **Rotate keys** if accidentally exposed
4. **Use environment variables** in production

---

## 🆘 Getting Help

If you encounter issues:

1. Check the verbose logs (enable in sidebar)
2. Review the error messages
3. Verify API keys are correct
4. Check internet connectivity
5. Ensure all dependencies are installed

---

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangChain Documentation](https://python.langchain.com/)
- [Google Gemini API Docs](https://ai.google.dev/docs)
- [ExchangeRate-API Docs](https://www.exchangerate-api.com/docs)

---

## 🎉 You're All Set!

Enjoy using your AI-powered Currency Converter! 💱🤖

---

**Last Updated**: November 2025

