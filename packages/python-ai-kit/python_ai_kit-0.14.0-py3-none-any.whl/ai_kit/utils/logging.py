from typing import Union, List, Dict, Any
from ..cli import console_instance

def pretty_print(obj: Union[List[Dict[str, Any]], str]) -> None:
    """Pretty print the results."""
    cons