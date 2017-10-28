

## Module Index
- [ADMINISTRATION](#administration)
- [FUN](#fun)
- [HELP](#help)
- [MINIGAMES](#minigames)
- [MUSIC](#music)
- [SETTINGS](#settings)
- [UTILITY](#utility)

### ADMINISTRATION
Commands | Description | Example
----------|-------------|--------
`?evaluate` `?evaluate` `?eval` `?py` `?python` `?code` `?exec` | Executes raw python code. This should be used with caution. (Bot Owner Only) | `?valuate print('hello world')`
`?geterror` | Gets an error's details using the given token. (Bot Owner Only) | `?eterror 9a2e9a374ac90294f225782f362e2ab1`
`?reload` | Reloads all of the modules in Marshmallow. This includes both commands and events. (Bot Owner Only) | `?eload`
`?setavatar` | Sets the avatar of the bot either to the linked or attached image. The officially supported formats for bot avatars are JPG and PNG images. Note that bots, like all users, have limited profile changes per time period. (Bot Owner Only) | `?etavatar https://my_fomain.net/my_avatar.png`
`?setstatus` | Sets the current playing status of the bot. To use this, the automatic status rotation needs to be disabled. It can be toggled with the togglestatus command. (Bot Owner Only) | `?etstatus with fishies`
`?setusername` | Sets the name of the bot to the inputted text. Note that bots, like all users, have limited profile changes per time period. (Bot Owner Only) | `?etusername Supreme Bot`
`?shutdown` | Forces the bot to disconnect from Discord and shut down all processes. (Bot Owner Only) | `?hutdown`
`?sysexec` `?sh` | Executes a shell command. Extreme warning! (Bot Owner Only) | `?ysexec echo 'Hello'`
`?test` `?t` | For testing purposes, obviously. Used as a placeholder for testing functions. (Bot Owner Only) | `?est`
`?togglestatus` | Toggles if the automatic status rotation is enabled or disabled. (Bot Owner Only) | `?ogglestatus`
[Back To Top](#module-index)

### FUN
Commands | Description | Example
----------|-------------|--------
`?award` `?pay` | Awards a chosen amount of Kud from the vault to a targeted person. The amount of Kud needs to go first, followed by the target. Only server managers can award Kud from the vault. Anybody can contribute to the vault with the givetovault command. | `?ward 500 @person`
`?givetovault` `?givetobank` `?gtv` `?gtb` | The vault is a server specific Kud storage system. Members can contribute to the vault with this command. Adding to the vault taxes 5% of the Kud. The kud can then be awarded to users using the award command. | `?ivetovault`
`?vault` `?bank` | Shows the current amount of Kud in the guild's vault. | `?ault`
[Back To Top](#module-index)

### HELP
Commands | Description | Example
----------|-------------|--------
`?commands` | Shows the commands in a module group category. To view all the module group categories, use the modules command. | `?ommands minigames`
`?help` | Show information about a command if something in inputted. | `?elp fish`
`?modules` | Shows all the module categories. | `?odules`
[Back To Top](#module-index)

### MINIGAMES
Commands | Description | Example
----------|-------------|--------
`?coinflip` `?cf` | Flips a coin. Nothing complex. You can try guessing the results by typing either Heads or Tails. | `?oinflip Heads`
`?eightball` `?8ball` | The 8Ball has answers to ALL your questions. Come one, come all, and ask the mighty allknowing 8Ball! Provide a question at the end of the command and await the miraculous answer! | `?ightball Will I ever be pretty?`
`?roll` `?dice` | Gives a random number from 0 to 100. You can specify the highest number the function calls by adding a number after the command. The Number TECHNICALLY does not have a limit but the bigger you use, the bigger the message, which just looks plain spammy. | `?oll 501`
`?rps` `?rockpaperscissors` | Play Rock-Paper-Scissors with the bot. No cheating, we swear. Maybe she just doesn't like you. | `?ps s`
`?slots` | Spin the slot machine, maybe you win, maybe you don't. Who knows? It costs 10 Kud to spin the slot machine by default. But you can specify how much you want to put in the machine. And the rewards are based on how many of the same icon you get in the middle row. Rewards are different for each icon. The slots can be spun only once every 60 seconds. | `?lots 52`
[Back To Top](#module-index)

### MUSIC
Commands | Description | Example
----------|-------------|--------
`?disconnect` `?stop` | Stops the music, disconnects the bot from the current voice channel, and purges the music queue. | `?isconnect`
`?musicoverride` `?overridemusic` `?musickill` `?killmusic` | Overrides the current music player in instances where marshmallow is stuck in a channel. This will not purge the queue, just disconnect the bot. (Bot Owner Only) | `?usicoverride`
`?nowplaying` `?currentsong` `?playing` `?np` | Shows information regarding the currently playing song. | `?owplaying`
`?play` `?start` | Starts playing the music queue. | `?lay`
`?queue` `?add` | Queues up a song to play from YouTube. Either from a direct URL or text search. Playlists are supported but take a long time to process. | `?ueue Kaskade Disarm You Illenium Remix`
`?repeat` | Toggles if the current queue should be repeated. Whenever a song is played, it's re-added to the end of the queue. | `?epeat`
`?shuffle` | Randomizes the current song queue. | `?huffle`
`?skip` `?next` | Skips the currently playing song. | `?kip`
`?summon` `?move` | If the bot isn't connected to any channel, it'll connect to yours. If it is connected, it will move to you. | `?ummon`
`?unqueue` `?remove` | Removes a song from the queue. Minimum number is 1 and the maximum is however many items the queue has. Even though list indexes start at zero. | `?nqueue 5`
[Back To Top](#module-index)

### SETTINGS
Commands | Description | Example
----------|-------------|--------
`?chatterbot` | Toggles if the Chatterbot functions should be active. If active, when a message starts with a mention of marshmallow, she will respond. This setting is active by default. | `?hatterbot`
`?deletecommands` `?delcmds` | Toggles if messages that are a command should be automatically deleted. | `?eletecommands`
`?logavatars` | Toggles if avatar changes should be logged. | `?ogavatars`
`?logedits` | Toggles if message editing should be logged in the server's logging channel. | `?ogedits`
`?loggingchannel` `?logchannel` `?logch` | Designates a channel where server events will be logged to. The stuff that is logged is member movement and moderator actions. Such as warns, bans, muting members and pruning channels. To disable the logging channel, input "disable" as the channel argument. | `?oggingchannel #logging`
`?lognames` | Toggles if username changes should be logged. This does not log nickname changes. See the lognicknames command. | `?ognames`
`?lognicknames` | Toggles if nickname changes should be logged. This does not log username changes. See the lognames command. | `?ognicknames`
`?prefix` | Sets the prefix that marshmallow should respond to. This will be bound to your server and you can set it to anything you'd like. However, the prefix can not contain spaces. They will be automatically removed. | `?refix !!`
`?unflip` | Toggles if marshmallow should respond to tables being flipped. | `?nflip`
[Back To Top](#module-index)

### UTILITY
Commands | Description | Example
----------|-------------|--------
`?botinformation` `?botinfo` `?info` | Shows information about the bot, version, codename, authors, etc. | `?otinformation`
`?channelinformation` `?channelinfo` `?chinfo` `?cinfo` | Shows information and data about the mentioned channel. If no channel is mentioned, it will show data for the channel that the command is used in. | `?hannelinformation #channel`
`?owners` | Shows a list of marshmallow's owners. Users in this list have access to the administration module. | `?wners`
`?permissions` `?perms` | Shows which permissions a user has and which they do not. If no user is mentioned, it will target the message author. | `?ermissions @person`
`?roleinformation` `?roleinfo` `?rinfo` | Shows information and data about the inputted role. Roles mentions do not work here, lookup is done via role name. | `?oleinformation`
`?serverinformation` `?serverinfo` `?sinfo` | Shows information and data about the server that the command is used in. | `?erverinformation`
`?statistics` `?stats` | Shows marshmallow's current statistics. Population, message and command counts, and rates since startup. As well as when the bot last started. | `?tatistics`
`?status` | Shows the status of marshmallow's machine. Processor information, memory, storage, network, etc. | `?tatus`
`?userinformation` `?userinfo` `?uinfo` | Shows information and data about the mentioned user. If no user is mentioned, it will show data for the message author. | `?serinformation @person`
[Back To Top](#module-index)