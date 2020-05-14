import os

no_docs = True
async def run(**kwargs):
    c = kwargs['c']
    if not kwargs['m'].id in kwargs['ids']:
        return await c.send(kwargs['owneronly'])
    if not len(kwargs['args']) > 0:
        return await c.send("You must include bash code to execute!")
    try:
        # execute the bash code
        a = os.popen(" ".join(kwargs['args']))
        # read the result
        result = a.read()
        # and send it
        await c.send(result)
    except Exception as e:
        await c.send(str(e))

