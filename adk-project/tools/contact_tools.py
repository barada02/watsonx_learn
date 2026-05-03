"""
Contact Management Tools for Watson Orchestrate
These tools provide basic contact management functionality.
"""

import json
from typing import Dict, List, Optional


# In-memory storage (in production, use a database)
contacts_db = []


def add_contact(
    name: str,
    phone: Optional[str] = None,
    email: Optional[str] = None,
    address: Optional[str] = None,
    category: Optional[str] = "general",
    notes: Optional[str] = None
) -> Dict:
    """
    Add a new contact to the contact manager.
    
    Args:
        name: Full name of the contact (required)
        phone: Phone number
        email: Email address
        address: Physical address
        category: Category (family, friends, work, general)
        notes: Additional notes about the contact
    
    Returns:
        Dictionary with the created contact information
    """
    contact_id = len(contacts_db) + 1
    
    contact = {
        "id": contact_id,
        "name": name,
        "phone": phone,
        "email": email,
        "address": address,
        "category": category,
        "notes": notes
    }
    
    contacts_db.append(contact)
    
    return {
        "success": True,
        "message": f"Contact '{name}' added successfully",
        "contact": contact
    }


def search_contact(query: str) -> Dict:
    """
    Search for contacts by name, phone, or email.
    
    Args:
        query: Search term to look for in contact information
    
    Returns:
        Dictionary with matching contacts
    """
    query_lower = query.lower()
    matches = []
    
    for contact in contacts_db:
        if (query_lower in contact["name"].lower() or
            (contact["phone"] and query_lower in contact["phone"].lower()) or
            (contact["email"] and query_lower in contact["email"].lower())):
            matches.append(contact)
    
    return {
        "success": True,
        "count": len(matches),
        "contacts": matches
    }


def update_contact(
    contact_id: int,
    name: Optional[str] = None,
    phone: Optional[str] = None,
    email: Optional[str] = None,
    address: Optional[str] = None,
    category: Optional[str] = None,
    notes: Optional[str] = None
) -> Dict:
    """
    Update an existing contact's information.
    
    Args:
        contact_id: ID of the contact to update (required)
        name: New name
        phone: New phone number
        email: New email address
        address: New address
        category: New category
        notes: New notes
    
    Returns:
        Dictionary with the updated contact information
    """
    for contact in contacts_db:
        if contact["id"] == contact_id:
            if name:
                contact["name"] = name
            if phone:
                contact["phone"] = phone
            if email:
                contact["email"] = email
            if address:
                contact["address"] = address
            if category:
                contact["category"] = category
            if notes:
                contact["notes"] = notes
            
            return {
                "success": True,
                "message": f"Contact ID {contact_id} updated successfully",
                "contact": contact
            }
    
    return {
        "success": False,
        "message": f"Contact with ID {contact_id} not found"
    }


def delete_contact(contact_id: int) -> Dict:
    """
    Delete a contact from the contact manager.
    
    Args:
        contact_id: ID of the contact to delete
    
    Returns:
        Dictionary with deletion status
    """
    for i, contact in enumerate(contacts_db):
        if contact["id"] == contact_id:
            deleted_contact = contacts_db.pop(i)
            return {
                "success": True,
                "message": f"Contact '{deleted_contact['name']}' deleted successfully",
                "contact": deleted_contact
            }
    
    return {
        "success": False,
        "message": f"Contact with ID {contact_id} not found"
    }


def list_contacts(category: Optional[str] = None) -> Dict:
    """
    List all contacts or contacts in a specific category.
    
    Args:
        category: Optional category to filter by (family, friends, work, general)
    
    Returns:
        Dictionary with list of contacts
    """
    if category:
        filtered_contacts = [c for c in contacts_db if c["category"] == category]
        return {
            "success": True,
            "category": category,
            "count": len(filtered_contacts),
            "contacts": filtered_contacts
        }
    
    return {
        "success": True,
        "count": len(contacts_db),
        "contacts": contacts_db
    }


def categorize_contact(contact_id: int, category: str) -> Dict:
    """
    Change the category of a contact.
    
    Args:
        contact_id: ID of the contact
        category: New category (family, friends, work, general)
    
    Returns:
        Dictionary with the updated contact
    """
    valid_categories = ["family", "friends", "work", "general"]
    
    if category not in valid_categories:
        return {
            "success": False,
            "message": f"Invalid category. Must be one of: {', '.join(valid_categories)}"
        }
    
    for contact in contacts_db:
        if contact["id"] == contact_id:
            contact["category"] = category
            return {
                "success": True,
                "message": f"Contact categorized as '{category}'",
                "contact": contact
            }
    
    return {
        "success": False,
        "message": f"Contact with ID {contact_id} not found"
    }

# Made with Bob
