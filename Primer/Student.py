import os
import urllib.request
class Student:
    def __init__(self,pp):
        self.pp=pp
        self.login=pp.config['student']['default_login']
        self.hi=pp.config['auth']['hi']
        self.bye=pp.config['auth']['bye']
        self.audio_dir = pp.config['audio']['session_audio_dir']
        self.last_session_link = self.audio_dir+'/last'
        self.language=pp.config['default_language']
        self.trial=0
        self.max_trials=pp.config['student']['max_trials']
        print(self.last_session_link)
        self.new_session()

    async def logout(self):
        await self.pp.queue['display'].put({"c":f"{self.bye} {self.login}"})
        self.login=self.pp.config['student']['default_login']
        self.pp.folio.text=self.pp.config['auth']['hi']
        await self.pp.queue['display'].put({"c":self.pp.config['auth']['hi']})

    async def activate_training(self):
        contents = urllib.request.urlopen("https://"+self.pp.config['mikroserver_stt']['train_host']+"/"+self.language+"::"+self.login).read()

    def new_session(self):
        last_session=os.path.basename(os.path.realpath(self.last_session_link))
        self.session_id=str(int(last_session) + 1)
        new_session_dir=self.audio_dir+self.session_id
        os.mkdir(new_session_dir)
        os.unlink(self.audio_dir+'/last')
        os.symlink(new_session_dir,self.last_session_link,True)
        #self.logger.info('new session dir:' + new_session_dir)


