import operator

import discord
from humanfriendly.tables import format_pretty_table as boop


def percentify(small, big):
    prc_flt = small / big
    out = int(prc_flt * 100)
    return out


async def rolepopulation(cmd, message, args):
    if args:
        rl_qry = ' '.join(args)
        role_search = discord.utils.find(lambda x: x.name.lower() == rl_qry.lower(), message.guild.roles)
        if role_search:
            counter = 0
            for member in message.guild.members:
                member_role_search = discord.utils.find(lambda x: x.id == role_search.id, member.roles)
                if member_role_search:
                    counter += 1
            response = discord.Embed(color=role_search.color)
            response.set_author(name=message.guild.name, icon_url=message.guild.icon_url)
            response.add_field(name=f'{role_search.name} Population', value=f'```[y\n{counter}\n```')
        else:
            response = discord.Embed(color=0x696969, title=f'🔍 {rl_qry} not found.')
    else:
        role_dict = {}
        for role in message.guild.roles:
            if role.name != '@everyone':
                role_key = role.name
                role_count = 0
                for member in message.guild.members:
                    member_role_search = discord.utils.find(lambda x: x.id == role.id, member.roles)
                    if member_role_search:
                        role_count += 1
                role_dict.update({role_key: role_count})
        sorted_roles = sorted(role_dict.items(), key=operator.itemgetter(1), reverse=True)
        output = []
        for srole in sorted_roles[:20]:
            output.append([srole[0], srole[1], f'{str(percentify(srole[1], len(message.guild.members)))}%'])
        out_text = boop(output)
        response = discord.Embed(color=0x3B88C3)
        response.set_author(name=message.guild.name, icon_url=message.guild.icon_url)
        response.add_field(name='Statistics',
                           value=f'```py\nShowing {len(output)} roles out of {len(message.guild.roles)}\n```',
                           inline=False)
        response.add_field(name=f'Role Population', value=f'```haskell\n{out_text}\n```', inline=False)
    await message.channel.send(embed=response)