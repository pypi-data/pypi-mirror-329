import sys
sys.path.append("../src")

import redflagbpm

bpm=redflagbpm.BPMService()

def holaMundo(msg):
    bpm.__setAddress(msg)
    bpm.service.notifyUser("lbessone","Hola!","Desde python3!")
    bpm.reply("Hola Mundo!")

bpm.register_handler("testing.holaMundo",holaMundo)

print("Escuchando!")
bpm.start()
print("Finalizado!")
