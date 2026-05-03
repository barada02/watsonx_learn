"""
Correct implementation for Watson Orchestrate agent interaction.
Based on IBM's official API documentation.
"""

import os
import time
import json
from typing import Optional, Dict, Any
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class WatsonxOrchestrate:
    """Client for interacting with watsonx orchestrate agents."""
    
    def __init__(
        self,
        instance_url: str,
        api_key: str,
        token_ttl_seconds: int = 3000  # 50 minutes default
    ):
        """
        Initialize the watsonx orchestrate client.
        
        Args:
            instance_url: Your Watson Orchestrate instance URL
            api_key: Your IBM Cloud API key
            token_ttl_seconds: Token time-to-live in seconds
        """
        self.instance_url = instance_url.rstrip("/")
        self.api_key = api_key
        # Use IBM Cloud IAM endpoint (works with your instance)
        self.token_endpoint = "https://iam.cloud.ibm.com/identity/token"
        self.token_ttl_seconds = token_ttl_seconds
        
        # Token cache
        self._token = None
        self._token_expiry = 0.0
        
        # HTTP session for connection pooling
        self.session = requests.Session()
    
    def get_token(self) -> str:
        """
        Get an authentication token (cached if still valid).
        
        Returns:
            str: Bearer token for API authentication
        """
        now = time.monotonic()
        
        # Return cached token if still valid
        if self._token and now < self._token_expiry:
            return self._token
        
        # Request new token
        print("Fetching new authentication token...")
        
        # Use IBM Cloud IAM format (tested and working)
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
        data = {
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
            "apikey": self.api_key,
        }
        
        response = self.session.post(
            self.token_endpoint,
            data=data,
            headers=headers
        )
        response.raise_for_status()
        
        token_data = response.json()
        token = token_data.get("access_token") or token_data.get("token")
        
        if not token:
            raise ValueError("Authentication server did not return a token")
        
        # Cache token
        self._token = token
        self._token_expiry = now + self.token_ttl_seconds
        
        print("✓ Token obtained successfully")
        return token
    
    def list_agents(self) -> Dict[str, Any]:
        """
        List all available agents.
        
        Returns:
            Dict containing agents list
        """
        token = self.get_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        
        url = f"{self.instance_url}/v1/orchestrate/agents"
        response = self.session.get(url, headers=headers)
        response.raise_for_status()
        
        return response.json()
    
    def send_message(
        self,
        query: str,
        agent_id: str,
        thread_id: Optional[str] = None,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Send a message to an agent.
        
        Args:
            query: The message/question to send
            agent_id: The ID of the agent to use
            thread_id: Optional thread ID (creates new if not provided)
            stream: Whether to use streaming
            
        Returns:
            Dict containing the response
        """
        token = self.get_token()
        
        # Headers include both Bearer token and API key
        headers = {
            "Authorization": f"Bearer {token}",
            "IAM-API_KEY": self.api_key,
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        
        # Build request body
        body = {
            "message": {
                "role": "user",
                "content": query
            },
            "agent_id": agent_id
        }
        
        if thread_id:
            body["thread_id"] = thread_id
        
        # Build URL with query parameters
        params = {
            "stream": "true" if stream else "false",
            "stream_timeout": "120000",
            "multiple_content": "true"
        }
        
        url = f"{self.instance_url}/v1/orchestrate/runs"
        
        print(f"\nSending message to agent '{agent_id}'...")
        print(f"Query: {query}")
        if thread_id:
            print(f"Thread ID: {thread_id}")
        
        response = self.session.post(
            url,
            headers=headers,
            params=params,
            json=body
        )
        response.raise_for_status()
        
        data = response.json()
        
        # Extract response
        thread_id = data.get("thread_id")
        status = data.get("status", "completed")
        
        # Extract message content
        response_text = self._extract_response_text(data)
        
        print("✓ Response received")
        
        return {
            "status": status,
            "response": response_text,
            "thread_id": thread_id,
            "raw": data
        }
    
    def _extract_response_text(self, data: Dict[str, Any]) -> str:
        """
        Extract the response text from the API response.
        
        Args:
            data: The API response data
            
        Returns:
            str: Extracted response text
        """
        # Try result.data.message.content format
        try:
            result = data.get("result", {})
            if isinstance(result, dict):
                data_obj = result.get("data", {})
                if isinstance(data_obj, dict):
                    message = data_obj.get("message", {})
                    if isinstance(message, dict):
                        content = message.get("content")
                        if isinstance(content, list):
                            texts = []
                            for item in content:
                                if isinstance(item, dict):
                                    text = item.get("text")
                                    if text and isinstance(text, str):
                                        texts.append(text)
                            if texts:
                                return "\n".join(texts).strip()
        except Exception:
            pass
        
        # Try direct message field
        if "message" in data:
            msg = data["message"]
            if isinstance(msg, str):
                return msg.strip()
            elif isinstance(msg, dict):
                content = msg.get("content")
                if isinstance(content, str):
                    return content.strip()
        
        # Try response field
        if "response" in data and isinstance(data["response"], str):
            return data["response"].strip()
        
        return ""
    
    def close(self):
        """Close the HTTP session."""
        self.session.close()


def main():
    """Main function demonstrating agent usage."""
    
    # Load configuration
    INSTANCE_URL = os.getenv("INSTANCE_URL")
    API_KEY = os.getenv("API_KEY")
    AGENT_ID = os.getenv("AGENT_ID")
    
    # Validate required environment variables
    if not all([INSTANCE_URL, API_KEY]):
        print("ERROR: Missing required environment variables!")
        print("Please set the following in your .env file:")
        print("  - INSTANCE_URL (your Watson Orchestrate instance URL)")
        print("  - API_KEY (your IBM Cloud API key)")
        print("  - AGENT_ID (optional, will prompt if not set)")
        return
    
    # Prompt for agent_id if not in environment
    if not AGENT_ID:
        AGENT_ID = input("Enter your Agent ID: ").strip()
        if not AGENT_ID:
            print("ERROR: Agent ID is required")
            return
    
    print("=" * 60)
    print("Watsonx Orchestrate Agent Runner")
    print("=" * 60)
    
    # Initialize client (type checking already done above)
    client = WatsonxOrchestrate(
        instance_url=INSTANCE_URL,  # type: ignore
        api_key=API_KEY  # type: ignore
    )
    
    try:
        # Example 1: Single message
        print("\n--- Example 1: Single Message ---")
        result = client.send_message(
            query="Hello! Can you help me?",
            agent_id=AGENT_ID
        )
        print(f"\nAgent Response:\n{result['response']}")
        print(f"Thread ID: {result['thread_id']}")
        
        # Example 2: Continue conversation in same thread
        print("\n--- Example 2: Continue Conversation ---")
        thread_id = result['thread_id']
        result2 = client.send_message(
            query="What can you do?",
            agent_id=AGENT_ID,
            thread_id=thread_id
        )
        print(f"\nAgent Response:\n{result2['response']}")
        
        # Interactive mode
        print("\n--- Interactive Mode ---")
        print("Type your messages (or 'quit' to exit):\n")
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if not user_input:
                continue
            
            result = client.send_message(
                query=user_input,
                agent_id=AGENT_ID,
                thread_id=thread_id
            )
            
            print(f"\nAgent: {result['response']}\n")
    
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        client.close()
        print("\n✓ Session closed")


if __name__ == "__main__":
    main()

# Made with Bob
