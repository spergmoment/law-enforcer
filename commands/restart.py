import subprocess

async def run(c, m, owneronly, ids, restart):
    if not m.id in ids:
        return await c.send(owneronly)
    await c.send("Restarting...")
    # runs the restart command, see constants
    subprocess.Popen(restart.split());