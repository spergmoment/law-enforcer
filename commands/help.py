import discord, random

async def run(**kwargs):
    args = kwargs['args']
    c = kwargs['c']
    helpCmd = kwargs['helpCmd']
    # initialize an embed
    helpEmb = discord.Embed()
    ids = kwargs['ids']
    # get 2 random ids from the owners
    id1 = f"<@{ids[random.randint(0, 1)]}>"
    id2 = f"<@{ids[random.randint(0, 1)]}>"
    prefix = kwargs['prefix']
    # no args
    if not len(args) > 0:
        # set an author
        helpEmb.set_author(name="Invite me here!", url=kwargs['oauth'], icon_url=kwargs['client'].user.avatar_url)
        # set a title
        helpEmb.title = "All commands"
        # set the description
        helpEmb.description = "Here is a list of all commands I have."
        # add fields for all the commands
        helpEmb.add_field(name="ping", value="Get the current Client ping and API ping", inline=False)
        helpEmb.add_field(name="ban", value="Ban a user", inline=False)
        helpEmb.add_field(name="unban", value="Unban a user", inline=False)
        helpEmb.add_field(name="kick", value="Kick a user", inline=False)
        helpEmb.add_field(name="mute", value="Mute a user", inline=False)
        helpEmb.add_field(name="unmute", value="Unmute a user", inline=False)
        helpEmb.add_field(name="clear", value="Clear messages in a channel", inline=False)
        helpEmb.add_field(name="addtag", value="Add a tag to the server", inline=False)
        helpEmb.add_field(name="tag", value="Access a tag in the server", inline=False)
        helpEmb.add_field(name="taginfo", value="Get a tag's info in the server", inline=False)
        # set the footer
        helpEmb.set_footer(text="Law Enforcer v0.6", icon_url=kwargs['client'].user.avatar_url)
    # check what command they want
    elif args[0] == "ping":
        # helpCmd is a helper function I made
        # that utilized the fact that all of my original
        # command docs had the exact same pattern

        # you can see that pattern in the constants
        
        helpEmb = helpCmd(helpEmb, 'ping', 'Get the current Client and API ping.', "", False, False,
        "Client ping is the hard Client latency, while the API ping is how long I take to respond.", "None")
    elif args[0] == "ban":
        helpEmb = helpCmd(helpEmb, 'ban', 'Ban a user from the server.', '(user) (reason || None)', 
        f"{id1} dumb stupid", id2, "The user is DMed upon being banned.", '`BAN_MEMBERS`')
    elif args[0] == "kick":
        helpEmb = helpCmd(helpEmb, 'kick', 'Kick a user from the server.', "(user) (reason || None)", f"{id1} don't do that again", id2,
        f"The user is DMed upon being kicked. Additionally, they are given a one-time invite to rejoin with."
        f"\nIn later versions, there will be options to disable this.", "`KICK_MEMBERS`\n`CREATE_INSTANT_INVITE`")
    elif args[0] == "mute":
        helpEmb = helpCmd(helpEmb, 'mute', "Mute a user for a certain amount of time.", 
        '(user) (reason || None)', f"{id1} 24 stop spamming", f"{id2} 0.5",
        "The user is DMed when they are muted.", "`MUTE_MEMBERS`\n`KICK_MEMBERS`")
    elif args[0] == "unmute":
        helpEmb = helpCmd(helpEmb, 'unmute', 'Unmute a muted user.', '(user) (reason || None)', f"{id1} said sorry in dms", id2,
        "The user is DMed when unmuted.", "`MUTE_MEMBERS`\n`KICK_MEMBERS`")
    elif args[0] == "clear":
        helpEmb = helpCmd(helpEmb, 'clear', 'Clear a certain amount of messages.', '(amount || 20)',
        40, "", "You may clear as many messages as you want (up to 10000), but beware higher (>2000) values will be slow.",
        '`MANAGE_MESSAGES`\n`READ_MESSAGE_HISTORY`')
    elif args[0] == "unban":
        helpEmb = helpCmd(helpEmb, 'unban', 'Unban a banned user.', '(user ID) (reason || None)', 
        f"{ids[random.randint(0, 1)]} is not dumb", ids[random.randint(0, 1)], 
        "The user is DMed upon being unbanned (If they can be DMed).", '`BAN_MEMBERS`')
    elif args[0] == 'addtag':
        helpEmb = helpCmd(helpEmb, 'addtag', 'Add a tag to the server.', '(tag name) (tag content...)',
        f"example This is a cool tag!", f"test Test", f"Access tags with {prefix}tag (tag), "
        f"and their info with {prefix}taginfo (tag).", '`MANAGE_SERVER`')
    elif args[0] == 'tag':
        helpEmb = helpCmd(helpEmb, 'tag', 'Access a tag in the server.', '(tag name)', 'example', 'test',
        'Tags are specific to servers. Global tags may be added later, but for now, tags can only be used in the server they were created in.',
        'None')
    elif args[0] == 'taginfo':
        helpEmb = helpCmd(helpEmb, 'taginfo', 'Get some info on a tag in the server.', '(tag name)', 'example', 'test',
        f"Similarly to {prefix}tag, tags are specific to servers. This command gives you the tag name, content, author, and creation date.",
        'None')
    elif args[0] == 'removetag':
        helpEmb = helpCmd(helpEmb, 'removetag', 'Remove a tag from the server.', '(tag name)',
        f"example", f"test", None, '`MANAGE_SERVER`')
    # no valid command? go here
    else:
        helpEmb.title = "Invalid command!"
        helpEmb.description = f"The command you entered, {args[0]}, is invalid."
        helpEmb.set_footer(text=f"Use {prefix}help for a list of commands.", icon_url=kwargs['client'].user.avatar_url)
    await c.send(embed=helpEmb)

