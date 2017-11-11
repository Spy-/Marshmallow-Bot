import arrow
import discord
from marshmallow.core.utilities.constants import *

async def roleinformation(cmd, message, args):
    if args:
        role_lookup = ' '.join(args)
        role = discord.utils.find(lambda x: x.name.lower() == role_lookup.lower(), message.guild.roles)
        if role:
            creation_time = arrow.get(role.created_at).format('DD. MMMM YYYY')
            desc_text = f'Name: **{role.name}**'
            desc_text += f'\nID: **{role.id}**'
            desc_text += f'\nColor: **{str(role.color).upper()}**'
            desc_text += f'\nHoisted: **{role.hoist}**'
            desc_text += f'\nMembers: **{len(role.members)}**'
            desc_text += f'\nCreated: **{creation_time}**'
            response = discord.Embed(color=role.color)
            response.add_field(name=f'{role.name} Information', value=desc_text)
        else:
            response = discord.Embed(color=ERROR, title=f'❗ No {role_lookup} role found.')
    else:
        response = discord.Embed(color=ERROR, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)