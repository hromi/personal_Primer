import asyncio
import RPi.GPIO as GPIO

async def handle_button(pp):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pp.config['button']['gpio'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    pp.recorder.is_recording = False
    while True:
        button_state = GPIO.input(pp.config['button']['gpio'])
        if button_state == GPIO.LOW and not pp.recorder.is_recording:  # Button pressed
            pp.recorder.is_recording = True
            await pp.queue['button'].put("start")
            #await pp.queue['display'].put({'t':"Recording"})
            #pp.student.new_session()
            #await pp.recorder.start_recording("Hallo")
        elif button_state == GPIO.HIGH and pp.recorder.is_recording:  # Button released
            #print("BRELEASE")
            pp.recorder.is_recording = False
            #await pp.queue['display'].put({'t':"Waiting"})
            await pp.queue['button'].put("stop")
            #await pp.recorder.stop_recording()
        await asyncio.sleep(pp.config['button']['sleep_interval'])  # debounce time

