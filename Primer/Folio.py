import random
from Primer.VoiceController import VoiceController
from Primer.Exercise import Exercise

class Folio(Exercise):
    def __init__(self,pp):
        self.pp=pp
        self.text=pp.config['auth']['hi']
        self.content=""
        self.imgs=[]
        self.current_folio = None
        self.current_voice = pp.config['voices']['default']
        self.scorer_id=None
        self.siblings = []
        self.path = []
        self.sibling_index=0
        self.default_task_action="learn"
        self.voice_control=None
        self.task_action=self.default_task_action
        self.trial=0
        self.title_text=None
        self.body_text=None
        self.image_name=None
        self.parent_name=None
        super().__init__()

    async def descend(self):
        children = self.current_folio.get('children', [])
        self.parent_name=self.current_folio['name']
        if children:
            self.siblings=children
            self.sibling_index=0
            # Move to the first child of the current folio
            # Push the current folio and index to the path
            self.path.append((self.current_folio, 0))
            self.current_folio = children[0]
            await self.activate_current_folio()


    async def ascend(self):
        print("ascending",self.path)
        if self.path:
            # Pop the last parent folio and index from the path
            #print(self.path[-1][0])
            #self.siblings=self.path[-1][0]['children']
            try:
                self.sibling_index=0
                self.current_folio, _ = self.path.pop()
                self.siblings=self.path[-1][0]['children']
                #self.siblings=self.path[-1]['children']
                await self.activate_current_folio()
            except:
                pass


    async def next_folio(self):
        if self.siblings:
            # Move to the next sibling folio
            self.sibling_index = (self.sibling_index + 1) % len(self.siblings)
            self.current_folio = self.siblings[self.sibling_index]
            await self.activate_current_folio()

    async def previous_folio(self):
        if self.siblings:
            # Move to the next sibling folio
            self.sibling_index = (self.sibling_index - 1) % len(self.siblings)
            self.current_folio = self.siblings[self.sibling_index]
            await self.activate_current_folio()

    async def display_current_folio_content(self):
        #print(self.current_folio['content'])
        await self.pp.queue['display'].put({'b':self.current_folio['content']})
     
    async def display_current_folio_name(self):
        await self.pp.queue['display'].put({'t':self.current_folio['name']})
   
    async def display_image(self):
        if self.current_folio['imgs']:
            await self.pp.queue['display'].put({'i':random.choice(self.current_folio['imgs'])})

    async def next_voice(self):
        self.current_voice=self.voice_control.next_voice()
        await self.pp.queue['display'].put({'f':self.current_voice,'f_emoji':True})
        await self.pp.player.stop_player()
        try:
            await self.pp.player.play_wav(self.current_folio['wavs'][self.current_voice])
        except:
            1

    async def activate_current_folio(self):
        #print(self.task_matches)
        #print(self.exercise_matches)
        #print(self.task_mismatches)
        #print(self.exercise_mismatches)
        #reset variables related to old folio
        self.trial=0
        if self.current_folio['task_action']:
            self.task_action=self.current_folio['task_action']
        else:
            self.task_action=self.default_task_action

        if self.current_folio['name'] not in self.task_matches:
            self.task_matches[self.current_folio['name']]={'learn':0,'test':0}
            self.task_mismatches[self.current_folio['name']]={'learn':0,'test':0}

        # Stop any ongoing audio
        await self.pp.player.stop_player()
        #print("WTF")
        #print(self.current_folio) 
        #print("WTFSTOP")
        self.voice_control=VoiceController(self.current_folio['wavs'],self.current_voice)
 
        #this should be rather done on exercise level
        #if "id" in self.current_folio:
        #    self.scorer_id=self.current_folio["id"]
         
        exercise_mode=self.exercise_modes[self.exercise_action+'_'+self.task_action]
        print(exercise_mode)
        self.text=self.current_folio['content'] if self.primer_title=='content' else self.current_folio['name'] #this will be changed later for either/or/and name/content
        # Display on eink
        if exercise_mode['title'] and self.primer_title!='none':
            if self.primer_title=='content':
                await self.pp.queue['display'].put({'t':self.current_folio['content'],'b':' '})
            elif self.primer_title=='parent':
                await self.pp.queue['display'].put({'t':self.parent_name})
            else:
                await self.pp.queue['display'].put({'t':self.current_folio['name'],'b':' '})
        if exercise_mode['body']:
            await self.pp.queue['display'].put({'b':self.current_folio['content']})
        #if exercise_mode['img'] and ('img' in self.current_folio or 'emoji' in self.current_folio):
        if exercise_mode['img']:
            print("IMAGE")
            if 'emoji' in self.current_folio:
                await self.pp.queue['display'].put({'t':self.current_folio['emoji'],'t_emoji':True,'b':' '})
            else:
                chosen_image=random.choice(self.current_folio['imgs'])
                print(chosen_image)
                await self.pp.queue['display'].put({'i':chosen_image})
        # Play audio
        if exercise_mode['audio'] and 'wavs' in self.current_folio:
            if self.current_voice in self.current_folio['wavs']:
                await self.pp.player.play_wav(self.current_folio['wavs'][self.current_voice])
            elif self.pp.config['voices']['default'] in self.current_folio['wavs']:
                await self.pp.player.play_wav(self.current_folio['wavs'][self.pp.config['voices']['default']])
            else:
                await self.next_voice()

        # Execute associated code
        if 'code' in self.current_folio:
            self.execute_code(folio['code'])

