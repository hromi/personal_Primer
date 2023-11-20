import asyncio
from Primer.Curriculum import Curriculum
class Exercise(Curriculum):
    exercise_modes={
            'read_test':{'audio':False,'img':False,'name':True,'content':False},
            'read_learn':{'audio':True,'img':True,'name':True,'content':False},
            'naming_learn':{'audio':True,'img':True,'name':True,'content':False},
            'naming_test':{'audio':False,'img':True,'name':False,'content':False}
    }
    def __init__(self):
        self.exercise_action=self.pp.all_folios[0]['exercise_action']
        self.max_trials=self.pp.config['student']['max_trials']
        self.lang=self.pp.all_folios[0]['lang']
        self.exercise_matches={'learn':0,'test':0}
        self.exercise_mismatches={'learn':0,'test':0}
        self.task_matches={}
        self.task_mismatches={}
        self.loop = asyncio.new_event_loop()

    async def match(self,text):
        self.task_matches[text][self.pp.folio.task_action]+=1
        self.exercise_matches[self.pp.folio.task_action]+=1
        #start training after N trials defined in hmpl:training_trigger config variable
        await self.pp.queue['display'].put({"t":text,"i":self.pp.folio.current_folio['imgs'][0]})
        #HMPL enters the game
        if self.pp.folio.task_action=='learn' and (self.exercise_matches['learn']+self.exercise_mismatches['learn']+1) % self.pp.config['hmpl']['training_trigger'] == 0:
            print("activating training")
            await self.pp.queue['display'].put({"t":"🧚","emoji":True})
            await self.loop.run_in_executor(None,self.pp.student.activate_training)

    async def mismatch(self,text):
        #print("mismatch")
        self.task_mismatches[text][self.pp.folio.task_action]+=1
        self.exercise_mismatches[self.pp.folio.task_action]+=1
        self.pp.folio.task_action='learn'
        print(self.pp.folio.task_action)
        self.trial+=1
        if "audio" in self.pp.folio.current_folio:
            await self.pp.queue['display'].put({"t":text})
            await self.pp.player.play_wav(self.pp.folio.current_folio['audio'][0])
