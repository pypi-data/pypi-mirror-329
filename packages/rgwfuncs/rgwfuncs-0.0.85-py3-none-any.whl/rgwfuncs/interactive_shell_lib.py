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

def interactive_shell(local_vars: Dict[str, Any]) -> None:
    """
    Launch an interactive prompt for inspecting and modifying local variables,
    with a custom blue output and white prompt. All helper definitions are nested within.
    
    local_vars: dictionary with local variables to be available in the interactive shell.
    """
    
    # ANSI color escape codes.
    BLUE = "\033[94m"
    WHITE = "\033[37m"
    RESET = "\033[0m"
    
    # Helper: setup readline for history persistence.
    def setup_readline() -> None:
        HISTORY_FILE = os.path.expanduser("~/.rgwfuncs_shell_history")
        readline.set_history_length(1000)
        readline.parse_and_bind("tab: complete")
        if os.path.exists(HISTORY_FILE):
            try:
                readline.read_history_file(HISTORY_FILE)
            except Exception as e:
                print(f"Warning: Could not load history file: {e}")
        atexit.register(readline.write_history_file, HISTORY_FILE)
    
    # Nested BlueStdout: a wrapper for sys.stdout that prepends blue color on output.
    class BlueStdout:
        def __init__(self, wrapped):
            self.wrapped = wrapped
            self.at_line_start = True
            
        def write(self, s):
            # Do not interfere with the prompt strings.
            if s == sys.ps1 or s == sys.ps2:
                self.wrapped.write(s)
                return
            # Process output line by line.
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
            return getattr(self.wrapped, attr)
    
    # Nested ColorInteractiveConsole: a subclass of InteractiveConsole that temporarily
    # restores the original stdout when reading input so that readline functions properly.
    class ColorInteractiveConsole(code.InteractiveConsole):
        def raw_input(self, prompt=""):
            saved_stdout = sys.stdout
            sys.stdout = sys.__stdout__
            try:
                line = input(prompt)
            except EOFError:
                raise
            finally:
                sys.stdout = saved_stdout
            return line
    
    # Ensure that the passed local_vars is a dictionary.
    if not isinstance(local_vars, dict):
        raise TypeError("local_vars must be a dictionary")
    
    # Setup readline.
    setup_readline()
    
    # Make imported functions available in the REPL by merging globals.
    local_vars.update(globals())
    
    # Wrap ANSI escape sequences in markers recognized by readline so that they do not count
    # toward the visible prompt length.
    sys.ps1 = "\001" + WHITE + "\002" + ">>> " + "\001" + RESET + "\002"
    sys.ps2 = "\001" + WHITE + "\002" + "... " + "\001" + RESET + "\002"
    
    # Replace sys.stdout with our blue-printing wrapper.
    sys.stdout = BlueStdout(sys.__stdout__)
    
    # Instantiate our custom interactive console.
    console = ColorInteractiveConsole(locals=local_vars)
    
    banner = ("Welcome to the rgwfuncs interactive shell.\n"
              "Use up/down arrows for command history.\n"
              "Type 'exit()' or Ctrl+D to quit.")
    exitmsg = "Goodbye."
    
    try:
        console.interact(banner=banner)
    finally:
        print(exitmsg)

