# -*- coding: latin1 -*-

import requests
import json
import sys
"""
Olá!
Facebot é uma proposta para melhorar o atendimento de pequenas e medias empresas ao publico
usando a API GRAPH do Facebook, podemos automatizar ações comuns de usuário, agilizando o precesso de atendimento
O Facebot também conta com o monitoramento de páginas, grupos e perfil, isso para evitar os 'tempos mortos' e
gerar respostas em tempo real!
Inicialmente o prejeto conta as seguinetes funcionalidades:

                   |--> atualiza status
          [ POST ] |--> cometa obejtos --> comenta e reponde a comentarios
          |        |--> curte objetos
          |
metodo----[ GET ]  |--> retorna postagem no feed
          |        |--> retorna comentários
          |        |--> retorna todas as curtidas em objetos
          |
          [ DELETE] |--> remove qualquer objeto



LINKS UTEIS, ou nao:
ACCESS_TOKEN = https://developers.facebook.com/tools/explorer/
COMO USAR O GRAPH API = https://developers.facebook.com/docs/graph-api/using-graph-api/#fieldexpansion
JSON = http://www.json.org/ se dormir ele te mata
follow me{
Twitter = @noxix666
facebook = fb/itkcah
}
"""
class usr_api(object):
    token = ''
    __v = ['2.1','2.2','2.3','2.4','2.5','2.6','2.7']
    v = ''
    no = 'me'
    bordas = ''
    campos = ''
    __url = 'https://graph.facebook.com/'
    
    def __init__(self,token='necessario em toda chamada de uma API,seja para receber ou enviar dados',v='2.7'):
        self.token = token

        if v not in self.v:
            msg = "sem suporte para versao "+v
            sys.stderr.write(msg)
            print
            return  0

        self.v = v
        access_token = 'access_token='+self.token
        self.__url = 'https://graph.facebook.com/v'+v+"/"+self.no+"?"+access_token
        """inicia o bot com o token de acesso e a versão da api"""

    def hello_wolrd(self):
        """considerado o metodo mais basido da API, apenas retorna seus dados comuns"""
        access_token = 'access_token='+self.token
        self.__url = 'https://graph.facebook.com/v2.7/'+self.no+"?"+self.bordas+"&"+access_token

        return self.__requests__(method='get')

    def __requests__(self,method,data=''):
        """ motor de processamento das requisições """
        try:
            if method.lower() == 'post':
                resp = requests.post(url=self.__url,data=data)
                dados = json.loads(resp.text)
                
            elif method.lower() == 'get':
                resp = requests.get(url=self.__url)
                dados = json.loads(resp.text)
                
            elif method.lower() == 'delete':
                resp = requests.delete(url=self.__url)
                dados = json.loads(resp.text)
            else:
                pass

            if 'error' in dados:
                """ erro ao tentar acessar a API, a falha e processada e exibida"""
                msg = dados['error']['message']
                code = dados['error']['code']
                tipo = dados['error']['type']

                print
                e = "-"*20
                sys.stderr.write(e+" FALHA "+e)
                print
                sys.stderr.write("mensagem: "+msg)
                print
                sys.stderr.write("code: "+str(code))
                print
                sys.stderr.write("tipo: "+tipo)
                print                
                sys.stderr.write(e+" END "+e)
                sys.exit(0)
                
            return dados
        
        except Exception, e:
            print e

    def minhas_fotos(self):
        """forna somente seus albums, quem quiser implementar um bkp fique a vontade"""
        self.bordas = 'albums'
        self.no = 'me'
        albums = {}
        access_token = 'access_token='+self.token
        """ toda chamada a qualquer metodo do bot é feita uma adaptação da url"""
        self.__url = 'https://graph.facebook.com/v'+self.v+"/"+self.no+"/"+self.bordas+"?"+access_token
        
        data = self.__requests__(method='get')

        for album in data['data']:
            albums[album['id']] = album['name']

        return albums

    """ retorna a lista de albums e seus respctivos ids"""


    def postar(self,status,no='me',borda='feed'):
        """ atualiza o status com um texto, retorna o object id"""
        access_token = 'access_token='+self.token
        self.bordas = borda
        data = {'message':status}
        
        self.no = no
        
        self.__url = 'https://graph.facebook.com/v'+self.v+"/"+self.no+"/"+self.bordas+"?"+access_token

        return self.__requests__(method='post',data=data)
    
    def curtir(self,no):
        """ recebe um id e curte, retorna o id da ação """
        access_token = 'access_token='+self.token
        self.__url = 'https://graph.facebook.com/v'+self.v+"/"+no+"/likes?"+access_token
        
        return self.__requests__(method='post')
    
    def deslike(self,no):
        """ removo curtidas eu um obejct id """
        access_token = 'access_token='+self.token
        self.__url = 'https://graph.facebook.com/v'+self.v+"/"+no+"/likes?"+access_token
        
        return self.__requests__(method='delete')
    
    def delete(self,no):
        """ recebe um id, removo o no do grafo, retorna o staus da ação"""
        access_token = 'access_token='+self.token
        self.no = no
        self.__url = 'https://graph.facebook.com/v'+self.v+"/"+self.no+"/?"+access_token

        return self.__requests__(method='delete')
    
    def get_comments(self,object_id, responder_todos=False,message='Obrigado!'):
        """ recebe um id e retorna a lista de comentários, responde todos de ums vez, caso seja passado True no resp.todos com a msg"""
        self.no = object_id
        self.bordas = 'comments'
        access_token = 'access_token='+self.token
        
        self.__url = 'https://graph.facebook.com/v'+self.v+"/"+self.no+"/"+self.bordas+"?"+access_token
        
        if responder_todos:
            
            data = self.__requests__(method='get')
            
            for c in data['data']:
                resp = self.comentar(c['id'],comentario=message)
                print resp
        else:
            return self.__requests__(method='get')

    def comentar(self, object_id,comentario=""):
        """ comenta em um post - no, recebe um id e retorna o do comentarios """
        self.bordas = 'comments'
        return self.postar(no=object_id,status=comentario,borda=self.bordas)

    def me_feed(self,limit=5):
        """ recebe os metadados do feed pessoal, com limit default de 5 postagem"""
        self.no = 'me'
        self.bordas = 'feed?limit='+str(limit)
        access_token = 'access_token='+self.token
        self.__url = 'https://graph.facebook.com/v'+self.v+"/"+self.no+"/"+self.bordas+"&"+access_token
        
        return self.__requests__(method='get')