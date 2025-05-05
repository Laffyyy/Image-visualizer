from tkinter import Tk, Label, Canvas, PhotoImage
from tkinterdnd2 import DND_FILES, TkinterDnD
from utils.image_loader import ImageLoader
from analyzer.color_selector import ColorSelector
from analyzer.color_analyzer import ColorAnalyzer

class ImageAnalyzerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Analyzer")
        self.master.geometry("600x400")

        self.label = Label(master, text="Drag and drop an image file here")
        self.label.pack(pady=20)

        self.canvas = Canvas(master, width=500, height=300, bg="lightgray")
        self.canvas.pack(pady=10)

        # Register the canvas as a drop target
        self.master.drop_target_register(DND_FILES)
        self.master.dnd_bind('<<Drop>>', self.drop)

    def drop(self, event):
        file_path = event.data.strip('{}')  # Remove curly braces if present
        self.load_image(file_path)

    def load_image(self, image_path):
        loader = ImageLoader()
        image = loader.load(image_path)

        if image is not None:
            self.display_image(image)
            self.analyze_image(image)

    def display_image(self, image):
        # Assuming image is a PhotoImage object
        self.canvas.create_image(250, 150, image=image)

    def analyze_image(self, image):
        color_selector = ColorSelector(image)
        selected_color = color_selector.select_color()

        color_analyzer = ColorAnalyzer(image)
        similar_colors = color_analyzer.find_similar_colors(selected_color)

        print("Similar colors found:", similar_colors)

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = ImageAnalyzerApp(root)
    root.mainloop()