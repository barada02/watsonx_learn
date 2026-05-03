# Running a Deployed Watson Orchestrate Agent with Python

A complete technical guide for interacting with deployed Watson Orchestrate agents using Python.

---

## Overview

This guide demonstrates how to programmatically interact with a deployed Watson Orchestrate agent using Python and the Watson Orchestrate REST API.

## Prerequisites

- Python 3.8 or higher
- A deployed Watson Orchestrate agent
- IBM Cloud API key
- Watson Orchestrate instance URL

---

## Architecture

### API Flow

```
1. Authenticate → Get Bearer Token
2. Send Message → Receive run_id
3. Poll Run Status → Wait for completion
4. Extract Response → Display to user
```

### Key Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `https://iam.cloud.ibm.com/identity/token` | POST | Get authentication token |
| `{INSTANCE_URL}/v1/orchestrate/runs` | POST | Send message to agent |
| `{INSTANCE_URL}/v1/orchestrate/runs/{run_id}` | GET | Poll for run result |

---

## Step 1: Environment Setup

### Install Dependencies

```bash
pip install requests python-dotenv
```

### Create Environment File

Create a `.env` file with your credentials:

```bash
# Your Watson Orchestrate instance URL
INSTANCE_URL=https://api.jp-tok.watson-orchestrate.cloud.ibm.com/instances/your-instance-id

# Your IBM Cloud API key
API_KEY=your_api_key_here

# Your deployed agent ID
AGENT_ID=your_agent_id_here
```

**How to get these values:**

1. **INSTANCE_URL**: From your Watson Orchestrate instance details (without `/v1/orchestrate/runs`)
2. **API_KEY**: IBM Cloud Console → Manage → Access (IAM) → API keys
3. **AGENT_ID**: Run `orchestrate agents list` to see your deployed agents

---

## Step 2: Authentication

### Token Request

**Endpoint:** `POST https://iam.cloud.ibm.com/identity/token`

**Headers:**
```python
{
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json"
}
```

**Body:**
```python
{
    "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
    "apikey": "your_api_key"
}
```

**Response:**
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "...",
    "token_type": "Bearer",
    "expires_in": 3600
}
```

### Python Implementation

```python
import requests

def get_token(api_key: str) -> str:
    """Get authentication token from IBM Cloud IAM."""
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": api_key
    }
    
    response = requests.post(url, data=data, headers=headers)
    response.raise_for_status()
    
    return response.json()["access_token"]
```

**Token Caching:**
- Tokens are valid for ~50 minutes
- Cache the token and reuse until expiry
- Implement token refresh logic for long-running applications

---

## Step 3: Send Message to Agent

### Message Request

**Endpoint:** `POST {INSTANCE_URL}/v1/orchestrate/runs`

**Headers:**
```python
{
    "Authorization": "Bearer {token}",
    "IAM-API_KEY": "{api_key}",
    "accept": "application/json",
    "Content-Type": "application/json"
}
```

**Query Parameters:**
```python
{
    "stream": "false",
    "stream_timeout": "120000",
    "multiple_content": "true"
}
```

**Body:**
```json
{
    "message": {
        "role": "user",
        "content": "Hello! Can you help me?"
    },
    "agent_id": "4ae6afb5-9732-46ac-995d-3793f9939fbd",
    "thread_id": "optional-thread-id-for-continuing-conversation"
}
```

**Response:**
```json
{
    "thread_id": "4e6adb48-acb3-47df-a52f-1ecc45bcd1f9",
    "run_id": "579c49d5-92a1-4813-8284-4191c99222cb",
    "task_id": "e4359da9-eff0-4019-8456-18d1a3fdcaab",
    "message_id": "a2aa7051-792c-48dc-bdee-4394a8f23cc2",
    "trace_id": "9fb8acd2ed82b2f1f45f9a841d68bc83"
}
```

### Python Implementation

```python
def send_message(
    instance_url: str,
    token: str,
    api_key: str,
    agent_id: str,
    query: str,
    thread_id: str = None
) -> dict:
    """Send a message to the agent."""
    url = f"{instance_url}/v1/orchestrate/runs"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "IAM-API_KEY": api_key,
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    
    params = {
        "stream": "false",
        "stream_timeout": "120000",
        "multiple_content": "true"
    }
    
    body = {
        "message": {
            "role": "user",
            "content": query
        },
        "agent_id": agent_id
    }
    
    if thread_id:
        body["thread_id"] = thread_id
    
    response = requests.post(url, headers=headers, params=params, json=body)
    response.raise_for_status()
    
    return response.json()
```

---

## Step 4: Poll for Run Result

### Why Polling is Needed

The initial POST request returns immediately with a `run_id`, but the agent's response is generated asynchronously. You must poll the run endpoint to get the final result.

### Poll Request

**Endpoint:** `GET {INSTANCE_URL}/v1/orchestrate/runs/{run_id}`

**Headers:**
```python
{
    "Authorization": "Bearer {token}",
    "IAM-API_KEY": "{api_key}",
    "accept": "application/json"
}
```

**Response (when completed):**
```json
{
    "status": "completed",
    "result": {
        "data": {
            "message": {
                "content": [
                    {
                        "text": "Hello! I'm happy to help you manage your contacts..."
                    }
                ]
            }
        }
    },
    "thread_id": "4e6adb48-acb3-47df-a52f-1ecc45bcd1f9"
}
```

### Python Implementation

```python
import time

def poll_run_result(
    instance_url: str,
    token: str,
    api_key: str,
    run_id: str,
    timeout: int = 60,
    interval: float = 0.7
) -> dict:
    """Poll for run completion and return result."""
    url = f"{instance_url}/v1/orchestrate/runs/{run_id}"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "IAM-API_KEY": api_key,
        "accept": "application/json"
    }
    
    start_time = time.time()
    
    while True:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        status = data.get("status", "").lower()
        
        # Check if completed
        if status in {"completed", "succeeded", "success", "done"}:
            return data
        
        # Check if failed
        if status in {"failed", "error", "cancelled"}:
            raise RuntimeError(f"Run failed: {data}")
        
        # Check timeout
        if time.time() - start_time > timeout:
            raise TimeoutError("Polling timed out")
        
        # Wait before next poll
        time.sleep(interval)
```

---

## Step 5: Extract Response Text

### Response Structure

The agent's response is nested in the result:

```
result → data → message → content → [0] → text
```

### Python Implementation

```python
def extract_response_text(data: dict) -> str:
    """Extract the agent's response text from the result."""
    try:
        # Navigate the nested structure
        result = data.get("result", {})
        data_obj = result.get("data", {})
        message = data_obj.get("message", {})
        content = message.get("content", [])
        
        # Extract text from content array
        texts = []
        for item in content:
            if isinstance(item, dict):
                text = item.get("text")
                if text and isinstance(text, str):
                    texts.append(text)
        
        # Join multiple text blocks
        return "\n".join(texts).strip()
    
    except Exception:
        return ""
```

---

## Step 6: Thread Management

### Continuing Conversations

To continue a conversation, include the `thread_id` from the previous response:

```python
# First message - creates new thread
response1 = send_message(
    instance_url=INSTANCE_URL,
    token=token,
    api_key=API_KEY,
    agent_id=AGENT_ID,
    query="Hello!"
)

thread_id = response1["thread_id"]

# Continue conversation - use same thread_id
response2 = send_message(
    instance_url=INSTANCE_URL,
    token=token,
    api_key=API_KEY,
    agent_id=AGENT_ID,
    query="What can you do?",
    thread_id=thread_id  # Same thread
)
```

### Thread Lifecycle

- **New Thread**: Omit `thread_id` in request
- **Continue Thread**: Include `thread_id` from previous response
- **Thread Persistence**: Threads persist on the server for the session

---

## Complete Working Example

### Full Implementation

See [`run_agent_correct.py`](run_agent_correct.py) for the complete implementation.

### Quick Start

```bash
# 1. Install dependencies
pip install requests python-dotenv

# 2. Configure .env file
cp .env.example .env
# Edit .env with your credentials

# 3. Run the script
python run_agent_correct.py
```

### Example Output

```
============================================================
Watsonx Orchestrate Agent Runner
============================================================

--- Example 1: Single Message ---
Fetching new authentication token...
✓ Token obtained successfully

Sending message to agent '4ae6afb5-9732-46ac-995d-3793f9939fbd'...
Query: Hello! Can you help me?
Polling for result (run_id: 579c49d5-92a1-4813-8284-4191c99222cb)...
✓ Response received

Agent Response:
Hello! I'm happy to help you manage your contacts...

Thread ID: 4e6adb48-acb3-47df-a52f-1ecc45bcd1f9
```

---

## API Reference

### Authentication

```python
POST https://iam.cloud.ibm.com/identity/token
Content-Type: application/x-www-form-urlencoded

grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={API_KEY}
```

### Send Message

```python
POST {INSTANCE_URL}/v1/orchestrate/runs?stream=false&stream_timeout=120000&multiple_content=true
Authorization: Bearer {TOKEN}
IAM-API_KEY: {API_KEY}
Content-Type: application/json

{
    "message": {"role": "user", "content": "query"},
    "agent_id": "agent_id",
    "thread_id": "optional_thread_id"
}
```

### Poll Run

```python
GET {INSTANCE_URL}/v1/orchestrate/runs/{run_id}
Authorization: Bearer {TOKEN}
IAM-API_KEY: {API_KEY}
```

---

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| 400 Bad Request | Invalid API key or request format | Verify API key and request body |
| 401 Unauthorized | Invalid or expired token | Refresh authentication token |
| 403 Forbidden | Insufficient permissions | Check API key permissions |
| 404 Not Found | Invalid endpoint or agent ID | Verify URLs and agent ID |
| 408 Timeout | Polling timeout exceeded | Increase timeout or check agent status |

### Error Handling Example

```python
try:
    token = get_token(API_KEY)
    response = send_message(INSTANCE_URL, token, API_KEY, AGENT_ID, "Hello")
    run_id = response["run_id"]
    result = poll_run_result(INSTANCE_URL, token, API_KEY, run_id)
    text = extract_response_text(result)
    print(f"Agent: {text}")

except requests.HTTPError as e:
    print(f"HTTP Error: {e.response.status_code}")
    print(f"Details: {e.response.text}")

except TimeoutError:
    print("Request timed out waiting for agent response")

except Exception as e:
    print(f"Error: {str(e)}")
```

---

## Best Practices

### 1. Token Management

```python
class TokenManager:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.token = None
        self.expiry = 0
    
    def get_token(self) -> str:
        now = time.time()
        if self.token and now < self.expiry:
            return self.token
        
        # Fetch new token
        self.token = get_token(self.api_key)
        self.expiry = now + 3000  # 50 minutes
        return self.token
```

### 2. Connection Pooling

```python
import requests

session = requests.Session()
# Reuse session for all requests
response = session.post(url, headers=headers, json=body)
```

### 3. Retry Logic

```python
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504]
)

adapter = HTTPAdapter(max_retries=retry_strategy)
session = requests.Session()
session.mount("https://", adapter)
```

### 4. Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Sending message to agent {agent_id}")
logger.debug(f"Request body: {body}")
```

---

## Performance Considerations

### Polling Optimization

- **Interval**: Start with 0.7 seconds, adjust based on agent response time
- **Timeout**: Set appropriate timeout (60-120 seconds)
- **Exponential Backoff**: Increase interval if agent is slow

```python
def poll_with_backoff(url, headers, max_interval=5.0):
    interval = 0.7
    while True:
        response = requests.get(url, headers=headers)
        if response.json().get("status") == "completed":
            return response.json()
        
        time.sleep(interval)
        interval = min(interval * 1.5, max_interval)
```

### Concurrent Requests

For multiple agents or parallel conversations:

```python
from concurrent.futures import ThreadPoolExecutor

def process_query(query):
    token = get_token(API_KEY)
    response = send_message(INSTANCE_URL, token, API_KEY, AGENT_ID, query)
    result = poll_run_result(INSTANCE_URL, token, API_KEY, response["run_id"])
    return extract_response_text(result)

with ThreadPoolExecutor(max_workers=5) as executor:
    queries = ["Query 1", "Query 2", "Query 3"]
    results = executor.map(process_query, queries)
```

---

## Security Best Practices

1. **Never commit credentials**: Use `.env` files and add to `.gitignore`
2. **Rotate API keys**: Regularly rotate keys in production
3. **Use HTTPS**: All API calls use HTTPS by default
4. **Validate inputs**: Sanitize user inputs before sending to agent
5. **Handle errors gracefully**: Don't expose sensitive error details to users

---

## Troubleshooting

### Agent Not Responding

```bash
# Check agent status
orchestrate agents list

# Test with CLI
orchestrate chat ask --agent-name your_agent_name "test"
```

### Authentication Issues

```python
# Test token generation
token = get_token(API_KEY)
print(f"Token length: {len(token)}")  # Should be ~1500 characters
```

### Polling Timeout

```python
# Increase timeout and add logging
def poll_run_result(url, headers, timeout=120):
    start = time.time()
    while time.time() - start < timeout:
        response = requests.get(url, headers=headers)
        data = response.json()
        print(f"Status: {data.get('status')}")  # Debug output
        # ... rest of polling logic
```

---

## Resources

- [Watson Orchestrate Documentation](https://developer.watson-orchestrate.ibm.com/)
- [IBM Cloud IAM Documentation](https://cloud.ibm.com/docs/account?topic=account-iamoverview)
- [Python Requests Library](https://requests.readthedocs.io/)

---

**Last Updated**: 2026-05-03  
**Version**: 1.0  
**Status**: Production Ready ✅