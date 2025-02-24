#!/usr/bin/env python3
import code
import readline
import rlcompleter  # noqa: F401
import sys
import os
import atexit
from typing import Dict, Any
from .df_lib import *  # noqa: F401, F403, E402
from .algebra_lib import *  # noqa: F401, F403, E402
from .str_lib import *  # noqa: F401, F403, E402
from .docs_lib import *  # noqa: F401, F403, E402

def interactive_shell(local_vars: Dict[str, Any], shell_color: str = '\033[94m') -> None:
    """
    Launches an interactive prompt for inspecting and modifying local variables, making all methods
    in the rgwfuncs library available by default. Persists command history across sessions.
    User input is displayed in white, while shell output uses the specified color.

    Parameters:
        local_vars (dict): Dictionary of local variables to be available in the interactive shell.
        shell_color (str): ANSI color code for shell output (default: blue '\033[94m').
    """

    def setup_readline(shell_color: str = '\033[94m') -> None:
        """Set up readline for history persistence with a given shell color."""
        HISTORY_FILE = os.path.expanduser("~/.rgwfuncs_shell_history")
        readline.set_history_length(1000)
        readline.parse_and_bind("tab: complete")
        if os.path.exists(HISTORY_FILE):
            try:
                readline.read_history_file(HISTORY_FILE)
            except Exception as e:
                print(f"{shell_color}Warning: Could not load history file: {e}\033[0m")
        atexit.register(readline.write_history_file, HISTORY_FILE)

    class ColoredConsole(code.InteractiveConsole):
        """Custom console to handle colored output while keeping input white."""
        def __init__(self, locals=None, shell_color='\033[94m'):
            super().__init__(locals)
            self.shell_color = shell_color
            self.reset_color = '\033[0m'
            self.input_color = '\033[97m'  # Bright white for input

        def write(self, data):
            """Write output with shell color."""
            sys.stdout.write(f"{self.shell_color}{data}{self.reset_color}")
            sys.stdout.flush()

        def raw_input(self, prompt=""):
            """Get input with white color."""
            sys.stdout.write(f"{self.shell_color}{prompt}{self.input_color}")
            sys.stdout.flush()
            line = input()
            sys.stdout.write(self.reset_color)
            return line

    if not isinstance(local_vars, dict):
        raise TypeError("local_vars must be a dictionary")

    # Set up readline for history and completion
    setup_readline(shell_color)

    # Make imported functions available in the REPL
    local_vars.update(globals())

    # Create interactive console with local context and custom coloring
    console = ColoredConsole(locals=local_vars, shell_color=shell_color)

    # Start interactive session with a custom banner and exit message
    banner = f"{shell_color}Welcome to the rgwfuncs interactive shell.\nUse up/down arrows for command history.\nType 'exit()' or Ctrl+D to quit.{shell_color}"
    exitmsg = f"{shell_color}Goodbye.{shell_color}"

    # Run the interactive session
    console.interact(banner=banner, exitmsg=exitmsg)

