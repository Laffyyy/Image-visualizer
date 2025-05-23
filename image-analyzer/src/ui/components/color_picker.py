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

        # Color wheel
        self.wheel_canvas = Canvas(self.frame, width=120, height=120)
        self.wheel_canvas.pack(side='left', padx=5)
        self._draw_color_wheel()
        self.wheel_canvas.bind('<Button-1>', self._on_wheel_click)

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

    def _draw_color_wheel(self):
        # Draw a simple color wheel (not anti-aliased, but effective)
        r = 55
        cx, cy = 60, 60
        for angle in range(360):
            rad = angle * 3.14159 / 180
            x = cx + r * 0.9 * math.cos(rad)
            y = cy + r * 0.9 * math.sin(rad)
            rgb = colorsys.hsv_to_rgb(angle/360, 1, 1)
            color = '#{:02x}{:02x}{:02x}'.format(int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
            self.wheel_canvas.create_line(cx, cy, x, y, fill=color)

    def _on_wheel_click(self, event):
        # Convert click to HSV
        cx, cy = 60, 60
        dx, dy = event.x - cx, event.y - cy
        dist = math.sqrt(dx*dx + dy*dy)
        if dist > 55:
            return
        angle = (math.degrees(math.atan2(dy, dx)) + 360) % 360
        self.hue.set(angle)
        self.sat.set(100)
        self.val.set(100)
        self._update_color_preview_from_hsv()
        self._update_sliders_from_hsv()

    def _on_slider_change(self, _=None):
        self._update_color_preview_from_hsv()

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