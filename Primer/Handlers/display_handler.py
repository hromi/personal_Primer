import asyncio

async def handle_display(pp):
    while True:
        #print("handle_display")
        message = await pp.queue['display'].get()
        if message:
            if "i" in message and "t" in message:
                await pp.display.display_folio(message['t'],message['i'])
            elif "c" in message:
                await pp.display.display_content(message['c'])
            else:
                await pp.display.display_folio(message['t'])

