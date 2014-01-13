import colorsys
import math

GRADIENT_SPEC = [
    (1.0, 1.0, 1.0),  # white
    (1.0, 0.0, 0.0),  # red
    (0.0, 1.0, 0.0),  # green
    (0.0, 0.0, 1.0),  # blue
    (0.0, 0.0, 0.0)]  # black

def gradient(d, spec=GRADIENT_SPEC):
    N = len(spec)
    idx = int(d * (N - 1))
    t = math.fmod(d * (N - 1), 1.0)
    col1 = colorsys.rgb_to_hsv(*spec[min(N - 1, idx)])
    col2 = colorsys.rgb_to_hsv(*spec[min(N - 1, idx + 1)])
    hsv = tuple(a * (1 - t) + b * t for a, b in zip(col1, col2))
    r, g, b = colorsys.hsv_to_rgb(*hsv)
    return '#%02X%02X%02X' % (r * 255, g * 255, b * 255)

