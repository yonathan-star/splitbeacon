"""MicroPython entry point. Pico RP2040; see docs/WIRING.md."""
from machine import Pin, ADC, PWM, SPI
import neopixel, time, json, os
from core import Session, Debounce, matrix_frame, brightness_from_adc, target_from_adc, stamp, restore_laps
from st7789 import Display

buttons = [Pin(n, Pin.IN, Pin.PULL_UP) for n in (5, 6, 7)]
edges = [Debounce() for _ in buttons]
bright, ambient, target = [ADC(n) for n in (26, 27, 28)]
pixels = neopixel.NeoPixel(Pin(15, Pin.OUT, value=0), 32)
pixels2 = neopixel.NeoPixel(Pin(14, Pin.OUT, value=0), 32)
pixels.fill((0, 0, 0)); pixels.write()
pixels2.fill((0, 0, 0)); pixels2.write()
backlight = PWM(Pin(11)); backlight.freq(20000); backlight.duty_u16(0)
buzzer = PWM(Pin(8)); buzzer.duty_u16(0)
spi = SPI(0, baudrate=20000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
lcd = Display(spi, Pin(17, Pin.OUT), Pin(12, Pin.OUT), Pin(13, Pin.OUT))
s = Session()
try:
    with open('session.json') as f: s.laps = restore_laps(json.load(f).get('laps', []))
except (OSError, ValueError, AttributeError): pass

WHITE = lcd.color(235, 245, 255)
CYAN = lcd.color(30, 220, 240)
ORANGE = lcd.color(255, 125, 35)
GRAY = lcd.color(115, 130, 150)

def save():
    # Atomic rename keeps the old file if power is lost during writing.
    try:
        with open('session.tmp', 'w') as f: json.dump({'version':1, 'laps':s.laps}, f)
        os.rename('session.tmp', 'session.json')
        return True
    except OSError: return False

def screen():
    lcd.fb.fill(lcd.color(8, 17, 30))
    lcd.text('SPLITBEACON', 8, 8, CYAN)
    lcd.text('RUN' if s.running else 'PAUSE', 184, 8, WHITE)
    lcd.fb.hline(8, 22, 224, GRAY)
    if s.page == 0:
        lcd.text(stamp(s.current_ms), 8, 36, WHITE, 3)
        lcd.text('TARGET %3ds  NEXT %3ds' % (s.lap_target_ms//1000, s.target_ms//1000), 8, 72, CYAN)
        lcd.text('TOTAL '+stamp(s.elapsed_ms), 8, 91, GRAY)
        lcd.text('LAPS %02d  LAP TO RECORD' % len(s.laps), 8, 113, WHITE)
    elif s.page == 1:
        lcd.text('RECENT SPLITS', 8, 32, CYAN)
        for i, (duration, goal) in enumerate(s.laps[-4:]):
            lcd.text('%02d %s %+5.1fs' % (max(1,len(s.laps)-3)+i, stamp(duration), (duration-goal)/1000), 8, 52+i*17, ORANGE if duration>goal else WHITE)
        if not s.laps: lcd.text('RECORD YOUR FIRST LAP', 8, 62, WHITE)
    else:
        lcd.text('SESSION SUMMARY', 8, 33, CYAN)
        if s.laps:
            times = [r[0] for r in s.laps]
            lcd.text('BEST '+stamp(min(times)), 8, 55, WHITE)
            lcd.text('AVG  '+stamp(sum(times)//len(times)), 8, 76, WHITE)
        else: lcd.text('NO COMPLETED LAPS', 8, 55, WHITE)
        lcd.text('HOLD VIEW 2s TO RESET', 8, 111, ORANGE)
    lcd.show()

last_tick = time.ticks_ms(); now = 0; next_frame = 0; beep_until = 0
view_down = None; reset_fired = False; save_error = False
try:
    while True:
        tick = time.ticks_ms()
        now += max(0, time.ticks_diff(tick, last_tick)); last_tick = tick
        s.tick(now)
        s.target_ms = target_from_adc(target.read_u16()) * 1000
        pressed = [not b.value() for b in buttons]
        events = [e.update(v, now) for e,v in zip(edges,pressed)]
        if events[0]:
            running = s.toggle(now)
            if not running: save_error = not save()
        if events[1] and s.lap(now):
            buzzer.freq(1700); buzzer.duty_u16(7000); beep_until = now+50
        if events[2]: view_down, reset_fired = now, False
        if edges[2].stable and view_down is not None and now-view_down >= 2000 and not reset_fired:
            s.reset(now); save_error = not save(); reset_fired = True
        if not edges[2].stable and view_down is not None:
            if not reset_fired: s.next_page()
            view_down = None
        if s.cue_due():
            buzzer.freq(2400); buzzer.duty_u16(7000); beep_until = now+180
        if now >= beep_until: buzzer.duty_u16(0)
        if now >= next_frame:
            amount = brightness_from_adc(bright.read_u16(), ambient.read_u16())
            backlight.duty_u16(int(65535 * max(.08, amount)))
            for i, rgb in enumerate(matrix_frame(s, amount)):
                if i < 32: pixels[i] = rgb
                else: pixels2[i-32] = rgb
            pixels.write(); pixels2.write(); screen()
            if save_error:
                lcd.text('SAVE FAILED', 136, 125, ORANGE); lcd.show()
            next_frame = now+50
        time.sleep_ms(5)
finally:
    buzzer.duty_u16(0); backlight.duty_u16(0)
    pixels.fill((0,0,0)); pixels.write()
    pixels2.fill((0,0,0)); pixels2.write()
