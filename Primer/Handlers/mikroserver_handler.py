import json
import asyncio
import websockets
from urllib.parse import quote

async def handle_mikroserver(pp):
    stt_config=pp.config['mikroserver_stt']
    auth_config=pp.config['mikroserver_auth']
    known_student = False if pp.student.login==pp.config['student']['default_login'] else True
    
    while True:
        message=await pp.queue['mikroserver'].get()
        if message:
            #print(message)
            text=message['t']
            audio_file=message['f']
            await pp.queue['display'].put({'t':"..."})
            #not yet logged in
            if not known_student:
                uri="wss://"+auth_config["auth_host"]+":"+auth_config['port']+"/auth/"+quote(pp.folio.text)+"/"+pp.student.login+"/"
            else:
                #uri="wss://"+stt_config['host']+":"+stt_config['port']+"/stt/"+str(pp.folio.scorer_id)+"/"+quote(pp.folio.text)+"/"+pp.student.login+"/de/0"
                uri="wss://"+stt_config['inference_host']+":"+stt_config['port']+"/hmpl/"+str(pp.folio.scorer_id)+"/"+quote(pp.folio.text)+"/"+pp.student.login+"/de/"+pp.folio.action+"/"+str(pp.student.trial)
            #print(uri)
            async with websockets.connect(uri) as ws:
                with open(audio_file, mode='rb') as file:  # b is important -> binary
                    await ws.send(file.read())
                try:
                    result =  await ws.recv()
                    response=json.loads(result)
                    if not known_student:
                        if json.loads(result)['login']:
                            pp.student.login=response['login']
                            await pp.queue['display'].put({"t":text+" "+pp.student.login})
                            known_student=True
                    else:
                        #print(response)
                        if ('text' in response) and (response['text'] == text.lower()):
                            #print("correct")
                            #await pp.queue['display'].put({"t":text+" ;)"})
                            pp.folio.action='test'
                            pp.student.trial=0
                            await pp.queue['display'].put({"t":text,"i":pp.folio.current_folio['imgs'][0]})

                        #if stuck, move to new folio
                        elif pp.student.trial > pp.student.max_trials:
                            print("max_trials exceeded")
                            await pp.folio.next_folio()
                
                        elif "text" not in response or response['text'] is not text.lower():
                            #print("false")
                            pp.folio.action='learn'
                            pp.student.trial+=1
                            if "audio" in pp.folio.current_folio:
                                await pp.queue['display'].put({"t":text})
                                await pp.player.play_wav(pp.folio.current_folio['audio'][0])
                            #await pp.queue['display'].put({"t":text+" ;("})

                except Exception as e:
                    print(e)
