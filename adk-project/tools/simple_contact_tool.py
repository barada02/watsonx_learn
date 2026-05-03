"""Simple contact management tool for Watson Orchestrate."""

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
    contact = {
        "name": name,
        "phone": phone,
        "email": email,
        "status": "success",
        "message": f"Contact {name} added successfully"
    }
    return contact


def search_contact(query: str) -> dict:
    """
    Search for a contact by name.
    
    Args:
        query (str): The name to search for
    
    Returns:
        dict: Search results
    """
    return {
        "query": query,
        "results": [],
        "message": f"Searching for: {query}"
    }

# Made with Bob
