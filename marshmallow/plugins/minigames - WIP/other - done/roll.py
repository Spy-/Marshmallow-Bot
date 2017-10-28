import secrets
import discord


async def roll(cmd, message, args):
    if args:
        if 'd' in args[0].lower():
            params = args.lower().split('d')
            count = int(params[0])
            high_end = int(params[1])
        else:
            count = 1
            high_end = int(args[0])
        if len(args) > 1:
            modifier = int(args[-1])
        else:
            modifier = 0
    else:
        count = 1
        high_end = 6
        modifier = 0
    if count <= 10:
        if high_end <= 9999999999:
            if high_end > 0:
                roll_out = ''
                for i in range(0, count):
                    num = secrets.randbelow(high_end) + 1
                    if modifier:
                        num += modifier
                    roll_out += f'\nDice #{i + 1}: **{num}**'
                response = discord.Embed(color=0xea5963)
                response.add_field(name='🎲 You Rolled', value=roll_out)
            else:
                response = discord.Embed(color=0xBE1931, title='❗ The high end must be positive and not a zero.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Maximum number allowed is 999999999999.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Up to 10 dice please.')
    await message.channel.send(None, embed=response)
