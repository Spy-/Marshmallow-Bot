import discord

from .nodes.recipe_core import RecipeCore

recipe_core = None


async def viewrecipe(cmd, message, args):
    global recipe_core
    if not recipe_core:
        recipe_core = RecipeCore(cmd.resource('data'))
    if args:
        lookup = ' '.join(args)
        recipe = recipe_core.find_recipe(lookup)
        currency = cmd.bot.cfg.pref.currency
        if recipe:
            response = discord.Embed(color=recipe.color)
            ingredients = ''
            ing_value = 0
            recipe.ingredients.sort(key=lambda x: x.name)
            req_satisfied = True
            for ingredient in recipe.ingredients:
                user_inv = cmd.db.get_inventory(message.author)
                in_inventory = False
                for item in user_inv:
                    if item['item_file_id'] == ingredient.file_id:
                        in_inventory = True
                        break
                if in_inventory:
                    in_inventory = '▫'
                else:
                    in_inventory = '▪'
                    req_satisfied = False
                ingredients += f'\n{in_inventory} **{ingredient.name}**'
                ing_value += ingredient.value
            ing_icon = recipe.ingredients[0].icon
            item_title = f'{recipe.icon} {recipe.name}'
            item_short = f'Type: **{recipe.type}**\nValue: **{recipe.value} {currency}**'
            item_short += f'\nHave Ingredients: **{req_satisfied}**'
            item_short += f'\nIngredient Value: **{ing_value} {currency}**'
            response.add_field(name=item_title, value=item_short, inline=True)
            response.add_field(name=f'{ing_icon} Ingredients', value=ingredients, inline=True)
            response.add_field(name='📰 Description', value=recipe.desc, inline=False)
        else:
            response = discord.Embed(color=0x696969, title=f'🔍 I couldn\'t find that.')
    else:
        response = discord.Embed(color=0xBE1931, title=f'❗ Nothing inputted.')
    await message.channel.send(embed=response)