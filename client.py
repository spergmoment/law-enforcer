import discord, json, math, asyncio, ast, random, subprocess, os
from datetime import datetime

from constants.auth import token, prefix, game, ids
from constants.info import oauth, restart, staticinfo, endinfo
from constants.resp import botlower, userlower, owneronly, userperms, botperms
from constants.help import helpCmd

client = discord.Client()

# for eval
def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)
# used for threading timers
async def unmute(m, t, r, role, user):
    await asyncio.sleep(t*60*60)
    await m.remove_roles(role, reason=r)
    try:
        await m.send(f"You've been unmuted in {m.guild} by {user}.\nReason: {r}")
    except:
        pass


startTime = 0
@client.event
async def on_ready():
    global startTime
    # used for uptime
    startTime = datetime.now()
    await client.change_presence(status=discord.Status.online, activity=discord.Game(game))
    print("Successfully logged in.")


@client.event
async def on_message(msg):
    # initialize muted role
    muted_role = False
    # ignore bots
    if msg.author.bot:
        return
    # ignore messages not starting with our prefix
    if not msg.content.startswith(prefix):
        return
    # the actual arguments
    args = msg.content[len(prefix):len(msg.content)].strip().split(" ")
    # get the command
    cmd = args[0].lower()
    # remove the command from args
    args.pop(0)
    # used for shortening code
    c = msg.channel
    g = msg.guild
    m = msg.author
    # grabs the guild muted role
    if not muted_role: 
        for role in g.roles:
            if role.name.lower() == "muted":
                muted_role = role
                break
    if cmd == "ping":
        # get the current time
        start = datetime.now()
        # send the client ping
        message = await c.send(f"Client Ping: {round(client.latency*1000)}")
        # then add the current time - the start time
        await message.edit(content=f"Client Ping: {round(client.latency*1000)}\nAPI Ping: {round((datetime.now().microsecond-start.microsecond)/1000)}")
    if cmd == "ban":
        # checks bot perms, see constants
        if not g.me.guild_permissions.ban_members:
            return await c.send(botperms('ban members'))
        # checks user perms, see constants
        if not m.guild_permissions.ban_members:
            return await c.send(userperms('ban_members'))
        # checks for mentions
        if not msg.mentions:
            return await c.send("Please provide a member to ban.")
        # uses the first mention
        member = msg.mentions[0]
        # the reason, or "None"
        reason = " ".join(args[1:len(args)]) or "None"
        # checks role hierarchy, see constants
        if g.me.top_role < member.top_role:
            return await c.send(botlower)
        if m.top_role < member.top_role:
            return await c.send(userlower)
        # try block
        try:
            # try to tell the member they've been banned
            try:
                await member.send(f"{member}, you have been **banned** from {g} by {m}.\nReason: {reason}")
            # if it doesn't work, ignore it and move on
            except:
                pass
            await member.ban(reason=reason)
            await c.send(f"{m}, I have **banned** {member}.\nReason: {reason}")
        # if any error occurs, catch it and send it
        except Exception as e:
            await c.send(f"Error while banning user: {e}")
    if cmd == 'unban':
        if not g.me.guild_permissions.ban_members:
            return await c.send(botperms('ban members'))
        if not m.guild_permissions.ban_members:
            return await c.send(userperms('ban_members'))
        # checks the length of the args
        if len(args) < 1:
            return await c.send(f"Please enter a user ID to unban.\n"
            f"To get a user ID, enable **Developer Mode** in the **Appearance** tab in settings, then right-click the user and select **\"Copy ID.\"**")
        # makes sure its a number
        if math.isnan(int(args[0])):
            return await c.sned("Please enter a user ID to unban.")
        id = int(args[0])
        reason = " ".join(args[1:len(args)]) or "None"
        ban = None
        try:
            # fetch the ban for that id
            ban = await g.fetch_ban(id)
        except:
            # fetch_ban throws an exception if the user isn't banned, so catch it here to notify the user
            return await c.send("This user is not banned.")
        try:
            await g.unban(ban[0], reason=reason)
            await c.send(f"Successfully unbanned {ban[0]}.\nReason: {reason}")
            try:
                await ban[0].send(f"You have been **unbanned** in {g} by {m}.\nReason: {reason}")
            except:
                pass
        except Exception as e:
            await c.send(f"Error while unbanning user.\n{e}")
        
    if cmd == "kick":
        if not g.me.guild_permissions.kick_members:
            return await c.send(botperms('kick members'))
        if not m.guild_permissions.kick_members:
            return await c.send(userperms('kick_members'))
        if not msg.mentions:
            return await c.send("Please provide a member to kick.")
        member = msg.mentions[0]
        reason = " ".join(args[1:len(args)]) or "None"
        if g.me.top_role < member.top_role:
            return await c.send(botlower)
        if m.top_role < member.top_role:
            return await c.send(userlower)
        try:
            try:
                await member.send(f"{member}, you have been **kicked** from {g} by {m}.\nReason: {reason}")
            except:
                pass
            await member.kick(reason=reason)
            await c.send(f"{m}, I have **kicked** {member}.\nReason: {reason}")
        except Exception as e:
            await c.send(f"Error while kicking user: {e}")
    if cmd == "mute":
        if not g.me.guild_permissions.mute_members:
            return await c.send(botperms('mute members'))
        if not m.guild_permissions.mute_members:
            return await c.send(userperms('mute_members'))
        if not g.me.guild_permissions.kick_members:
            return await c.send(botperms('kick members'))
        if not m.guild_permissions.kick_members:
            return await c.send(userperms('kick_members'))
        # checks the muted role
        if not muted_role:
            return await c.send("No muted role exists. Please create one.")
        if not msg.mentions:
            return await c.send("Please mention a valid member.")
        mem = msg.mentions[0]
        if g.me.top_role < mem.top_role:
            return await c.send(botlower)
        if m.top_role < mem.top_role:
            return await c.send(userlower)
        # makes sure they aren't already muted
        if muted_role in mem.roles:
            return await c.send("That member is already muted.")
        if not len(args) > 1:
            return await c.send("Please provide an amount of time to mute this user for.")
        if math.isnan(float(args[1])):
            return await c.send("Please provide a valid number.")
        reason = " ".join(args[2:len(args)]) or "None"
        time = float(args[1])
        try:
            # add the muted role to the member
            await mem.add_roles(muted_role, reason=reason)
            await c.send(f"Successfully muted {mem} for {time} hours. Reason: {reason}")
            try:
                await mem.send(f"You've been muted in {g} by {m} for {time} hours.\nReason: {reason}")
            except:
                pass
            # goes to the unmute function, muting them for the specified time
            await unmute(mem, time, "Mute time expired", muted_role, m)
        except Exception as e:
            await c.send(f"Error while muting member: {e}")
    if cmd == "unmute":
        if not g.me.guild_permissions.mute_members:
            return await c.send(botperms('mute members'))
        if not m.guild_permissions.mute_members:
            return await c.send(userperms('mute_members'))
        if not g.me.guild_permissions.kick_members:
            return await c.send(botperms('kick members'))
        if not m.guild_permissions.kick_members:
            return await c.send(userperms('kick_members'))
        if not muted_role:
            return await c.send("No muted role exists.")
        if not msg.mentions:
            return await c.send("Please mention a valid member.")
        mem = msg.mentions[0]
        if g.me.top_role < mem.top_role:
            return await c.send(botlower)
        if m.top_role < mem.top_role:
            return await c.send(userlower)
        reason = " ".join(args[1:len(args)]) or "None"
        if not muted_role in mem.roles:
            return await c.send("This member is not muted.")
        await mem.remove_roles(muted_role, reason=reason)
        await c.send(f"Successfully unmuted {mem}.\nReason: {reason}")
    if cmd == "eval":
        # makes sure the user is the owner, check constants
        if not m.id in ids:
            return await c.send(owneronly)
        if not len(args) > 0:
            return await c.send("You must include code to eval!")
        # the following code is modified from https://gist.github.com/nitros12/2c3c265813121492655bc95aa54da6b9. go check that one out
        fn_name = "_eval_expr"

        cmd = " ".join(args).strip("` ")

        emb = discord.Embed()
        emb.add_field(name="Eval", value=f"```py\n{cmd}```", inline=False)
        emb.color = random.randint(0,16777215)

        # add a layer of indentation
        cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

        # wrap in async def body
        body = f"async def {fn_name}():\n{cmd}"

        parsed = ast.parse(body)
        body = parsed.body[0].body

        insert_returns(body)
        # environment for execution
        env = {
            'm': m,
            'g': g,
            'msg': msg,
            'c': c,
            'discord': discord,
            'math': math,
            'client': client
        }
        try:
            # eval the code
            exec(compile(parsed, filename="<ast>", mode="exec"), env)

            result = (await eval(f"{fn_name}()", env))
            await c.send(embed=emb.add_field(name="Returns", value=f"```py\n{result}```", inline=False))
        except Exception as err:
            emb.color = discord.Colour.red()
            await c.send(embed=emb.add_field(name="Error", value=f"```py\n{err}```", inline=False))
    
    if cmd == "clear":
        if not g.me.guild_permissions.manage_messages:
            return await c.send(botperms('manage messages'))
        if not m.guild_permissions.manage_messages:
            return await c.send(userperms('manage_messages'))
        if not g.me.guild_permissions.read_message_history:
            return await c.send(botperms('read message history'))
        if not m.guild_permissions.read_message_history:
            return await c.send(userperms('read_message_history'))
        if len(args) < 1:
            amt = 20
        else:
            amt = int(args[0])
        if amt > 10000 or amt < 2:
            return await c.send("Please use a valid amount between 2 and 10000.")
        try:
            # deletes the messages. it's +1 to handle the original message
            # discord.py purge actually can support over 100, unlike d.js and the api
            # it uses separate calls for >100 values
            await c.purge(limit=amt+1)
            message = await c.send(f"Successfully cleared {amt} messages.")
            # delete the sent message after 3 secs
            await message.delete(delay=3)
        except Exception as er:
            await c.send(f"Error while clearing messages: {er}")

    if cmd == "bash":
        if not m.id in ids:
            return await c.send(owneronly)
        if not len(args) > 0:
            return await c.send("You must include bash code to execute!")
        try:
            # execute the bash code
            a = os.popen(" ".join(args))
            # read the result
            result = a.read()
            # and send it
            await c.send(result)
        except Exception as e:
            await c.send(str(e))
    if cmd == "restart":
        if not m.id in ids:
            return await c.send(owneronly)
        await c.send("Restarting...")
        # runs the restart command, see constants
        subprocess.Popen(restart.split());
    if cmd == 'info':
        global startTime
        # staticinfo and endinfo are used to shorten this a bit, see constants
        # the uptime is just the current total of seconds it's been up
        await c.send(f"{staticinfo}\nCurrent uptime: "
        f"{round((datetime.now()-startTime).total_seconds())} seconds\nCurrent latency: {round(client.latency*1000)}```\n{endinfo}")
    if cmd == "help":
        # initialize an embed
        helpEmb = discord.Embed()
        # get 2 random ids from the owners
        id1 = f"<@{ids[random.randint(0, 1)]}>"
        id2 = f"<@{ids[random.randint(0, 1)]}>"
        # no args
        if not len(args) > 0:
            # set an author
            helpEmb.set_author(name="Invite me here!", url=oauth, icon_url=client.user.avatar_url)
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
            # set the footer
            helpEmb.set_footer(text="Law Enforcer v0.5", icon_url=client.user.avatar_url)
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
            f"\nIn later versions, there will be options to disable this.", "`KICK_MEMBERS`")
        elif args[0] == "mute":
            helpEmb = helpCmd(helpEmb, 'mute', "Mute a user for a certain amount of time.", '(user) (reason || None)', f"{id1} 24 stop spamming", f"{id2} 0.5",
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
        # no valid command? go here
        else:
            helpEmb.title = "Invalid command!"
            helpEmb.description = f"The command you entered, {args[0]}, is invalid."
            helpEmb.set_footer(text=f"Use {prefix}help for a list of commands.", icon_url=client.user.avatar_url)
        await c.send(embed=helpEmb)
# tries to login with the token
try:
    client.run(token)
# if it fails, print the error
except discord.errors.LoginFailure as err:
    print(f"Failed to login. Token: {token}\n{err}")
