import os
import urllib.request
class Student:
    def __init__(self,pp):
        self.pp=pp
        self.login=pp.config['student']['default_login']
        self.name=''
        self.hi=pp.config['auth']['hi']
        self.bye=pp.config['auth']['bye']
        self.language=pp.config['default_language']
        self.new_session()


    def set_session_info(self):
        self.session_dir = self.pp.config['student']['session_dir']+'/'+self.login
        self.last_session_link = self.session_dir+'/last'

    async def greeting(self):
        #await self.pp.queue['display'].put({"b":self.hi})
        await self.pp.player.stop_player()
        await self.pp.queue['display'].put({"b":self.hi,"t":" "})
        await self.pp.player.play_wav(self.pp.config['assets_dir']+self.hi+'.wav')

    def convert_login(self,login):
        # Split the login into first name and surname
        parts = login.split('-')
        # Capitalize the first letter of each part and join them with a space
        self.name = ' '.join(part.capitalize() for part in parts)

    async def init_user(self,login):
        self.login=login
        self.convert_login(login)
        #self.set_session_info()
        self.new_session()
        await self.pp.queue['display'].put({'b':self.pp.config['auth']['hi']+" "+self.name,'t':' '})
        self.activate_model()
        print("ACTIVATIN ROOT FOLIO")
        self.pp.folio.current_folio=self.pp.folio.all_foliae[0]
        print(self.pp.folio.current_folio)
        await self.pp.folio.activate_current_folio()

    async def logout(self):
        await self.pp.player.stop_player()
        await self.pp.queue['display'].put({"b":f"{self.bye} {self.login}","t":" "})
        self.login=self.pp.config['student']['default_login']
        self.set_session_info()
        #self.new_session()
        self.pp.folio.expected_utterance=self.pp.config['auth']['hi']
        await self.pp.queue['display'].put({'b':self.pp.config['auth']['hi']})
    
    def activate_model(self):
        urllib.request.urlopen("https://"+self.pp.config['mikroserver_stt']['inference_host']+":"+self.pp.config['mikroserver_stt']['port']+'/update_model/?voice='+self.login+'&lang='+self.language)

    def activate_training(self):
        #launch fine-tuning
        contents = urllib.request.urlopen("https://"+self.pp.config['mikroserver_stt']['train_host']+"/"+self.language+"::"+self.login).read()
        #inform the inference engine that model was updated
        self.activate_model()

    #sessions are stored in student directories, symlink /last points to last session
    def new_session(self):
        self.set_session_info()
        print("new session")
        last_session=os.path.basename(os.path.realpath(self.last_session_link))
        try:
            self.session_id=str(int(last_session) + 1)
            os.unlink(self.last_session_link)
        except:
            self.session_id="0"
        new_session_dir=self.session_dir+"/"+self.session_id
        os.makedirs(new_session_dir,exist_ok=True)
        #print(new_session_dir)
        #print(self.last_session_link)
        os.symlink(new_session_dir,self.last_session_link,True)
