import os
from utils.image_loader import ImageLoader
from analyzer.color_selector import ColorSelector
from analyzer.color_analyzer import ColorAnalyzer
from ui.app import App

def main():
    app = App()
    app.run()

if __name__ == "__main__":
    main()