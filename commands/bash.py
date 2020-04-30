import os

async def run(args, c, m, owneronly, ids):
    if not m.id in ids:
        return await c.send(owneronly)
    if not len(args) > 0:
        return await c.send("You must include bash code to execute!")
    try:
        # execute the bash code
        a = os.popen(" ".join(args))
        # read the result
        result = a.read()
        # and send it
        await c.send(result)
    except Exception as e:
        await c.send(str(e))