import os
import sys
from pathlib import Path

# Add the src directory to Python path
src_dir = Path(__file__).parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

import ttkbootstrap as ttk
from gui import SymphonyLangGUI

if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    gui = SymphonyLangGUI(root)
    root.mainloop()