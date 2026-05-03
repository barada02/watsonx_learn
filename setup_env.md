# Watson Orchestrate Environment Setup Commands

## Step-by-Step Commands to Run

### 1. Activate the Virtual Environment

First, activate the `bobenv` virtual environment:

**PowerShell:**
```powershell
.\bobenv\Scripts\Activate.ps1
```

**Command Prompt:**
```cmd
.\bobenv\Scripts\activate.bat
```

You should see `(bobenv)` in your terminal prompt.

### 2. Add Watson Orchestrate Environment

**IMPORTANT**: You need to run these commands to add and activate your Watson Orchestrate environment.

Replace `<YOUR_ORCHESTRATE_URL>` with your actual Watson Orchestrate instance URL:

```bash
# Add the environment (you'll be prompted for your API key)
orchestrate env add --name bobenv --url <YOUR_ORCHESTRATE_URL>

# Activate the environment
orchestrate env activate bobenv
```

**Example:**
```bash
# Add the environment
orchestrate env add --name bobenv --url https://your-instance.watsonx.orchestrate.ibm.com

# Activate it
orchestrate env activate bobenv
```

When you run the `add` command, you will be prompted to enter your **API key**.

### 3. Verify Environment Setup

Check that your environment was added successfully:

```bash
orchestrate env list
```

You should see `bobenv` in the list with an asterisk (*) indicating it's active.

### 4. Check Orchestrate Version

```bash
orchestrate --version
```

## Where to Get Your Credentials

### Watson Orchestrate URL
- Log into your IBM Cloud account
- Navigate to your Watson Orchestrate instance
- Copy the instance URL (usually in format: `https://your-instance.watsonx.orchestrate.ibm.com`)

### API Key
- Go to IBM Cloud Console
- Navigate to "Manage" → "Access (IAM)" → "API keys"
- Create a new API key or use an existing one
- Copy the API key (you'll need it when running the `orchestrate env add` command)

## Alternative: Using Environment Variables

If you prefer, you can set environment variables instead:

**PowerShell:**
```powershell
$env:ORCHESTRATE_URL="https://your-instance.watsonx.orchestrate.ibm.com"
$env:ORCHESTRATE_API_KEY="your-api-key-here"
```

**Command Prompt:**
```cmd
set ORCHESTRATE_URL=https://your-instance.watsonx.orchestrate.ibm.com
set ORCHESTRATE_API_KEY=your-api-key-here
```

Then add the environment:
```bash
orchestrate env add --name bobenv --url %ORCHESTRATE_URL% --activate
```

## Complete Setup Sequence

Here's the complete sequence of commands to run:

```bash
# 1. Activate virtual environment
.\bobenv\Scripts\Activate.ps1

# 2. Add Watson Orchestrate environment (you'll be prompted for API key)
orchestrate env add --name bobenv --url <YOUR_ORCHESTRATE_URL>

# 3. Activate the environment
orchestrate env activate bobenv

# 4. Verify setup
orchestrate env list
orchestrate --version

# 5. Import tools (using @tool decorator)
orchestrate tools import --kind python --file adk-project/tools/contact_tools_decorated.py

# 6. Verify tools
orchestrate tools list

# 7. Import agent
orchestrate agents import --file adk-project/agents/contact_manager_agent.yaml

# 8. Verify agent
orchestrate agents list

# 9. Test the agent
orchestrate chat
```

## Troubleshooting

### Error: "orchestrate: command not found"
**Solution**: Make sure the virtual environment is activated. You should see `(bobenv)` in your prompt.

### Error: "Invalid API key"
**Solution**: Double-check your API key from IBM Cloud. Make sure there are no extra spaces.

### Error: "Cannot connect to URL"
**Solution**: Verify your Watson Orchestrate instance URL is correct and accessible.

## Next Steps

After successfully adding the environment, proceed to:
1. Import the tools (Step 5 above)
2. Import the agent (Step 7 above)
3. Start using the Personal Contact Manager!

**Important:** If you encounter issues importing tools, refer to [`adk-project/TOOL_CREATION_GUIDE.md`](adk-project/TOOL_CREATION_GUIDE.md) for detailed troubleshooting and alternative methods.

Also see:
- [`SETUP_COMPLETE.md`](SETUP_COMPLETE.md) - Complete setup summary
- [`adk-project/QUICKSTART.md`](adk-project/QUICKSTART.md) - Quick start guide