# 🚀 Quick Start Guide

## MCP Multi-Service Dashboard API

A comprehensive FastAPI application with AI-powered dashboards for both Outlook Email and GitHub repositories.

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## ⚡ Quick Installation

### Option 1: Automatic Installation
```bash
python install.py
```

### Option 2: Manual Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Create environment file
cp env_template.txt .env
# Edit .env with your API keys
```

## 🔑 Setup API Keys

1. **Microsoft OAuth** (for Outlook):
   - Go to [Azure Portal](https://portal.azure.com)
   - Create an app registration
   - Get Client ID and Client Secret
   - Add to `.env` file

2. **GitHub OAuth** (for GitHub):
   - Go to [GitHub Developer Settings](https://github.com/settings/developers)
   - Create new OAuth App
   - Get Client ID and Client Secret
   - Add to `.env` file

3. **Google Gemini AI** (for AI features):
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create API key
   - Add to `.env` file

## 🏃‍♂️ Running the Application

### Option 1: Smart Startup
```bash
python start.py
```

### Option 2: Direct Start
```bash
python main.py
```

### Option 3: Uvicorn
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🌐 Access the Application

1. Open your browser
2. Go to `http://localhost:8000`
3. Choose your service (Outlook or GitHub)
4. Authenticate and enjoy!

## 📁 Project Structure

```
_MCP_Agent/
├── api/                    # Backend API
│   ├── models/            # Data models
│   ├── routers/           # API endpoints
│   ├── services/          # Business logic
│   └── auth.py           # Authentication
├── frontend/              # Frontend templates
│   └── templates/         # HTML templates
├── main.py               # Application entry point
├── start.py              # Smart startup script
├── install.py            # Installation script
├── requirements.txt      # Python dependencies
└── .env                 # Environment variables
```

## 🔧 Troubleshooting

### Common Issues

1. **Import Error**: Run `python install.py` to install dependencies
2. **Authentication Error**: Check your API keys in `.env` file
3. **Port Already in Use**: Change port in `main.py` or kill existing process
4. **Template Not Found**: Ensure all files are in correct directories

### Debug Mode

```bash
# Run with verbose output
python -v start.py
```

## 📚 Features

### Outlook Dashboard
- 📧 Email summarization
- 📊 Email statistics
- 🤖 AI-powered insights
- 💬 Email assistant chatbot

### GitHub Dashboard
- 🐙 Repository analysis
- 🐛 Issue tracking
- 🔀 Pull request monitoring
- 📈 Activity insights
- 🤖 GitHub assistant chatbot

## 🆘 Support

If you encounter issues:

1. Check the console output for error messages
2. Verify all API keys are correct
3. Ensure all dependencies are installed
4. Check file permissions and paths

## 📄 License

This project is licensed under the MIT License. 