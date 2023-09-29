import os

class Student:
    def __init__(self,pp):
        self.pp=pp
        self.login=pp.config['student']['default_login']
        self.audio_dir = pp.config['audio']['session_audio_dir']
        self.last_session_link = self.audio_dir+'/last'
        print(self.last_session_link)
        self.new_session()

    def new_session(self):
        last_session=os.path.basename(os.path.realpath(self.last_session_link))
        self.session_id=str(int(last_session) + 1)
        new_session_dir=self.audio_dir+self.session_id
        os.mkdir(new_session_dir)
        os.unlink(self.audio_dir+'/last')
        os.symlink(new_session_dir,self.last_session_link,True)
        #self.logger.info('new session dir:' + new_session_dir)


