import asyncio
import curses

from frame_drawer import FrameDrawer


async def main():
    curses.update_lines_cols()
    drawer = FrameDrawer()
    await curses.wrapper(drawer.init)

if __name__ == '__main__':
    asyncio.run(main())
