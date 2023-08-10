import asyncio


class Flame:

    def __init__(self, row=10, column=10, speed=-0.3, symbol='*'):
        self.row = row
        self.column = column
        self.speed = speed
        self.symbol = symbol

    async def spawn(self):
        self.symbol = '*'
        await asyncio.sleep(0.2)

        self.symbol = 'O'
        await asyncio.sleep(0.2)

        self.symbol = ' '
        await asyncio.sleep(0.1)

    async def move(self):
        await self.spawn()

        self.symbol = '|'
        while self.row >= 2:  # TODO  логика если упёрся в стенку|Выстерл летит только прямо
            self.row += self.speed
            await asyncio.sleep(0.1)

        self.symbol = ' '
