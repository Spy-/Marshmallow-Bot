
## Module Index
- [ADMINISTRATION](#administration)
- [FUN](#fun)
- [HELP](#help)
- [MATHEMATICS](#mathematics)
- [MINIGAMES](#minigames)
- [MISCELLANEOUS](#miscellaneous)
- [MUSIC](#music)
- [SETTINGS](#settings)
- [UTILITY](#utility)

### ADMINISTRATION
Commands | Description | Example
----------|-------------|--------
`?evaluate` `?evaluate` `?eval` `?py` `?python` `?code` `?exec` | Executes raw python code. This should be used with caution. (Bot Owner Only) | `?evaluate print('hello world')`
`?geterror` | Gets an error's details using the given token. (Bot Owner Only) | `?geterror 9a2e9a374ac90294f225782f362e2ab1`
`?reload` | Reloads all of the modules in Marshmallow. This includes both commands and events. (Bot Owner Only) | `?reload`
`?setavatar` | Sets the avatar of the bot either to the linked or attached image. The officially supported formats for bot avatars are JPG and PNG images. Note that bots, like all users, have limited profile changes per time period. (Bot Owner Only) | `?setavatar https://my_fomain.net/my_avatar.png`
`?setstatus` | Sets the current playing status of the bot. To use this, the automatic status rotation needs to be disabled. It can be toggled with the togglestatus command. (Bot Owner Only) | `?setstatus with fishies`
`?setusername` | Sets the name of the bot to the inputted text. Note that bots, like all users, have limited profile changes per time period. (Bot Owner Only) | `?setusername Supreme Bot`
`?shutdown` | Forces the bot to disconnect from Discord and shut down all processes. (Bot Owner Only) | `?shutdown`
`?sysexec` `?sh` | Executes a shell command. Extreme warning! (Bot Owner Only) | `?sysexec echo 'Hello'`
`?test` `?t` | For testing purposes, obviously. Used as a placeholder for testing functions. (Bot Owner Only) | `?test`
`?togglestatus` | Toggles if the automatic status rotation is enabled or disabled. (Bot Owner Only) | `?togglestatus`
[Back To Top](#module-index)

### FUN
Commands | Description | Example
----------|-------------|--------
`?award` `?pay` | Awards a chosen amount of Kud from the vault to a targeted person. The amount of Kud needs to go first, followed by the target. Only server managers can award Kud from the vault. Anybody can contribute to the vault with the givetovault command. | `?award 500 @person`
`?dog` | Outputs a random dog image. | `?dog`
`?givetovault` `?givetobank` `?gtv` `?gtb` | The vault is a server specific Kud storage system. Members can contribute to the vault with this command. Adding to the vault taxes 5% of the Kud. The kud can then be awarded to users using the award command. | `?givetovault`
`?vault` `?bank` | Shows the current amount of Kud in the guild's vault. | `?vault`
`?xkcd` | If you like humorous things and know a bit of technology, you will lose a lot of time reading these. XKCD comics are perfect for procrastination and time wasting. | `?xkcd [num]`
[Back To Top](#module-index)

### HELP
Commands | Description | Example
----------|-------------|--------
`?commands` `?command` | Shows the commands in a module group category. To view all the module group categories, use the modules command. | `?commands minigames`
`?help` | Show information about a command if something in inputted. | `?help fish`
`?modules` `?module` | Shows all the module categories. | `?modules`
[Back To Top](#module-index)

### MATHEMATICS
Commands | Description | Example
----------|-------------|--------
`?collectchain` | Collects messages sent by the mentioned user and saves it as a chain. Only one person can use the command at the time due to the processing load it takes. | `?collectchain @person #channel`
`?impersonate` `?mimic` | Tries to impersonate the mentioned user if a chain file for them exists. This command is on a 20 second cooldown due to it's weight. | `?impersonate @person`
`?makehash` `?hash` | Creates a hash using the inputed has type. These are all the hash types you can use. sha512, sha3_224, sha3_512, MD4, dsaWithSHA, ripemd160, RIPEMD160, SHA, ecdsa-with-SHA1, sha3_384, SHA512, sha1, SHA224, md4, DSA-SHA, SHA384, blake2b, dsaEncryption, SHA256, sha384, sha, DSA, shake_128, sha224, SHA1, shake_256, sha256, MD5, blake2s, md5, sha3_256, whirlpool | `?makehash md5 Nabzie is best tree.`
`?timeconvert` `?tconv` | Converts the given time in the given time zone to the inputted time zone. | `?timeconvert 18:57 UTC>PST`
`?wipechain` | It wipes your entire Markov chain, if you have one. | `?wipechain`
`?wolframalpha` `?wa` | Makes a request for Wolfram Alpha to process. This can be a lot of things, most popular being complex math operations. | `?wolframalpha 69+42`
[Back To Top](#module-index)

### MINIGAMES
Commands | Description | Example
----------|-------------|--------
`?coinflip` `?cf` | Flips a coin. Nothing complex. You can try guessing the results by typing either Heads or Tails. | `?coinflip Heads`
`?eightball` `?8ball` | The 8Ball has answers to ALL your questions. Come one, come all, and ask the mighty allknowing 8Ball! Provide a question at the end of the command and await the miraculous answer! | `?eightball Will I ever be pretty?`
`?mathgame` `?mg` | A mathematics minigame. You are given a problem, solve it. Numbers are rounded to 2 decimals. You can also specify how hard you want the problem to be. The scale goes from 1-9. The default difficulty is 3. The time and Kud reward scale with the difficulty and number of hard operators. | `?mathgame 4`
`?quiz` | A quiz minigame with various quizzes to choose from. With a lot more coming soon... | `?quiz`
`?roll` `?dice` | Gives a random number from 0 to 100. You can specify the highest number the function calls by adding a number after the command. The Number TECHNICALLY does not have a limit but the bigger you use, the bigger the message, which just looks plain spammy. | `?roll 501`
`?rps` `?rockpaperscissors` | Play Rock-Paper-Scissors with the bot. No cheating, we swear. Maybe she just doesn't like you. | `?rps s`
`?slots` | Spin the slot machine, maybe you win, maybe you don't. Who knows? It costs 10 Kud to spin the slot machine by default. But you can specify how much you want to put in the machine. And the rewards are based on how many of the same icon you get in the middle row. Rewards are different for each icon. The slots can be spun only once every 60 seconds. | `?slots 52`
`?trivia` `?triv` `?t` | A trivia minigame. You are given a question and have to input the number of your answer. Guess correctly and you win 5-15 Kud, depending on the difficulty. You have 20 seconds to answer the question. | `?trivia`
`?unscramble` `?usg` | A minigame where you guess the scrambled word. You have 30 seconds to guess the word shown. The Kud reward is equal to the number of letters in the word. | `?unscramble`
[Back To Top](#module-index)

### MISCELLANEOUS
Commands | Description | Example
----------|-------------|--------
`?afk` | Sets you as afk. Whenever someone mentions you they will be notified that you are afk. When you send a message your afk status will be removed. This automatic removal ignores messages that start with the command prefix. | `?afk Sleeping or eating, probably both!`
`?choose` | The bot will select a thing from the inputed list. Separate list items with a semicolon and space. | `?choose Sleep; Eat; Code; Lewd Stuff`
`?httpstatus` `?http` | Shows information about a HTTP response status code. | `?httpstatus 404`
`?myreminders` `?reminders` `?rms` | Shows a list of the reminders that you have created. The location where they are set to execute in. And in what time they execute in. If you add "here" to the end of the command, it will only show reminders made in the current channel. | `?myreminders here`
`?poll` | Creates a poll with the items from the inputted list. Separate list items with a semicolon and a space. | `?poll Want to eat?; Yes; No; Hand me the cheese!`
`?randombetween` `?ranin` | Outputs a random number between two inputted numbers. | `?randombetween 59 974`
`?reminderinfo` `?reminder` `?rminfo` `?rmi` | Shows information about your reminder with the given ID. Such as when it executes and where. | `?reminderinfo f93f`
`?remindme` `?remind` `?setreminder` `?alarm` `?rmme` | Sets a timer that will mention the author when it's done. The time format is H:M:S, but is not limited to the constraints of their types. Meaning you can type "200:5000:999999" if you wish. Reminders are limited to 90 days, and you are limited to 15 reminders. | `?remindme 1:03:15 LEEEEROOOOY JEEEEEENKIIIIINS!`
`?removereminder` `?delreminder` `?delrm` | Deletes a reminder of yours with the inputted ID. | `?removereminder 1a9e`
[Back To Top](#module-index)

### MUSIC
Commands | Description | Example
----------|-------------|--------
`?disconnect` `?stop` | Stops the music, disconnects the bot from the current voice channel, and purges the music queue. | `?disconnect`
`?musicoverride` `?overridemusic` `?musickill` `?killmusic` | Overrides the current music player in instances where marshmallow is stuck in a channel. This will not purge the queue, just disconnect the bot. | `?musicoverride`
`?nowplaying` `?currentsong` `?playing` `?np` | Shows information regarding the currently playing song. | `?nowplaying`
`?pause` | Pauses the music player. | `?pause`
`?play` `?start` | Starts playing the music queue. | `?play`
`?queue` `?add` | Queues up a song to play from YouTube. Either from a direct URL or text search. Playlists are supported but take a long time to process. | `?queue Kaskade Disarm You Illenium Remix`
`?repeat` | Toggles if the current queue should be repeated. Whenever a song is played, it's re-added to the end of the queue. | `?repeat`
`?resume` | Resumes the music player. | `?resume`
`?shuffle` | Randomizes the current song queue. | `?shuffle`
`?skip` `?next` | Skips the currently playing song. | `?skip`
`?summon` `?move` | If the bot isn't connected to any channel, it'll connect to yours. If it is connected, it will move to you. | `?summon`
`?unqueue` `?remove` | Removes a song from the queue. Minimum number is 1 and the maximum is however many items the queue has. Even though list indexes start at zero. | `?unqueue 5`
`?volume` `?vol` | Changes the volume of the bot. | `?volume 50`
[Back To Top](#module-index)

### SETTINGS
Commands | Description | Example
----------|-------------|--------
`?chatterbot` | Toggles if the Chatterbot functions should be active. If active, when a message starts with a mention of marshmallow, she will respond. This setting is active by default. | `?chatterbot`
`?deletecommands` `?delcmds` | Toggles if messages that are a command should be automatically deleted. | `?deletecommands`
`?logavatars` | Toggles if avatar changes should be logged. | `?logavatars`
`?logedits` | Toggles if message editing should be logged in the server's logging channel. | `?logedits`
`?loggingchannel` `?logchannel` `?logch` | Designates a channel where server events will be logged to. The stuff that is logged is member movement and moderator actions. Such as warns, bans, muting members and pruning channels. To disable the logging channel, input "disable" as the channel argument. | `?loggingchannel #logging`
`?lognames` | Toggles if username changes should be logged. This does not log nickname changes. See the lognicknames command. | `?lognames`
`?lognicknames` | Toggles if nickname changes should be logged. This does not log username changes. See the lognames command. | `?lognicknames`
`?prefix` | Sets the prefix that marshmallow should respond to. This will be bound to your server and you can set it to anything you'd like. However, the prefix can not contain spaces. They will be automatically removed. | `?prefix !!`
`?unflip` | Toggles if marshmallow should respond to tables being flipped. | `?unflip`
[Back To Top](#module-index)

### UTILITY
Commands | Description | Example
----------|-------------|--------
`?avatar` `?av` | Shows the mentioned user's avatar. If no user is mentioned, it shows the author's avatar. You can add "gif" to the end of the command to indicate that it's a gif. Or you can add "auto" to make the color strip the dominant color of the image. | `?avatar @person`
`?botinformation` `?botinfo` `?info` | Shows information about the bot, version, codename, authors, etc. | `?botinformation`
`?bots` | Lists the bots on the server where the command is used and shows their status. | `?bots`
`?channelid` `?chid` `?cid` | Shows the User ID of the mentioned channel. If no channel is mentioned, it will show the ID of the channel the command is used in. If you don't want the return message to be an embed, add "text" at the end. | `?channelid #channel`
`?channelinformation` `?channelinfo` `?chinfo` `?cinfo` | Shows information and data about the mentioned channel. If no channel is mentioned, it will show data for the channel that the command is used in. | `?channelinformation #channel`
`?color` `?colour` `?clr` | Shows the inputted color. It accepts either a HEX code or an RGB array. | `?color #1abc9c`
`?ingame` | Shows the top played games on the server. | `?ingame @person`
`?owners` | Shows a list of marshmallow's owners. Users in this list have access to the administration module. | `?owners`
`?permissions` `?perms` | Shows which permissions a user has and which they do not. If no user is mentioned, it will target the message author. | `?permissions @person`
`?roleinformation` `?roleinfo` `?rinfo` | Shows information and data about the inputted role. Roles mentions do not work here, lookup is done via role name. | `?roleinformation`
`?rolepopulation` `?rolepop` | Shows the population of the inputted role. If no arguments are provided, it will show the top 20 roles by population. | `?rolepopulation Warlard`
`?servericon` `?srvicon` `?icon` | Shows the server's icon image. | `?servericon`
`?serverid` `?guildid` `?srvid` `?sid` `?gid` | Shows the Server ID of the server the command is used in. | `?serverid`
`?serverinformation` `?serverinfo` `?sinfo` | Shows information and data about the server that the command is used in. | `?serverinformation`
`?shortenurl` `?shorten` `?bitly` | Shortens a URL for you using BitLy. All URLs returned via Marshmallow are without ads, merely shortened using the service. | `?shortenurl https://i.redd.it/ngwebbf5nwfz.jpg`
`?statistics` `?stats` | Shows marshmallow's current statistics. Population, message and command counts, and rates since startup. As well as when the bot last started. | `?statistics`
`?status` | Shows the status of marshmallow's machine. Processor information, memory, storage, network, etc. | `?status`
`?userid` `?uid` | Shows the User ID of the mentioned user. If no user is mentioned, it will show the author's ID. If you don't want the return message to be an embed, add "text" at the end. | `?userid @person`
`?userinformation` `?userinfo` `?uinfo` | Shows information and data about the mentioned user. If no user is mentioned, it will show data for the message author. | `?userinformation @person`
`?whoplays` | Generates a list of users playing the inputted game. | `?whoplays Overwatch`
[Back To Top](#module-index)