import discord, json, math, asyncio, ast, random, subprocess, os
from datetime import datetime

from constants.auth import token, prefix, game, ids
from constants.info import oauth, restart as restartcmd, staticinfo, endinfo
from constants.resp import botlower, userlower, owneronly, userperms, botperms
from constants.help import helpCmd

from commands import __dict__ as commands

client = discord.Client()

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
    pt = os.path.dirname(os.path.abspath(__file__))
    commandfiles = [f for f in os.listdir(f"{pt}/commands") if os.path.isfile(os.path.join(f"{pt}/commands", f))]
    if not f"{cmd}.py" in commandfiles or cmd == "__init__":
        return
    run = commands.get(cmd + "C")
    await run(args=args, msg=msg, client=client, g=g, c=c, m=m, botlower=botlower,
    userlower=userlower, botperms=botperms, userperms=userperms, owneronly=owneronly, ids=ids, 
    helpCmd=helpCmd, oauth=oauth, startTime=startTime, staticinfo=staticinfo, endinfo=endinfo, muted_role=muted_role, restartcmd=restartcmd)
    
# tries to login with the token
try:
    client.run(token)
# if it fails, print the error
except discord.errors.LoginFailure as err:
    print(f"Failed to login. Token: {token}\n{err}")
