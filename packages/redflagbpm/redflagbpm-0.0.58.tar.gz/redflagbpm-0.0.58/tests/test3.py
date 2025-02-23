import sys
sys.path.append("../src")

import redflagbpm

bpm=redflagbpm.BPMService()

# def holaMundo(msg):
#     bpm.setAddress(msg)
#     bpm.service.notifyUser("redflag","Hola!","Desde python3 debug!")
#     bpm.reply("Hola Mundo!")

#bpm.register_handler("TEST/helloWorld.py",holaMundo)
bpm.register_handler("TEST/helloWorld.py","test.py")

bpm.start()

