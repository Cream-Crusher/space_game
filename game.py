import random
import asyncio
import constants

from star import star
from flame import Flame
from rocket import Rocket, get_rocket_frames
from itertools import cycle


def get_stars_task(count_stars):
    stars = set()

    for _ in range(count_stars):
        row = random.randint(1, constants.WINDOW_HEIGHT-2)
        column = random.randint(1, constants.WINDOW_WIDTH-2)
        symbol = random.choice('+*.:')

        star_instance = star(row, column, symbol)
        stars.add(star_instance)

        asyncio.create_task(star_instance.blink())  # вызов тасков с create_task(Чит док)

    return stars


def get_flame_task():
    flame_instance = set()
    start_row = 10
    start_column = 10
    flame_instance = Flame(start_row, start_column)

    asyncio.create_task(flame_instance.move())  # вызов тасков с create_task(Чит док)

    return flame_instance


def get_rocket():
    row_spawn = 10
    column_spawn = 30
    rocet_frames = get_rocket_frames()
    iterator_rocet_frames = cycle(rocet_frames)
    rocket_instance = Rocket(row_spawn, column_spawn, iterator_rocet_frames)

    return rocket_instance
