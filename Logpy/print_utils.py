"""
Print Utilities - Reusable colored printing functions

This module provides formatted printing functions with color support that can be:
1. Imported into other scripts for consistent output formatting
2. Run independently to test printing functionality

Available message types:
- title: Bold headers with newlines
- msg: Plain messages  
- ok: Green checkmark for success
- info: Blue arrow for information
- err: Red X for errors (exits program)
- ask: Cyan question prompt with input

Usage as import (inside the Logpy package):
    from Logpy import smart_print, ok, info, err
    # or, equivalently:
    from Logpy.print_utils import smart_print, ok, info, err
    smart_print("Hello", "info")
    ok("Success!")

Usage as standalone:
    python -m Logpy.print_utils
    python print_utils.py
"""

import sys


# ── Colours ──────────────────────────────────────────────────────────────────
class C:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    DIM    = "\033[2m"
    GREEN  = "\033[92m"
    BLUE   = "\033[94m"
    CYAN   = "\033[96m"
    WHITE  = "\033[97m"
    RED    = "\033[91m"


def title(msg): 
    """Print a bold title with newlines before and after."""
    print(f"\n{C.BOLD}{msg}{C.RESET}\n")


def msg(msg):  
    """Print a plain message."""
    print(f"  {msg}")


def ok(msg):   
    """Print a success message with green checkmark."""
    print(f"  {C.GREEN}✓{C.RESET}  {msg}")


def info(msg): 
    """Print an info message with blue arrow."""
    print(f"  {C.BLUE}→{C.RESET}  {msg}")


def err(msg):  
    """Print an error message with red X and exit the program."""
    print(f"  {C.RED}✗{C.RESET}  {msg}")
    sys.exit(1)


def ask(prompt, default=""):
    """
    Prompt user for input with cyan question mark.
    
    Args:
        prompt (str): The question to ask
        default (str): Default value if user presses enter
        
    Returns:
        str: User's input or default value
    """
    hint = f" [{C.DIM}{default}{C.RESET}]" if default else ""
    return input(f"  {C.CYAN}?{C.RESET}  {prompt}{hint}: ").strip() or default


def smart_print(message, msg_type=None):
    """
    Reusable function for formatted printing with message type support.
    
    Args:
        message (str): The message to print.
        msg_type (str): Optional message type ('ok', 'info', 'err', 'ask', 'title', 'msg').
                       If None, uses regular print().
    """
    if msg_type:
        if msg_type == "ok":
            ok(message)
        elif msg_type == "info":
            info(message)
        elif msg_type == "err":
            err(message)
        elif msg_type == "ask":
            return ask(message)
        elif msg_type == "title":
            title(message)
        elif msg_type == "msg":
            msg(message)
        else:
            print(f"  {C.RED}✗{C.RESET}  Unknown message type: {msg_type}")
    else:
        print(message)


# ==============================================================================
# DEMO / TESTING - Run when called independently
# ==============================================================================

if __name__ == "__main__":
    print('\n')
    print("=" * 60)
    print("PRINT UTILITIES DEMONSTRATION")
    print("=" * 60)
    
    # Demo all message types
    title("Print Utilities Demo")
    
    msg("This is a regular message")
    ok("This is a success message")
    info("This is an info message")
    
    # Demo smart_print function
    print("\nUsing smart_print function:")
    smart_print("Success via smart_print!", "ok")
    smart_print("Info via smart_print!", "info")
    smart_print("Title via smart_print!", "title")
    smart_print("Regular message via smart_print!")
    
    # Demo user input (commented out for automated testing)
    print("\nInteractive demo:")
    print("# user_name = ask('What is your name?', 'Anonymous')")
    print("# smart_print(f'Hello {user_name}!', 'ok')")
    
    print("\n" + "=" * 60)
    print("Demo complete! Import this module in your scripts:")
    print("  from Logpy import smart_print, ok, info, err")
    print("=" * 60)
    print('\n')