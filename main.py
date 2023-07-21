import time
import curses
import asyncio
import random

TIC_TIMEOUT = 0.1


async def blink(canvas, row, column, symbol):  # TODO наверное нужно  убрать копипасть, кхкх.
    canvas.addstr(row, column, symbol, curses.A_DIM)
    for num in range(random.randint(0, 2), 2):
        asyncio.sleep(0)
        await asyncio.sleep(0)
        for num in range(20):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)
        for num in range(3):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await asyncio.sleep(0)
        for num in range(5):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)
        for num in range(3):
            await asyncio.sleep(0)


def get_coroutines(canvas):
    coroutines = []

    for num in range(60):
        column = random.randint(1, 85)
        row = random.randint(1, 21)
        symbol = random.choice('+*.:')
        coroutines.append(blink(canvas, row, column, symbol))
    return coroutines


def draw(canvas):
    canvas.border()
    coroutines = get_coroutines(canvas)

    while True:

        for coroutine in coroutines:
            try:
                coroutine.send(None)
                canvas.refresh()
            except StopIteration:
                coroutines.remove(coroutine)
        time.sleep(TIC_TIMEOUT)
        if len(coroutines) == 0:
            break


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
    curses.window.getmaxyx(50, 50)
    curses.curs_set(False)
