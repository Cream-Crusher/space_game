import time
import curses
import asyncio


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)


# def show_addstr(row, column, canvas, time_sleep, *a_dim):
#     canvas.addstr(row, column, '*', *a_dim)
#     canvas.refresh()
#     time.sleep(time_sleep)


def draw(canvas):
    row, column = (5, 20)
    canvas.border()
    coroutine = blink(canvas, row, column)
    coroutine.send(None)
    canvas.refresh()
    time.sleep(1)

    # while True:
    #     show_addstr(row, column, canvas, 2, curses.A_DIM)
    #     show_addstr(row, column, canvas, 0.3)
    #     show_addstr(row, column, canvas, 0.5, curses.A_BOLD)
    #     show_addstr(row, column, canvas, 0.3)



if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
    curses.curs_set(False)
