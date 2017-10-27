import asyncio


async def population_clockwork(ev):
    collection = 'GeneralStats'
    search = ev.db[ev.bot.cfg.db.database][collection].find_one({'name': 'population'})
    if not search:
        ev.db[ev.bot.cfg.db.database][collection].insert_one({'name': 'population'})
    ev.bot.loop.create_task(update_population_stats_node(ev))


async def update_population_stats_node(ev):
    while True:
        collection = 'GeneralStats'
        database = ev.bot.cfg.db.database
        server_count = len(list(ev.bot.guilds))
        member_count = len(list(ev.bot.get_all_members()))
        channel_count = len(list(ev.bot.get_all_channels()))
        # Guilds
        update_target = {"name": 'population'}
        update_data = {"$set": {'guild_count': server_count}}
        ev.db[database][collection].update_one(update_target, update_data)
        # Members
        update_target = {"name": 'population'}
        update_data = {"$set": {'member_count': member_count}}
        ev.db[database][collection].update_one(update_target, update_data)
        # Channels
        update_target = {"name": 'population'}
        update_data = {"$set": {'channel_count': channel_count}}
        ev.db[database][collection].update_one(update_target, update_data)
        await asyncio.sleep(60)
