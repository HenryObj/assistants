# ************************************************************************************************
# ****************************************** IMPORTS *********************************************
from typing import Callable, Any, Union, Optional
from datetime import datetime
import inspect
import re
from config import *

# *************************************************************************************************
# ****************************************** FUNCTIONS ********************************************
# *************************************************************************************************

def log_issue(exception: Exception, func: Callable[..., Any], additional_info: str = "") -> None:
    '''
    Logs an issue. Can be called anywhere and will display an error message showing the module, the function, the exception and if specified, the additional info.

    Args:
        exception (Exception): The exception that was raised.
        func (Callable[..., Any]): The function in which the exception occurred.
        additional_info (str): Any additional information to log. Default is an empty string.

    Returns:
        None
    '''
    now = datetime.now().strftime("%d/%m/%y %H:%M:%S")
    module_name = get_module_name(func)
    additional = f"""
    ****************************************
    Additional Info: 
    {additional_info}
    ****************************************""" if additional_info else ""
    print(f"""
    ----------------------------------------------------------------
    🚨 ERROR 🚨
    Occurred: {now}
    Module: {module_name} | Function: {func.__name__}
    Exception: {exception}{additional}
    ----------------------------------------------------------------
    """)

def get_module_name(func: Callable[..., Any]) -> str:
    '''
    Given a function, returns the name of the module in which it is defined.
    '''
    module = inspect.getmodule(func)
    if module is None:
        return ''
    else:
        return module.__name__.split('.')[-1]
    
def get_now(exact: bool = False) -> str:
    '''
    Small function to get the timestamp in string format.
    By default we return the following format: "10_Jan_2023" but if exact is True, we will return 10_Jan_2023_@15h23s33
    '''
    now = datetime.now()
    return datetime.strftime(now, "%d_%b_%Y@%Hh%Ms%S") if exact else datetime.datetime.strftime(now, "%d_%b_%Y")

def check__if_password_safe(password: str) -> bool:
    """
    Checks if a password is composed of regular chars or not.
    """
    if not isinstance(password, str): return False
    return bool(re.match(r'^[a-zA-Z0-9$*&@#%!=+,.:;<>?[\]^_`{|}~"-]+$', password))