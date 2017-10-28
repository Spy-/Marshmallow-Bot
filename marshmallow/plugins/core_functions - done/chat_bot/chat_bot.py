from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

cb = None


def init_chatterbot(ev):
    global cb
    if ev.db.chatterbot.statements.count():
        train = False
    else:
        train = True
    cb = ChatBot(
        "Marshmallow",
        database='chatterbot',
        database_uri=ev.db.db_address,
        storage_adapter='chatterbot.storage.MongoDatabaseAdapter'
    )
    if train:
        ev.log.info('Training Chatterbot...')
        cb.set_trainer(ChatterBotCorpusTrainer)
        cb.train('chatterbot.corpus.english')
        ev.log.info('Chatterbot Training Complete')


async def chat_bot(ev, message):
    if not cb:
        init_chatterbot(ev)
    if message.guild:
        active = ev.db.get_guild_settings(message.guild.id, 'ChatterBot')
        if active:
            mention = f'<@{ev.bot.user.id}>'
            mention_alt = f'<@!{ev.bot.user.id}>'
            if message.content.startswith(mention) or message.content.startswith(mention_alt):
                args = message.content.split(' ')
                interaction = ' '.join(args[1:])
                cb_resp = cb.get_response(interaction)
                response = f'{message.author.mention} {cb_resp}'
                await message.channel.send(response)