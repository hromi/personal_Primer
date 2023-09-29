import asyncio

async def handle_display(pp):
    while True:
        #print("handle_display")
        message = await pp.queue['display'].get()
        if message:
            #print(message)
            # Update the e-ink display
            if "i" in message:
                await pp.display.display_folio(message['t'],message['i'])
            else:
                await pp.display.display_folio(message['t'])

