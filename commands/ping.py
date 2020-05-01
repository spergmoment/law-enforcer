from datetime import datetime

async def run(**kwargs):
    # get the current time
    start = datetime.now()
    # send the client ping
    message = await kwargs['c'].send(f"Client Ping: {round(kwargs['client'].latency*1000)}")
    # then add the current time - the start time
    await message.edit(content=f"{message.content}\nAPI Ping: {round((datetime.now().microsecond-start.microsecond)/1000)}")
