# Watson Orchestrate - Personal Contact Manager

This project demonstrates how to build a simple Personal Contact Manager agent using IBM watsonx Orchestrate.

## 📚 Documentation

- **[`setup_env.md`](setup_env.md)** - Step-by-step environment setup commands
- **[`SETUP_COMPLETE.md`](SETUP_COMPLETE.md)** - Complete setup summary
- **[`adk-project/QUICKSTART.md`](adk-project/QUICKSTART.md)** - Quick start guide
- **[`adk-project/TOOL_CREATION_GUIDE.md`](adk-project/TOOL_CREATION_GUIDE.md)** - Comprehensive tool creation and troubleshooting guide

## Project Structure

```
.
├── bobenv/                 # Virtual environment
├── adk-project/           # ADK project directory
│   ├── agents/           # Agent definitions
│   ├── tools/            # Custom tools
│   ├── knowledge/        # Knowledge bases
│   └── flows/            # Workflow definitions
└── README.md             # This file
```

## Prerequisites

- Python 3.8 or higher
- IBM watsonx Orchestrate account
- API key for watsonx Orchestrate

## Setup Instructions

### 1. Virtual Environment (Already Created)

The virtual environment `bobenv` has been created and the Watson Orchestrate package has been installed.

### 2. Activate the Environment

To activate the virtual environment:

**Windows (PowerShell):**
```powershell
.\bobenv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
.\bobenv\Scripts\activate.bat
```

### 3. Configure Watson Orchestrate Environment

You need to add and activate your Watson Orchestrate environment. Run the following command:

```bash
orchestrate env add --name bobenv --url <YOUR_ORCHESTRATE_URL> --activate
```

You will be prompted to enter your API key.

**Note:** Replace `<YOUR_ORCHESTRATE_URL>` with your actual Watson Orchestrate instance URL.

### 4. Verify Installation

Check the installed version:
```bash
orchestrate --version
```

List available environments:
```bash
orchestrate env list
```

## Available Commands

### Environment Management
- `orchestrate env add` - Add a new environment
- `orchestrate env activate` - Activate an environment
- `orchestrate env list` - List all environments
- `orchestrate env remove` - Remove an environment

### Agent Management
- `orchestrate agents create` - Create a new agent
- `orchestrate agents list` - List all agents
- `orchestrate agents import` - Import an agent definition
- `orchestrate agents export` - Export an agent
- `orchestrate agents remove` - Remove an agent

### Tools Management
- `orchestrate tools list` - List available tools
- `orchestrate tools import` - Import custom tools

### Knowledge Bases
- `orchestrate knowledge-bases` - Manage knowledge bases

## Personal Contact Manager Agent

The Personal Contact Manager agent will help you:
- Store and manage contact information
- Search for contacts
- Update contact details
- Delete contacts
- Organize contacts by categories

### Next Steps

1. **Activate your environment** (you will do this with your API key)
2. **Create the agent definition** in `adk-project/agents/`
3. **Define custom tools** for contact management in `adk-project/tools/`
4. **Import the agent** using `orchestrate agents import`
5. **Test the agent** using the chat interface

## Resources

- [Watson Orchestrate Documentation](https://developer.watson-orchestrate.ibm.com/)
- [Getting Started Tutorial](https://developer.ibm.com/tutorials/getting-started-with-watsonx-orchestrate/)
- [ADK Installation Guide](https://developer.watson-orchestrate.ibm.com/getting_started/installing)

## Notes

- The virtual environment must be activated before running any `orchestrate` commands
- Keep your API key secure and never commit it to version control
- The ADK project structure follows Watson Orchestrate best practices