

async def run(args, msg, g, c, m, botlower, userlower, botperms, userperms):
    if not g.me.guild_permissions.kick_members:
        return await c.send(botperms('kick members'))
    if not m.guild_permissions.kick_members:
        return await c.send(userperms('kick_members'))
    if not g.me.guild_permissions.create_instant_invite:
        return await c.send(botperms('create invites'))
    if not m.guild_permissions.create_instant_invite:
        return await c.send(userperms('create_instant_invite'))
    if not msg.mentions:
        return await c.send("Please provide a member to kick.")
    member = msg.mentions[0]
    reason = " ".join(args[1:len(args)]) or "None"
    if g.me.top_role < member.top_role:
        return await c.send(botlower)
    if m.top_role < member.top_role:
        return await c.send(userlower)
    inv = await c.create_invite(reason=f"Temporary invite for {member}", max_uses=1)
    try:
        try:
            await member.send(f"{member}, you have been **kicked** from {g} by {m}.\nReason: {reason}\nI have created a one-time invite for you to join back with: {inv}")
        except:
            pass
        await member.kick(reason=reason)
        await c.send(f"{m}, I have **kicked** {member}.\nReason: {reason}")
    except Exception as e:
        await c.send(f"Error while kicking user: {e}")