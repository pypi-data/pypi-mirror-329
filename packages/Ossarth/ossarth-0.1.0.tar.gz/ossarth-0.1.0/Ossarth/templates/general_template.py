TOOL_TEMPLATE = """from langchain_core.tools import tool

@tool(parse_docstring=True)
def {func_name}({params}):
    \"\"\"{description}

    Args:
        {args_doc}

    Returns:
        {return_type}: {return_desc}
    \"\"\"    
    {body}
"""

FUNCTION_TEMPLATE = """def {func_name}({params}):
    \"\"\"{description}

    Args:
        {args_doc}

    Returns:
        {return_type}: {return_desc}
    \"\"\"    
    {body}
"""
