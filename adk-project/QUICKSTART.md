# Personal Contact Manager - Quick Start Guide

This guide will help you get started with the Personal Contact Manager agent.

## Prerequisites

Before you begin, make sure you have:
1. Activated the `bobenv` virtual environment
2. Configured your Watson Orchestrate environment with your API key

## Step 1: Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\bobenv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
.\bobenv\Scripts\activate.bat
```

## Step 2: Configure Watson Orchestrate Environment

**Note:** The user will run this command with their API key:

```bash
orchestrate env add --name bobenv --url <YOUR_ORCHESTRATE_URL> --activate
```

Then activate the environment:
```bash
orchestrate env activate bobenv
```

## Step 3: Import the Tools

Import the contact management tools:

```bash
orchestrate tools import --file adk-project/tools/contact_tools.yaml
```

Verify the tools were imported:
```bash
orchestrate tools list
```

## Step 4: Import the Agent

Import the Personal Contact Manager agent:

```bash
orchestrate agents import --file adk-project/agents/contact_manager_agent.yaml
```

Verify the agent was created:
```bash
orchestrate agents list
```

## Step 5: Test the Agent

You can test the agent using the chat interface:

```bash
orchestrate chat
```

Or deploy the agent:

```bash
orchestrate agents deploy --name personal_contact_manager
```

## Example Interactions

Once the agent is running, you can interact with it using natural language:

### Adding a Contact
```
"Add a new contact named John Doe with email john@example.com and phone 555-1234"
```

### Searching for Contacts
```
"Search for contacts with the name John"
```

### Listing Contacts
```
"Show me all my contacts"
"List all contacts in the work category"
```

### Updating a Contact
```
"Update contact ID 1 with new phone number 555-5678"
```

### Categorizing Contacts
```
"Categorize contact ID 1 as work"
```

### Deleting a Contact
```
"Delete contact ID 1"
```

## Project Structure

```
adk-project/
├── agents/
│   └── contact_manager_agent.yaml    # Agent definition
├── tools/
│   ├── contact_tools.py              # Tool implementations
│   └── contact_tools.yaml            # Tool definitions
├── knowledge/                         # (Empty - for future use)
└── flows/                            # (Empty - for future use)
```

## Customization

### Adding More Tools

1. Add new functions to `tools/contact_tools.py`
2. Update `tools/contact_tools.yaml` with the new tool definitions
3. Re-import the tools using `orchestrate tools import`

### Modifying the Agent

1. Edit `agents/contact_manager_agent.yaml`
2. Update the instructions, tools list, or configuration
3. Re-import the agent using `orchestrate agents import`

### Adding Knowledge Bases

You can add knowledge bases to help the agent answer questions:

```bash
orchestrate knowledge-bases upload --name contact_help --file path/to/help.pdf
```

Then update the agent definition to include the knowledge base.

## Troubleshooting

### Environment Not Activated
If you get an error about the environment not being activated:
```bash
orchestrate env activate bobenv
```

### Tools Not Found
If the agent can't find the tools, make sure they're imported:
```bash
orchestrate tools list
```

### Agent Not Responding
Check the agent status:
```bash
orchestrate agents list
```

## Next Steps

1. **Enhance the Tools**: Add more sophisticated contact management features
2. **Add Persistence**: Replace in-memory storage with a database
3. **Add Knowledge**: Upload documentation about contact management
4. **Create Flows**: Build automated workflows for contact management tasks
5. **Add Integrations**: Connect to external services (email, calendar, etc.)

## Resources

- [Watson Orchestrate Documentation](https://developer.watson-orchestrate.ibm.com/)
- [ADK Developer Guide](https://developer.watson-orchestrate.ibm.com/getting_started/installing)
- [Tool Development Guide](https://developer.watson-orchestrate.ibm.com/tools)
- [Agent Development Guide](https://developer.watson-orchestrate.ibm.com/agents)

## Support

For issues or questions:
- Check the Watson Orchestrate documentation
- Review the error logs
- Ensure your API key and environment are properly configured