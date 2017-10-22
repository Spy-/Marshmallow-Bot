import asyncio
import discord
import secrets

statuses = [
    '?help'
]


async def status_rotation(ev):
    if ev.bot.cfg.pref.status_rotation:
        ev.bot.loop.create_task(status_clockwork(ev))


async def status_clockwork(ev):
    while True:
        if ev.bot.cfg.pref.status_rotation:
            status = f'with {secrets.choice(statuses)}'
            game = discord.Game(name=status)
            try:
                await ev.bot.change_presence(game=game)
            except Exception:
                pass
        await asyncio.sleep(180)
