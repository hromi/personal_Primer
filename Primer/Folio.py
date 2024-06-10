import random
from Primer.ListController import ListController
from Primer.Exercise import Exercise
from PIL import Image,ImageDraw,ImageFont
import sys


class Folio(Exercise):
    def __init__(self, pp):
        self.pp = pp
        self.expected_utterance = pp.config['auth']['hi']
        self.content = ""
        self.imgs = []
        self.current_folio = None
        self.current_voice = pp.config['voices']['default']
        self.current_font = pp.config['gfx']['font']
        self.font_path = pp.config['gfx']['font_path']
        if pp.config['EPD']['front']:
            from waveshare_epd import epd5in65f
        self.last_child_index = {}
        self.scorer_id = None
        self.siblings = []
        self.path = []
        self.sibling_index = 0
        self.default_task_action = "learn"
        self.list_control = None
        self.task_action = self.default_task_action
        self.trial = 0
        self.title_text = None
        self.body_text = None
        self.image_name = None
        self.parent_name = None
        super().__init__()

    async def descend(self):
        """Move down to the previously visited child of the current folio, if any."""
        self.parent_name = self.current_folio['name']
        if children := self.current_folio.get('children', []):
            child_index = self.last_child_index.get(id(self.current_folio), 0)
            if child_index < len(children):
                self.path.append((self.current_folio, child_index))
                self.current_folio = children[child_index]
                await self.activate_current_folio()

    async def ascend(self):
        """Move up to the parent of the current folio, if not at the root."""
        if self.path:
            parent_folio, child_index = self.path.pop()
            #if self.path[-1]:
            if len(self.path):
                self.parent_name = self.path[-1][0]['name']
            self.last_child_index[id(parent_folio)] = child_index  # Update last visited child index
            self.current_folio = parent_folio
            await self.activate_current_folio()

    async def next_folio(self):
        """Move to the next sibling of the current folio, if possible."""
        if self.path:
            parent_folio, child_index = self.path[-1]
            if child_index + 1 < len(parent_folio['children']):
                self.path[-1] = (parent_folio, child_index + 1)
                self.current_folio = parent_folio['children'][child_index + 1]
                self.last_child_index[id(parent_folio)] = child_index + 1
                await self.activate_current_folio()

    async def previous_folio(self):
        """Move to the previous sibling of the current folio, if possible."""
        if self.path:
            parent_folio, child_index = self.path[-1]
            if child_index > 0:
                self.path[-1] = (parent_folio, child_index - 1)
                self.current_folio = parent_folio['children'][child_index - 1]
                self.last_child_index[id(parent_folio)] = child_index - 1
                await self.activate_current_folio()

    async def next_folio_old(self):
        if self.siblings:
            # Move to the next sibling folio
            #self.sibling_index = (self.sibling_index + 1) % len(self.siblings)
            self.sibling_index = (self.sibling_index + 1)
            if len(self.siblings) > self.sibling_index:
                self.current_folio = self.siblings[self.sibling_index]
                await self.activate_current_folio()
            else:
                await self.pp.queue['display'].put({'b':'das Ende'})
                if False and self.pp.config['EPD']['front'] and 'front' in self.current_folio and self.current_folio['front']:
                    if 'waveshare_epd' not in sys.modules:
                        from waveshare_epd import epd5in65f
                    epd = epd5in65f.EPD()
                    epd.init()
                    Himage = Image.open(self.pp.config['gfx']['image_path']+'/front/'+self.current_folio['front'])
                    epd.display(epd.getbuffer(Himage))
                    epd.sleep()

    async def previous_folio_old(self):
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
      
    async def display_parent_name(self):
        await self.pp.queue['display'].put({'t':self.current_folio['parent_name']})
      
    async def display_current_folio_full(self):
        print("FULLFOLIO")
        await self.pp.queue['display'].put({'t':self.parent_name,'b':self.current_folio['content']})
   
    async def display_image(self):
        if self.current_folio['imgs']:
            await self.pp.queue['display'].put({'i':random.choice(self.current_folio['imgs'])})

    async def next_font(self):
        self.current_font=self.list_control.next_font()
        await self.display_current_folio_full()
 
    async def next_voice(self):  # sourcery skip: do-not-use-bare-except
        try:
            self.current_voice=self.list_control.next_voice()
        except:
            1
        await self.pp.queue['display'].put({'f':self.current_voice,'f_emoji':True})
        await self.pp.player.stop_player()
        try:
            await self.pp.player.play_wav(self.current_folio['wavs'][self.current_voice])
        except:
            1

    async def activate_current_folio(self):
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
        self.list_control=ListController(self.font_path,self.current_folio['wavs'],self.current_voice,self.current_font)

        if self.source_scorer=='folio':
            self.scorer_id=self.current_folio["id"]

        #c.f. Exercise class for exercise mode dispatch table
        exercise_mode = self.exercise_modes[
            f'{self.exercise_action}_{self.task_action}'
        ]
        print("EXERCISE MODE:",exercise_mode)

        #this specifies what do we expect pupil to read
        self.expected_utterance=self.current_folio[self.source_utterance]

        # Display on eink
        if exercise_mode['title'] and self.primer_title!='none':
            print("PRIMER TITLE",self.primer_title)
            if self.primer_title=='content':
                await self.pp.queue['display'].put({'t':self.current_folio['content'],'b':' '})
            elif self.primer_title=='parent':
                print("PRIMERTITLE")
                await self.pp.queue['display'].put({'t':self.parent_name})
            else:
                await self.pp.queue['display'].put({'t':self.current_folio['name'],'b':' '})
        if exercise_mode['body']:
            await self.pp.queue['display'].put({'b':self.current_folio['content']})
        if exercise_mode['img']:
            if 'emoji' in self.current_folio:
                await self.pp.queue['display'].put({'b':self.current_folio['emoji'],'b_emoji':True,'t':' '})
            else:
                try:
                    chosen_image=random.choice(self.current_folio['imgs'])
                    #print(chosen_image)
                    await self.pp.queue['display'].put({'i':chosen_image})
                except:
                    print("NO IMG")
        # Play audio
        if exercise_mode['audio'] and 'wavs' in self.current_folio:
            if self.current_voice in self.current_folio['wavs']:
                await self.pp.player.play_wav(self.current_folio['wavs'][self.current_voice])
            elif self.pp.config['voices']['default'] in self.current_folio['wavs']:
                await self.pp.player.play_wav(self.current_folio['wavs'][self.pp.config['voices']['default']])
            elif len(self.current_folio['wavs']):
                await self.next_voice()

        # Execute associated code
        if 'code' in self.current_folio:
            self.execute_code(folio['code'])

