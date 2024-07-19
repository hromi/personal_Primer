import json
import asyncio
import websockets
from urllib.parse import quote

async def handle_mikroserver(pp):
    stt_config=pp.config['mikroserver_stt']
    auth_config=pp.config['mikroserver_auth']

    while True:
        message=await pp.queue['mikroserver'].get()
        if message:
            #print(message)
            text=message['t']
            audio_file=message['f']
            await pp.queue['display'].put({'t':"🤔",'t_emoji':True})
            #not yet logged in ? use the voice identification model
            student_known = pp.student.login != pp.config['student']['default_login']
            #if not student_known:
            #    uri = f"wss://{auth_config['auth_host']}:{auth_config['port']}/auth/{quote(pp.folio.expected_utterance)}/{pp.student.login}/"
            #    print(uri)
            #otherwise do speech recognition
            if 1:
            #else:
                uri = f"wss://{stt_config['inference_host']}:{stt_config['port']}/hmpl/{pp.folio.scorer_id}/{quote(pp.folio.expected_utterance)}/{pp.student.login}/{pp.folio.language}/{pp.folio.task_action}/{pp.folio.trial}"
            try:
                async with websockets.connect(uri) as ws:
                    with open(audio_file, mode='rb') as file:  # b is important -> binary
                        await ws.send(file.read())
                    result =  await ws.recv()
                    response=json.loads(result)
                    #print(response)
                    #print(text)
                    if not student_known:
                        if json.loads(result)['login']:
                            await pp.student.init_user(response['login'])
                            student_known=True
                        else:
                            await pp.queue['display'].put({"b":pp.config['auth']['hi'],"t_emoji":"🔁"})
                    else:
                        if ('text' in response) and (response['text'] == text.lower()) or response['score']:
                            await pp.folio.match(text,response)
                        #if stuck, move to new folio
                        elif pp.folio.trial > pp.folio.max_trials:
                            await pp.folio.next_folio()
                        elif "text" not in response or response['text'] is not text.lower():
                            await pp.folio.mismatch(text)

            except Exception as e:
                print(e)
