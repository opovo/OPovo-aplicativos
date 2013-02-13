# coding: utf-8
#
# Copyright 2009 Prima Tech Informatica LTDA.
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
# adm.py cinema_opovo
# modificado por Eric Mesquita em 01/10/2012
#
from time import time, strftime, strptime
from urllib import unquote
from publica.admin.error import UserError
from publica.utils.json import encode
from publica.utils.decorators import serialize, dbconnectionapp,\
                                     Permission

class Adm(object):
    """
        methods of the administration crud:
            . news types
            . autores
            . news
    """
    
    @dbconnectionapp
    def _getSessoesBusca(self):
        """
            returns all sessoes para busca

            >>> self._getSessoesBusca()
            <generator>
        """
        return self.execSql("select_sessoes_busca")

    @dbconnectionapp
    def _getGenero(self):
        """
            returns all news types

            >>> self._getGenero()
            <generator>
        """
        return self.execSql("select_genero")    

    @dbconnectionapp
    def _getCensura(self):
        """
            returns all news types

            >>> self._getCensura()
            <generator>
        """
        return self.execSql("select_censura")
        
    @dbconnectionapp
    def _getStatus(self):
        """
            returns all news types

            >>> self._getStatus()
            <generator>
        """
        return self.execSql("select_status")        

    @dbconnectionapp
    def _listarDiretores(self):
        """
            Lista todos os diretores

            >>> self._listarDiretores()
            <generator>
        """
        return self.execSql("select_diretor")

    @dbconnectionapp
    def _listarAtores(self):
        """
            Lista todos os atores

            >>> self._listarAtores()
            <generator>
        """
        return self.execSql("select_ator")

    @dbconnectionapp
    def _listarCinemas(self):
        """
            Lista todos os cinemas

            >>> self._listarCinemas()
            <generator>
        """
        return self.execSql("select_cinema")

    @dbconnectionapp
    def getDiretores(self):
        """
            list all diretores but returns a json object

            >>> self.getDiretores()
            <generator>
        """
        return encode([i for i in self.execSql("select_diretor")])

    @dbconnectionapp
    def getAtores(self):
        """
            list all atores but returns a json object

            >>> self.getAtores()
            <generator>
        """
        return encode([i for i in self.execSql("select_ator")])

    @dbconnectionapp
    def getCinemas(self):
        """
            list all cinemas but returns a json object

            >>> self.getCinemas()
            <generator>
        """
        return encode([i for i in self.execSql("select_cinema")])

    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def addDiretor(self, nome, url_imdb):
        """
            insert a new diretor

            >>> self.addDiretor(nome=\"name\", url_imdb=\"url_imdb\"")
        """
        self.execSqlu("insert_diretor",
                      nome=nome,
                      url_imdb=url_imdb)

        return "Diretor adicionado com sucesso!"

    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def addAtor(self, nome, url_imdb):
        """
            insert a new ator

            >>> self.addAtor(nome=\"name\", url_imdb=\"url_imdb\"")
        """
        self.execSqlu("insert_ator",
                      nome=nome,
                      url_imdb=url_imdb)

        return "Ator adicionado com sucesso!"

    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def addCinema(self, nome, localizacao, endereco, fone):
        """
            insert a new cinema

            >>> self.addAtor(nome=\"name\", localizacao=\"localizacao\", endereco=\"endereco\", fone=\"fone\"")
        """
        self.execSqlu("insert_cinema",
                      nome=nome,
                      localizacao=localizacao,
                      endereco=endereco,
                      fone=fone)

        return "Cinema adicionado com sucesso!"

    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def delDiretor(self, id_diretores=[]):
        """
            delete a list of diretores

            >>> self.delDiretor(id_diretores=[1,2,3])
        """
        for i in id_diretores:
            self.execSqlBatch("delete_diretor",
                              id_diretor=int(i))
        self.execSqlCommit()
        return "Diretor deletado com sucesso!"

    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def delAtor(self, id_atores=[]):
        """
            delete a list of atores

            >>> self.delAtor(id_atores=[1,2,3])
        """
        for i in id_atores:
            self.execSqlBatch("delete_ator",
                              id_ator=int(i))
        self.execSqlCommit()
        return "Ator deletado com sucesso!"

    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def delCinema(self, id_cinemas=[]):
        """
            delete a list of cinemas

            >>> self.delCinema(id_cinemas=[1,2,3])
        """
        for i in id_cinemas:
            self.execSqlBatch("delete_cinema",
                              id_cinema=int(i))
        self.execSqlCommit()
        return "Cinema deletado com sucesso!"

    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def getDiretor(self, id_diretor):
        """
            returns data of an diretor

            >>> self.getDiretor(1)
            {\"nome\":\"\", \"url_imdb\":\"\"}
        """
        return self.execSql("select_diretor_unico",
                            id_diretor=int(id_diretor)).next()

    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def getAtor(self, id_ator):
        """
            returns data of an ator

            >>> self.getAtor(1)
            {\"nome\":\"\", \"url_imdb\":\"\"}
        """
        return self.execSql("select_ator_unico",
                            id_ator=int(id_ator)).next()

    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def getCinema(self, id_cinema):
        """
            returns data of an cinema

            >>> self.getCinema(1)
            {\"nome\":\"\", \"localizacao\":\"\, \"endereco\":\"\, \"fone\":\"\"}
        """
        return self.execSql("select_cinema_unico",
                            id_cinema=int(id_cinema)).next()

    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def editDiretor(self, id_diretor, nome, url_imdb):
        """
            edit the data of an diretor

            >>> self.editDiretor(id_diretor=1, nome=\"nome\",
                               url_imdb=\"url_imdb\")
        """
        self.execSqlu("update_diretor",
                      id_diretor=int(id_diretor),
                      nome=nome,
                      url_imdb=url_imdb)

        return "Diretor editado com sucesso!"

    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def editAtor(self, id_ator, nome, url_imdb):
        """
            edit the data of an ator

            >>> self.editAtor(id_ator=1, nome=\"nome\",
                               url_imdb=\"url_imdb\")
        """
        self.execSqlu("update_ator",
                      id_ator=int(id_ator),
                      nome=nome,
                      url_imdb=url_imdb)

        return "Ator editado com sucesso!"

    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def editCinema(self, id_cinema, nome, localizacao, endereco, fone):
        """
            edit the data of an cinema

            >>> self.editCinema(id_cinema=1, nome=\"nome\",
                               localizacao=\"localizacao\",
                               endereco=\"endereco\",
                               fone=\"fone\")
        """
        self.execSqlu("update_cinema",
                      id_cinema=int(id_cinema),
                      nome=nome,
                      localizacao=localizacao,
                      endereco=endereco,
                      fone=fone)

        return "Cinema editado com sucesso!"

    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def addFilme(self, id_site, id_treeapp, id_aplicativo, titulo,
                         titulo_original, url_imdb, descricao, genero, censura, status, corpo, publicado_em,
                         diretor=[], ator=[], cinema=[], sala=[], horarios=[], legendado=[], 
                         tresd=[], ativo=[], videos=[], editor=None, expira_em=None,
                         publicado=None, foto_id=[], foto_grande_id=[],
                         foto_credito=[], foto_legenda=[], foto_link=[],
                         foto_alinhamento=[], foto_descricao=[],
                         video=None, audio=None, galeria=None,
                         titulo_destaque=None, descricao_destaque=None,
                         imagem_destaque=None, peso_destaque=None,
                         data_edicao=None, relacionamento=[], tags="",
                         exportar=None, exportar_xml=None,
                         exportar_json=None, permissao=None,
                         retranca=None, seo={}, **kargs):
        """ 
            method to add a news

            @id_site: id of site that this content will be
            @id_treeapp: id of tree that this content will be
            @id_aplicativo: id of application of the site
            @titulo: title of the content
            @titulo_original: original title of the content
            @url_imdb: url_imdb of the content
            @descricao: description of this content
            @genero: id from table schema.genero
            @censura: id from table schema.censura
            @status: id from table schema.status
            @corpo: body of the content
            @publicado_em: datetime to publish the content
            @diretor: list of id of the diretores
            @ator: list of id of the atores
            @cinema: list of id of the cinemas
            @sala: list of the salas of the cinema
            @horarios: list of the horarios of the cinema
            @legendado: list of the legendado of the cinema
            @tresd: list of the tresd of the cinema
            @ativo: list of the ativo of the cinema
            @videos: list the embed
            @editor: true or false if editor is in use or not
            @expira_em: datetime to expire the content 
            @publicado: True of False if the content is publicado
            @foto_id: list of the images used in this content
            @foto_grande_id: list of the big images used in this content
            @foto_credito: list of the credit of the photo
            @foto_legenda: list of the legend of the photo
            @foto_link: list of the link of the photo
            @video: True or False to inform if this content has video
            @audio: True or False to inform if this content has audio
            @galeria: True or False to inform if this content has photo gallery
            @titulo_destaque: title of this content highlights
            @descricao_destaque: description of this content highlights
            @imagem_destaque: image of this content highlights
            @peso_destaque: height number of this content
            @data_edicao: date
            @relacionamento: list of relationship of this content with others
            @tags: string of words with single space
            @exportar:True or False if the html of this content must be create
            @exportar_xml: True of False if the xml of this content must be create
            @exportar_json: True of False if the json of this content must be create
            @permissao: dictionary with the information of this content permission


            >>> self.addFilme(id_site=1,
                                id_treeapp=2,
                                id_aplicativo=3,
                                titulo="title",
                                titulo_original="original title",
                                url_imdb="url imdb",
                                descricao="description",
                                genero=1,
                                censura=1,
                                status=1,
                                corpo="body of this content",
                                publicado_em="20/01/2010 11:33",
                                diretor=[1,2,3],
                                ator=[1,2,3],
                                cinema=[1,2,3],
                                sala=["Sala 10", ],
                                horarios=["10h15m", ],
                                legendado=[True, ],
                                tresd=[True, ],
                                ativo=[True, ],
                                videos=["<embed></embed>", ],
                                editor=True,
                                expira_em="01/01/2012 00:00",
                                publicado=True,
                                foto_id=["tmpimg16849616.png", ],
                                foto_grande_id=["tmpimg987641.gif", ],
                                foto_credito=["credit of this photo", ],
                                foto_legenda=["description of this photo", ],
                                foto_link=[{...}, ],
                                foto_alinhamento=["left", ],
                                video=True,
                                audio=True,
                                galeria=True,
                                titulo_destaque="title of destaque",
                                descricao_destaque="description of destaque",
                                imagem_destaque="tmpimg9876535461.png",
                                peso_destaque=1,
                                data_edicao="01/01/2012",
                                relacionamento=[],
                                tags="tag1 tag2 tag3",
                                exportar=True,
                                exportar_xml=True,
                                exportar_json=True,
                                permissao={"livre":1,
                                           "exclusiva"None,
                                           "data":None},
                                )
        """
        id_conteudo = self.execSql("select_nextval_filme").next()["id"]
        publicado = True if publicado else False
        tags = tags if tags else None

        dt = publicado_em
        try:
            p = strptime(publicado_em, "%d/%m/%Y %H:%M")
            publicado_em = strftime("%Y-%m-%d %H:%M", p)
        except ValueError, e:
            raise UserError(("Ocorreu um erro: "
                             "Data de publica&ccedil;&aring;o "
                             "inv&aacute;lida (%s)") % publicado_em)

        try:
            p = strptime(expira_em, "%d/%m/%Y %H:%M")
            expira_em = strftime("%Y-%m-%d %H:%M", p)
        except ValueError, e:
           expira_em = None

        try:
            p = strptime(data_edicao, "%d/%m/%Y")
            data_edicao = strftime("%Y-%m-%d", p)
        except ValueError, e:
            data_edicao = None

        editor = True if editor else False
        video = True if video else False
        audio = True if audio else False
        galeria = True if galeria else False

        # adicionar filme
        self.execSqlBatch("insert_filme", 
                          id_conteudo=id_conteudo,
                          video=video,
                          audio=audio,
                          galeria=galeria,
                          titulo=unquote(titulo),
                          titulo_original=unquote(titulo_original),
                          url_imdb=url_imdb,
                          descricao=descricao,
                          id_genero=int(genero),
                          id_censura=int(censura),
                          id_status=int(status),
                          corpo=corpo,
                          publicado_em=publicado_em,
                          expira_em=expira_em,
                          publicado=publicado,
                          data_edicao=data_edicao,
                          editor=editor)

        # adicionar diretor
        dados_diretor = []
        ndir = 1
        for t in diretor:
            dir = kargs.get("ddiretor%s" % ndir)
            ndir += 1
            if dir:
                ldir = [i for i in self.execSql("select_diretor_unico_nome",
                                                nome=dir["nome"])]
                if not ldir:
                    id_diretor = self.execSql("select_nextval_diretor").next()["id"]
                    self.execSqlu("insert_diretori",
                                  id_diretor=id_diretor,
                                  nome=dir["nome"],
                                  url_imdb=dir["url_imdb"])
                else:
                    id_diretor = ldir[0]["id_diretor"] 

                self.execSqlBatch("insert_filme_diretor", 
                                  id_conteudo=id_conteudo,
                                  id_diretor=int(id_diretor),
                                  ordem=ndir)
                dados_diretor.append(int(id_diretor))

        # adicionar ator
        dados_ator = []
        nato = 1
        for t in ator:
            ato = kargs.get("dator%s" % nato)
            nato += 1
            if ato:
                lato = [i for i in self.execSql("select_ator_unico_nome",
                                                nome=ato["nome"])]
                if not lato:
                    id_ator = self.execSql("select_nextval_ator").next()["id"]
                    self.execSqlu("insert_atori",
                                  id_ator=id_ator,
                                  nome=ato["nome"],
                                  url_imdb=ato["url_imdb"])
                else:
                    id_ator = lato[0]["id_ator"] 

                self.execSqlBatch("insert_filme_ator", 
                                  id_conteudo=id_conteudo,
                                  id_ator=int(id_ator),
                                  ordem=nato)
                dados_ator.append(int(id_ator))

        # adicionar cinema
        objTresd = tresd[:]
        objAtivo = ativo[:]
        dados_cinema = []
        ncin = 1
        for t in range(len(cinema)):
            cin = kargs.get("dcinema%s" % ncin)
            ncin += 1
            if cin:
                lcin = [i for i in self.execSql("select_cinema_unico_nome",
                                                nome=cin["nome"])]
                if not lcin:
                    id_cinema = self.execSql("select_nextval_cinema").next()["id"]
                    self.execSqlu("insert_cinemai",
                                  id_cinema=id_cinema,
                                  nome=cin["nome"],
                                  localizacao=cin["localizacao"],
                                  endereco=cin["endereco"],
                                  fone=cin["fone"])
                else:
                    id_cinema = lcin[0]["id_cinema"] 

                tresd = True if objTresd[t] else False
                ativo = True if objAtivo[t] else False
                self.execSqlBatch("insert_filme_cinema", 
                                  id_conteudo=id_conteudo,
                                  id_cinema=int(id_cinema),
                                  sala=sala[t],
                                  horarios=horarios[t],
                                  legendado=legendado[t],
                                  tresd=tresd,
                                  ativo=ativo,
                                  ordem=ncin)
                dados_cinema.append(int(id_cinema))

        # fotos
        dados_fotos = []
        for i in range(len(foto_id)):

            arquivo = foto_id[i]
            arquivo_grande = foto_grande_id[i]
            alinhamento = foto_alinhamento[i]
            credito = foto_credito[i]
            legenda = foto_legenda[i]
            # backward compatibility with other softwares
            try:
                descricao = foto_descricao[i]
            except IndexError, e:
                descricao = ""
            link = foto_link[i]
            imagem = self._addFile(arquivo=arquivo,
                                    id_conteudo=id_conteudo,
                                    schema=self.schema,
                                    dt=dt)

            if not imagem:
                continue

            imagemg = self._addFile(arquivo=arquivo_grande,
                                     id_conteudo=id_conteudo,
                                     schema=self.schema,
                                     dt=dt)
            if not imagemg:
                imagemg = None

            self.execSqlBatch("insert_foto_filme", 
                              id_conteudo=id_conteudo,
                              arquivo=imagem,
                              arquivo_grande=imagemg,
                              alinhamento=alinhamento,
                              credito=credito,
                              legenda=legenda,
                              descricao=descricao,
                              link=link)

            dados_fotos.append({"arquivo":imagem,
                                "arquivo_grande":imagemg,
                                "alinhamento":alinhamento,
                                "credito":credito,
                                "legenda":legenda,
                                "link":link})
        # fotos antes-depois
        dados_fotos_antes_depois = []
        for i in range(len(kargs.get("foto_antes", []))):
            foto_antes = kargs["foto_antes"][i]
            foto_depois = kargs["foto_depois"][i]
            alinhamento = kargs["foto_alinhamento_ad"][i]
            credito_antes = kargs["foto_credito_antes"][i]
            credito_depois = kargs["foto_credito_depois"][i]
            legenda = kargs["foto_legenda_antes_depois"][i]
            link = kargs["foto_link_ad"][i]

            foto_antes = self._addFile(arquivo=foto_antes,
                                       id_conteudo=id_conteudo,
                                       schema=self.schema,
                                       dt=dt)

            if not foto_antes:
                continue

            foto_depois = self._addFile(arquivo=foto_depois,
                                        id_conteudo=id_conteudo,
                                        schema=self.schema,
                                        dt=dt)
            if not foto_depois:
                foto_depois = None

            self.execSqlBatch("insert_foto_filme_ad", 
                              id_conteudo=id_conteudo,
                              foto_antes=foto_antes,
                              foto_depois=foto_depois,
                              alinhamento=alinhamento,
                              credito_antes=credito_antes,
                              credito_depois=credito_depois,
                              legenda=legenda,
                              link=link)

            dados_fotos_antes_depois.append({"foto_antes":foto_antes,
                                            "foto_depois":foto_depois,
                                            "alinhamento":alinhamento,
                                            "credito_antes":credito_antes,
                                            "credito_depois":credito_depois,
                                            "legenda":legenda,
                                            "link":link})
        
        # videos
        dados_video = []
        for i in videos:
            self.execSqlBatch("insert_video",
                              id_conteudo=id_conteudo,
                              embed=i)
            dados_video.append({"embed":i})

        # destaque
        try:
            peso_destaque = int(peso_destaque)
        except:
            peso_destaque = 0

        dados_destaque = []
        if titulo_destaque or imagem_destaque or descricao_destaque:
            imagem_destaque = self._addFile(arquivo=imagem_destaque,
                                             id_conteudo=id_conteudo,
                                             schema=self.schema,
                                             dt=dt)
            if not imagem_destaque:
                imagem_destaque = None

            self.execSqlBatch("insert_destaque", 
                              id_conteudo=id_conteudo,
                              titulo=titulo_destaque,
                              descricao=descricao_destaque,
                              img=imagem_destaque,
                              peso=peso_destaque)

            dados_destaque.append({"titulo":titulo_destaque,
                                   "descricao":descricao,
                                   "img":imagem_destaque,
                                   "peso":peso_destaque})

        self.execSqlCommit()
        if retranca:
            self.execSqlu("update_retranca",
                          id_conteudo=id_conteudo,
                          retranca=retranca)
 
        dados = self._setDados(id_conteudo=id_conteudo)
        self._addContentPortal(env_site=self.id_site,
                               id_pk=id_conteudo,
                               schema=self.schema,
                               meta_type=self.meta_type,
                               id_aplicativo=id_aplicativo,
                               id_treeapp=id_treeapp,
                               peso=peso_destaque,
                               titulo=titulo,
                               publicado=publicado,
                               publicado_em=publicado_em,
                               expira_em=expira_em,
                               titulo_destaque=titulo_destaque,
                               descricao_destaque=descricao_destaque,
                               imagem_destaque=imagem_destaque,
                               seo=seo,
                               tags=tags,
                               permissao=permissao,
                               relacionamento=relacionamento,
                               dados=dados)

        if exportar_xml or exportar_json or exportar:

            self._addLog("Novo filme cadastrado e publicado '%s'" % titulo)
            self._exportContent(id_aplicativo=id_aplicativo,
                                id_conteudo=id_conteudo,
                                schema=self.schema,
                                id_treeapp=id_treeapp,
                                html=exportar,
                                xml=exportar_xml,
                                json=exportar_json,
                                dados=dados,
                                subitems=None,
                                add=1)

            return ("Filme cadastrado com sucesso! "
                    "Publica&ccedil;&atilde;o iniciada.")

        self._addLog("Novo filme cadastrado '%s'" % titulo)
        return "Filme cadastrado com sucesso."


    @dbconnectionapp
    def _getFilme(self, id_conteudo):
        """
        """
        dic = {}
        filme = self.execSql("select_filme",
                               id_conteudo=int(id_conteudo)).next()

        fotos = [i for i in self.execSql("select_filme_fotos",
                                         id_conteudo=int(id_conteudo))]
        fotos_antes_depois = [i for i in self.execSql("select_filme_fotos_ad",
                                         id_conteudo=int(id_conteudo))]
        videos = [i for i in self.execSql("select_videos",
                                         id_conteudo=int(id_conteudo))]

        diretores = [i["id_diretor"] for i in self.execSql("select_filme_diretores",
                                                 id_conteudo=int(id_conteudo))]
        if len(diretores) == 1:
            diretores.append(None)
        elif len(diretores) == 0:
            diretores = [None, None]

        atores = [i["id_ator"] for i in self.execSql("select_filme_atores",
                                                 id_conteudo=int(id_conteudo))]
        if len(atores) == 1:
            atores.append(None)
        elif len(atores) == 0:
            atores = [None, None]

        cinemas = [i for i in self.execSql("select_filme_cinemas",
                                                 id_conteudo=int(id_conteudo))]

        return {"filme":filme,
                "fotos":fotos,
                "diretores":diretores,
                "atores":atores,
                "cinemas":cinemas,
                "videos":videos,
                "fotos_ad":fotos_antes_depois}


    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def editFilme(self, id_treeapp, id_aplicativo, id_conteudo, titulo,
                          titulo_original, url_imdb, descricao, genero, censura, status, corpo, publicado_em,
                          diretor=[], ator=[], cinema=[], sala=[], horarios=[], legendado=[], 
                          tresd=[], ativo=[], videos=[], editor=None, expira_em=None,
                          publicado=None, foto_id=[], foto_grande_id=[],
                          foto_credito=[], foto_legenda=[], foto_link=[],
                          foto_alinhamento=[], foto_descricao=[],
                          video=None, audio=None, galeria=None,
                          titulo_destaque=None, descricao_destaque=None,
                          imagem_destaque=None, peso_destaque=None,
                          id_destaque=None,
                          relacionamento=[], tags=None,
                          data_edicao=None, exportar=None, exportar_json=None,
                          exportar_xml=None, permissao=None, seo={}, **kargs):
        """
            method to edit a news

            @id_treeapp: id of tree that this content will be
            @id_aplicativo: id of application of the site
            @id_conteudo: id of table schema.conteudo pk
            @titulo: title of the content
            @titulo_original: original title of the content
            @url_imdb: url imdb of the content
            @descricao: description of this content
            @genero: id from table schema.genero
            @censura: id from table schema.censura
            @status: id from table schema.status
            @corpo: body of the content
            @publicado_em: datetime to publish the content
            @diretor: list of id of the diretores
            @ator: list of id of the atores
            @cinema: list of id of the cinemas
            @sala: list of the salas of the cinema
            @horarios: list of the horarios of the cinema
            @legendado: list of the legendado of the cinema
            @tresd: list of the tresd of the cinema
            @ativo: list of the ativo of the cinema
            @videos: list the embed
            @editor: true or false if editor is in use or not
            @expira_em: datetime to expire the content 
            @publicado: True of False if the content is publicado
            @foto_id: list of the images used in this content
            @foto_grande_id: list of the big images used in this content
            @foto_credito: list of the credit of the photo
            @foto_legenda: list of the legend of the photo
            @foto_link: list of the link of the photo
            @video: True or False to inform if this content has video
            @audio: True or False to inform if this content has audio
            @galeria: True or False to inform if this content has photo gallery
            @titulo_destaque: title of this content highlights
            @descricao_destaque: description of this content highlights
            @imagem_destaque: image of this content highlights
            @id_destaque: id of table schema.destaque pk
            @peso_destaque: height number of this content
            @data_edicao: date
            @relacionamento: list of relationship of this content with others
            @tags: string of words with single space
            @exportar:True or False if the html of this content must be create
            @exportar_xml: True of False if the xml of this content must be create
            @exportar_json: True of False if the json of this content must be create
            @permissao: dictionary with the information of this content permission

            >>> self.editFilme(id_treeapp=2,
                                id_aplicativo=3,
                                id_conteudo=1,
                                titulo="title",
                                titulo_original="original title",
                                url_imdb="url imdb",
                                descricao="description",
                                genero=1,
                                censura=1,
                                status=1,
                                corpo="body of this content",
                                publicado_em="20/01/2010 11:33",
                                diretor=[1,2,3],
                                ator=[1,2,3],
                                cinema=[1,2,3],
                                sala=["Sala 10", ],
                                horarios=["10h15m", ],
                                legendado=[True, ],
                                tresd=[True, ],
                                ativo=[True, ],
                                videos=["<embed></embed>", ],
                                editor=True,
                                expira_em="01/01/2012 00:00",
                                publicado=True,
                                foto_id=["tmpimg16849616.png", ],
                                foto_grande_id=["tmpimg987641.gif", ],
                                foto_credito=["credit of this photo", ],
                                foto_legenda=["description of this photo", ],
                                foto_link=[{...}, ],
                                foto_alinhamento=["left", ],
                                video=True,
                                audio=True,
                                galeria=True,
                                titulo_destaque="title of destaque",
                                descricao_destaque="description of destaque",
                                imagem_destaque="tmpimg9876535461.png",
                                peso_destaque=1,
                                id_destaque=1,
                                data_edicao="01/01/2012",
                                relacionamento=[],
                                tags="tag1 tag2 tag3",
                                exportar=True,
                                exportar_xml=True,
                                exportar_json=True,
                                permissao={"livre":1,
                                           "exclusiva"None,
                                           "data":None},
                                )

        """
        publicado = True if publicado else False
        tags = tags if tags else None

        dt = publicado_em
        try:
            publicado_em_t = strptime(publicado_em, "%d/%m/%Y %H:%M")
            publicado_em = strftime("%Y-%m-%d %H:%M", publicado_em_t)
        except ValueError, e:
            raise UserError(("Ocorreu um erro: "
                             "Data de publica&ccedil;&aring;o "
                             "inv&aacute;lida (%s)") % publicado_em)
        try:
            p = strptime(expira_em, "%d/%m/%Y %H:%M")
            expira_em = strftime("%Y-%m-%d %H:%M", p)
        except ValueError, e:
           expira_em = None

        try:
            p = strptime(data_edicao, "%d/%m/%Y")
            data_edicao = strftime("%Y-%m-%d", p)
        except ValueError, e:
           data_edicao = None

        atualizado_em = strftime('%Y-%m-%d %H:%M')
        editor = True if editor else False
        video = True if video else False
        audio = True if audio else False
        galeria = True if galeria else False

        self.execSqlBatch("delete_dados_filme",
                          id_conteudo=int(id_conteudo))
        # atualizar filme
        self.execSqlBatch("update_filme",
                          id_conteudo=int(id_conteudo),
                          video=video,
                          audio=audio,
                          galeria=galeria,
                          titulo=unquote(titulo),
                          titulo_original=unquote(titulo_original),
                          url_imdb=url_imdb,
                          descricao=descricao,
                          id_genero=int(genero),
                          id_censura=int(censura),
                          id_status=int(status),
                          corpo=corpo,
                          publicado_em=publicado_em,
                          expira_em=expira_em,
                          publicado=publicado,
                          atualizado_em=atualizado_em,
                          data_edicao=data_edicao,
                          editor=editor)

        # adicionar diretor
        dados_diretor = []
        ndir = 0
        for dir in diretor:
            self.execSqlBatch("insert_filme_diretor",
                              id_conteudo=int(id_conteudo),
                              id_diretor=int(dir),
                              ordem=ndir)
            dados_diretor.append(int(dir))
            ndir += 1
            
        # adicionar ator
        dados_ator = []
        nato = 0
        for ato in ator:
            self.execSqlBatch("insert_filme_ator",
                              id_conteudo=int(id_conteudo),
                              id_ator=int(ato),
                              ordem=nato)
            dados_ator.append(int(ato))
            nato += 1

        # adicionar cinema
        objTresd = tresd[:]
        objAtivo = ativo[:]
        dados_cinema = []
        ncin = 0
        for cin in range(len(cinema)):
            tresd = True if objTresd[cin] else False
            ativo = True if objAtivo[cin] else False
            self.execSqlBatch("insert_filme_cinema",
                              id_conteudo=int(id_conteudo),
                              id_cinema=int(cinema[cin]),
                              sala=sala[cin],
                              horarios=horarios[cin],
                              legendado=legendado[cin],
                              tresd=tresd,
                              ativo=ativo,
                              ordem=ncin)
            dados_cinema.append(int(cinema[cin]))
            ncin += 1

        # fotos
        dados_fotos = []
        for i in range(len(foto_id)):
            arquivo = foto_id[i]
            arquivo_grande = foto_grande_id[i]
            alinhamento = foto_alinhamento[i]
            credito = foto_credito[i]
            legenda = foto_legenda[i]
            # backward compatibility with other softwares
            try:
                descricao = foto_descricao[i]
            except IndexError, e:
                descricao = ""
            link = foto_link[i]

            arquivon = self._addFile(arquivo=arquivo,
                                      id_conteudo=id_conteudo,
                                      schema=self.schema,
                                      dt=dt)
 
            if arquivon:
                arquivo = arquivon

            arquivogn = self._addFile(arquivo=arquivo_grande,
                                       id_conteudo=id_conteudo,
                                       schema=self.schema,
                                       dt=dt)
 
            if arquivogn:
                arquivo_grande = arquivogn

            self.execSqlBatch("insert_foto_filme", 
                              id_conteudo=int(id_conteudo), 
                              arquivo_grande=arquivo_grande,
                              arquivo=arquivo,
                              alinhamento=alinhamento,
                              credito=credito,
                              legenda=legenda,
                              descricao=descricao,
                              link=link)

            dados_fotos.append({"arquivo":arquivo,
                                "arquivo_grande":arquivo_grande,
                                "alinhamento":alinhamento,
                                "credito":credito,
                                "legenda":legenda,
                                "link":link})

        # fotos antes-depois
        dados_fotos_antes_depois = []
        for i in range(len(kargs.get("foto_antes", []))):
            foto_antes = kargs["foto_antes"][i]
            foto_depois = kargs["foto_depois"][i]
            alinhamento = kargs["foto_alinhamento_ad"][i]
            credito_antes = kargs["foto_credito_antes"][i]
            credito_depois = kargs["foto_credito_depois"][i]
            legenda = kargs["foto_legenda_antes_depois"][i]
            link = kargs["foto_link_ad"][i]

            foto_antes = self._addFile(arquivo=foto_antes,
                                       id_conteudo=id_conteudo,
                                       schema=self.schema,
                                       dt=dt)

            if not foto_antes:
                continue

            foto_depois = self._addFile(arquivo=foto_depois,
                                        id_conteudo=id_conteudo,
                                        schema=self.schema,
                                        dt=dt)
            if not foto_depois:
                foto_depois = None

            self.execSqlBatch("insert_foto_filme_ad", 
                              id_conteudo=int(id_conteudo),
                              foto_antes=foto_antes,
                              foto_depois=foto_depois,
                              alinhamento=alinhamento,
                              credito_antes=credito_antes,
                              credito_depois=credito_depois,
                              legenda=legenda,
                              link=link)

            dados_fotos_antes_depois.append({"foto_antes":foto_antes,
                                            "foto_depois":foto_depois,
                                            "alinhamento":alinhamento,
                                            "credito_antes":credito_antes,
                                            "credito_depois":credito_depois,
                                            "legenda":legenda,
                                            "link":link})

        # videos
        dados_videos = []
        for i in videos:
            self.execSqlBatch("insert_video", 
                              id_conteudo=int(id_conteudo),
                              embed=i)
            dados_videos.append({"embed":i})

        # destaque
        try:
            peso_destaque = int(peso_destaque)
        except:
            peso_destaque = 0

        dados_destaque = []
        if titulo_destaque or imagem_destaque or descricao_destaque:

            imagem_destaquen = self._addFile(arquivo=imagem_destaque,
                                              id_conteudo=int(id_conteudo),
                                              schema=self.schema,
                                              dt=dt)
 
            if imagem_destaquen:
                imagem_destaque = imagem_destaquen
            elif not imagem_destaque:
                imagem_destaque = None

            if id_destaque:
                self.execSqlBatch("update_destaque", 
                                  id_conteudo=int(id_conteudo),
                                  id_destaque=int(id_destaque),
                                  titulo=titulo_destaque,
                                  descricao=descricao_destaque,
                                  img=imagem_destaque,
                                  peso=peso_destaque)
            else:
                self.execSqlBatch("insert_destaque", 
                                  id_conteudo=int(id_conteudo),
                                  titulo=titulo_destaque,
                                  descricao=descricao_destaque,
                                  img=imagem_destaque,
                                  peso=peso_destaque)
        elif id_destaque:
            self.execSqlBatch("delete_destaque",
                              id_destaque=int(id_destaque))
            titulo_destaque = titulo_destaque
            descricao_destaque = descricao_destaque
            imagem_destaque = imagem_destaque

        dados_destaque.append({"titulo":titulo_destaque,
                               "descricao":descricao_destaque,
                               "img":imagem_destaque,
                               "peso":peso_destaque})

        self.execSqlCommit()

        dados = self._setDados(id_conteudo=id_conteudo)
        self._editContentPortal(env_site=self.id_site,
                                id_pk=id_conteudo,
                                id_aplicativo=int(id_aplicativo),
                                schema=self.schema,
                                id_treeapp=id_treeapp,
                                peso=peso_destaque,
                                titulo=titulo,
                                publicado=publicado,
                                publicado_em=publicado_em,
                                expira_em=expira_em,
                                titulo_destaque=titulo_destaque,
                                descricao_destaque=descricao_destaque,
                                imagem_destaque=imagem_destaque,
                                seo=seo,
                                permissao=permissao,
                                tags=tags,
                                relacionamento=relacionamento,
                                dados=dados)

        if exportar_xml or exportar_json or exportar:

            self._addLog("Filme '%s' editado e publicado" % titulo)
            self._exportContent(id_aplicativo=id_aplicativo,
                                id_conteudo=id_conteudo,
                                schema=self.schema,
                                id_treeapp=id_treeapp,
                                html=exportar,
                                xml=exportar_xml,
                                json=exportar_json,
                                dados=dados,
                                subitems=None,
                                edit=1)

            return ("Filme editado com sucesso! "
                    "Publica&ccedil;&atilde;o iniciada.")

        self._addLog("Filme '%s' editado" % titulo)
        return "Filme editado com sucesso."
