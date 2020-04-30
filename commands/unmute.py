

async def run(args, msg, g, c, m, botlower, userlower, botperms, userperms, muted_role):
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
    if g.me.top_role < muted_role:
        return await c.send("I am at a lower level on the hierarchy than the muted role.")
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
    try:
        await mem.send(f"You've been unmuted in {g} by {m}.\nReason: {reason}")
    except:
        pass