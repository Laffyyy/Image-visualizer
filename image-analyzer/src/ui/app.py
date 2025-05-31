from tkinter import Tk, Label
from tkinterdnd2 import DND_FILES, TkinterDnD
from utils.image_loader import ImageLoader
from analyzer.color_analyzer import ColorAnalyzer
from ui.components.color_picker import ColorPickerUI
from ui.components.image_display import ImageDisplay

class ImageAnalyzerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Analyzer")
        self.master.geometry("600x400")

        self.setup_ui()
        self.setup_drag_and_drop()
        self.setup_event_handlers()

    def setup_ui(self):
        self.label = Label(self.master, text="Drag and drop an image file here")
        self.label.pack(pady=10)
        
        self.color_picker = ColorPickerUI(self.master)
        self.image_display = ImageDisplay(self.master)
        self.image_display.set_color_preview_callback(self.color_picker.update_color_preview)

    def setup_drag_and_drop(self):
        self.master.drop_target_register(DND_FILES)
        self.master.dnd_bind('<<Drop>>', self.drop)

    def setup_event_handlers(self):
        self.color_picker.set_button_command(self.enable_color_picking)
        self.image_display.bind_events(self.on_canvas_click, self.image_display.on_mouse_move)

    def enable_color_picking(self):
        if self.image_display.current_image:
            self.image_display.enable_color_picking()

    def on_canvas_click(self, event):
        if not (self.image_display.is_color_picking_enabled and self.image_display.current_image):
            return

        color = self.image_display.get_color_at_position(event.x, event.y)
        if color:
            self.color_picker.update_color_preview(color)
            if hasattr(self.color_picker, 'set_hsv_from_rgb'):
                self.color_picker.set_hsv_from_rgb(color)
            color_analyzer = ColorAnalyzer(self.image_display.current_image)
            similar_colors = color_analyzer.find_similar_colors(color)
            print("Similar colors found:", similar_colors)
            self.image_display.disable_color_picking()

    def drop(self, event):
        file_path = event.data.strip('{}')
        self.load_image(file_path)

    def load_image(self, image_path):
        loader = ImageLoader()
        image = loader.load(image_path)

        if image is not None:
            self.image_display.display_image(image)
            self.color_picker.enable_button()

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = ImageAnalyzerApp(root)
    root.mainloop()