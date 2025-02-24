import os
import atexit
import code
import readline  # Assuming this is imported elsewhere in your module
import sys
from typing import Dict, Any
from .df_lib import *  # noqa: F401, F403, E402
from .algebra_lib import *  # noqa: F401, F403, E402
from .str_lib import *  # noqa: F401, F403, E402
from .docs_lib import *  # noqa: F401, F403, E402

class CustomConsole(code.InteractiveConsole):
    """Custom console to make user input white while keeping prompts and output default."""
    def raw_input(self, prompt=""):
        # Print the prompt (>>>), then switch to white for input
        sys.stdout.write(prompt)  # Prompt in default color
        sys.stdout.write("\033[97m")  # Switch to white for input
        sys.stdout.flush()
        try:
            line = input()  # User types in white
        except EOFError:
            raise  # Handle Ctrl+D gracefully
        finally:
            sys.stdout.write("\033[0m")  # Reset to default after input
            sys.stdout.flush()
        return line

def interactive_shell(local_vars: Dict[str, Any], shell_color: str = '') -> None:
    """
    Launches an interactive prompt for inspecting and modifying local variables, making all methods
    in the rgwfuncs library available by default. Persists command history across sessions.
    User input is displayed in white; other text uses the terminal's default color.

    Parameters:
        local_vars (dict): Dictionary of local variables to be available in the interactive shell.
        shell_color (str): ANSI color code for shell output (default: empty for terminal default).
    """

    def setup_readline(shell_color: str = '') -> None:
        """Set up readline for history persistence with a given shell color."""
        HISTORY_FILE = os.path.expanduser("~/.rgwfuncs_shell_history")
        readline.set_history_length(1000)
        readline.parse_and_bind("tab: complete")
        if os.path.exists(HISTORY_FILE):
            try:
                readline.read_history_file(HISTORY_FILE)
            except Exception as e:
                print(f"{shell_color}Warning: Could not load history file: {e}")
        atexit.register(readline.write_history_file, HISTORY_FILE)

    if not isinstance(local_vars, dict):
        raise TypeError("local_vars must be a dictionary")

    # Set up readline for history and completion
    setup_readline()

    # Make imported functions available in the REPL
    local_vars.update(globals())

    # Set prompt to plain text (no color)
    sys.ps1 = ">>> "

    # Create custom console with local context
    console = CustomConsole(locals=local_vars)

    # Start interactive session with a custom banner and exit message in default color
    banner = f"{shell_color}Welcome to the rgwfuncs interactive shell.\nUse up/down arrows for command history.\nType 'exit()' or Ctrl+D to quit."
    exitmsg = f"{shell_color}Goodbye."

    # Run the interactive session
    console.interact(banner=banner, exitmsg=exitmsg)

