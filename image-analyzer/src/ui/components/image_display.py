from tkinter import Canvas
from PIL import Image, ImageTk

class ImageDisplay:
    def __init__(self, parent):
        self.canvas = Canvas(parent, width=500, height=300, bg="lightgray")
        self.canvas.pack(pady=10)
        self.current_image = None
        self.displayed_image = None
        self.is_color_picking_enabled = False
        self.color_preview_callback = None

    def set_color_preview_callback(self, callback):
        self.color_preview_callback = callback

    def display_image(self, image):
        self.current_image = image
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        img_width, img_height = image.size
        width_ratio = canvas_width / img_width
        height_ratio = canvas_height / img_height
        scale_factor = min(width_ratio, height_ratio)
        
        new_width = int(img_width * scale_factor)
        new_height = int(img_height * scale_factor)
        
        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        photo_image = ImageTk.PhotoImage(resized_image)
        
        self.canvas.delete("all")
        self.canvas.create_image(canvas_width//2, canvas_height//2, image=photo_image)
        self.canvas.image = photo_image

    def get_color_at_position(self, x, y):
        if not self.current_image:
            return None

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        img_width, img_height = self.current_image.size
        
        width_ratio = canvas_width / img_width
        height_ratio = canvas_height / img_height
        scale_factor = min(width_ratio, height_ratio)
        
        scaled_width = int(img_width * scale_factor)
        scaled_height = int(img_height * scale_factor)
        
        x_offset = (canvas_width - scaled_width) // 2
        y_offset = (canvas_height - scaled_height) // 2
        
        img_x = int((x - x_offset) / scale_factor)
        img_y = int((y - y_offset) / scale_factor)
        
        if 0 <= img_x < img_width and 0 <= img_y < img_height:
            return self.current_image.getpixel((img_x, img_y))
        return None

    def on_mouse_move(self, event):
        if self.is_color_picking_enabled and self.color_preview_callback:
            color = self.get_color_at_position(event.x, event.y)
            if color:
                self.color_preview_callback(color)

    def enable_color_picking(self):
        self.is_color_picking_enabled = True
        self.canvas.config(cursor="crosshair")

    def disable_color_picking(self):
        self.is_color_picking_enabled = False
        self.canvas.config(cursor="")

    def bind_events(self, click_handler, motion_handler):
        self.canvas.bind('<Button-1>', click_handler)
        self.canvas.bind('<Motion>', motion_handler) 