import os
import sys

# Add the src directory to the Python module search path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.image_loader import ImageLoader
from analyzer.color_selector import ColorSelector
from analyzer.color_analyzer import ColorAnalyzer
from ui.app import ImageAnalyzerApp

def main():
    from tkinterdnd2 import TkinterDnD
    root = TkinterDnD.Tk()
    app = ImageAnalyzerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()