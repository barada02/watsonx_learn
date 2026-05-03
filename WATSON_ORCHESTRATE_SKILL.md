# Watson Orchestrate Development Skill Guide

## Purpose
This document provides clear, step-by-step instructions for working with IBM Watson Orchestrate. It is designed to be easily understood by LLMs and developers for future reference.

---

## Table of Contents
1. [Environment Setup](#environment-setup)
2. [Tool Creation](#tool-creation)
3. [Agent Creation](#agent-creation)
4. [Testing and Deployment](#testing-and-deployment)
5. [Common Commands Reference](#common-commands-reference)
6. [Troubleshooting](#troubleshooting)
7. [Best Practices](#best-practices)

---

## Environment Setup

### Prerequisites
- Python 3.8 or higher
- IBM Watson Orchestrate account
- API key and instance URL

### Step 1: Create Virtual Environment
```bash
# Create virtual environment
python -m venv bobenv

# Activate (Windows PowerShell)
.\bobenv\Scripts\Activate.ps1

# Activate (Windows CMD)
.\bobenv\Scripts\activate.bat

# Activate (Linux/Mac)
source bobenv/bin/activate
```

### Step 2: Install Watson Orchestrate
```bash
pip install ibm-watsonx-orchestrate
```

### Step 3: Configure Environment
```bash
# Add environment (you'll be prompted for API key)
orchestrate env add --name <env_name> --url <your_orchestrate_url>

# Activate environment
orchestrate env activate <env_name>

# Verify setup
orchestrate env list
orchestrate --version
```

**Important Notes:**
- Keep API keys secure, never commit to version control
- The environment name can be anything (e.g., "bobenv", "dev", "prod")
- URL format: `https://your-instance.watsonx.orchestrate.ibm.com`

---

## Tool Creation

### Method 1: Using @tool Decorator (RECOMMENDED)

**File Structure:**
```python
from typing import Dict, Optional
from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool
def function_name(
    required_param: str,
    optional_param: Optional[str] = None
) -> Dict:
    """Brief description of what the tool does.
    
    Args:
        required_param (str): Description of required parameter
        optional_param (str): Description of optional parameter
    
    Returns:
        Dict: Description of return value
    """
    # Tool implementation
    result = {"status": "success", "data": "result"}
    return result
```

**Import Command:**
```bash
orchestrate tools import --kind python --file path/to/tool.py
```

**Key Requirements:**
1. Import `@tool` decorator from `ibm_watsonx_orchestrate.agent_builder.tools`
2. Use type hints for all parameters
3. Write clear docstrings in Google style
4. Return structured data (Dict/JSON)
5. Handle errors gracefully

### Method 2: Auto-Discover (Alternative)
```bash
orchestrate tools import --kind python --file path/to/tool.py --auto-discover
```

### Method 3: OpenAPI Specification
```bash
orchestrate tools import --kind openapi --file path/to/openapi.yaml
```

### Verify Tool Import
```bash
orchestrate tools list
```

---

## Agent Creation

### Method 1: YAML Definition File

**File: agent_definition.yaml**
```yaml
name: agent_name
description: Brief description of what the agent does
kind: native
style: default

instructions: |
  Detailed instructions for the agent.
  Explain the agent's role and capabilities.
  
  You can help with:
  - Task 1
  - Task 2
  - Task 3

tools:
  - tool_name_1
  - tool_name_2
  - tool_name_3

knowledge_bases: []

collaborators: []

config:
  hidden: false
  enable_cot: true

context_access_enabled: true
context_variables:
  - user_name
  - user_email

tags:
  - tag1
  - tag2
```

**Import Command:**
```bash
orchestrate agents import --file path/to/agent_definition.yaml
```

### Method 2: CLI Creation
```bash
orchestrate agents create \
  --name agent_name \
  --description "Agent description" \
  --tools tool1 \
  --tools tool2 \
  --instructions "Agent instructions"
```

### Method 3: AI Builder (Interactive)
```bash
orchestrate agents ai-builder
```

### Verify Agent Creation
```bash
orchestrate agents list
```

---

## Testing and Deployment

### Option 1: Web-Based Chat UI
```bash
# Start web interface
orchestrate chat start

# Stop web interface
orchestrate chat stop
```

### Option 2: CLI Interactive Chat
```bash
# Start interactive chat with specific agent
orchestrate chat ask --agent agent_name

# Ask a single question
orchestrate chat ask --agent agent_name "Your question here"
```

### Option 3: Deploy Agent
```bash
# Deploy agent
orchestrate agents deploy --name agent_name

# Undeploy agent
orchestrate agents undeploy --name agent_name
```

### Export Agent
```bash
# Export to YAML
orchestrate agents export --name agent_name --output agent.yaml

# Export to ZIP (with dependencies)
orchestrate agents export --name agent_name --output agent.zip
```

---

## Common Commands Reference

### Environment Management
```bash
orchestrate env add --name <name> --url <url>          # Add environment
orchestrate env activate <name>                         # Activate environment
orchestrate env list                                    # List environments
orchestrate env remove <name>                           # Remove environment
```

### Tool Management
```bash
orchestrate tools import --kind python --file <path>    # Import Python tool
orchestrate tools import --kind openapi --file <path>   # Import OpenAPI tool
orchestrate tools list                                  # List all tools
orchestrate tools remove --name <tool_name>             # Remove tool
```

### Agent Management
```bash
orchestrate agents create [OPTIONS]                     # Create agent
orchestrate agents import --file <path>                 # Import agent
orchestrate agents list                                 # List all agents
orchestrate agents export --name <name> --output <path> # Export agent
orchestrate agents remove --name <name>                 # Remove agent
orchestrate agents deploy --name <name>                 # Deploy agent
orchestrate agents undeploy --name <name>               # Undeploy agent
```

### Knowledge Base Management
```bash
orchestrate knowledge-bases upload --name <name> --file <path>
orchestrate knowledge-bases list
orchestrate knowledge-bases remove --name <name>
```

### Server Management (Local Development)
```bash
orchestrate server start                                # Start local server
orchestrate server stop                                 # Stop local server
orchestrate server status                               # Check server status
```

### Chat Interface
```bash
orchestrate chat start                                  # Start web UI
orchestrate chat stop                                   # Stop web UI
orchestrate chat ask --agent <name>                     # Interactive CLI chat
orchestrate chat ask --agent <name> "question"          # Single question
```

---

## Troubleshooting

### Issue: "orchestrate: command not found"
**Solution:**
1. Ensure virtual environment is activated (you should see `(bobenv)` in prompt)
2. Reinstall: `pip install ibm-watsonx-orchestrate`

### Issue: "No valid tools found"
**Solution:**
1. Ensure you're using `@tool` decorator from `ibm_watsonx_orchestrate.agent_builder.tools`
2. Check that functions have proper docstrings
3. Verify type hints are present
4. Try with `--auto-discover` flag

### Issue: "Environment not configured"
**Solution:**
1. Run `orchestrate env list` to check active environment
2. Activate environment: `orchestrate env activate <name>`
3. If no environment exists, add one: `orchestrate env add --name <name> --url <url>`

### Issue: "Invalid API key"
**Solution:**
1. Verify API key from IBM Cloud console
2. Remove and re-add environment with correct credentials
3. Check for extra spaces or special characters

### Issue: "Agent not responding"
**Solution:**
1. Check agent status: `orchestrate agents list`
2. Verify tools are imported: `orchestrate tools list`
3. Check agent definition includes correct tool names
4. Try redeploying: `orchestrate agents deploy --name <name>`

---

## Best Practices

### Tool Development
1. **Use @tool decorator** - Simplest and most reliable method
2. **Type hints are mandatory** - Required for proper tool registration
3. **Clear docstrings** - Use Google-style format
4. **Return structured data** - Always return Dict/JSON
5. **Error handling** - Wrap logic in try-except blocks
6. **Keep functions focused** - One tool, one purpose

### Agent Design
1. **Clear instructions** - Be specific about agent capabilities
2. **Appropriate tools** - Only include relevant tools
3. **Test incrementally** - Start with simple tools, add complexity
4. **Use categories** - Organize tools logically
5. **Enable chain-of-thought** - Set `enable_cot: true` for better reasoning

### Project Structure
```
project/
├── bobenv/                 # Virtual environment
├── adk-project/           # ADK project directory
│   ├── agents/           # Agent definitions (.yaml)
│   ├── tools/            # Tool implementations (.py)
│   ├── knowledge/        # Knowledge base files
│   └── flows/            # Workflow definitions
├── .gitignore            # Exclude bobenv, secrets
└── README.md             # Project documentation
```

### Security
1. **Never commit API keys** - Use .gitignore
2. **Use environment variables** - For sensitive data
3. **Validate inputs** - In tool functions
4. **Sanitize outputs** - Remove sensitive information

---

## Example: Complete Workflow

### 1. Setup
```bash
# Create and activate environment
python -m venv bobenv
.\bobenv\Scripts\Activate.ps1
pip install ibm-watsonx-orchestrate

# Configure Watson Orchestrate
orchestrate env add --name myenv --url https://my-instance.watsonx.orchestrate.ibm.com
orchestrate env activate myenv
```

### 2. Create Tool
**File: tools/my_tool.py**
```python
from typing import Dict
from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool
def greet_user(name: str) -> Dict:
    """Greet a user by name.
    
    Args:
        name (str): Name of the user to greet
    
    Returns:
        Dict: Greeting message
    """
    return {"message": f"Hello, {name}!"}
```

### 3. Import Tool
```bash
orchestrate tools import --kind python --file tools/my_tool.py
orchestrate tools list  # Verify
```

### 4. Create Agent
**File: agents/greeter_agent.yaml**
```yaml
name: greeter
description: A friendly greeting agent
kind: native
style: default

instructions: |
  You are a friendly assistant that greets users.
  Use the greet_user tool to create personalized greetings.

tools:
  - greet_user

config:
  enable_cot: true
```

### 5. Import and Test Agent
```bash
orchestrate agents import --file agents/greeter_agent.yaml
orchestrate agents list  # Verify
orchestrate chat ask --agent greeter "Greet John"
```

---

## Quick Reference Card

| Task | Command |
|------|---------|
| Activate env | `.\bobenv\Scripts\Activate.ps1` |
| Add Watson env | `orchestrate env add --name <name> --url <url>` |
| Activate Watson env | `orchestrate env activate <name>` |
| Import tool | `orchestrate tools import --kind python --file <path>` |
| Import agent | `orchestrate agents import --file <path>` |
| List tools | `orchestrate tools list` |
| List agents | `orchestrate agents list` |
| Start chat UI | `orchestrate chat start` |
| CLI chat | `orchestrate chat ask --agent <name>` |
| Deploy agent | `orchestrate agents deploy --name <name>` |

---

## For LLMs: Key Points to Remember

1. **Always use @tool decorator** from `ibm_watsonx_orchestrate.agent_builder.tools`
2. **Type hints are required** for all function parameters
3. **Docstrings must be Google-style** with Args and Returns sections
4. **Import command is**: `orchestrate tools import --kind python --file <path>`
5. **Chat commands have subcommands**: `orchestrate chat start` or `orchestrate chat ask`
6. **Environment must be activated** before any orchestrate commands
7. **Two environments**: Python venv (bobenv) AND Watson Orchestrate env
8. **Return structured data** (Dict/JSON) from all tools
9. **Agent YAML must list tool names** exactly as they appear in tool list
10. **Test incrementally**: tool → agent → chat

---

## Additional Resources

- [Watson Orchestrate Documentation](https://developer.watson-orchestrate.ibm.com/)
- [Tool Creation Guide](https://developer.watson-orchestrate.ibm.com/tools/create_tool)
- [Agent Development Guide](https://developer.watson-orchestrate.ibm.com/agents)
- [API Reference](https://developer.watson-orchestrate.ibm.com/api)

---

**Last Updated:** 2026-05-03  
**Version:** 1.0  
**Project:** Watson Orchestrate Personal Contact Manager