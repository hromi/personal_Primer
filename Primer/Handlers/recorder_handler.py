import asyncio

async def handle_recorder(pp):
    while True:
        command = await pp.queue['button'].get()
        if command == "start":
            await pp.queue['display'].put({'t':"👂",'t_emoji':True})
            #print("Starting Recording...")
            #pp.student.new_session()
            await pp.recorder.start_recording(pp.folio.text)
        elif command == "stop":
            #await pp.queue['display'].put({"t":".."})
            #print("Stopping Recording...")
            await pp.recorder.stop_recording()
            # Save the buffer

