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

# ANSI color escape codes
BLUE = "\033[34m"
WHITE = "\033[37m"
RESET = "\033[0m"

class BlueStdout:
    """
    A wrapper for sys.stdout that automatically prepends blue
    color codes on output.
    """
    def __init__(self, wrapped):
        self.wrapped = wrapped
        self.at_line_start = True

    def write(self, s):
        # Do not interfere with prompt strings.
        if s == sys.ps1 or s == sys.ps2:
            self.wrapped.write(s)
            return

        # Process text line by line so that new lines are colored.
        lines = s.split('\n')
        for i, line in enumerate(lines):
            if self.at_line_start and line:
                self.wrapped.write(BLUE + line)
            else:
                self.wrapped.write(line)
            if i < len(lines) - 1:
                self.wrapped.write('\n' + RESET)
                self.at_line_start = True
            else:
                self.at_line_start = (line == "")

    def flush(self):
        self.wrapped.flush()

    def isatty(self):
        return self.wrapped.isatty()

    def fileno(self):
        return self.wrapped.fileno()

    def __getattr__(self, attr):
        # Delegate attribute access to the original stdout.
        return getattr(self.wrapped, attr)

class ColorInteractiveConsole(code.InteractiveConsole):
    """Subclass InteractiveConsole to temporarily restore the real stdout when reading input."""
    def raw_input(self, prompt=""):
        # Before calling input(), restore the original stdout so that readline works properly.
        saved_stdout = sys.stdout
        sys.stdout = sys.__stdout__
        try:
            line = input(prompt)
        except EOFError:
            raise
        finally:
            # Restore our blue-printing stdout.
            sys.stdout = saved_stdout
        return line

def interactive_shell(local_vars: Dict[str, Any]) -> None:
    """
    Launches an interactive prompt for inspecting and modifying local variables,
    making all methods in the rgwfuncs library available by default.
    Persists command history across sessions.

    Parameters:
        local_vars (dict): Dictionary of local variables to be available in the interactive shell.
    """
    def setup_readline() -> None:
        """Set up readline for history persistence."""
        HISTORY_FILE = os.path.expanduser("~/.rgwfuncs_shell_history")
        readline.set_history_length(1000)
        readline.parse_and_bind("tab: complete")
        if os.path.exists(HISTORY_FILE):
            try:
                readline.read_history_file(HISTORY_FILE)
            except Exception as e:
                print(f"Warning: Could not load history file: {e}")
        atexit.register(readline.write_history_file, HISTORY_FILE)

    if not isinstance(local_vars, dict):
        raise TypeError("local_vars must be a dictionary")

    # Set up readline.
    setup_readline()

    # Make imported functions available in the REPL.
    local_vars.update(globals())

    # Note: Wrap ANSI codes in markers that readline understands so that they don’t count in prompt length.
    sys.ps1 = "\001" + WHITE + "\002" + ">>> " + "\001" + RESET + "\002"
    sys.ps2 = "\001" + WHITE + "\002" + "... " + "\001" + RESET + "\002"

    # Wrap sys.stdout for colored output.
    sys.stdout = BlueStdout(sys.__stdout__)  # Wrap the original stdout.

    # Use our custom interactive console.
    console = ColorInteractiveConsole(locals=local_vars)

    banner = ("Welcome to the rgwfuncs interactive shell.\n"
              "Use up/down arrows for command history.\n"
              "Type 'exit()' or Ctrl+D to quit.")
    exitmsg = "Goodbye."

    try:
        console.interact(banner=banner)
    finally:
        print(exitmsg)

