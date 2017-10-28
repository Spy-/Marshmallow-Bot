import discord
from marshmallow.core.utilities.data_processing import user_avatar


async def unqueue(cmd, message, args):
    if args:
        if message.author.voice:
            same_bound = True
            if message.guild.voice_client:
                if message.guild.voice_client.channel.id != message.author.voice.channel.id:
                    same_bound = False
            if same_bound:
                if message.guild.voice_client:
                    queue = cmd.bot.music.get_queue(message.guild.id)
                    if queue:
                        try:
                            order_num = int(args[0])
                            if order_num >= 1:
                                order_num -= 1
                            queue_size = len(queue)
                            if order_num <= queue_size - 1:
                                item = queue[order_num]
                                cmd.bot.music.queue_del(message.guild.id, order_num)
                                response = discord.Embed(color=0x66CC66, title=f'✅ Removed {item.title}.')
                                requester = f'{message.author.name}#{message.author.discriminator}'
                                response.set_author(name=requester, icon_url=user_avatar(message.author))
                            else:
                                response = discord.Embed(color=0xBE1931, title='❗ Input out of range.')
                        except ValueError:
                            response = discord.Embed(color=0xBE1931, title='❗ Invalid input. Numbers only.')
                    else:
                        response = discord.Embed(color=0xBE1931, title='❗ The queue is empty.')
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ I am not connected to any channel.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ You are not in my voice channel.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ You are not in a voice channel.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)