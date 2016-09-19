from facebot import usr_api
import datetime

thalison = usr_api(token='',v='2.7')

relogio = datetime.datetime.now()
hora = relogio.hour

bom_dia = hora >= 0 and hora <= 12
boa_tarde = hora >= 12 and hora <= 18
boa_noite = hora >= 18 and hora <= 23

msg = {}

msg['bom dia! '] = bom_dia
msg['boa tarde! '] = boa_tarde
msg['boa noite! '] = boa_noite

githubrepositorio = 'https://www.github.com/thalisonwilker/facebot'

for x in msg:
    if msg[x]:
        status = x+"""
        conheça o facebot, meu robozinho que cuida do meu face.
        """+githubrepositorio
        thalison.postar(status=status)


