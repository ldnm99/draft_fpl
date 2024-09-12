from fpl import FPL
import aiohttp
import asyncio

async def main():
    session = aiohttp.ClientSession()
    fpl = FPL(session)
    player = await fpl.get_player(10)
    print(player)
    await session.close()

asyncio.run(main())