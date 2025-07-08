"""
Utility functions for the API
"""

def read_template_file(file_path: str) -> str:
    """
    Safely read a template file with proper encoding handling
    
    Args:
        file_path: Path to the template file
        
    Returns:
        Content of the template file as string
        
    Raises:
        FileNotFoundError: If the template file doesn't exist
        UnicodeDecodeError: If the file can't be decoded with any encoding
    """
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            raise FileNotFoundError(f"Template file not found: {file_path}")
    
    # If all encodings fail, try with error handling
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        raise UnicodeDecodeError(f"Could not read template file {file_path}: {str(e)}")

def safe_format(template: str, **kwargs) -> str:
    """
    Safely format a template string with the given parameters
    
    Args:
        template: The template string
        **kwargs: Parameters to format the template with
        
    Returns:
        Formatted template string
    """
    try:
        return template.format(**kwargs)
    except KeyError as e:
        # Replace missing keys with empty string
        missing_key = str(e).strip("'")
        return template.format(**{k: v if k != missing_key else '' for k, v in kwargs.items()})
    except Exception as e:
        # Return template as-is if formatting fails
        return template 