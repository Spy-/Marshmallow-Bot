async def ev_member_join(ev, member):
    def_stat_data = {
        'event': 'member_join',
        'count': 0
    }
    collection = 'EventStats'
    database = ev.bot.cfg.db.database
    check = ev.db[database][collection].find_one({"event": 'member_join'})
    if not check:
        ev.db[database][collection].insert_one(def_stat_data)
        ev_count = 0
    else:
        ev_count = check['count']
    ev_count += 1
    update_target = {"event": 'member_join'}
    update_data = {"$set": {'count': ev_count}}
    ev.db[database][collection].update_one(update_target, update_data)
