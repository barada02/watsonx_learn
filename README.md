# Watson Orchestrate Learning Project

A comprehensive guide and toolkit for working with IBM Watson Orchestrate, including agent development, deployment, and interaction.

## 📁 Project Structure

```
watsonx_learn/
├── bobenv/                          # Virtual environment (not in git)
├── adk-project/                     # ADK project directory
│   ├── agents/                      # Agent definitions (.yaml)
│   │   └── contact_manager_agent.yaml
│   ├── tools/                       # Tool implementations (.py)
│   │   └── contact_tools_decorated.py
│   ├── knowledge/                   # Knowledge bases
│   ├── flows/                       # Workflow definitions
│   ├── QUICKSTART.md               # Quick start guide
│   └── TOOL_CREATION_GUIDE.md      # Tool creation guide
├── run_agent.py                     # Simple Python agent runner
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment template
├── .env                            # Your credentials (not in git)
├── AGENT_RUNNER_GUIDE.md           # Guide for running agents
├── WATSON_ORCHESTRATE_SKILL.md     # Complete Watson Orchestrate guide
├── SETUP_COMPLETE.md               # Setup summary
├── setup_env.md                    # Environment setup commands
└── README.md                       # This file
```

## 🚀 Quick Start

### 1. Setup Virtual Environment

```bash
# Activate virtual environment
.\bobenv\Scripts\Activate.ps1  # Windows PowerShell
# or
source bobenv/bin/activate     # Linux/Mac
```

### 2. Configure Watson Orchestrate

```bash
# Add your Watson Orchestrate environment
orchestrate env add --name bobenv --url <YOUR_ORCHESTRATE_URL>

# Activate it
orchestrate env activate bobenv

# Verify
orchestrate env list
```

### 3. Run a Deployed Agent

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your credentials

# Run the agent
python run_agent.py
```

## 📚 Documentation

### Core Guides

1. **[WATSON_ORCHESTRATE_SKILL.md](WATSON_ORCHESTRATE_SKILL.md)** - Complete Watson Orchestrate guide
   - Environment setup
   - Tool creation with `@tool` decorator
   - Agent creation and deployment
   - Testing and troubleshooting
   - Best practices

2. **[AGENT_RUNNER_GUIDE.md](AGENT_RUNNER_GUIDE.md)** - Running deployed agents with Python
   - Simple Python script usage
   - Authentication and token management
   - Message sending and response handling
   - Comparison with FastAPI version
   - Advanced usage examples

3. **[SETUP_COMPLETE.md](SETUP_COMPLETE.md)** - Setup summary and next steps

4. **[setup_env.md](setup_env.md)** - Environment setup commands

### ADK Project Guides

5. **[adk-project/QUICKSTART.md](adk-project/QUICKSTART.md)** - Quick start for ADK projects

6. **[adk-project/TOOL_CREATION_GUIDE.md](adk-project/TOOL_CREATION_GUIDE.md)** - Detailed tool creation guide

## 🛠️ Key Features

### 1. Agent Runner Script ([`run_agent.py`](run_agent.py))

A simple, standalone Python script to interact with deployed Watson Orchestrate agents:

- ✅ **Authentication**: Automatic token management with caching
- ✅ **Thread Management**: Create and manage conversation threads
- ✅ **Message Handling**: Send queries and receive responses
- ✅ **Response Processing**: Handles both inline and polled responses
- ✅ **Interactive Mode**: Chat with your agent in the terminal
- ✅ **Library Usage**: Import and use in your own scripts

**Example Usage:**
```python
from run_agent import WatsonxOrchestrate

client = WatsonxOrchestrate(
    thread_endpoint="https://...",
    token_endpoint="https://...",
    api_key="your_key"
)

result = client.send_message(
    query="Hello!",
    agent_id="your_agent_id"
)

print(result['response'])
```

### 2. Personal Contact Manager Agent

A fully functional agent with tools for:
- Adding contacts
- Searching contacts
- Updating contact information
- Deleting contacts
- Listing and categorizing contacts

## 📋 Requirements

- Python 3.8 or higher
- IBM Watson Orchestrate account
- IBM Cloud API key
- Deployed Watson Orchestrate agent

## 🔧 Installation

### Step 1: Clone and Setup

```bash
# Navigate to project directory
cd watsonx_learn

# Activate virtual environment
.\bobenv\Scripts\Activate.ps1  # Windows
# or
source bobenv/bin/activate     # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment

Create a `.env` file from the template:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```bash
THREAD_ENDPOINT=https://your-instance.watsonx.orchestrate.ibm.com/v1/threads
TOKEN_ENDPOINT=https://iam.cloud.ibm.com/identity/token
API_KEY=your_api_key_here
AGENT_ID=your_agent_id_here
```

### Step 3: Deploy Your Agent

```bash
# Import tools
orchestrate tools import --kind python --file adk-project/tools/contact_tools_decorated.py

# Import agent
orchestrate agents import --file adk-project/agents/contact_manager_agent.yaml

# Deploy agent
orchestrate agents deploy --name personal_contact_manager

# Get agent ID
orchestrate agents list
```

## 🎯 Usage Examples

### Running the Agent Script

```bash
# Basic usage
python run_agent.py

# The script will:
# 1. Authenticate with Watson Orchestrate
# 2. Run example queries
# 3. Enter interactive mode
```

### Using as a Library

```python
from run_agent import WatsonxOrchestrate
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize client
client = WatsonxOrchestrate(
    thread_endpoint=os.getenv("THREAD_ENDPOINT"),
    token_endpoint=os.getenv("TOKEN_ENDPOINT"),
    api_key=os.getenv("API_KEY")
)

# Send a message
result = client.send_message(
    query="What can you help me with?",
    agent_id=os.getenv("AGENT_ID")
)

print(f"Response: {result['response']}")
print(f"Thread ID: {result['thread_id']}")

# Continue conversation
result2 = client.send_message(
    query="Tell me more",
    agent_id=os.getenv("AGENT_ID"),
    thread_id=result['thread_id']
)

print(f"Response: {result2['response']}")

# Clean up
client.close()
```

### Interactive Chat

```bash
$ python run_agent.py

============================================================
Watsonx Orchestrate Agent Runner
============================================================

Fetching new authentication token...
✓ Token obtained successfully

--- Example 1: Single Message ---

Sending message to agent 'your_agent_id'...
Query: Hello! Can you help me?
✓ Received inline response

Agent Response:
Of course! I'm here to help. What do you need assistance with?
Thread ID: thread_abc123

--- Interactive Mode ---
Type your messages (or 'quit' to exit):

You: What can you do?

Agent: I can help you manage your contacts...

You: quit
Goodbye!

✓ Session closed
```

## 🔑 Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `THREAD_ENDPOINT` | Yes | Thread operations endpoint | `https://instance.watsonx.orchestrate.ibm.com/v1/threads` |
| `TOKEN_ENDPOINT` | Yes | Authentication endpoint | `https://iam.cloud.ibm.com/identity/token` |
| `API_KEY` | Yes | IBM Cloud API key | `your_api_key_here` |
| `AGENT_ID` | Yes* | Deployed agent ID | `agent_123` |
| `TOKEN_TTL_SECONDS` | No | Token cache duration | `3000` (default: 50 min) |

*Can be provided at runtime if not in `.env`

## 🧪 Testing

### Test the Agent Runner

```bash
# Run with your deployed agent
python run_agent.py
```

### Test with Watson Orchestrate CLI

```bash
# Interactive chat
orchestrate chat ask --agent-name your_agent_name

# Web UI
orchestrate chat start
```

## 📖 Common Commands

### Environment Management
```bash
orchestrate env list                    # List environments
orchestrate env activate <name>         # Activate environment
orchestrate env add --name <name> --url <url>  # Add environment
```

### Agent Management
```bash
orchestrate agents list                 # List agents
orchestrate agents deploy --name <name> # Deploy agent
orchestrate agents export --name <name> # Export agent
```

### Tool Management
```bash
orchestrate tools list                  # List tools
orchestrate tools import --kind python --file <path>  # Import tool
```

## 🐛 Troubleshooting

### Issue: "Missing required environment variables"
**Solution**: Ensure `.env` file exists with all required variables

### Issue: "Authentication server did not return a token"
**Solution**: Verify API key and TOKEN_ENDPOINT are correct

### Issue: "Server did not return a thread_id"
**Solution**: Check THREAD_ENDPOINT and ensure agent is deployed

### Issue: "Polling timed out"
**Solution**: Increase timeout in code or check agent status

See [AGENT_RUNNER_GUIDE.md](AGENT_RUNNER_GUIDE.md) for detailed troubleshooting.

## 🔗 Resources

- [Watson Orchestrate Documentation](https://developer.watson-orchestrate.ibm.com/)
- [IBM Cloud API Keys](https://cloud.ibm.com/docs/account?topic=account-userapikey)
- [Python Requests Library](https://requests.readthedocs.io/)
- [Python dotenv](https://pypi.org/project/python-dotenv/)

## 📝 License

This is a learning project for IBM Watson Orchestrate.

## 🤝 Contributing

This is a personal learning project. Feel free to fork and adapt for your needs.

---

**Last Updated**: 2026-05-03  
**Version**: 1.0  
**Made with Bob** 🤖