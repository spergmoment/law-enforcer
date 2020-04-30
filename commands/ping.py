from datetime import datetime

async def run(client, c):
    # get the current time
    start = datetime.now()
    # send the client ping
    message = await c.send(f"Client Ping: {round(client.latency*1000)}")
    # then add the current time - the start time
    await message.edit(content=f"Client Ping: {round(client.latency*1000)}\nAPI Ping: {round((datetime.now().microsecond-start.microsecond)/1000)}")