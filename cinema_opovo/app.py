# coding: utf-8
#
# Copyright 2009 Prima Tech Informatica Ltda.
#
# Licensed under the Environ License, Version 1.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.cmspublica.com.br/licenses/ENVIRON-LICENSE-1.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# app.py cinema_opovo
# modificado por Eric Mesquita em 01/10/2012
#
from publica.utils.BeautifulSoup import BeautifulSoup
from time import time, strftime, strptime
from publica.core.portal import Portal
from publica.admin.error import UserError
from publica.utils.json import encode
from publica.utils.decorators import serialize, dbconnectionapp,\
                                     Permission, logportal
from publica.admin.appportal import PortalUtils
from publica.admin.interfaces import BaseApp


from publica import settings
from public import Public
from adm import Adm

haslist = True
haslink = True
title = "Cinema"
meta_type = "cinema_opovo"


class App(BaseApp, PortalUtils, Adm, Public):
    """
    """
    title = title
    meta_type = meta_type
    haslist = haslist
    haslink = haslink


    def __init__(self, id_site, schema=None, request=None):
        """
        """
        self.id_site = id_site
        self.schema = schema
        self.request = request


    @dbconnectionapp
    def _install(self, title, 
                       rss_titulo=None, rss_link=None, rss_descricao=None,
                       rss_idioma=None, rss_categoria=None, rss_copyright=None,
                       rss_imagem_titulo=None, rss_imagem_link=None,
                       rss_imagem=None):
        """Adiciona uma instancia do produto
        """
        nid = str(time()).replace(".", "")
        if not self.schema:
            self.schema = "%s_%s" % (meta_type, nid)
        self.execSqlu("structure")
        portal = Portal(id_site=self.id_site,
                        request=self.request)
        user_dinamic = portal._getUserDinamic(id_site=self.id_site)
        if user_dinamic:
            self.execSqlu("permissions",
                          user=buffer(user_dinamic))

        if settings.USER_PERMISSION:
            for u in settings.USER_PERMISSION:
                self.execSqlu("permissions_admin",
                              user=buffer(u))

        rss = {"titulo":rss_titulo,
               "link":rss_link,
               "descricao":rss_descricao,
               "idioma":rss_idioma,
               "categoria":rss_categoria,
               "copyright":rss_copyright,
               "imagem_titulo":rss_imagem_titulo,
               "imagem_link":rss_imagem_link,
               "rss_imagem":rss_imagem}

        return {"rss":rss}


    @dbconnectionapp
    @serialize
    @Permission("ADM APP")
    def editApp(self, title, 
                       rss_titulo=None, rss_link=None, rss_descricao=None,
                       rss_idioma=None, rss_categoria=None, rss_copyright=None,
                       rss_imagem_titulo=None, rss_imagem_link=None,
                       rss_imagem=None):
        """Edita os atributos da instancia
        """
        rss = {"titulo":rss_titulo,
               "link":rss_link,
               "descricao":rss_descricao,
               "idioma":rss_idioma,
               "categoria":rss_categoria,
               "copyright":rss_copyright,
               "imagem_titulo":rss_imagem_titulo,
               "imagem_link":rss_imagem_link,
               "rss_imagem":rss_imagem}

        dados = {"rss":rss}
        portal = Portal(id_site=self.id_site, request=self.request)
        portal._editApp(env_site=self.id_site, 
                        schema=self.schema,
                        titulo=title, 
                        dados=dados)
        user_dinamic = portal._getUserDinamic(id_site=self.id_site)
        if user_dinamic:
            self.execSqlu("permissions",
                          user=buffer(user_dinamic))

        if settings.USER_PERMISSION:
            for u in settings.USER_PERMISSION:
                self.execSqlu("permissions_admin",
                              user=buffer(u))

        return "Aplicativo configurado com sucesso"


    @staticmethod
    def retornarWidgets():
        """ Retorna os itens para a listagem
        """
        return ({"action":"viewd",
                 "img":"/imgs/preview.gif",
                 "titulo":"Preview",
                 "url":"",
                 "target":""},
                {"action":"viewe",
                 "img":"/imgs/previewe.gif",
                 "titulo":"Publicado",
                 "url":"",
                 "target":""},
                {"action":"viewp",
                 "img":"/imgs/env.comment.png",
                 "titulo":"Coment&aacute;rios",
                 "url":"/app/listcomentapp.env",
                 "target":"edicao"},
                {"action":"viewp",
                 "img":"/imgs/env.comment.mod.png",
                 "titulo":"Modera&ccedil;&atilde;o",
                 "url":"/app/addcomentmod.env",
                 "target":"edicao"},
                {"action":"qrcode",
                 "img":"/imgs/qrcode.png",
                 "titulo":"Qrcode",
                 "url":""})


    @dbconnectionapp
    def _verifyStatusContent(self, id_conteudo):
        """
        """
        for i in self.execSql("select_status_content",
                              id_conteudo=int(id_conteudo)):
            return i["publicado"] 


    @dbconnectionapp
    def _setDados(self, id_conteudo):
        """
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)

        for i in self.execSql("select_filme_dados",
                              id_conteudo=int(id_conteudo)):

            tags = [j["tag"] for j in portal._getTags(
                                   id_site=self.id_site,
                                   id_conteudo=id_conteudo,
                                   schema=self.schema,
                                   text=None)]
            dados = {"genero":i["genero"],
                     "censura":i["censura"],
                     "status":i["status"],
                     "titulo":i["titulo"],
                     "titulo_original":i["titulo_original"],
                     "url_imdb":i["url_imdb"],
                     "descricao":i["descricao"],
                     "editor":i["editor"],
                     "corpo":i["corpo"],
                     "has_video":i["video"],
                     "has_audio":i["audio"],
                     "has_galeria":i["galeria"],
                     "data_edicao":i["data_edicao"],
                     "diretor":[],
                     "ator":[],
                     "cinema":[],
                     "foto":[],
                     "video":[],
                     "antesdepois":[],
                     "destaque":[],
                     "tags":tags}

            dados["destaque"].append({"titulo":i["titulo_destaque"],
                                      "descricao":i["descricao_destaque"],
                                      "img":i["imagem_destaque"]})

            for j in self.execSql("select_videos",
                                  id_conteudo=int(id_conteudo)):
                dados["video"].append(j)

            for j in self.execSql("select_filme_diretores",
                                  id_conteudo=int(id_conteudo)):
                dados["diretor"].append(j)

            for j in self.execSql("select_filme_atores",
                                  id_conteudo=int(id_conteudo)):
                dados["ator"].append(j)
                
            for j in self.execSql("select_filme_cinemas",
                                  id_conteudo=int(id_conteudo)):
                dados["cinema"].append(j)

            for j in self.execSql("select_filme_fotos",
                                  id_conteudo=int(id_conteudo)):
                dados["foto"].append({"arquivo":j["arquivo"],
                                      "arquivo_grande":j["arquivo_grande"],
                                      "alinhamento":j["alinhamento"],
                                      "credito":j["credito"],
                                      "legenda":j["legenda"],
                                      "descricao":j["descricao"],
                                      "link":j["link"]})

            for j in self.execSql("select_filme_fotos_ad",
                                  id_conteudo=int(id_conteudo)):
                dados["antesdepois"].append({"foto_antes":j["foto_antes"],
                                             "foto_depois":j["foto_depois"],
                                             "alinhamento":j["alinhamento"],
                                             "credito_antes":j["credito_antes"],
                                             "credito_depois":j["credito_depois"],
                                             "legenda":j["legenda"],
                                             "link":j["link"]})

            url = portal.getUrlByApp(env_site=self.id_site,
                                     schema=self.schema,
                                     id_conteudo=id_conteudo,
                                     exportar=1,
                                     admin=1,
                                     mkattr=1)

            return {"titulo":i["titulo"],
                    "meta_type":self.meta_type,
                    "id_conteudo":id_conteudo,
                    "publicado_em":i["publicado_em"],
                    "expira_em":i["expira_em"],
                    "atualizado_em":i["atualizado_em"],
                    "publicado":True if i["publicado"] else False,
                    "url":url,
                    "diretores":[i["nome"] for i in dados["diretor"]],
                    "atores":[i["nome"] for i in dados["ator"]],
                    "cinemas":[i["nome"] for i in dados["cinema"]],
                    "dados":dados
                    }

        return {}


    @dbconnectionapp
    def _getTitleDados(self, id_pk):
        """
        """
        for i in self.execSql("select_titulo",
                              id_conteudo=int(id_pk)):
            return {"title":i["titulo"]}


    @dbconnectionapp
    def _getDublinCore(self, id_pk):
        """
        """
        dados = {"title":"",
                 "created":"",
                 "modified":"",
                 "description":"",
                 "keywords":""}

        for i in self.execSql("select_dublin_core",
                              id_conteudo=int(id_pk)):

            portal = Portal(id_site=self.id_site,
                            request=self.request)

            tags = [j["tag"] for j in portal._getTags(id_site=self.id_site,
                                                      id_conteudo=int(id_pk),
                                                      schema=self.schema,
                                                      text=None)]
            tags = " ".join(tags)
            dados["title"] = i["titulo"]
            dados["created"] = i["publicado_em"]
            dados["modified"] = i["atualizado_em"]
            if i["descricao"]:
                dados["description"] = i["descricao"][:159]
            else:
                desc = ''.join(BeautifulSoup(i["corpo"],
                               fromEncoding=settings.GLOBAL_ENCODING).findAll(text=True))
                dados["description"] = unicode(desc[:159]).encode(settings.GLOBAL_ENCODING)
            dados["keywords"] = tags

        return dados 


    @dbconnectionapp
    def _getListContentRef(self):
        """
        """
        for i in self.execSql("select_conteudo"):
            serialized = self._setDados(i["id_conteudo"])
            i["serialized"] = serialized
            yield i


    @dbconnectionapp
    @serialize 
    @Permission("ADM SITE")
    def copyFiles2Temp(self, id_pk, id_site=None):
        """
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)

        fotos = self._getFotosSite(id_filme=id_pk)
        antesdepois = self._getFotosADSite(id_filme=id_pk)
        destaque = self._getDestaqueSite(id_filme=id_pk)

        for foto in fotos:
            if foto["arquivo"]:
                portal._copyFile2Temp(arq=foto["arquivo"],
                                      id_site=id_site)
            if foto["arquivo_grande"]:
                 portal._copyFile2Temp(arq=foto["arquivo_grande"],
                                       id_site=id_site)

        for item in antesdepois:
            if item["foto_antes"]:
                portal._copyFile2Temp(arq=item["foto_antes"],
                                      id_site=id_site)

            if item["foto_depois"]:
                portal._copyFile2Temp(arq=item["foto_depois"],
                                      id_site=id_site)

        if destaque:
          if destaque["img"]:
             portal._copyFile2Temp(arq=destaque["img"],
                                   id_site=id_site)

        return "Arquivos copiados com sucesso!" 


    @dbconnectionapp
    @logportal
    @Permission("PERM APP")
    def delConteudo(self, id_conteudo):
        """
        """
        titulo = ""
        for i in self.execSql("select_filme",
                              id_conteudo=int(id_conteudo)):
            titulo = i["titulo"]

        self.logmsg = "Filme '%s' deletado" % titulo
        self.execSqlu("delete_filme",
                      id_conteudo=int(id_conteudo))


    @dbconnectionapp
    def _addConteudo(self, id_treeapp, id_aplicativo, data):
        """
            dados = {"genero":i["genero"],
                     "censura":i["censura"],
                     "status":i["status"],
                     "titulo":i["titulo"],
                     "titulo_original":i["titulo_original"],
                     "url_imdb":i["url_imdb"],
                     "descricao":i["descricao"],
                     "editor":i["editor"],
                     "corpo":i["corpo"],
                     "has_video":i["video"],
                     "has_audio":i["audio"],
                     "has_galeria":i["galeria"],
                     "data_edicao":i["data_edicao"],
                     "diretor":[],
                     "ator":[],
                     "cinema":[],
                     "foto":[],
                     "video":[],
                     "destaque":[],
                     "tags":tags}

            {"titulo":i["titulo"],
                    "meta_type":self.meta_type,
                    "id_conteudo":id_conteudo,
                    "publicado_em":i["publicado_em"],
                    "expira_em":i["expira_em"],
                    "atualizado_em":i["atualizado_em"],
                    "url":url,
                    "diretores":[i["nome"] for i in dados["diretor"]],
                    "atores":[i["nome"] for i in dados["ator"]],
                    "cinemas":[i["nome"] for i in dados["cinema"]],
                    "dados":dados
                    }
        """
        data_publicado = strptime(data["publicado_em"], "%Y-%m-%d %H:%M")
        data_publicado = strftime("%d/%m/%Y %H:%M", data_publicado)
        # verify the genero
        id_genero = None
        for i in self.execSql("select_genero"):
            if i["nome"] == data["dados"]["genero"]:
                id_genero = i["id_genero"]
                break
        if not id_genero:
            raise UserError(("Nao foi possivel encontrar o "
                "genero.id_genero '{0}' "
                "no schema de destino.").format(data["dados"]["genero"]))
        # verify the censura
        id_censura = None
        for i in self.execSql("select_censura"):
            if i["nome"] == data["dados"]["censura"]:
                id_censura = i["id_censura"]
                break
        if not id_censura:
            raise UserError(("Nao foi possivel encontrar o "
                "censura.id_censura '{0}' "
                "no schema de destino.").format(data["dados"]["censura"]))
        # verify the status
        id_status = None
        for i in self.execSql("select_status"):
            if i["nome"] == data["dados"]["status"]:
                id_status = i["id_status"]
                break
        if not id_status:
            raise UserError(("Nao foi possivel encontrar o "
                "status.id_status '{0}' "
                "no schema de destino.").format(data["dados"]["status"]))

        id_conteudo = self.execSql("select_nextval_filme").next()["id"]
        publicado = True if data.get("publicado", 1) else False
        self.execSqlBatch("insert_filme",
                          id_conteudo=id_conteudo,
                          video=data["dados"]["has_video"],
                          audio=data["dados"]["has_audio"],
                          galeria=data["dados"]["has_galeria"],
                          titulo=data["dados"]["titulo"],
                          titulo_original=data["dados"]["titulo_original"],
                          url_imdb=data["dados"]["url_imdb"],
                          descricao=data["dados"]["descricao"],
                          id_genero=id_genero,
                          id_censura=id_censura,
                          id_status=id_status,
                          corpo=data["dados"]["corpo"],
                          publicado_em=data["publicado_em"],
                          expira_em=data["expira_em"],
                          publicado=publicado,
                          data_edicao=data["dados"]["data_edicao"],
                          editor=data["dados"]["editor"])

        # verify the diretor
        # FD.id_diretor, FD.id_conteudo, D.nome, D.url_imdb
        ndir = 0
        for i in data["dados"]["diretor"]:

            ndir += 1
            ldir = [i for i in self.execSql("select_diretor_unico_nome",
                                            nome=i["nome"])]
            if not ldir:
                id_diretor = self.execSql("select_nextval_diretor").next()["id"]
                self.execSqlu("insert_diretori",
                              id_diretor=id_diretor,
                              nome=i["nome"],
                              url_imdb=i["url_imdb"])
            else:
                id_diretor = ldir[0]["id_diretor"]

            self.execSqlBatch("insert_filme_diretor",
                              id_conteudo=id_conteudo,
                              id_diretor=int(id_diretor),
                              ordem=ndir)

        # verify the ator
        # FA.id_ator, FA.id_conteudo, A.nome, A.url_imdb
        nato = 0
        for i in data["dados"]["ator"]:

            nato += 1
            lato = [i for i in self.execSql("select_ator_unico_nome",
                                            nome=i["nome"])]
            if not lato:
                id_ator = self.execSql("select_nextval_ator").next()["id"]
                self.execSqlu("insert_atori",
                              id_ator=id_ator,
                              nome=i["nome"],
                              url_imdb=i["url_imdb"])
            else:
                id_ator = lato[0]["id_ator"]

            self.execSqlBatch("insert_filme_ator",
                              id_conteudo=id_conteudo,
                              id_ator=int(id_ator),
                              ordem=nato)
                              
        # verify the cinema
        # FC.id_cinema, FC.id_conteudo, FC.horarios, FC.legendado, FC.tresd, FC.ativo, C.nome, C.localizacao, C.endereco, C.fone
        ncin = 0
        for i in data["dados"]["cinema"]:

            ncin += 1
            lcin = [i for i in self.execSql("select_cinema_unico_nome",
                                            nome=i["nome"])]
            if not lcin:
                id_cinema = self.execSql("select_nextval_cinema").next()["id"]
                self.execSqlu("insert_cinemai",
                              id_cinema=id_cinema,
                              nome=i["nome"],
                              localizacao=i["localizacao"],
                              endereco=i["endereco"],
                              fone=i["fone"])
            else:
                id_cinema = lcin[0]["id_cinema"]

            self.execSqlBatch("insert_filme_cinema",
                              id_conteudo=id_conteudo,
                              id_cinema=int(id_cinema),
                              sala=i["sala"],
                              horarios=i["horarios"],
                              legendado=i["legendado"],
                              tresd=i["tresd"],
                              ativo=i["ativo"],
                              ordem=ncin)                              

        # verify the photos
        # {"arquivo_grande": "ns1/app/filme_129710078867/2012/02/04/2245/20120204191633504898u.jpeg",
        #  "credito": "teste", "link": "", "legenda": "teste legenda", 
        #  "arquivo": "ns1/app/filme_129710078867/2012/02/04/2245/20120204191611399082e.jpg",
        #  "alinhamento": "center"}
        for i in data["dados"]["foto"]:
            if i["arquivo"]:
                path = i["arquivo"]
                if not path.startswith("tmp/"):
                    path = "tmp/{0}/{1}".format(strftime("%Y%m%d"),
                                                     i["arquivo"].split("/")[-1])
                imagem = self._addFile(
                        arquivo=path,
                        id_conteudo=id_conteudo,
                        schema=self.schema,
                        dt=data_publicado)

                if not imagem:
                    continue

                imagemg = None
                if i["arquivo_grande"]:

                    path = i["arquivo_grande"]
                    if not path.startswith("tmp/"):
                        path = "tmp/{0}/{1}".format(strftime("%Y%m%d"),
                                                     i["arquivo_grande"].split("/")[-1])
                    imagemg = self._addFile(
                      arquivo=path,
                      id_conteudo=id_conteudo,
                      schema=self.schema,
                      dt=data_publicado)

                self.execSqlBatch("insert_foto_filme",
                                  id_conteudo=id_conteudo,
                                  arquivo=imagem,
                                  arquivo_grande=imagemg,
                                  alinhamento=i["alinhamento"],
                                  credito=i["credito"],
                                  legenda=i["legenda"],
                                  descricao=i.get("descricao", None),
                                  link=i["link"])

        # verify the antes-depois
        for i in data["dados"].get("antesdepois", []):

            foto_antes = None
            foto_depois = None

            if i["foto_antes"]:

                 path = i["foto_antes"]
                 if not path.startswith("tmp/"):
                     path = "tmp/{0}/{1}".format(strftime("%Y%m%d"),
                                               i["foto_antes"].split("/")[-1])

                 foto_antes = self._addFile(
                        arquivo=path,
                        id_conteudo=id_conteudo,
                        schema=self.schema,
                        dt=data_publicado)

            if not foto_antes:
                continue

            if i["foto_depois"]:

                 path = i["foto_depois"]
                 if not path.startswith("tmp/"):
                     path = "tmp/{0}/{1}".format(strftime("%Y%m%d"),
                                               i["foto_depois"].split("/")[-1])

                 foto_depois = self._addFile(
                        arquivo=path,
                        id_conteudo=id_conteudo,
                        schema=self.schema,
                        dt=data_publicado)

            self.execSqlBatch("insert_foto_filme_ad",
                              id_conteudo=id_conteudo,
                              foto_antes=foto_antes,
                              foto_depois=foto_depois,
                              alinhamento=i["alinhamento"],
                              credito_antes=i["credito_antes"],
                              credito_depois=i["credito_depois"],
                              legenda=i["legenda"],
                              link=i["link"])

        # verify the videos
        # [{"embed": "video 1", "id_video": 532}]
        for i in data["dados"]["video"]:
            self.execSqlBatch("insert_video",
                              id_conteudo=id_conteudo,
                              embed=i["embed"])

        # verify the destaque
        # [{"titulo": "titulo destaque", "img": "ns1/app/filme_129710078867/"
        #   "2012/02/04/2245/20120204191714495297a.png",
        #   "descricao": "descricao destaque"}]
        peso_destaque = None
        titulo_destaque = None
        descricao_destaque = None
        imagem_destaque = None
        for i in data["dados"]["destaque"]:

           imagem_destaque = None
           titulo_destaque = i["titulo"]
           descricao_destaque = i["descricao"]

           if i["img"]:
               path = i["img"]
               if not path.startswith("tmp/"):
                   path = "tmp/{0}/{1}".format(strftime("%Y%m%d"),
                                                   i["img"].split("/")[-1])
               imagem_destaque = self._addFile(
                      arquivo=path,
                      id_conteudo=id_conteudo,
                      schema=self.schema,
                      dt=data_publicado)

           self.execSqlBatch("insert_destaque",
                              id_conteudo=id_conteudo,
                              titulo=i["titulo"],
                              descricao=i["descricao"],
                              img=imagem_destaque,
                              peso=0)

        self.execSqlCommit()
        dados = self._setDados(id_conteudo=id_conteudo)
        self._addContentPortal(env_site=self.id_site,
                               id_pk=id_conteudo,
                               schema=self.schema,
                               meta_type=self.meta_type,
                               id_aplicativo=id_aplicativo,
                               id_treeapp=id_treeapp,
                               peso=peso_destaque,
                               titulo=data["dados"]["titulo"],
                               publicado=publicado,
                               publicado_em=data["publicado_em"],
                               expira_em=data["expira_em"],
                               titulo_destaque=titulo_destaque,
                               descricao_destaque=descricao_destaque,
                               imagem_destaque=imagem_destaque,
                               tags=" ".join(data["dados"].get("tags", [])),
                               permissao=[],
                               relacionamento=[],
                               dados=dados)
        return id_conteudo



