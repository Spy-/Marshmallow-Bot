

## Module Index
- [ADMINISTRATION](#administration)
- [HELP](#help)
- [MUSIC](#music)

### ADMINISTRATION
Commands | Description | Example
----------|-------------|--------
`?geterror` | Gets an error's details using the given token. (Bot Owner Only) | `?eterror 9a2e9a374ac90294f225782f362e2ab1`
`?reload` | Reloads all of the modules in Marshmallow. This includes both commands and events. (Bot Owner Only) | `?eload`
`?shutdown` | Forces the bot to disconnect from Discord and shut down all processes. (Bot Owner Only) | `?hutdown`
[Back To Top](#module-index)

### HELP
Commands | Description | Example
----------|-------------|--------
`?commands` | Shows the commands in a module group category. To view all the module group categories, use the modules command. | `?ommands minigames`
`?help` | Show information about a command if something in inputted. | `?elp fish`
`?modules` | Shows all the module categories. | `?odules`
[Back To Top](#module-index)

### MUSIC
Commands | Description | Example
----------|-------------|--------
`?disconnect` `?stop` | Stops the music, disconnects the bot from the current voice channel, and purges the music queue. | `?isconnect`
`?musicoverride` `?overridemusic` `?musickill` `?killmusic` | Overrides the current music player in instances where marshmallow is stuck in a channel. This will not purge the queue, just disconnect the bot. | `?usicoverride`
`?nowplaying` `?currentsong` `?playing` `?np` | Shows information regarding the currently playing song. | `?owplaying`
`?play` `?start` | Starts playing the music queue. | `?lay`
`?queue` `?add` | Queues up a song to play from YouTube. Either from a direct URL or text search. Playlists are supported but take a long time to process. | `?ueue Kaskade Disarm You Illenium Remix`
`?repeat` | Toggles if the current queue should be repeated. Whenever a song is played, it's re-added to the end of the queue. | `?epeat`
`?shuffle` | Randomizes the current song queue. | `?huffle`
`?skip` `?next` | Skips the currently playing song. | `?kip`
`?summon` `?move` | If the bot isn't connected to any channel, it'll connect to yours. If it is connected, it will move to you. | `?ummon`
`?unqueue` `?remove` | Removes a song from the queue. Minimum number is 1 and the maximum is however many items the queue has. Even though list indexes start at zero. | `?nqueue 5`
[Back To Top](#module-index)