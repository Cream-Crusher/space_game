import time
import curses
import asyncio


async def blink(canvas, row, column, symbol='*'):
    canvas.addstr(row, column, symbol, curses.A_DIM)
    await asyncio.sleep(0)

    canvas.addstr(row, column, symbol)
    await asyncio.sleep(0)

    canvas.addstr(row, column, symbol, curses.A_BOLD)
    await asyncio.sleep(0)

    canvas.addstr(row, column, symbol)
    await asyncio.sleep(0)


def get_coroutines(canvas, row, column):
    coroutines = []

    for num in range(5):
        column += 1
        coroutines.append(blink(canvas, row, column))
    return coroutines


def draw(canvas):
    canvas.border()
    row, column = (5, 20)

    coroutines = get_coroutines(canvas, row, column)

    while True:

        for coroutine in coroutines:
            try:
                coroutine.send(None)
                canvas.refresh()
            except StopIteration:
                coroutines.remove(coroutine)
        time.sleep(1)
        if len(coroutines) == 0:
            break


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
    curses.curs_set(False)
