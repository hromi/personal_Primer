import asyncio

async def handle_display(pp):
    while True:
        message = await pp.queue['display'].get()
        if message:
            await pp.display.clear_content()
            if "t" in message:
                if 'emoji' in message:
                    await pp.display.display_title(message['t'],emoji=True)
                else:
                    await pp.display.display_title(message['t'])
                #if not "i" in message and not "c" in message:
                #await pp.display.clear_content()
            if "i" in message:
                #await pp.display.clear_content()
                await pp.display.display_image(message['i'])
                #if not "t" in message:
                #    await pp.display.clear_title()
            if "c" in message:
                await pp.display.display_content(message['c'])
                if not "t" in message:
                    await pp.display.clear_title()
 

