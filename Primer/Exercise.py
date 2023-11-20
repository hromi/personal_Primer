from Primer.Curriculum import Curriculum
class Exercise(Curriculum):
    exercise_modes={
            'read_test':{'audio':True,'img':False,'name':True,'content':False},
            'read_learn':{'audio':True,'img':True,'name':True,'content':False},
            'naming_learn':{'audio':True,'img':True,'name':True,'content':False},
            'naming_test':{'audio':False,'img':True,'name':False,'content':False}
    }
    exercise_action=None
    exercise_matches={'learn':0,'test':0}
    tasks={}
    max_trials=None
    trial=0

    async def match(self,text):
        self.tasks[text][self.pp.folio.task_action]+=1
        self.exercise_matches[self.pp.folio.task_action]+=1
        if self.exercise_matches['learn']>self.pp.config['hmpl']['training_trigger']:
            print("activating training")
            self.pp.student.activate_training()
        await self.pp.queue['display'].put({"t":text,"i":self.pp.folio.current_folio['imgs'][0]})

    async def mismatch(self,text):
        print("mismatch")
        self.pp.folio.task_action='learn'
        print(self.pp.folio.task_action)
        self.trial+=1
        if "audio" in self.pp.folio.current_folio:
            await self.pp.queue['display'].put({"t":text})
            await self.pp.player.play_wav(self.pp.folio.current_folio['audio'][0])
