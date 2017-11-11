import asyncio
import secrets

import discord


async def status_rotation(ev):
    if ev.bot.cfg.pref.status_rotation:
        ev.bot.loop.create_task(status_clockwork(ev))


async def status_clockwork(ev):
    while True:
        if ev.bot.cfg.pref.status_rotation:
            statuses = [
                'Roblox'
            ]
            status = f'{secrets.choice(statuses)}'
            game = discord.Game(name=status)
            await ev.bot.change_presence(game=game)
        await asyncio.sleep(180)