import json
import secrets
import discord
import aiohttp


async def xkcd(cmd, message, args):
    if args:
        comic_num = args[0]
    else:
        comic_num = secrets.randbelow(1908) + 1
    comic_url = f'http://xkcd.com/{comic_num}'
    joke_url = f'{comic_url}/info.0.json'
    async with aiohttp.ClientSession() as session:
        async with session.get(joke_url) as data:
            joke_json = await data.read()
            joke_json = json.loads(joke_json)
    image_url = joke_json['img']
    comic_title = joke_json['title']
    embed = discord.Embed(color=0xF9F9F9, title=f'XKCD: {comic_title}')
    embed.set_image(url=image_url)
    await message.channel.send(None, embed=embed)