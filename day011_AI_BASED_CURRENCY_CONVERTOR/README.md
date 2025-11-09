# 💱 AI-Powered Currency Converter

An intelligent currency conversion application powered by Google Gemini AI and LangChain, providing real-time exchange rates through natural language queries.

## 🌟 Features

- **Natural Language Processing**: Ask currency conversion questions in plain English
- **Real-time Exchange Rates**: Live data from ExchangeRate API
- **AI-Powered Agent**: Google Gemini AI with LangChain for intelligent query understanding
- **Multiple Interfaces**:
  - Chat-based natural language converter
  - Quick form-based converter
  - Conversation history tracking
- **Verbose Mode**: Debug and see detailed execution logs
- **Clean UI**: Modern, responsive Streamlit interface

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- ExchangeRate API key from [ExchangeRate-API](https://www.exchangerate-api.com/)

### Installation

1. **Clone or navigate to the project directory**:
```bash
cd day011_AI_BASED_CURRENCY_CONVERTOR
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up API keys** (Choose one method):

   **Method A: Using secrets.toml (Recommended)**
   
   Create a `.streamlit` folder and `secrets.toml` file:
   ```bash
   mkdir .streamlit
   ```
   
   Create `.streamlit/secrets.toml` with your API keys:
   ```toml
   GEMINI_API_KEY = "your-gemini-api-key-here"
   EXCHANGERATE_API_KEY = "your-exchangerate-api-key-here"
   ```

   **Method B: Using the UI**
   
   Run the app and enter your API keys in the input fields provided.

4. **Run the application**:
```bash
streamlit run streamlit_app.py
```

The app will open in your default browser at `http://localhost:8501`

## 📖 Usage

### Chat Converter
Use natural language to ask currency conversion questions:
- "Convert 100 USD to EUR"
- "How much is 50 GBP in Indian Rupees?"
- "What's 1000 JPY in USD?"

### Quick Convert
Use the form-based interface for quick conversions:
1. Enter the amount
2. Select source currency
3. Select target currency
4. Click "Quick Convert"

### Chat History
View all your previous conversions and responses in the Chat History tab.

## 🔧 Configuration

### Supported Currencies

The app supports 30+ major currencies including:
- USD, EUR, GBP, JPY, AUD, CAD, CHF, CNY
- INR, MXN, BRL, ZAR, KRW, SGD, HKD
- And many more...

### Verbose Mode

Enable verbose mode in the sidebar to see:
- Detailed agent execution logs
- Tool invocation details
- API request/response information

## 🏗️ Architecture

```
User Query → Streamlit UI → LangChain Agent → Currency Converter Tool
                                ↓
                          Google Gemini AI
                                ↓
                         ExchangeRate API
                                ↓
                        Formatted Response
```

### Components

- **Streamlit**: Web interface and user interaction
- **LangChain**: Agent framework and tool orchestration
- **Google Gemini**: AI model for understanding queries
- **ExchangeRate API**: Real-time currency exchange rates
- **Currency Converter Tool**: Custom LangChain tool for conversions

## 🛡️ Security

- API keys are stored securely in `secrets.toml` (which is gitignored)
- Sensitive data is never logged or exposed
- Password fields are used for API key input

## 📝 Example Queries

```
"Convert 100 USD to EUR"
"How much is 250 British Pounds in Canadian Dollars?"
"What's the exchange rate for 1000 Japanese Yen to US Dollars?"
"Convert 500 Indian Rupees to Singapore Dollars"
```

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📄 License

This project is open source and available for educational purposes.

## 🙏 Acknowledgments

- Google Gemini AI for natural language understanding
- ExchangeRate-API for real-time currency data
- LangChain for the agent framework
- Streamlit for the web interface

## 📧 Support

If you encounter any issues or have questions, please:
1. Check the verbose logs for detailed error information
2. Verify your API keys are correct
3. Ensure all dependencies are installed
4. Check your internet connection for API access

---

Built with ❤️ using LangChain, Google Gemini, and Streamlit





Here's a portfolio-ready paragraph for your AI Currency Converter project:

---

## 💱 AI-Powered Currency Converter

**Portfolio Description:**

Developed an intelligent currency conversion application that leverages AI agents to process natural language queries and provide real-time exchange rates. The system uses Google Gemini AI integrated with LangChain's agent framework to understand user intent from conversational inputs like "Convert 100 USD to EUR" and automatically invokes custom tools to fetch live currency data from ExchangeRate API. Built with **Streamlit** for an interactive web interface, **LangChain** for agent orchestration and tool integration, and **Google Gemini 2.0 Flash** for natural language understanding. Through this project, I gained hands-on experience in building agentic AI systems that can reason about user queries, make intelligent tool calls, and seamlessly integrate multiple APIs. Key learnings include implementing custom LangChain tools with the `@tool` decorator, managing agent workflows with function calling, handling API authentication securely using secrets management, and creating production-ready web applications with session state management and error handling. The project demonstrates practical applications of AI agents in real-world scenarios, showcasing how LLMs can be augmented with external tools to perform specific tasks beyond their training data.

---

**Short Version (if you need a more concise one):**



Description
Built an AI-powered currency converter using Google Gemini and LangChain that interprets natural language queries to provide real-time exchange rates. Implemented custom tools for API integration, created an agent-based system for intelligent query processing, and deployed a user-friendly Streamlit web interface. Gained expertise in agentic AI, tool calling, and production-ready application development with secure API management.

