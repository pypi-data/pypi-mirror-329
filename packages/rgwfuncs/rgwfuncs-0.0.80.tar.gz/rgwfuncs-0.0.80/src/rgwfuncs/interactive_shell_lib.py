import os
import atexit
import code
import readline  # Assuming this is imported elsewhere
import sys
from typing import Dict, Any
from .df_lib import *  # noqa: F401, F403, E402
from .algebra_lib import *  # noqa: F401, F403, E402
from .str_lib import *  # noqa: F401, F403, E402
from .docs_lib import *  # noqa: F401, F403, E402

class CustomConsole(code.InteractiveConsole):
    """Custom console to make user input white while keeping prompts and output blue."""
    def raw_input(self, prompt=""):
        sys.stdout.write("\033[94m" + prompt)  # Blue prompt
        sys.stdout.write("\033[97m")  # White for input
        sys.stdout.flush()
        try:
            line = input()  # User types in white
        except EOFError:
            raise
        finally:
            sys.stdout.write("\033[94m")  # Back to blue
            sys.stdout.flush()
        return line

    def write(self, data):
        sys.stdout.write("\033[94m" + data)  # Blue output
        sys.stdout.flush()

def interactive_shell(local_vars: Dict[str, Any], shell_color: str = '\033[94m') -> None:
    """
    Launches an interactive prompt for inspecting and modifying local variables, making all methods
    in the rgwfuncs library available by default. Persists command history across sessions.
    User input is displayed in white; other text (prompt, banner, output) is blue.

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
                print(f"{shell_color}Warning: Could not load history file: {e}\033[94m")
        atexit.register(readline.write_history_file, HISTORY_FILE)

    if not isinstance(local_vars, dict):
        raise TypeError("local_vars must be a dictionary")

    # Test colors explicitly
    sys.stdout.write("\033[94mBLUE TEST\033[0m\n")
    sys.stdout.write("\033[97mWHITE TEST\033[0m\n")
    sys.stdout.flush()

    # Set initial color to blue
    sys.stdout.write("\033[94m")
    sys.stdout.flush()

    # Set up readline
    setup_readline()

    # Make imported functions available in the REPL
    local_vars.update(globals())

    # Set prompt (color handled by raw_input)
    sys.ps1 = ">>> "

    # Create custom console
    console = CustomConsole(locals=local_vars)

    # Banner and exit message in blue
    banner = f"{shell_color}Welcome to the rgwfuncs interactive shell.\nUse up/down arrows for command history.\nType 'exit()' or Ctrl+D to quit.\033[94m"
    exitmsg = f"{shell_color}Goodbye.\033[94m"

    # Run the interactive session
    console.interact(banner=banner, exitmsg=exitmsg)

