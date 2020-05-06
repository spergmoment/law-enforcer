async def run(**kwargs):
    g = kwargs['g']
    c = kwargs['c']
    args = kwargs['args']
    conn = kwargs['conn']
    tags = kwargs['tags']
    if len(args) < 1:
        return await c.send("Please provide a tag.")
    tagname = args[0]
    tagg = g.id
    s = tags.select().where(tags.c.name==tagname).where(tags.c.guild==tagg)
    result = conn.execute(s)
    try:
        row = result.fetchone()
        return await c.send(row.content)
    except Exception as e:
        await c.send(f"That tag does not exist in this server.")
        print(e)