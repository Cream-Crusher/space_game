import asyncio
import curses
import constants

from game import get_stars_task, get_flame_task, get_rocket


class FrameDrawer:

    def __init__(self):
        self.stars = set()
        self.flame = set()
        self.rocket = set()
        self.stdscr = curses.initscr()
        self.column_console = ()
        self.row_console = ()

    async def init(self, canvas):
        curses.curs_set(False)
        curses.noecho()
        curses.resize_term(constants.WINDOW_HEIGHT, constants.WINDOW_WIDTH)

        count_stars = 50
        self.stars = get_stars_task(count_stars)
        self.flame = get_flame_task()
        self.rocket = get_rocket()

        while True:
            await self.draw_frame(canvas)
            # Читаю действия игрока
            self.read_controls(canvas)

    async def draw_frame(self, canvas):
        self.stdscr.clear()
        canvas.border()
        curses.resize_term(constants.WINDOW_HEIGHT, constants.WINDOW_WIDTH)

        for star in self.stars:
            self.draw_star(canvas, star)

        self.draw_rocket(canvas)
        self.draw_flame(canvas)
        canvas.refresh()
        await asyncio.sleep(constants.TICK_TIMEOUT)

    def draw_star(self, canvas, star):
        canvas.addstr(star.row, star.column, star.symbol, star.brightness)

    def draw_flame(self, canvas):
        flame = self.flame
        canvas.addstr(int(flame.row), flame.column, flame.symbol)

    def draw_rocket(self, canvas):
        rocket = self.rocket
        rocket_frame = next(rocket.rocet_frame)
        rocket_row = rocket.rows_direction
        rocket_column = rocket.columns_direction
        rocket.get_rocket_frame_size(rocket_frame)

        for text in rocket_frame:
            rocket_row += 1
            text = text.replace('\n', '')
            canvas.addstr(rocket_row, rocket_column, text)

    def read_controls(self, canvas):
        canvas.nodelay(True)
        self.rocket.rocket_controller(canvas)
