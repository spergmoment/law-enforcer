import discord

async def run(**kwargs):
    g = kwargs['g']
    c = kwargs['c']
    args = kwargs['args']
    conn = kwargs['conn']
    tags = kwargs['tags']
    if len(args) < 1:
        return await c.send("Please provide a tag to search for.")
    tagname = args[0]
    tagg = g.id
    s = tags.select().where(tags.c.name==tagname).where(tags.c.guild==tagg)
    result = conn.execute(s)
    try:
        row = result.fetchone()
        emb = discord.Embed()
        emb.title = f"Tag {row.name}"
        emb.description = row.content
        emb.add_field(name="Created By", value=f"{row.creatortag}\n{row.creatorid}", inline=False)
        emb.set_footer(text=row.createdat, icon_url = kwargs['client'].user.avatar_url)
        await c.send(embed=emb)
    except Exception as e:
        await c.send(f"That tag does not exist in this server.")
        print(e)