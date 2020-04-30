import math, asyncio

async def unmute(m, t, r, role):
    await asyncio.sleep(t*60*60)
    if not muted_role in m.roles:
        return
    await m.remove_roles(role, reason=r)
    try:
        await m.send(f"You've been automatically unmuted in {m.guild}.")
    except:
        pass

async def run(args, msg, g, c, m, botlower, userlower, botperms, userperms, muted_role):
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
    if g.me.top_role < muted_role:
        return await c.send("I am at a lower level on the hierarchy than the muted role.")
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
        await unmute(mem, time, "Mute time expired", muted_role)
    except Exception as e:
        await c.send(f"Error while muting member: {e}")