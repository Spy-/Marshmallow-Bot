import discord
from .move_log_embed import make_move_log_embed
from marshmallow.core.utilities.data_processing import user_avatar


async def leave_move_log(ev, guild):
    if ev.bot.cfg.pref.movelog_channel:
        mlc_id = ev.bot.cfg.pref.movelog_channel
        mlc = discord.utils.find(lambda x: x.id == mlc_id, ev.bot.get_all_channels())
        if mlc:
            if guild.icon_url:
                icon = guild.icon_url
            else:
                icon = user_avatar(guild.owner)
            log_embed = discord.Embed(color=0xBE1931)
            log_embed.set_author(name='Left A Guild', icon_url=icon, url=icon)
            make_move_log_embed(log_embed, guild)
            await mlc.send(embed=log_embed)