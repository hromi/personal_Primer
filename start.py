import sys
import asyncio,yaml,importlib
from Primer.Handlers import recorder_handler, button_handler, display_handler, mikroserver_handler, gesture_handler
from Primer.IO.Audio.Recorder import Recorder
from Primer.IO.Audio.Player import Player
from Primer.IO.Gesture import Gesture
from Primer.Student import Student
from Primer.Folio import Folio

class PersonalPrimer:
    def __init__(self):
        with open('primer.yaml', 'r') as file:
            self.config = yaml.safe_load(file)
        #if URL/filename not defined as first parameter, use lesson0 defined in primer.yaml
        if len(sys.argv)>1:
            self.config['lesson0']=sys.argv[1]

        self.display_driver=importlib.import_module("Primer.IO.EPD."+self.config['EPD']['driver'])
        self.queue=dict()

    async def start(self):
        #GPT4::The asyncio.Queue objects must be created in the same event loop where they are used.
        print("starting")
        self.queue={
                'button' : asyncio.Queue(),
                'display' : asyncio.Queue(),
                'gesture' : asyncio.Queue(),
                'mikroserver' : asyncio.Queue(),
                'student' : asyncio.Queue()
        }
        print("predisplay")
        self.display=self.display_driver.EInkDisplay(self)
        self.student=Student(self)
        print("pregesture")
        self.gesture=Gesture(self)
        print("prerecorder")
        self.recorder=Recorder(self)
        print("preplayer")
        self.player=Player(self)
        self.folio=Folio(self)

        self.loop = asyncio.get_running_loop() #necessary for executor loops in libraries like pyalsaaudio

        #hello world
        #await self.student.greeting()

        #we pass the main object to all handlers so that they can access it through pp. or self.pp
        await asyncio.gather(
            self.folio.load_exercise(),
            button_handler.handle_button(self),
            recorder_handler.handle_recorder(self),
            mikroserver_handler.handle_mikroserver(self),
            gesture_handler.handle_gesture(self),
            display_handler.handle_display(self),
            #feel free to add additional sensor/actuator handlers here
        )

asyncio.run(PersonalPrimer().start())

