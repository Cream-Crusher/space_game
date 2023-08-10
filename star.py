import asyncio
import curses
import random


class star:

    def __init__(self, row, column, symbol):
        self.row = int(row)
        self.column = column
        self.symbol = symbol
        self.brightness = curses.A_DIM

    async def blink(self):
        # Реализовал разницу появления через Не Целые числа(от 0 до 2)
        offset_tics = random.random() * 2

        await asyncio.sleep(offset_tics)

        while True:
            self.brightness = curses.A_DIM
            await asyncio.sleep(2)

            self.brightness = False
            await asyncio.sleep(0.3)

            self.brightness = curses.A_BOLD
            await asyncio.sleep(0.5)

            self.brightness = False
            await asyncio.sleep(0.3)
