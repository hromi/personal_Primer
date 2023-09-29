class Folio:
    def __init__(self,pp):
        self.pp=pp
        self.text=pp.config['auth']['greeting']
        self.content=""
        self.imgs=[]
        self.current_folio = pp.all_folios[0]  # Start with the root folio
        self.scorer_id=self.current_folio["knot_id"]
        self.siblings = []
        self.path = [(self.current_folio,0)]
        self.sibling_index=0
    async def display_current_folio(self):
        #await self.display.display_folio(self.current_folio['name'],self.current_folio['imgs'][0])
        await self.pp.queue['display'].put({'t':self.current_folio['name'],'i':self.current_folio['imgs'][0]})
       
    async def activate_current_folio(self):
        self.text=self.current_folio['name'] #this will be changed later for either/or/and name/content
        
        if "knot_id" in self.current_folio:
            self.scorer_id=self.current_folio["knot_id"]

        # Stop any ongoing audio
        #await self.audio.stop_player()

        # Display content on eink
        await self.display_current_folio()

        # Play audio
        #if 'audio' in self.current_folio:
        #    await self.audio.play_wav(self.current_folio['audio'][0])

        # Execute associated code
        if 'code' in self.current_folio:
            self.execute_code(folio['code'])

 

