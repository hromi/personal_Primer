from Primer.Exercise import Exercise

class Folio(Exercise):
    def __init__(self,pp):
        self.pp=pp
        self.text=pp.config['auth']['hi']
        self.content=""
        self.imgs=[]
        self.current_folio = None
        self.scorer_id=None
        self.siblings = []
        self.path = []
        self.sibling_index=0
        self.default_task_action="test"
        self.task_action=self.default_task_action
        self.trial=0
        super().__init__()

    async def descend(self):
        children = self.current_folio.get('children', [])
        if children:
            self.siblings=children
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
        print(self.current_folio['content'])
        #await self.display.display_folio(self.current_folio['name'],self.current_folio['imgs'][0])
        await self.pp.queue['display'].put({'c':self.current_folio['content']})
     
    async def display_current_folio_name(self):
        #await self.display.display_folio(self.current_folio['name'],self.current_folio['imgs'][0])
        await self.pp.queue['display'].put({'t':self.current_folio['name']})
       
    async def activate_current_folio(self):
        print(self.task_matches)
        print(self.exercise_matches)
        print(self.task_mismatches)
        print(self.exercise_mismatches)
        #reset variables related to old folio
        self.trial=0
        self.task_action=self.default_task_action

        if self.current_folio['name'] not in self.task_matches:
            self.task_matches[self.current_folio['name']]={'learn':0,'test':0}
            self.task_mismatches[self.current_folio['name']]={'learn':0,'test':0}

        # Stop any ongoing audio
        await self.pp.player.stop_player()
 
        if "id" in self.current_folio:
            self.scorer_id=self.current_folio["id"]
         
        exercise_mode=self.exercise_modes[self.exercise_action+'_'+self.task_action]
        self.text=self.current_folio['name'] #this will be changed later for either/or/and name/content
        print(exercise_mode) 
        # Display on eink
        if exercise_mode['name']:
            await self.pp.queue['display'].put({'t':self.current_folio['name']})
            #await self.display_current_folio_name()
        if exercise_mode['content']:
            #await self.display_current_folio_content()
            await self.pp.queue['display'].put({'c':self.current_folio['content']})
        if exercise_mode['img'] and 'img' in self.current_folio:
            await self.pp.queue['display'].put({'i':self.current_folio['img']})
        # Play audio
        if exercise_mode['audio'] and 'wavs' in self.current_folio:
            await self.pp.player.play_wav(self.current_folio['wavs'][0])

        # Execute associated code
        if 'code' in self.current_folio:
            self.execute_code(folio['code'])

