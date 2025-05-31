import colorsys
from tkinter import Frame, Button, Canvas, Scale, HORIZONTAL, DoubleVar, Label
import math

class ColorPickerUI:
    def __init__(self, parent):
        self.frame = Frame(parent)
        self.frame.pack(pady=5)

        # Color preview
        self.color_frame = Frame(self.frame, width=40, height=40)
        self.color_frame.pack(side='left', padx=5)
        self.color_frame.pack_propagate(False)

        # HSV values
        self.hue = DoubleVar(value=0)
        self.sat = DoubleVar(value=1)
        self.val = DoubleVar(value=1)

        # Canvas for hue ring and SV square
        self.ring_size = 180
        self.sv_size = 100
        self.ring_canvas = Canvas(self.frame, width=self.ring_size, height=self.ring_size)
        self.ring_canvas.pack(side='left', padx=5)
        self._draw_hue_ring()

        # SV square as PhotoImage, overlayed in the center
        self.sv_img = None
        self.sv_img_id = None
        self._draw_sv_square_image()
        # Bind events for both ring and SV square
        self.ring_canvas.bind('<Button-1>', self._on_ring_click)
        self.ring_canvas.bind('<B1-Motion>', self._on_ring_click)
        self.ring_canvas.tag_bind('sv', '<Button-1>', self._on_sv_click)
        self.ring_canvas.tag_bind('sv', '<B1-Motion>', self._on_sv_click)

        # Sliders
        slider_frame = Frame(self.frame)
        slider_frame.pack(side='left', padx=5)
        self.hue_slider = Scale(slider_frame, from_=0, to=359, orient=HORIZONTAL, label='Hue', variable=self.hue, command=self._on_slider_change)
        self.sat_slider = Scale(slider_frame, from_=0, to=100, orient=HORIZONTAL, label='Saturation', variable=self.sat, command=self._on_slider_change)
        self.val_slider = Scale(slider_frame, from_=0, to=100, orient=HORIZONTAL, label='Value', variable=self.val, command=self._on_slider_change)
        self.hue_slider.pack(fill='x')
        self.sat_slider.pack(fill='x')
        self.val_slider.pack(fill='x')

        # Color pick button
        self.pick_color_button = Button(self.frame, text="Pick Color")
        self.pick_color_button.pack(side='left', padx=5)
        self.pick_color_button.config(state='disabled')

        self._update_color_preview_from_hsv()

    def _draw_hue_ring(self):
        # Draw a hue ring (color wheel) on the ring_canvas
        cx, cy = self.ring_size // 2, self.ring_size // 2
        outer_r = self.ring_size // 2 - 2
        inner_r = outer_r - 18
        for angle in range(360):
            rad = math.radians(angle)
            x1 = cx + outer_r * math.cos(rad)
            y1 = cy + outer_r * math.sin(rad)
            x2 = cx + inner_r * math.cos(rad)
            y2 = cy + inner_r * math.sin(rad)
            rgb = colorsys.hsv_to_rgb(angle/360, 1, 1)
            color = '#{:02x}{:02x}{:02x}'.format(int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
            self.ring_canvas.create_line(x1, y1, x2, y2, fill=color, width=3)

    def _draw_sv_square_image(self):
        # Draw the SV square as a PhotoImage and overlay it in the center of the ring_canvas
        from tkinter import PhotoImage
        hue = self.hue.get() / 360
        size = self.sv_size
        img = PhotoImage(width=size, height=size)
        for i in range(size):
            row = ""
            for j in range(size):
                s = i / (size - 1)
                v = 1 - (j / (size - 1))
                r, g, b = colorsys.hsv_to_rgb(hue, s, v)
                row += '#{:02x}{:02x}{:02x} '.format(int(r*255), int(g*255), int(b*255))
            img.put(row, to=(i, 0, i+1, size))
        self.sv_img = img
        # Remove previous SV image and selector
        self.ring_canvas.delete('sv')
        self.ring_canvas.delete('selector')
        # Center the SV square
        cx, cy = self.ring_size // 2, self.ring_size // 2
        x0 = cx - size // 2
        y0 = cy - size // 2
        self.sv_img_id = self.ring_canvas.create_image(x0, y0, anchor='nw', image=self.sv_img, tags='sv')
        self._draw_sv_selector()

    def _draw_sv_selector(self):
        # Draw selector circle only
        size = self.sv_size
        cx, cy = self.ring_size // 2, self.ring_size // 2
        x0 = cx - size // 2
        y0 = cy - size // 2
        x = x0 + self.sat.get() / 100 * (size - 1)
        y = y0 + (1 - self.val.get() / 100) * (size - 1)
        self.ring_canvas.delete('selector')
        self.ring_canvas.create_oval(x-4, y-4, x+4, y+4, outline='black', width=2, tags='selector')

    def _on_sv_click(self, event):
        # Update S and V based on click position in the SV square
        size = self.sv_size
        cx, cy = self.ring_size // 2, self.ring_size // 2
        x0 = cx - size // 2
        y0 = cy - size // 2
        x = min(max(event.x - x0, 0), size-1)
        y = min(max(event.y - y0, 0), size-1)
        s = x / (size - 1)
        v = 1 - (y / (size - 1))
        self.sat.set(s * 100)
        self.val.set(v * 100)
        self._update_color_preview_from_hsv()
        self._update_sliders_from_hsv()
        self._draw_sv_selector()

    def _on_ring_click(self, event):
        # Detect if click is in the ring, and update hue if so
        cx, cy = self.ring_size // 2, self.ring_size // 2
        dx, dy = event.x - cx, event.y - cy
        dist = math.sqrt(dx*dx + dy*dy)
        outer_r = self.ring_size // 2 - 2
        inner_r = outer_r - 18
        if inner_r < dist < outer_r:
            angle = (math.degrees(math.atan2(dy, dx)) + 360) % 360
            self.hue.set(angle)
            self._update_color_preview_from_hsv()
            self._draw_sv_square_image()
        else:
            # If click is inside SV square, delegate to SV handler
            size = self.sv_size
            x0 = cx - size // 2
            y0 = cy - size // 2
            if x0 <= event.x < x0 + size and y0 <= event.y < y0 + size:
                self._on_sv_click(event)

    def _on_slider_change(self, _=None):
        self._update_color_preview_from_hsv()
        self._draw_sv_square_image()

    def _update_color_preview_from_hsv(self):
        h = self.hue.get() / 360
        s = self.sat.get() / 100
        v = self.val.get() / 100
        rgb = colorsys.hsv_to_rgb(h, s, v)
        color = (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
        self.update_color_preview(color)

    def _update_sliders_from_hsv(self):
        # Called after wheel click to update sliders
        self.hue_slider.set(self.hue.get())
        self.sat_slider.set(self.sat.get())
        self.val_slider.set(self.val.get())

    def update_color_preview(self, color):
        if color:
            hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
            self.color_frame.config(bg=hex_color)

    def enable_button(self):
        self.pick_color_button.config(state='normal')

    def disable_button(self):
        self.pick_color_button.config(state='disabled')

    def set_button_command(self, command):
        self.pick_color_button.config(command=command)

    def set_hsv_from_rgb(self, color):
        # color is (r, g, b)
        r, g, b = [c / 255 for c in color]
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        self.hue.set(h * 360)
        self.sat.set(s * 100)
        self.val.set(v * 100)
        self._update_sliders_from_hsv()
        self._update_color_preview_from_hsv() 