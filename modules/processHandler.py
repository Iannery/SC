from modules.genKeys import KeyGenerator
from modules.sign import SignHandler
from modules.verify import VerifyHandler
class ProcessHandler:
    def __init__(self):
        self.genKeys = KeyGenerator()
        self.sign = SignHandler()
        self.verify = VerifyHandler()
        pass
    
    def run(self):
        self.genKeys.run()
        with open('message.txt', 'r+') as messageFile:
            msg_list = messageFile.read().splitlines()
        msg = ""
        for i in msg_list:
            msg += i
        
        signature = self.sign.run(msg)
        self.verify.run(msg, signature)
        pass