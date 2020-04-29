import discord, json, math, asyncio, owner_ids, constants, ast, random, subprocess, os
from datetime import datetime

client = discord.Client()

token = constants.token
prefix = constants.prefix

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
    startTime = datetime.now()
    await client.change_presence(status=discord.Status.online, activity=constants.game)
    print("Successfully logged in.")


@client.event
async def on_message(msg):
    muted_role = False
    if msg.author.bot:
        return
    if not msg.content.startswith(prefix):
        return
    args = msg.content[len(prefix):len(msg.content)].strip().split(" ")
    cmd = args[0].lower()
    args.pop(0)
    c = msg.channel
    g = msg.guild
    m = msg.author
    if not muted_role: 
        for role in g.roles:
            if role.name.lower() == "muted":
                muted_role = role
                break
    if cmd == "ping":
        start = datetime.now()
        message = await c.send(f"Client Ping: {round(client.latency*1000)}")
        await message.edit(content=f"Client Ping: {round(client.latency*1000)}\nAPI Ping: {round((datetime.now().microsecond-start.microsecond)/1000)}")
    if cmd == "ban":
        if not g.me.guild_permissions.ban_members:
            return await c.send("I lack the permissions to ban members.")
        if not m.guild_permissions.ban_members:
            return await c.send("You must have the `BAN_MEMBERS` permission to do this.")
        if not msg.mentions:
            return await c.send("Please provide a member to ban.")
        member = msg.mentions[0]
        reason = " ".join(args[1:len(args)]) or "None"
        if g.me.top_role < member.top_role:
            return await c.send("I am at a lower level on the role hierarchy than this member.")
        if m.top_role < member.top_role:
            return await c.send("This member has a higher role than you.")
        try:
            try:
                await member.send(f"{member}, you have been **banned** from {g} by {m}.\nReason: {reason}")
            except:
                pass
            await member.ban(reason=reason)
            await c.send(f"{m}, I have **banned** {member}.\nReason: {reason}")
        except Exception as e:
            await c.send(f"Error while banning user: {e}")
    if cmd == 'unban':
        if not g.me.guild_permissions.ban_members:
            return await c.send("I lack the permissions to ban members.")
        if not m.guild_permissions.ban_members:
            return await c.send("You must have the `BAN_MEMBERS` permission to do this.")
        if len(args) < 1:
            return await c.send(f"Please enter a user ID to unban.\n"
            f"To get a user ID, enable **Developer Mode** in the **Appearance** tab in settings, then right-click the user and select **\"Copy ID.\"**")
        if math.isnan(int(args[0])):
            return await c.sned("Please enter a user ID to unban.")
        id = int(args[0])
        reason = None
        if len(args) < 2:
            reason = "None"
        else:
            reason = args[1]
        ban = None
        try:
            ban = await g.fetch_ban(id)
        except:
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
            return await c.send("I lack the permissions to kick members.")
        if not m.guild_permissions.kick_members:
            return await c.send("You must have the `KICK_MEMBERS` permission to do this.")
        if not msg.mentions:
            return await c.send("Please provide a member to kick.")
        member = msg.mentions[0]
        reason = " ".join(args[1:len(args)]) or "None"
        if g.me.top_role < member.top_role:
            return await c.send("I am at a lower level on the role hierarchy than this member.")
        if m.top_role < member.top_role:
            return await c.send("This member has a higher role than you.")
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
            return await c.send("I lack the permissions to mute members.")
        if not m.guild_permissions.mute_members:
            return await c.send("You must have the `MUTE_MEMBERS` permission to do this.")
        if not g.me.guild_permissions.kick_members:
            return await c.send("I lack the permissions to kick members.")
        if not m.guild_permissions.kick_members:
            return await c.send("You must have the `KICK_MEMBERS` permission to do this.")
        if not muted_role:
            return await c.send("No muted role exists. Please create one.")
        if not msg.mentions:
            return await c.send("Please mention a valid member.")
        mem = msg.mentions[0]
        if g.me.top_role < mem.top_role:
            return await c.send("I am at a lower level on the role hierarchy than this member.")
        if m.top_role < mem.top_role:
            return await c.send("This member has a higher role than you.")
        if muted_role in mem.roles:
            return await c.send("That member is already muted.")
        if not len(args) > 1:
            return await c.send("Please provide an amount of time to mute this user for.")
        if math.isnan(float(args[1])):
            return await c.send("Please provide a valid number.")
        reason = " ".join(args[2:len(args)]) or "None"
        time = float(args[1])
        try:
            await mem.add_roles(muted_role, reason=reason)
            await c.send(f"Successfully muted {mem} for {time} hours. Reason: {reason}")
            try:
                await mem.send(f"You've been muted in {g} by {m} for {time} hours.\nReason: {reason}")
            except:
                pass
            await unmute(mem, time, "Mute time expired", muted_role, m)
        except Exception as e:
            await c.send(f"Error while muting member: {e}")
    if cmd == "unmute":
        if not g.me.guild_permissions.mute_members:
            return await c.send("I lack the permissions to mute members.")
        if not m.guild_permissions.mute_members:
            return await c.send("You must have the `MUTE_MEMBERS` permission to do this.")
        if not g.me.guild_permissions.kick_members:
            return await c.send("I lack the permissions to kick members.")
        if not m.guild_permissions.kick_members:
            return await c.send("You must have the `KICK_MEMBERS` permission to do this.")
        if not muted_role:
            return await c.send("No muted role exists.")
        if not msg.mentions:
            return await c.send("Please mention a valid member.")
        mem = msg.mentions[0]
        if g.me.top_role < mem.top_role:
            return await c.send("I am at a lower level on the role hierarchy than this member.")
        if m.top_role < mem.top_role:
            return await c.send("This member has a higher role than you.")
        reason = " ".join(args[1:len(args)]) or "None"
        if not muted_role in mem.roles:
            return await c.send("This member is not muted.")
        await mem.remove_roles(muted_role, reason=reason)
        await c.send(f"Successfully unmuted {mem}.\nReason: {reason}")
    if cmd == "eval":
        if not m.id in owner_ids.ids:
            return await c.send("You must be a bot owner to use this command.")
        if not len(args) > 0:
            return await c.send("You must include code to eval!")
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
            exec(compile(parsed, filename="<ast>", mode="exec"), env)

            result = (await eval(f"{fn_name}()", env))
            await c.send(embed=emb.add_field(name="Returns", value=f"```py\n{result}```", inline=False))
        except Exception as err:
            emb.color = discord.Colour.red()
            await c.send(embed=emb.add_field(name="Error", value=f"```py\n{err}```", inline=False))
    
    if cmd == "clear":
        if not g.me.guild_permissions.manage_messages:
            return await c.send("I lack the permissions to manage members.")
        if not m.guild_permissions.manage_messages:
            return await c.send("You must have the `MANAGE_MESSAGES` permission to do this.")
        if not g.me.guild_permissions.read_message_history:
            return await c.send("I lack the permissions to clear messages.")
        if not m.guild_permissions.read_message_history:
            return await c.send("You must have the `READ_MESSAGE_HISTORY` permission to do this.")
        if len(args) < 1:
            amt = 20
        else:
            amt = int(args[0])
        if amt > 10000 or amt < 2:
            return await c.send("Please use a valid amount between 2 and 1000.")
        try:
            await c.purge(limit=amt+1)
            message = await c.send(f"Successfully cleared {amt} messages.")
            await message.delete(delay=3)
        except Exception as er:
            await c.send(f"Error while clearing messages: {er}")

    if cmd == "bash":
        if not m.id in owner_ids.ids:
            return await c.send("You must be a bot owner to use this command.")
        if not len(args) > 0:
            return await c.send("You must include bash code to execute!")
        try:
            a = os.popen(" ".join(args))
            result = a.read()
            await c.send(result)
        except Exception as e:
            await c.send(str(e))
    if cmd == "restart":
        if not m.id in owner_ids.ids:
            return await c.send("You must be a bot owner to use this command.")
        await c.send("Restarting...")
        subprocess.Popen("pm2 restart 3".split());
    if cmd == 'info':
        global startTime
        await c.send(f"```Owner: monkey#4097\nOwner ID: 694331934339498058\n"
        f"Running on: 5.6.3-arch1-1 x86_64 64 bit\nProcessors: 4 × Intel Core i5-3210M CPU @ 2.50GHz\nMemory: 7.7 GB\n"
        f"Current uptime: {round((datetime.now()-startTime).total_seconds())} seconds\nCurrent latency: {round(client.latency*1000)}```\n"
        f"Join the official support server: https://discord.gg/jsP2HY6")
    if cmd == "help":
        helpEmb = discord.Embed()
        if not len(args) > 0:
            helpEmb.set_author(name="Invite me here!", 
            url="https://discordapp.com/api/oauth2/authorize?client_id=696124534679535728&permissions=268561591&scope=bot", icon_url=client.user.avatar_url)
            helpEmb.title = "All commands"
            helpEmb.description = "Here is a list of all commands I have."
            helpEmb.add_field(
                name="ping", value="Get the current Client ping and API ping", inline=False)
            helpEmb.add_field(name="ban", value="Ban a user", inline=False)
            helpEmb.add_field(name="unban", value="Unban a user", inline=False)
            helpEmb.add_field(name="kick", value="Kick a user", inline=False)
            helpEmb.add_field(name="mute", value="Mute a user", inline=False)
            helpEmb.add_field(name="unmute", value="Unmute a user", inline=False)
            helpEmb.add_field(name="clear", value="Clear messages in a channel", inline=False)
            helpEmb.set_footer(text="Law Enforcer v0.5", icon_url=client.user.avatar_url)
        elif args[0] == "ping":
            helpEmb.title = "ping"
            helpEmb.description = "Grab the Client and API ping."
            helpEmb.add_field(name="Usage", value=f"\\{prefix}ping", inline=False)
            helpEmb.add_field(name="Extra Notes", value="Client ping is the hard Client latency, while the API ping is how long I take to respond.")
            helpEmb.add_field(name="Required Permissions", value="None")
        elif args[0] == "ban":
            helpEmb.title = "ban"
            helpEmb.description = "Ban a user from the server."
            helpEmb.add_field(name="Usage", value=f"\\{prefix}ban (user) (reason || None)", inline=False)
            helpEmb.add_field(name="Examples", value=f"\\{prefix}ban <@{owner_ids.ids[random.randint(0, 1)]}> dumb stupid\n\\{prefix}ban <@{owner_ids.ids[random.randint(0, 1)]}>", inline=False)
            helpEmb.add_field(name="Extra Notes", value="The user is DMed upon being banned.")
            helpEmb.add_field(name="Required Permissions", value="`BAN_MEMBERS`")
        elif args[0] == "kick":
            helpEmb.title = "kick"
            helpEmb.description = "Kick a user from the server."
            helpEmb.add_field(name="Usage", value=f"\\{prefix}kick (user) (reason || None)", inline=False)
            helpEmb.add_field(name="Examples", value=f"\\{prefix}kick <@{owner_ids.ids[random.randint(0, 1)]}> don't do that again\n\\{prefix}kick <@{owner_ids.ids[random.randint(0, 1)]}>", inline=False)
            helpEmb.add_field(name="Extra Notes", value=f"The user is DMed upon being kicked. Additionally, they are given a one-time invite to rejoin with."
            f"\nIn later versions, there will be options to disable this.")
            helpEmb.add_field(name="Required Permissions", value="`KICK_MEMBERS`")
        elif args[0] == "mute":
            helpEmb.title = "mute"
            helpEmb.description = "Mute a user for a certain amount of time."
            helpEmb.add_field(name="Usage", value=f"\\{prefix}mute (user) (time in hours) (reason || None)", inline=False)
            helpEmb.add_field(name="Example", value=f"\\{prefix}mute <@{owner_ids.ids[random.randint(0, 1)]}> 24 stop spamming\n\\{prefix}mute <@{owner_ids.ids[random.randint(0, 1)]}> 0.5", inline=False)
            helpEmb.add_field(name="Extra Notes", value="The user is DMed when they are muted.")
            helpEmb.add_field(name="Required Permissions", value="`MUTE_MEMBERS`\n`KICK_MEMBERS`")
        elif args[0] == "unmute":
            helpEmb.title = "unmute"
            helpEmb.description = "Unmute a user."
            helpEmb.add_field(name="Usage", value=f"\\{prefix}unmute (user) (reason || None)", inline=False)
            helpEmb.add_field(name="Examples", value=f"\\{prefix}unmute <@{owner_ids.ids[random.randint(0, 1)]}> said sorry in dms\n\\{prefix}unmute <@{owner_ids.ids[random.randint(0, 1)]}>", inline=False)
            helpEmb.add_field(name="Extra Notes", value="The user is DMed when unmuted.")
            helpEmb.add_field(name="Required Permissions", value="`MUTE_MEMBERS`\n`KICK_MEMBERS`")
        elif args[0] == "clear":
            helpEmb.title = "clear"
            helpEmb.description = "Clear a certain amount of messages."
            helpEmb.add_field(name="Usage", value=f"\\{prefix}clear (amount || 20)", inline=False)
            helpEmb.add_field(name="Examples", value=f"\\{prefix}clear 40\n\\{prefix}clear", inline=False)
            helpEmb.add_field(name="Extra Notes", value="You may clear as many messages as you want (up to 10000), but beware higher (>2000) values will be slow.")
            helpEmb.add_field(name="Required Permissions", value="`MANAGE_MESSAGES`\n`READ_MESSAGE_HISTORY`")
        elif args[0] == "unban":
            helpEmb.title = "unban"
            helpEmb.description = "Unban a banned user."
            helpEmb.add_field(name="Usage", value=f"\\{prefix}unban (user ID) (reason || None)", inline=False)
            helpEmb.add_field(name="Examples", value=f"\\{prefix}unban <@{owner_ids.ids[random.randint(0, 1)]}> is not dumb\n\\{prefix}unban <@{owner_ids.ids[random.randint(0, 1)]}>", inline=False)
            helpEmb.add_field(name="Extra Notes", value="The user is DMed upon being unbanned (If they can be DMed).")
            helpEmb.add_field(name="Required Permissions", value="`BAN_MEMBERS`")
        else:
            helpEmb.title = "Invalid command!"
            helpEmb.description = f"The command you entered, {args[0]}, is invalid."
            helpEmb.set_footer(text=f"Use {prefix}help for a list of commands.", icon_url=client.user.avatar_url)
        await c.send(embed=helpEmb)
def login():
    try:
        client.run(token)
    except discord.errors.LoginFailure as err:
        print(f"Failed to login. Token: {token}\n{err}")
login()
