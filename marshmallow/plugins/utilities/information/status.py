import sys
import arrow
import socket
import psutil
import discord
import humanfriendly


def get_os_icon():
    if sys.platform == 'win32':
        icon = 'https://i.imgur.com/wTMT4yG.png'
        color = 0x11b7ee
    elif sys.platform == 'linux':
        icon = 'https://i.imgur.com/pKxZYK7.png'
        color = 0xefba20
    else:
        icon = 'https://i.imgur.com/QxlJJgA.png'
        color = 0x696969
    return icon, color


async def status(cmd, message, args):
    os_icon, os_color = get_os_icon()
    general_text = f'Latency: **{int(cmd.bot.latency * 1000)}ms**'
    general_text += f'\nPlatform: **{sys.platform.upper()}**'
    general_text += f'\nStarted: **{arrow.get(psutil.boot_time()).humanize()}**'
    cpu_clock = psutil.cpu_freq()
    if cpu_clock:
        cpu_clock = cpu_clock.current
    else:
        cpu_clock = 'Unknown'
    cpu_text = f'Count: **{psutil.cpu_count()} ({psutil.cpu_count(logical=False)})**'
    cpu_text += f'\nUsage: **{psutil.cpu_percent()}%**'
    cpu_text += f'\nClock: **{cpu_clock} MHz**'
    used_mem = humanfriendly.format_size(psutil.virtual_memory().used, binary=True)
    total_mem = humanfriendly.format_size(psutil.virtual_memory().total, binary=True)
    mem_text = f'Used: **{used_mem}**'
    mem_text += f'\nTotal: **{total_mem}**'
    mem_text += f'\nPercent: **{int(psutil.virtual_memory().percent)}%**'
    response = discord.Embed(color=os_color)
    response.set_author(name=socket.gethostname(), icon_url=os_icon)
    response.add_field(name='General', value=general_text)
    response.add_field(name='CPU', value=cpu_text)
    response.add_field(name='Memory', value=mem_text)
    await message.channel.send(embed=response)