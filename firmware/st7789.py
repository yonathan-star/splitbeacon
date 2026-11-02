"""Minimal original ST7789 SPI driver for Adafruit 4383, landscape 240x135.
Offsets follow the manufacturer's module geometry. No external packages needed.
"""
import framebuf
from time import sleep_ms

class Display:
    def __init__(self, spi, cs, dc, reset):
        self.spi, self.cs, self.dc = spi, cs, dc
        cs(1); dc(0); reset(1); sleep_ms(10); reset(0); sleep_ms(20); reset(1); sleep_ms(120)
        self.command(0x01); sleep_ms(150)
        self.command(0x11); sleep_ms(120)
        self.command(0x3A, b'\x55')  # RGB565
        self.command(0x36, b'\x60')  # MX + MV; RGB, landscape
        self.command(0x21)  # IPS panel inversion
        self.command(0x13); self.command(0x29); sleep_ms(20)
        self.buffer = bytearray(240 * 135 * 2)
        self.fb = framebuf.FrameBuffer(self.buffer, 240, 135, framebuf.RGB565)
    def command(self, cmd, data=None):
        self.cs(0); self.dc(0); self.spi.write(bytes([cmd]))
        if data: self.dc(1); self.spi.write(data)
        self.cs(1)
    @staticmethod
    def color(r, g, b):
        # framebuf is little-endian, controller wants big-endian bytes.
        c = ((r & 248) << 8) | ((g & 252) << 3) | (b >> 3)
        return ((c & 255) << 8) | (c >> 8)
    def show(self):
        self.command(0x2A, bytes([0, 40, 1, 23]))  # 40 .. 279
        self.command(0x2B, bytes([0, 53, 0, 187]))  # 53 .. 187
        self.command(0x2C)
        self.cs(0); self.dc(1); self.spi.write(self.buffer); self.cs(1)
    def text(self, text, x, y, color, scale=1):
        if scale == 1:
            self.fb.text(text, x, y, color)
        else:
            mask = bytearray(len(text) * 8)
            glyph = framebuf.FrameBuffer(mask, len(text)*8, 8, framebuf.MONO_VLSB)
            glyph.text(text, 0, 0, 1)
            for yy in range(8):
                for xx in range(len(text)*8):
                    if glyph.pixel(xx, yy): self.fb.fill_rect(x+xx*scale, y+yy*scale, scale, scale, color)
