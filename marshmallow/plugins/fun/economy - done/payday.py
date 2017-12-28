import discord

async def payday(cmd, message, args):
    currency_icon = cmd.bot.cfg.pref.currency_icon
    currency = cmd.bot.cfg.pref.currency
    current_kud = cmd.db.get_currency(message.author, message.guild)['current']
    cooldown = 60 * 60
    payday = 100

    if not cmd.bot.cool_down.on_cooldown(cmd.name, message.author):
        response = discord.Embed(color=0x5dadec, title=f'Payday: {currency_icon} {payday} {currency} has been given.')
        cmd.bot.cool_down.set_cooldown(cmd.name, message.author, cooldown)
        cmd.db.add_currency(message.author, message.guild, payday, additive=False)
    else:
        timeout = cmd.bot.cool_down.get_cooldown(cmd.name, message.author)
        response = discord.Embed(color=0x696969, title=f'🕙 You can spin again in {timeout} seconds.')
    await message.channel.send(embed=response)