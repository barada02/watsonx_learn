# Watson Orchestrate Tool Creation Guide

This guide explains how to create and import tools for Watson Orchestrate agents.

## Recommended Method: Using @tool Decorator

The **recommended and simplest** way to create Watson Orchestrate tools is using the `@tool` decorator from `ibm_watsonx_orchestrate.agent_builder.tools`.

### Example with @tool Decorator

```python
from typing import Dict, Optional
from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool
def add_contact(
    name: str,
    phone: Optional[str] = None,
    email: Optional[str] = None
) -> Dict:
    """Add a new contact to the contact manager.

    Args:
        name (str): Full name of the contact (required)
        phone (str): Phone number
        email (str): Email address

    Returns:
        Dict: Dictionary with the created contact information
    """
    return {
        "success": True,
        "name": name,
        "phone": phone,
        "email": email
    }
```

**Import Command:**
```bash
orchestrate tools import --kind python --file path/to/your_tools.py
```

**Key Benefits:**
- No need for `--auto-discover` flag
- Automatic tool registration
- Clean, Pythonic syntax
- Type hints and docstrings are automatically parsed

## Alternative Methods

### 1. Python Tools with Auto-Discover (Without @tool decorator)

The simplest method for Python functions with proper docstrings.

**Command:**
```bash
orchestrate tools import --kind python --file path/to/tool.py --auto-discover
```

**Requirements:**
- Python functions with Google-style docstrings
- Type hints for parameters
- Clear parameter descriptions in docstring

**Example Python Tool:**
```python
def add_contact(name: str, phone: str = "", email: str = "") -> dict:
    """
    Add a new contact to the contact manager.
    
    Args:
        name (str): Full name of the contact
        phone (str): Phone number of the contact
        email (str): Email address of the contact
    
    Returns:
        dict: A dictionary containing the contact information
    """
    return {"name": name, "phone": phone, "email": email}
```

### 2. OpenAPI Specification

For REST API tools, use OpenAPI/Swagger specifications.

**Command:**
```bash
orchestrate tools import --kind openapi --file path/to/openapi.yaml
```

### 3. Flow-based Tools

For workflow-based tools using JSON flow definitions.

**Command:**
```bash
orchestrate tools import --kind flow --file path/to/flow.json
```

### 4. LangFlow Tools

For LangFlow-based tools.

**Command:**
```bash
orchestrate tools import --kind langflow --name tool_name
```

## Testing Your Tools

### Step 1: Try the Simple Tool First

We've created a simplified tool for testing:

```bash
orchestrate tools import --kind python --file adk-project/tools/simple_contact_tool.py --auto-discover
```

### Step 2: Verify Import

```bash
orchestrate tools list
```

You should see the imported tools listed.

### Step 3: Test with Agent

Create a simple agent that uses the tool:

```bash
orchestrate agents create \
  --name test_contact_agent \
  --description "Test contact manager" \
  --tools add_contact \
  --tools search_contact
```

## Troubleshooting

### Issue: "No valid tools found"

**Possible Causes:**
1. Missing or incorrect docstrings
2. Missing type hints
3. Functions not at module level (inside classes)
4. Incorrect file path

**Solutions:**
- Ensure functions have proper Google-style docstrings
- Add type hints to all parameters
- Move functions to module level (not inside classes)
- Use `--auto-discover` flag

### Issue: "Import failed"

**Check:**
1. Virtual environment is activated
2. Watson Orchestrate environment is active (`orchestrate env list`)
3. File path is correct and relative to current directory
4. Python file has no syntax errors

## Alternative: Using Agent Builder

Instead of importing tools separately, you can use the agent builder:

```bash
orchestrate agents ai-builder
```

This interactive tool helps you:
- Create agents with AI assistance
- Define tools interactively
- Test agents immediately

## Best Practices

### 1. Function Design
- Keep functions simple and focused
- Use clear, descriptive names
- Return structured data (dict/JSON)
- Handle errors gracefully

### 2. Documentation
- Write clear docstrings
- Document all parameters
- Specify return types
- Include examples in docstrings

### 3. Type Hints
```python
from typing import Dict, List, Optional

def my_tool(
    required_param: str,
    optional_param: Optional[str] = None
) -> Dict[str, any]:
    """Tool description."""
    pass
```

### 4. Error Handling
```python
def safe_tool(param: str) -> dict:
    """Safe tool with error handling."""
    try:
        # Tool logic
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

## Example: Complete Tool File with @tool Decorator

```python
"""Contact management tools for Watson Orchestrate."""

from typing import Dict, Optional
from ibm_watsonx_orchestrate.agent_builder.tools import tool

# In-memory storage
contacts_db = []

@tool
def add_contact(
    name: str,
    phone: Optional[str] = None,
    email: Optional[str] = None
) -> Dict:
    """Add a new contact to the contact manager.
    
    Args:
        name (str): Full name of the contact (required)
        phone (str): Phone number
        email (str): Email address
    
    Returns:
        Dict: Contact information with status
    """
    contact_id = len(contacts_db) + 1
    contact = {
        "id": contact_id,
        "name": name,
        "phone": phone or "",
        "email": email or "",
        "status": "success"
    }
    contacts_db.append(contact)
    return {"success": True, "contact": contact}

@tool
def search_contact(query: str) -> Dict:
    """Search for contacts by name, phone, or email.
    
    Args:
        query (str): Search term
    
    Returns:
        Dict: Search results
    """
    matches = [c for c in contacts_db if query.lower() in c["name"].lower()]
    return {"success": True, "count": len(matches), "contacts": matches}
```

**Import this file:**
```bash
orchestrate tools import --kind python --file contact_tools.py
```

## Resources

- [Watson Orchestrate Tool Documentation](https://developer.watson-orchestrate.ibm.com/tools/create_tool)
- [Python Tool Examples](https://developer.watson-orchestrate.ibm.com/tools/python)
- [OpenAPI Tool Examples](https://developer.watson-orchestrate.ibm.com/tools/openapi)

## Quick Start

1. **Use the decorated version** (recommended):
   ```bash
   orchestrate tools import --kind python --file adk-project/tools/contact_tools_decorated.py
   ```

2. **Verify import**:
   ```bash
   orchestrate tools list
   ```

3. **Create an agent** that uses the tools:
   ```bash
   orchestrate agents import --file adk-project/agents/contact_manager_agent.yaml
   ```

4. **Test in chat** (choose one):
   ```bash
   # Web-based UI
   orchestrate chat start
   
   # Or CLI interactive chat
   orchestrate chat ask --agent-name personal_contact_manager
   ```

## Files in This Project

- **`contact_tools_decorated.py`** - ✅ Recommended: Uses @tool decorator
- **`contact_tools.py`** - Alternative: Plain Python with detailed docstrings
- **`simple_contact_tool.py`** - Minimal example for testing