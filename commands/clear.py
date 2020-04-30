async def run(args, g, c, m, botperms, userperms):
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