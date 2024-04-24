from itertools import product


def colours_generator():
    used = []

    for (r, g, b) in product([255, 0], repeat=3):
        if (r + g + b != 255 * 3) and (r + g + b != 0):
            used.append((r, g, b))
            yield r, g, b

    for (r, g, b) in product([127, 255, 0], repeat=3):
        if (r + g + b != 255 * 3) and (r + g + b != 0):
            if r == 127 or g == 127 or b == 127:
                used.append((r, g, b))
                yield r, g, b

    for (r, g, b) in product([190, 85, 255, 0], repeat=3):
        if (r + g + b != 255 * 3) and (r + g + b != 0):
            if r == 190 or g == 190 or b == 190 or r == 85 or g == 85 or b == 85:
                used.append((r, g, b))
                yield r, g, b
