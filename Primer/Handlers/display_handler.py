import os,asyncio

async def handle_display(pp):
    while True:
        message = await pp.queue['display'].get()
        if message:
            await pp.display.display_folio(message)

