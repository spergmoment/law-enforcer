import subprocess

async def run(**kwargs):
    if not kwargs['m'].id in kwargs['ids']:
        return await kwargs['c'].send(kwargs['owneronly'])
    await kwargs['c'].send("Restarting...")
    # runs the restart command, see constants
    try:
        exit()
    except:
        pass
