#!/usr/bin/env python3
import code
import readline
import rlcompleter  # noqa: F401
import sys  # noqa: F401
import os
import atexit
from typing import Dict, Any
from .df_lib import *  # noqa: F401, F403, E402
from .algebra_lib import *  # noqa: F401, F403, E402
from .str_lib import *  # noqa: F401, F403, E402
from .docs_lib import *  # noqa: F401, F403, E402

# File for command history
HISTORY_FILE = os.path.expanduser("~/.rgwfuncs_shell_history")

def setup_readline():
    """Set up readline for command history persistence"""
    readline.set_history_length(1000)  # Limit history to 1000 lines
    readline.parse_and_bind("tab: complete")  # Enable tab completion
    if os.path.exists(HISTORY_FILE):
        try:
            readline.read_history_file(HISTORY_FILE)
        except Exception as e:
            print(f"Warning: Could not load history file: {e}")
    atexit.register(readline.write_history_file, HISTORY_FILE)

def interactive_shell(local_vars: Dict[str, Any]) -> None:
    """
    Launches an interactive prompt for inspecting and modifying local variables, making all methods
    in the rgwfuncs library available by default. Persists command history across sessions.

    Parameters:
        local_vars (dict): Dictionary of local variables to be available in the interactive shell.
    """
    if not isinstance(local_vars, dict):
        raise TypeError("local_vars must be a dictionary")

    # Set up readline for history and completion
    setup_readline()

    # Make imported functions available in the REPL
    local_vars.update(globals())

    # Create interactive console with local context
    console = code.InteractiveConsole(locals=local_vars)

    # Start interactive session with a custom banner
    banner = "Welcome to the rgwfuncs interactive shell.\nUse up/down arrows for command history.\nType 'exit()' or Ctrl+D to quit."
    console.interact(banner=banner, exitmsg="Goodbye.")
