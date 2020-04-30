

async def run(args, msg, g, c, m, botlower, userlower, botperms, userperms):
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