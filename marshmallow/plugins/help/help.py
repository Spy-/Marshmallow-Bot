import discord


async def help(cmd, message, args):
    if args:
        cmd_name = ''.join(args).lower()
        if cmd_name in cmd.bot.modules.alts:
            cmd_name = cmd.bot.modules.alts[cmd_name]
        if cmd_name in cmd.bot.modules.commands:
            command = cmd.bot.modules.commands[cmd_name]
            response = discord.Embed(color=discord.Colour.orange(
            ), title=f'📄 {command.name.upper()} Usage and Information')
            response.add_field(name='Usage Example',
                               value=f'`{command.usage}`', inline=False)
            response.add_field(name='Command Description',
                               value=f'```\n{command.desc}\n```', inline=False)
            if command.alts:
                response.add_field(name='Command Aliases',
                                   value=f'```\n{", ".join(command.alts)}\n```')
        else:
            response = discord.Embed(
                color=0x696969, title='🔍 No such command was found...')
    else:
        commands = cmd.bot.modules.commands
        command_list = []
        module_list = []

        owner_image = 'https://hearthstone.gamepedia.com/media/hearthstone.gamepedia.com/thumb/d/dc/Snowflipper_Penguin_alternative_art.jpg/400px-Snowflipper_Penguin_alternative_art.jpg?version=231640852a401d7f4f7e6aeb5267fcd8'
        bot_image = 'https://raw.githubusercontent.com/Spy-/Marshmallow-Bot/master/image/marsh.jpg'
        bot_title = 'Marshmallow Man'
        invite_url = f'https://discordapp.com/oauth2/authorize?client_id={cmd.bot.user.id}&scope=bot&permissions=2146958591'
        support_text = f'**Add Me**: [Link]({invite_url})'
        support_text += f' | **Commands**: [Link](https://github.com/Spy-/Marshmallow-Bot/blob/master/docs/information/commands.md)'

        response = discord.Embed(color=discord.Colour.orange())
        response.add_field(name='Help', value=support_text, inline=True)
        response.set_author(name='Marshmallow Bot Commands', icon_url=bot_image,
                            url='https://github.com/Spy-/Marshmallow-Bot/blob/master')
        response.set_footer(text='A bot made by Spyn.', icon_url=owner_image)

        # gathers all the modules
        for command in commands:
            command = commands[command]
            category = command.category.upper()
            if category not in module_list:
                module_list.append(category)

        for module in module_list:
            module_commands = []
            for command in commands:
                command = commands[command]
                category = command.category.upper()
                if category == module:
                    module_commands.append(command.name)
            module_commands = sorted(module_commands)
            command_list.append(module_commands)

        for module in module_list:
            index = module_list.index(module)
            value = ''
            for command in command_list[index]:
                value += f'`{command}`  '
            response.add_field(name=module, value=value)

    await message.channel.send(embed=response)
