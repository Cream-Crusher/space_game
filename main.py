import time
import curses
import asyncio

TIC_TIMEOUT = 0.1


async def blink(canvas, row, column, symbol='*'):  # TODO наверное нужно  убрать копипасть, кхкх.
    canvas.addstr(row, column, symbol, curses.A_DIM)
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
        time.sleep(TIC_TIMEOUT)
        if len(coroutines) == 0:
            break


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
    curses.curs_set(False)
