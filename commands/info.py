from datetime import datetime

async def run(client, c, startTime, staticinfo, endinfo):
    # staticinfo and endinfo are used to shorten this a bit, see constants
    # the uptime is just the current total of seconds it's been up
    await c.send(f"{staticinfo}\nCurrent uptime: "
    f"{round((datetime.now()-startTime).total_seconds())} seconds\nCurrent latency: {round(client.latency*1000)}```\n{endinfo}")