"""SplitBeacon timing and display logic; portable to MicroPython and CPython."""
MAX_LAPS = 64
MAX_CHANNEL = 16  # Hardware build limit; never send raw 255-channel values.

def clamp(value, low, high):
    return max(low, min(high, value))

def target_from_adc(raw):
    return 5 + round(clamp(raw, 0, 65535) * 595 / 65535)

def brightness_from_adc(knob, ambient):
    # Both controls have a floor so a dark room never makes controls invisible.
    manual = 0.15 + clamp(knob, 0, 65535) / 65535 * 0.85
    room = 0.25 + clamp(ambient, 0, 65535) / 65535 * 0.75
    return manual * room

def stamp(ms):
    ms = max(0, int(ms))
    return '%02d:%02d.%02d' % (ms // 60000, (ms // 1000) % 60, (ms % 1000) // 10)

class Debounce:
    def __init__(self, initial=False, delay=30):
        self.raw = self.stable = initial
        self.changed = 0
        self.delay = delay
    def update(self, pressed, now):
        if pressed != self.raw:
            self.raw, self.changed = pressed, now
        if self.stable != self.raw and now - self.changed >= self.delay:
            self.stable = self.raw
            return self.stable  # True only on a stable press edge.
        return False

class Session:
    def __init__(self, target_s=30):
        self.target_ms = int(target_s * 1000)
        self.running = False
        self.elapsed_ms = 0
        self.last_now = None
        self.lap_start_ms = 0
        self.laps = []  # (duration_ms, target_ms_at_lap_start)
        self.lap_target_ms = self.target_ms
        self.page = 0
        self.alerted = False
    def tick(self, now):
        if self.last_now is not None and self.running:
            self.elapsed_ms += max(0, now - self.last_now)
        self.last_now = now
    def toggle(self, now):
        self.tick(now)
        self.running = not self.running
        if self.elapsed_ms == 0:
            self.lap_target_ms = self.target_ms
        return self.running
    def lap(self, now):
        self.tick(now)
        if not self.running or self.current_ms < 250:
            return False
        self.laps.append((self.current_ms, self.lap_target_ms))
        self.laps = self.laps[-MAX_LAPS:]
        self.lap_start_ms = self.elapsed_ms
        self.lap_target_ms = self.target_ms
        self.alerted = False
        return True
    def reset(self, now):
        target, page = self.target_ms, self.page
        self.__init__(target / 1000)
        self.page, self.last_now = page, now
    @property
    def current_ms(self):
        return self.elapsed_ms - self.lap_start_ms
    @property
    def delta_ms(self):
        return self.current_ms - self.lap_target_ms
    def cue_due(self):
        if self.running and not self.alerted and self.current_ms >= self.lap_target_ms:
            self.alerted = True
            return True
        return False
    def next_page(self):
        self.page = (self.page + 1) % 3

def matrix_index(x, y):
    # Two 8x4 Wings placed side by side, both with the same orientation.
    panel, local = x // 8, x % 8
    return panel * 32 + y * 8 + (local if y % 2 == 0 else 7 - local)

def matrix_frame(session, brightness=1):
    colors = [(0, 0, 0)] * 64
    level = round(MAX_CHANNEL * clamp(brightness, 0, 1))
    def put(x, y, rgb):
        colors[matrix_index(x, y)] = tuple(round(c * level) for c in rgb)
    if session.page == 1:  # History: each column a completed lap; height gives error.
        for x, (duration, target) in enumerate(session.laps[-16:]):
            error = (duration - target) / target
            height = clamp(1 + round(abs(error) * 10), 1, 4)
            rgb = (1, .25, 0) if error > .03 else (0, .8, 1) if error < -.03 else (0, 1, .2)
            for y in range(4 - height, 4): put(x, y, rgb)
    else:
        progress = session.current_ms / session.lap_target_ms
        lit = clamp(int(progress * 64), 0, 64)
        rgb = (1, .15, 0) if progress >= 1 else (0, .8, 1)
        for n in range(lit): put(n % 16, n // 16, rgb)
        if lit < 64: put(lit % 16, lit // 16, (.6, .6, .6))
    return colors

def restore_laps(records):
    """Validate persisted history before exposing it to rendering/division."""
    valid = []
    if not isinstance(records, list): return valid
    for r in records[-MAX_LAPS:]:
        if isinstance(r, (list, tuple)) and len(r) == 2:
            a, b = r
            if isinstance(a, int) and isinstance(b, int) and 250 <= a <= 86400000 and 5000 <= b <= 600000:
                valid.append((a, b))
    return valid
