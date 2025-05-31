class DragAndDrop:
    def __init__(self, ui_component):
        self.ui_component = ui_component
        self.setup_drag_and_drop()

    def setup_drag_and_drop(self):
        self.ui_component.bind("<DragEnter>", self.on_drag_enter)
        self.ui_component.bind("<Drop>", self.on_drop)

    def on_drag_enter(self, event):
        event.widget.focus_force()
        return event.action

    def on_drop(self, event):
        file_path = event.data
        if self.is_image_file(file_path):
            self.load_image(file_path)
        else:
            print("The dropped file is not an image.")

    def is_image_file(self, file_path):
        valid_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
        return any(file_path.lower().endswith(ext) for ext in valid_extensions)

    def load_image(self, file_path):
        # Logic to load the image and update the UI
        print(f"Image loaded: {file_path}")
        # Here you would typically call a method to update the UI with the loaded image.