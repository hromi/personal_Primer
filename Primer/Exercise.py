import random,asyncio,json,os,subprocess
from urllib import request,parse
from Primer.Curriculum import Curriculum
from PIL import Image
class Exercise(Curriculum):
    exercise_modes={
            'read_test':{'audio':False,'img':False,'title':True,'body':False},
            'read_learn':{'audio':True,'img':True,'title':True,'body':False},
            'narrate_test':{'audio':False,'img':False,'title':True,'body':True},
            'narrate_learn':{'audio':True,'img':False,'title':True,'body':True},
            'naming_learn':{'audio':True,'img':True,'title':True,'body':False},
            'naming_test':{'audio':False,'img':True,'title':False,'body':False}
    }
    def __init__(self):
        self.image_path=self.pp.config['gfx']['image_path']
        self.wav_store_dir=self.pp.config['audio']['wav_store_dir']
        self.ogg_store_dir=self.pp.config['audio']['ogg_store_dir']
        self.max_trials=self.pp.config['student']['max_trials']
        self.exercise_matches={'learn':0,'test':0}
        self.exercise_mismatches={'learn':0,'test':0}
        self.task_matches={}
        self.task_mismatches={}
        self.loop = asyncio.new_event_loop()
        self.exercise_action=None
        self.title='name'
        self.scorer_id=None

    async def load_foliae(self,json_file=None):
        if not json_file:
            json_file=self.pp.config['lesson0']
        with open(json_file, 'r', encoding='utf-8') as file:
            self.all_foliae=json.load(file)
        self.current_folio = self.all_foliae[0]  # Start with the root folio
        self.scorer_id=self.current_folio["id"]
        self.path.append((self.current_folio,0))
        self.language=self.all_foliae[0]['language']
        self.primer_title=self.all_foliae[0]['primer_title']
        self.exercise_action=self.all_foliae[0]['exercise_action']
        await self.preload_imgs(self.current_folio)
        await self.preload_wavs(self.current_folio)
        await self.traverse_tree(self.current_folio)
      
        if "id" in self.current_folio:
            self.scorer_id=self.current_folio["id"]
        print("Lesson loaded")

    async def preload_wavs(self,folio):
        #print(folio['voices'])
        folio['wavs']=dict()
        if type(folio['voices']) is list:
            for variant in folio['voices']:
                wav_path=self.wav_store_dir+'/'+folio['id']+'-'+folio['name']+'-'+variant['voice']+".wav"
                if not os.path.isfile(wav_path):
                    ogg_path=self.ogg_store_dir+'/'+folio['id']+'-'+variant['voice']+".ogg"
                    #check the ogg cache
                    if not os.path.isfile(ogg_path):
                        print("downloadin"+str(variant['variant_id']))
                        print(self.pp.config['audio']['external_store_url']+str(variant['variant_id'])+".ogg")
                        request.urlretrieve(self.pp.config['audio']['external_store_url']+str(variant['variant_id'])+".ogg",ogg_path)
                    subprocess.run(['opusdec', '--rate', '48000', ogg_path, wav_path], check=True)
                folio['wavs'][variant['voice']]=wav_path


    async def preload_imgs(self,folio):
        if type(folio['imgs']) is list:
            #await self.pp.queue['display'].put({"t":folio['name']})
            for img in folio['imgs']:
                img_path=self.image_path+'/'+img
                if not os.path.isfile(img_path):
                    url=self.pp.config['gfx']['external_store_url']+'/'+parse.quote(img)
                    print("WTF",url)
                    request.urlretrieve(url,img_path)
                    image=Image.open(img_path)
                    resized=image.resize((600,800))
                    resized.convert('L').save(self.image_path+'/600x800/'+img)

    async def preload_folio(self,folio):
        #load images
        #print(folio["name"])
        await self.preload_imgs(folio)
        await self.preload_wavs(folio)

    # Recursive function to traverse the tree
    async def traverse_tree(self,folio):
        await self.preload_folio(folio)
        for child in folio.get("children", []):
            await self.traverse_tree(child)

    async def match(self,text):
        self.task_matches[self.current_folio['name']][self.pp.folio.task_action]+=1
        self.exercise_matches[self.pp.folio.task_action]+=1
        #start training after N trials defined in hmpl:training_trigger config variable
        if type(self.pp.folio.current_folio['imgs']) is list:
            #print(self.pp.folio.current_folio['imgs'])
            await self.pp.queue['display'].put({"t":text,"i":self.pp.folio.current_folio['imgs'][0],'b':' '})
        else:
            await self.pp.queue['display'].put({"b":text,"t":"🧸","t_emoji":True})
        #HMPL enters the game
        if self.pp.folio.task_action=='learn' and (self.exercise_matches['learn']+self.exercise_mismatches['learn']+1) % self.pp.config['hmpl']['training_trigger'] == 0:
            print("activating training")
            await self.pp.queue['display'].put({"t":"🧚","t_emoji":True})
            await self.loop.run_in_executor(None,self.pp.student.activate_training)

    async def mismatch(self,text):
        self.task_mismatches[self.current_folio['name']][self.pp.folio.task_action]+=1
        self.exercise_mismatches[self.pp.folio.task_action]+=1
        self.pp.folio.task_action='learn'
        self.trial+=1
        print("MISMATCH")
        #if self.current_folio['emoji']:
        #    await self.pp.queue['display'].put({"b":text.upper(),"t":self.current_folio['emoji'],"t_emoji":True})
        #else:
            #await self.pp.queue['display'].put({"b":text.upper(),"t":' '})
        print("FALSCH")
        await self.pp.queue['display'].put({"t":'Falsch ;('})
        if "wavs" in self.pp.folio.current_folio:
            #await self.pp.queue['display'].put({"b":text.upper()})
            await self.pp.player.play_wav(random.choice(self.pp.folio.current_folio['wavs']))
