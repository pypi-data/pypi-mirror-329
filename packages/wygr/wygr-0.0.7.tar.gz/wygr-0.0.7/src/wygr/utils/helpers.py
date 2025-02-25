import re

def parse_user_input(prompt):
    """Parse the user's input for destination and duration."""
    match = re.search(r'travel plan to (\w+)(?: for (\d+) days)?', prompt, re.IGNORECASE)
    if match:
        destination = match.group(1)
        days = int(match.group(2)) if match.group(2) else 3
        return destination, days
    return None, None
