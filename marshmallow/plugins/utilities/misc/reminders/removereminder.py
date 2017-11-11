import discord
from marshmallow.core.utilities.constants import *

async def removereminder(cmd, message, args):
    if args:
        rem_id = args[0].lower()
        lookup_data = {'UserID': message.author.id, 'ReminderID': rem_id}
        reminder = cmd.db[cmd.db.db_cfg.database].Reminders.find_one(lookup_data)
        if reminder:
            cmd.db[cmd.db.db_cfg.database].Reminders.delete_one(lookup_data)
            response = discord.Embed(color=0x66CC66, title=f'✅ Reminder {rem_id} has been deleted.')
        else:
            response = discord.Embed(color=0x696969, title=f'🔍 Reminder `{rem_id}` not found.')
    else:
        response = discord.Embed(color=ERROR, title='❗ No reminder ID inputted.')
    await message.channel.send(embed=response)