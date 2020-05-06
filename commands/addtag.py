from datetime import datetime

async def run(**kwargs):
    g = kwargs['g']
    c = kwargs['c']
    m = kwargs['m']
    args = kwargs['args']
    conn = kwargs['conn']
    tags = kwargs['tags']
    if not g.me.guild_permissions.manage_guild:
        return await c.send(kwargs['botperms']('manage the server'))
    if not m.guild_permissions.manage_guild:
        return await c.send(kwargs['userperms']('manage_guild'))
    if len(args) < 1:
        return await c.send("Please provide a tag name.")
    if len(args) < 2:
        return await c.send("Please provide tag content.")
    tagname = args[0]
    tagcont = " ".join(args[1:len(args)])
    now = datetime.now()
    try:
        conn.execute(tags.insert(), [
            {'name': tagname, 'content': tagcont, 'creatortag': str(m), 
            'creatorid': m.id, 'createdat': f"{now.month}/{now.day}/{now.year}, at {now.hour}:{now.minute}",
            'guild': g.id}
        ])
        return await c.send(f"Successfully added tag {tagname}, with content:\n{tagcont}")
    except Exception as e:
        await c.send(f"This tag is already in the server.")
        print(e)
    