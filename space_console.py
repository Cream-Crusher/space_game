import os
import time
import curses
import random
import asyncio

from itertools import cycle
from curses_tools import read_controls, draw_frame, get_frame_size

TICk_TIMEOUT = 0.1


def get_rocet_frames(name_folder='rocket_frame'):
    rocet_frames = []
    file_names = os.listdir(name_folder)

    for file_name in file_names:
        path = os.path.join(name_folder, file_name)

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


async def asyncio_sleep_for_canvas(num):
    await asyncio.sleep(0)
    for num in range(num):
        await asyncio.sleep(0)


async def symbol_blink(canvas, row, column, symbol, offset_tics):
    canvas.addstr(row, column, symbol, curses.A_DIM)

    for num in range(offset_tics):

        canvas.addstr(row, column, symbol, curses.A_DIM)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)


def get_symbol_coroutines(canvas):
    symbol_coroutines = []

    for num in range(30):
        column = random.randint(1, 80)
        row = random.randint(1, 21)
        symbol = random.choice('+*.:')
        offset_tics = random.randint(0, 20)
        symbol_coroutines.append(symbol_blink(canvas, row, column, symbol, offset_tics))

    return symbol_coroutines


def get_rocket_spawn_coordinates(
        spawn_row, spawn_column,
        rows_direction, columns_direction,
        row_rocet, column_rocet,
        row_console, column_console):

    spawn_row += rows_direction
    if row_console <= spawn_row+row_rocet or row_rocet >= spawn_row+row_rocet:
        spawn_row -= rows_direction

    spawn_column += columns_direction
    if column_console <= spawn_column+column_rocet or column_rocet >= spawn_column+column_rocet:
        spawn_column -= columns_direction

    return spawn_row, spawn_column


def draw(canvas):
    canvas.border()
    canvas.nodelay(True)
    spawn_row = 18
    spawn_column = 40
    symbol_coroutines = get_symbol_coroutines(canvas)
    fire_coroutine = fire(canvas, spawn_row, spawn_column)
    rocet_frames = get_rocet_frames()
    iterator_rocet_frames = cycle(rocet_frames)
    row_console, column_console = canvas.getmaxyx()

    while True:
        rows_direction, columns_direction, space_pressed = read_controls(canvas)
        rocet_frame = next(iterator_rocet_frames)
        row_rocet, column_rocet = get_frame_size(rocet_frame)  # В цикле т.к фрейм может быть не одинаковыми по размеру с предыдущим.

        spawn_row, spawn_column = get_rocket_spawn_coordinates(
            spawn_row, spawn_column,
            rows_direction, columns_direction,
            row_rocet, column_rocet,
            row_console, column_console
            )

        draw_frame(canvas, spawn_row, spawn_column, rocet_frame)
        fire_coroutine.send(None)

        for coroutine in symbol_coroutines:
            try:
                coroutine.send(None)
            except StopIteration:
                symbol_coroutines.remove(coroutine)

            canvas.refresh()

        draw_frame(canvas, spawn_row, spawn_column, rocet_frame, negative=True)
        time.sleep(TICk_TIMEOUT)

        if len(symbol_coroutines) == 0:
            break


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
    curses.curs_set(False)
