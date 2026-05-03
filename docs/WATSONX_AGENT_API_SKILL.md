# Watson Orchestrate Deployed Agent API - LLM Skill Guide

## Purpose
This skill document teaches how to interact with deployed Watson Orchestrate agents using Python and REST API. Use this as a reference for future agent integration tasks.

---

## Core Concept

**Deployed Watson Orchestrate agents** are accessed via REST API with a 3-step process:
1. **Authenticate** → Get token
2. **Send message** → Get run_id  
3. **Poll run** → Get response

---

## Prerequisites

```python
# Required packages
pip install requests python-dotenv

# Required credentials
INSTANCE_URL = "https://api.{region}.watson-orchestrate.cloud.ibm.com/instances/{instance-id}"
API_KEY = "your_ibm_cloud_api_key"
AGENT_ID = "your_deployed_agent_id"
```

---

## Step 1: Authentication

### Endpoint
```
POST https://iam.cloud.ibm.com/identity/token
```

### Request
```python
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json"
}

data = {
    "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
    "apikey": API_KEY
}
```

### Response
```json
{
    "access_token": "eyJhbGc...",
    "expires_in": 3600
}
```

### Implementation
```python
def get_token(api_key: str) -> str:
    response = requests.post(
        "https://iam.cloud.ibm.com/identity/token",
        data={
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
            "apikey": api_key
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        }
    )
    return response.json()["access_token"]
```

**Key Points:**
- Token valid for ~50 minutes
- Cache and reuse token
- Use `access_token` field from response

---

## Step 2: Send Message

### Endpoint
```
POST {INSTANCE_URL}/v1/orchestrate/runs
```

### Headers
```python
{
    "Authorization": f"Bearer {token}",
    "IAM-API_KEY": api_key,  # Required!
    "Content-Type": "application/json"
}
```

### Query Parameters
```python
{
    "stream": "false",
    "stream_timeout": "120000",
    "multiple_content": "true"
}
```

### Request Body
```json
{
    "message": {
        "role": "user",
        "content": "Your question here"
    },
    "agent_id": "agent-id",
    "thread_id": "optional-for-continuing-conversation"
}
```

### Response
```json
{
    "thread_id": "thread-uuid",
    "run_id": "run-uuid",
    "task_id": "task-uuid",
    "message_id": "message-uuid"
}
```

### Implementation
```python
def send_message(instance_url: str, token: str, api_key: str, 
                 agent_id: str, query: str, thread_id: str = None) -> dict:
    url = f"{instance_url}/v1/orchestrate/runs"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "IAM-API_KEY": api_key,
        "Content-Type": "application/json"
    }
    
    params = {
        "stream": "false",
        "stream_timeout": "120000",
        "multiple_content": "true"
    }
    
    body = {
        "message": {"role": "user", "content": query},
        "agent_id": agent_id
    }
    
    if thread_id:
        body["thread_id"] = thread_id
    
    response = requests.post(url, headers=headers, params=params, json=body)
    return response.json()
```

**Key Points:**
- Response is immediate but doesn't contain agent's answer
- Returns `run_id` for polling
- Returns `thread_id` for conversation continuity
- Must include both `Authorization` and `IAM-API_KEY` headers

---

## Step 3: Poll for Result

### Endpoint
```
GET {INSTANCE_URL}/v1/orchestrate/runs/{run_id}
```

### Headers
```python
{
    "Authorization": f"Bearer {token}",
    "IAM-API_KEY": api_key
}
```

### Response (when completed)
```json
{
    "status": "completed",
    "result": {
        "data": {
            "message": {
                "content": [
                    {"text": "Agent's response here"}
                ]
            }
        }
    },
    "thread_id": "thread-uuid"
}
```

### Implementation
```python
import time

def poll_run_result(instance_url: str, token: str, api_key: str, 
                    run_id: str, timeout: int = 60) -> dict:
    url = f"{instance_url}/v1/orchestrate/runs/{run_id}"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "IAM-API_KEY": api_key
    }
    
    start_time = time.time()
    
    while True:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        status = data.get("status", "").lower()
        
        if status in {"completed", "succeeded", "success"}:
            return data
        
        if status in {"failed", "error", "cancelled"}:
            raise RuntimeError(f"Run failed: {data}")
        
        if time.time() - start_time > timeout:
            raise TimeoutError("Polling timed out")
        
        time.sleep(0.7)  # Poll every 0.7 seconds
```

**Key Points:**
- Poll every 0.7 seconds
- Check `status` field
- Wait for `completed` status
- Handle `failed` status
- Implement timeout (60 seconds recommended)

---

## Step 4: Extract Response

### Response Path
```
result → data → message → content → [0] → text
```

### Implementation
```python
def extract_response_text(data: dict) -> str:
    try:
        result = data.get("result", {})
        data_obj = result.get("data", {})
        message = data_obj.get("message", {})
        content = message.get("content", [])
        
        texts = []
        for item in content:
            if isinstance(item, dict) and "text" in item:
                texts.append(item["text"])
        
        return "\n".join(texts).strip()
    except Exception:
        return ""
```

**Key Points:**
- Response is nested deeply
- Content is an array
- Multiple text blocks possible
- Handle missing fields gracefully

---

## Complete Flow Example

```python
import requests
import time
from typing import Optional

def chat_with_agent(
    instance_url: str,
    api_key: str,
    agent_id: str,
    query: str,
    thread_id: Optional[str] = None
) -> tuple[str, str]:
    """
    Send a message to agent and get response.
    
    Returns:
        (response_text, thread_id)
    """
    # Step 1: Get token
    token = get_token(api_key)
    
    # Step 2: Send message
    response = send_message(instance_url, token, api_key, agent_id, query, thread_id)
    run_id = response["run_id"]
    thread_id = response["thread_id"]
    
    # Step 3: Poll for result
    result = poll_run_result(instance_url, token, api_key, run_id)
    
    # Step 4: Extract text
    text = extract_response_text(result)
    
    return text, thread_id

# Usage
response, thread_id = chat_with_agent(
    instance_url="https://api.jp-tok.watson-orchestrate.cloud.ibm.com/instances/xxx",
    api_key="your_api_key",
    agent_id="your_agent_id",
    query="Hello!"
)

print(f"Agent: {response}")

# Continue conversation
response2, _ = chat_with_agent(
    instance_url="https://api.jp-tok.watson-orchestrate.cloud.ibm.com/instances/xxx",
    api_key="your_api_key",
    agent_id="your_agent_id",
    query="What can you do?",
    thread_id=thread_id  # Same thread
)

print(f"Agent: {response2}")
```

---

## Thread Management

### New Conversation
```python
# Omit thread_id to start new conversation
response = send_message(url, token, key, agent_id, "Hello")
thread_id = response["thread_id"]  # Save for later
```

### Continue Conversation
```python
# Include thread_id to continue
response = send_message(url, token, key, agent_id, "Follow-up", thread_id)
```

**Key Points:**
- Each conversation has unique `thread_id`
- Thread maintains context
- Reuse `thread_id` for multi-turn conversations
- Threads persist on server

---

## Error Handling

```python
try:
    token = get_token(api_key)
    response = send_message(url, token, api_key, agent_id, query)
    result = poll_run_result(url, token, api_key, response["run_id"])
    text = extract_response_text(result)
    
except requests.HTTPError as e:
    if e.response.status_code == 401:
        print("Authentication failed - check API key")
    elif e.response.status_code == 404:
        print("Agent not found - check agent_id")
    else:
        print(f"HTTP Error: {e.response.status_code}")
        
except TimeoutError:
    print("Agent response timeout")
    
except Exception as e:
    print(f"Error: {str(e)}")
```

---

## Common Issues

### Issue: Empty Response
**Cause:** Response parsing failed  
**Solution:** Check response structure, add debug logging

### Issue: 401 Unauthorized
**Cause:** Invalid or expired token  
**Solution:** Regenerate token, check API key

### Issue: 404 Not Found
**Cause:** Wrong endpoint or agent_id  
**Solution:** Verify INSTANCE_URL and AGENT_ID

### Issue: Timeout
**Cause:** Agent taking too long  
**Solution:** Increase timeout, check agent status

---

## Best Practices

1. **Token Caching**
   ```python
   class TokenCache:
       def __init__(self):
           self.token = None
           self.expiry = 0
       
       def get_token(self, api_key):
           if time.time() < self.expiry:
               return self.token
           self.token = get_token(api_key)
           self.expiry = time.time() + 3000
           return self.token
   ```

2. **Connection Pooling**
   ```python
   session = requests.Session()
   # Reuse for all requests
   ```

3. **Retry Logic**
   ```python
   for attempt in range(3):
       try:
           return send_message(...)
       except requests.HTTPError:
           if attempt == 2:
               raise
           time.sleep(2 ** attempt)
   ```

4. **Logging**
   ```python
   import logging
   logging.info(f"Sending: {query}")
   logging.debug(f"Response: {response}")
   ```

---

## Quick Reference

| Step | Endpoint | Method | Key Headers |
|------|----------|--------|-------------|
| Auth | `iam.cloud.ibm.com/identity/token` | POST | `Content-Type: application/x-www-form-urlencoded` |
| Send | `{URL}/v1/orchestrate/runs` | POST | `Authorization`, `IAM-API_KEY` |
| Poll | `{URL}/v1/orchestrate/runs/{run_id}` | GET | `Authorization`, `IAM-API_KEY` |

**Response Path:** `result.data.message.content[0].text`

**Polling:** Every 0.7s, timeout 60s, check `status` field

**Thread:** Include `thread_id` to continue conversation

---

## For LLMs: Key Takeaways

1. **Three-step process**: Authenticate → Send → Poll
2. **Two required headers**: `Authorization: Bearer {token}` AND `IAM-API_KEY: {key}`
3. **Polling is mandatory**: Initial response only contains `run_id`, not the answer
4. **Deep nesting**: Response text is at `result.data.message.content[0].text`
5. **Thread continuity**: Save and reuse `thread_id` for conversations
6. **Token caching**: Tokens last 50 minutes, cache them
7. **Error handling**: Check status codes and implement timeouts

---

**Version:** 1.0  
**Last Updated:** 2026-05-03  
**Status:** Production Ready ✅