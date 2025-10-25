"""
Utility functions for the Streamlit app.

Add your helper functions here to keep the main app file clean.
"""

# Example utility functions

def format_message(message: str, role: str = "user") -> dict:
    """
    Format a message for display.
    
    Args:
        message: The message content
        role: The role (user, assistant, system)
        
    Returns:
        Formatted message dictionary
    """
    return {
        "role": role,
        "content": message
    }


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to a maximum length.
    
    Args:
        text: The text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text with ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def validate_api_key(api_key: str) -> bool:
    """
    Validate API key format.
    
    Args:
        api_key: The API key to validate
        
    Returns:
        True if valid format, False otherwise
    """
    if not api_key:
        return False
    
    # Basic validation - adjust based on your needs
    if len(api_key) < 20:
        return False
    
    return True


# Add more utility functions as needed

