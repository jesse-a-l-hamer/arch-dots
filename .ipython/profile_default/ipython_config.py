# Configuration file for ipython.
from copy import deepcopy
from IPython.utils.PyColorize import linux_theme, theme_table

theme = deepcopy(linux_theme)

# Choose catppuccin theme
# catppuccin_theme = "catppuccin-mocha"
catppuccin_theme = "catppuccin-macchiato"
# catppuccin_theme = "catppuccin-frappe"
# catppuccin_theme = "catppuccin-latte"

theme.base = catppuccin_theme
theme_table[catppuccin_theme] = theme

c = get_config()

c.AliasManager.user_aliases = [
    ("la", "eza -la")
]
c.PlainTextFormatter.max_width = 88

c.InteractiveShellApp.log_level = 20
c.InteractiveShellApp.exec_lines = [
    "from pathlib import Path",
    "import numpy as np",
    "import pandas as pd",
    "import matplotlib.pyplot as plt",
    "%matplotlib inline"
]

c.TerminalIPythonApp.display_banner = True

c.TerminalInteractiveShell.true_color = True
c.TerminalInteractiveShell.colors = catppuccin_theme
c.TerminalInteractiveShell.auto_match = True
c.TerminalInteractiveShell.autoformatter = "black"

