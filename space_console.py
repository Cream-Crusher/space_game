import os
import time
import curses
import asyncio
import random

from itertools import cycle
from curses_tools import read_controls, draw_frame, get_frame_size

TICk_TIMEOUT = 0.1


def get_rocet_frames(name_folder='rocket_frame'):
    rocet_frames = []
    file_names = os.listdir(name_folder)

    for file_name in file_names:
        path = os.path.join(name_folder, file_name)  # Если у вас не ubuntu, а другие os

        with open(path, "r") as file:
            rocet_frames.append(file.read())

    return rocet_frames


async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0.5):
    """Display animation of gun shot, direction and speed can be specified."""
    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


async def symbol_blink(canvas, row, column, symbol):  # TODO наверное нужно  убрать копипасть, кхкх.
    canvas.addstr(row, column, symbol, curses.A_DIM)
    for num in range(random.randint(0, 10), 10):

        await asyncio.sleep(0)
        for num in range(num):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)
        for num in range(num):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await asyncio.sleep(0)
        for num in range(num):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)
        for num in range(num):
            await asyncio.sleep(0)


def get_symbol_coroutines(canvas):  # TODO  Уточнить название
    symbol_coroutines = []

    for num in range(30):
        column = random.randint(1, 80)
        row = random.randint(1, 21)
        symbol = random.choice('+*.:')
        symbol_coroutines.append(symbol_blink(canvas, row, column, symbol))
    return symbol_coroutines


def draw(canvas):
    canvas.border()
    canvas.nodelay(True)
    start_row = 18
    start_column = 50
    symbol_coroutines = get_symbol_coroutines(canvas)
    fire_coroutine = fire(canvas, start_row, start_column)
    rocet_frames = get_rocet_frames()
    iterator_rocet_frames = cycle(rocet_frames)
    row, column = canvas.getmaxyx()

    while True:
        rows_direction, columns_direction, space_pressed = read_controls(canvas)
        rocet_frame = next(iterator_rocet_frames)
        row_rocet, column_rocet = get_frame_size(rocet_frame)  # В цикле т.к фрейм может быть не одинаковыми по размеру с предыдущим.

        if start_row != row:
            start_row += rows_direction
            start_column += columns_direction

        draw_frame(canvas, start_row, start_column, rocet_frame)
        fire_coroutine.send(None)

        for coroutine in symbol_coroutines:
            try:
                coroutine.send(None)
            except StopIteration:
                symbol_coroutines.remove(coroutine)

            canvas.refresh()

        draw_frame(canvas, start_row, start_column, rocet_frame, negative=True)
        time.sleep(TICk_TIMEOUT)
        if len(symbol_coroutines) == 0:
            break


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
    curses.curs_set(False)
