from tkinter import Frame, Button

class ColorPickerUI:
    def __init__(self, parent):
        self.frame = Frame(parent)
        self.frame.pack(pady=5)
        
        # Add text box with color preview
        self.color_frame = Frame(self.frame, width=100, height=30)
        self.color_frame.pack(side='left', padx=5)
        self.color_frame.pack_propagate(False)  # Maintain fixed size
        
        # Add color pick button
        self.pick_color_button = Button(self.frame, text="Pick Color")
        self.pick_color_button.pack(side='left', padx=5)
        self.pick_color_button.config(state='disabled')

    def update_color_preview(self, color):
        if color:
            # Convert RGB to hex color
            hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
            self.color_frame.config(bg=hex_color)

    def enable_button(self):
        self.pick_color_button.config(state='normal')

    def disable_button(self):
        self.pick_color_button.config(state='disabled')

    def set_button_command(self, command):
        self.pick_color_button.config(command=command) 