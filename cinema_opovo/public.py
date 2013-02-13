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
# public.py cinema_opovo
# modificado por Eric Mesquita em 01/10/2012
#
import re
import datetime
from time import strftime, strptime
from urllib import splitquery, splitvalue, unquote, quote
from publica import settings
from publica.core.portal import Portal
from publica.admin.exchange import getDadosSite, getSiteByHost
from publica.utils.json import encode, decode
from publica.utils.BeautifulSoup import BeautifulSoup
from publica.utils.decorators import dbconnectionapp, serialize, jsoncallback


class Public(object):

    """
        public class of methods of this content
    """

    @dbconnectionapp
    def _getFilmesByGenero(self, id_genero=None, id_conteudo=None):
        """
            returns the data from a news content

            @mkl: overwrites de default render method of links

            >>> self._getFilmesByGenero()
            {'id_conteudo':, 'titulo':, 'titulo_original':, 'url_imdb':, 'descricao':,
             'id_genero':, 'id_censura':, 'id_status':, 'editor':, 'corpo':, 'nota1':, 'nota2':,
             'nota3':, 'nota4':, 'nota5':, 'video':, 'audio':,
             'galeria':, 'publicado_em':, 'publicado':, 'atualizado_em':, "
             'id_destaque':, 'titulo_destaque':, 'descricao_destaque':,
             'imagem_destaque':, 'titulo_tree':, 'breadcrump':}
        """
        retorno = []
        for filme in self.execSql("select_filmes_por_genero",
                                   id_genero=int(id_genero),
                                   id_conteudo=int(id_conteudo)):
            soup = BeautifulSoup(filme["corpo"],
                                 fromEncoding=settings.GLOBAL_ENCODING)
            for a in soup.findAll("a"):
                href = unquote(a.get("href", "")).strip()
                if href.startswith("#h2href:"):
                    kingkong, dados = href.split("#h2href:", 1)
                    if mkl:
                        href, attrs = mkl(dados=decode(dados))
                        for i in attrs.keys():
                            a[i] = attrs[i]
                    else:
                        href = self._renderLink(dados=dados)

                    if href.find("javascript") >= 0:
                        href = href.replace("[target=blank]", "")
                    elif href.find("target=blank") >= 0:
                        href = href.replace("[target=blank]", "")
                        a["target"] = "blank"

                    a["href"] = href

            filme["corpo"] = unquote( unicode(soup) )
            
            filme["url"] = self._getUrlByApp(env_site=self.id_site,
                          schema=self.schema,
                          id_conteudo=filme["id_conteudo"],
                          exportar=1, admin=1)

            filme["atores"] = [i for i in self.execSql("select_filme_atores",
                                                        id_conteudo=int(filme["id_conteudo"]))]

            filme["diretores"] = [i for i in self.execSql("select_filme_diretores",
                                                        id_conteudo=int(filme["id_conteudo"]))]

            filme["fotos"] = [i for i in self.execSql("select_filme_fotos",
                                                        id_conteudo=int(filme["id_conteudo"]))]
                                                        
            filme["sessoes"] = [i for i in self.execSql("select_filme_cinemas_ativos",
                                                        id_conteudo=int(filme["id_conteudo"]))]

            retorno.append(filme);
        return retorno

    @dbconnectionapp
    def _getFilmesBusca(self):
        """
            returns the data from a news content

            @mkl: overwrites de default render method of links

            >>> self._getFilmesBusca()
            {'id_conteudo':, 'titulo':, 'titulo_original':, 'url_imdb':, 'descricao':,
             'id_genero':, 'id_censura':, 'id_status':, 'editor':, 'corpo':, 'nota1':, 'nota2':,
             'nota3':, 'nota4':, 'nota5':, 'video':, 'audio':,
             'galeria':, 'publicado_em':, 'publicado':, 'atualizado_em':, "
             'id_destaque':, 'titulo_destaque':, 'descricao_destaque':,
             'imagem_destaque':, 'titulo_tree':, 'breadcrump':}
        """
        retorno = []
        for filme in self.execSql("select_filmes_ativos"):
            soup = BeautifulSoup(filme["corpo"],
                                 fromEncoding=settings.GLOBAL_ENCODING)
            for a in soup.findAll("a"):
                href = unquote(a.get("href", "")).strip()
                if href.startswith("#h2href:"):
                    kingkong, dados = href.split("#h2href:", 1)
                    if mkl:
                        href, attrs = mkl(dados=decode(dados))
                        for i in attrs.keys():
                            a[i] = attrs[i]
                    else:
                        href = self._renderLink(dados=dados)

                    if href.find("javascript") >= 0:
                        href = href.replace("[target=blank]", "")
                    elif href.find("target=blank") >= 0:
                        href = href.replace("[target=blank]", "")
                        a["target"] = "blank"

                    a["href"] = href

            filme["corpo"] = unquote( unicode(soup) )
            
            filme["url"] = self._getUrlByApp(env_site=self.id_site,
                          schema=self.schema,
                          id_conteudo=filme["id_conteudo"],
                          exportar=1, admin=1)

            filme["atores"] = [i for i in self.execSql("select_filme_atores",
                                                        id_conteudo=int(filme["id_conteudo"]))]

            filme["diretores"] = [i for i in self.execSql("select_filme_diretores",
                                                        id_conteudo=int(filme["id_conteudo"]))]

            filme["fotos"] = [i for i in self.execSql("select_filme_fotos",
                                                        id_conteudo=int(filme["id_conteudo"]))]
                                                        
            filme["sessoes"] = [i for i in self.execSql("select_filme_cinemas_ativos",
                                                        id_conteudo=int(filme["id_conteudo"]))]

            retorno.append(filme);
        return retorno


    def _dothetags(self, tags):
        """
            render the tags string to a list of words

            >>> self._dothetags(\"tag1 tag2  tag3\")
            ['tag1', 'tag2', 'tag3']
        """
        if not tags:
            return []

        res = []
        p1 = re.compile("\'(.*?)\'")
        p2 = re.compile("\"(.*?)\"")
        res += p1.findall(tags)
        res += p2.findall(tags)
        tags = p1.sub("", tags)
        tags = p2.sub("", tags)
        tags = tags.replace("  ", " ")
        tags = tags.replace("\n", " ")
        res += tags.strip().split(" ")

        return res


    def _getTags(self, id_conteudo, text=None):
        """
            use portal's method _getTags to iterate over the tags of content
            
            >>> self._getTags(id_conteudo=1)
            >>> ['tag1', 'tag2']

            >>> self._getTags(id_conteudo=1, text=1)
            'tag1 tag2'
        """
        for i in self._getTag(id_conteudo=int(id_conteudo),
                              schema=self.schema):
            yield i      

    @dbconnectionapp
    def _getFilmePublicado(self, id_filme=None, mkl=None):
        """
            returns the data from a news content

            @mkl: overwrites de default render method of links

            >>> self._getFilmePublicado(id_filme=1)
            {'id_conteudo':, 'titulo':, 'titulo_original':, 'url_imdb':, 'descricao':,
             'id_genero':, 'id_censura':,'genero':, 'censura':, 'editor':, 'corpo':, 'nota1':, 'nota2':,
             'nota3':, 'nota4':, 'nota5':, 'video':, 'audio':,
             'galeria':, 'publicado_em':, 'publicado':, 'atualizado_em':, "
             'id_destaque':, 'titulo_destaque':, 'descricao_destaque':,
             'imagem_destaque':, 'titulo_tree':, 'breadcrump':}
        """
        filme = None
        if not filme:
            for filme in self.execSql("select_filme_publicado_ultimo"):
                break

        for filme in self.execSql("select_filme_publicado",
                                    id_conteudo=int(id_filme)):
            break

        if filme:
            soup = BeautifulSoup(filme["corpo"],
                                 fromEncoding=settings.GLOBAL_ENCODING)
            for a in soup.findAll("a"):
                href = unquote(a.get("href", "")).strip()
                if href.startswith("#h2href:"):
                    kingkong, dados = href.split("#h2href:", 1)
                    if mkl:
                        href, attrs = mkl(dados=decode(dados))
                        for i in attrs.keys():
                            a[i] = attrs[i]
                    else:
                        href = self._renderLink(dados=dados)

                    if href.find("javascript") >= 0:
                        href = href.replace("[target=blank]", "")
                    elif href.find("target=blank") >= 0:
                        href = href.replace("[target=blank]", "")
                        a["target"] = "blank"

                    a["href"] = href

            filme["corpo"] = unquote( unicode(soup) )
            filme["censura"] = self._getCensuraNome(id_censura=filme["id_censura"])
            filme["genero"] = self._getGeneroNome(id_genero=filme["id_genero"])
            filme["status"] = self._getStatusNome(id_status=filme["id_status"])
            filme["sessoes"] = [i for i in self.execSql("select_filme_cinemas_ativos",
                                                        id_conteudo=int(filme["id_conteudo"]))]

        return filme
        
    @dbconnectionapp
    def _getCensuraNome(self, id_censura=None):
        """
        """
        censura = [i for i in self.execSql("select_censura_unico",
                             id_censura=int(id_censura))]
        return censura[0]['nome']

    @dbconnectionapp
    def _getGeneroNome(self, id_genero=None):
        """
        """
        genero = [i for i in self.execSql("select_genero_unico",
                             id_genero=int(id_genero))]
        return genero[0]['nome']

    @dbconnectionapp
    def _getStatusNome(self, id_status=None):
        """
        """
        status = [i for i in self.execSql("select_status_unico",
                             id_status=int(id_status))]
        return status[0]['nome']

    @dbconnectionapp
    def _getFilmePublicadoUltimo(self, id_filme=None, hash=None, mkl=None):
        """
            Retorna os dados de um filme ou o ultimo do hash
            returns the data of an expecific content if the parameter
            id_filme is given or the first content of a folder hash

            >>> self._getFilmePublicadoUltimo(id_filme=1)
            # see data return in _getFilmePublicado method
        """
        if id_filme:
            return self._getFilmePublicado(id_filme=id_filme,
                                             mkl=mkl)
        elif hash:
            for i in self._getListContent(id_site=self.id_site,
                                           hash=[hash],
                                           comentario=False,
                                           acesso=False,
                                           acesso24h=None,
                                           voto=False,
                                           limit=1)["itens"]:
                return self._getFilmePublicado(id_filme=i["id_conteudo"],
                                                 mkl=mkl)


    @dbconnectionapp
    def _getDiretorFilme(self, id_filme):
        """
            retorna todos os diretores de um filme
            
            >>> self._getDiretorFilme(id_filme=1)
            <generator>
        """
        return self.execSql("select_diretor_filme",
                            id_conteudo=int(id_filme))

    @dbconnectionapp
    def _getAtorFilme(self, id_filme):
        """
            retorna todos os atores de um filme
            
            >>> self._getAtorFilme(id_filme=1)
            <generator>
        """
        return self.execSql("select_ator_filme",
                            id_conteudo=int(id_filme))

    @dbconnectionapp
    def _getCinemaFilme(self, id_filme):
        """
            retorna todos os cinemas de um filme
            
            >>> self._getCinemaFilme(id_filme=1)
            <generator>
        """
        return self.execSql("select_cinema_filme",
                            id_conteudo=int(id_filme))


    def _getAttrFilme(self, id_filme):
        """
            return portal data of content

            >>> self._getAttrFilme(1)
            {'id_treeapp':, 'id_aplicativo':, 'url':,
             'voto':, 'nvoto':, 'acesso':, 'comentario':, 'tags':}
        """
        return self._getAttrContent(schema=self.schema,
                                     id_conteudo=id_filme)


    @dbconnectionapp
    def _getDestaqueSite(self, id_filme):
        """
            return the highlight data from the content

            >>> self._getDestaqueSite(1)
            {'titulo':, 'descricao':, 'img':}
        """
        for i in self.execSql("select_filme_destaque",
                             id_conteudo=int(id_filme)):
            return i


    @dbconnectionapp
    def _getFotosSite(self, id_filme):
        """
            returns all photos of the content

            >>> self._getFotosSite(1)
            [{'id_foto':, 'arquivo':, 'arquivo_grande':, 'alinhamento':,
              'credito':, 'legenda':, 'link':}, ] 
        """
        return self.execSql("select_filme_fotos",
                            id_conteudo=int(id_filme))


    @dbconnectionapp
    def _getFotosADSite(self, id_filme):
        """Retorna as fotos comparativas do cadastro de um filme
        """
        return self.execSql("select_filme_fotos_ad",
                            id_conteudo=int(id_filme))


    @dbconnectionapp
    def _getVideosSite(self, id_filme):
        """
            returns all videos of the content

            >>> self._getVideosSite(1)
            [{'id_video':, 'embed':}, ]
        """
        return self.execSql("select_videos",
                            id_conteudo=int(id_filme))


    def _formatarCorpo(self, corpo, fotos=[], editor=None, base_img=None):
        """
            format text body with the photos related to the content

            >>> body = 'text text [FOTO1] text text'
            >>> photo = [{'arquivo':'ns1/arquivos/app/.../98731913687694.gif',
                         'credito':'credito', 'legenda':'legenda',
                         'alinhamento':'left'}, ]
            >>> self._formatarCorpo(body, photo, False)
            'text text <table width="1" class="foto_filme"
            style="float:left">
            <tr><td><img src="ns1/arquivos/app/.../98731913687694.gif"
            alt="credito" title="credito" border="0"/><td></tr>
            <tr><td>legenda</td></tr>
            </table>'
        """
        cft = """
        <table width="1" class="foto_filme" style="float:%(alinhamento)s">
        <tr><td><img src="%(arquivo)s" alt="%(credito)s" title="%(credito)s" border="0"/><td></tr>
        <tr><td>%(legenda)s</td></tr>
        </table>
        """
        if not base_img:
            base_img = ""
        if not corpo:
            corpo = ""
        if not editor:
            corpo = corpo.replace("\n", "<br/>")

        index = 1
        for i in fotos:
            if not i["arquivo"]:
                index += 1
                continue
            if base_img and i["arquivo"].startswith("ns"):
                arquivo = "/".join( i["arquivo"].split("/")[1:] )
                arquivo = "%s%s" % (base_img, arquivo)
            else:
                arquivo = base_img + i["arquivo"]
                
            cfti = cft % {"arquivo":arquivo,
                          "credito": i["credito"],
                          "legenda": i["legenda"],
                          "alinhamento": i["alinhamento"]}

            corpo = corpo.replace("[FOTO%s]" % index, cfti)
            index += 1

        return corpo


    @dbconnectionapp
    def _getSVG(self, id_conteudo):
        """
            get som, video and galeria attributes from table schema.conteudo
            from a content

            >>> self._getSVG(1)
            {'som': True, 'video': True, 'galeria':True}
        """
        dados = {"som":None, "video":None, "galeria":None}
        for i in self.execSql("select_svg",
                              id_conteudo=int(id_conteudo)):
            dados["som"] = i["audio"]
            dados["video"] = i["video"]
            dados["galeria"] = i["galeria"]

        return dados


    @dbconnectionapp
    def _getContentByRetranca(self, retranca):
        """
            Returns the id_conteudo, publicado_em from a content with the field retranca
        """
        for i in self.execSql("select_content_retranca",
                              retranca=retranca):
            return i["id_conteudo"], i["publicado_em"]


    # hurdle

    @jsoncallback
    def getUltimosFilmes(self, hash, limit=20, offset=0,
                                 d1=None, d2=None, qw=None,
                                 exportar=1, corpo=None,
                                 sametree=None, samesite=None):
        """
            call _getUltimosFilme method to return list of content
            
            @hash: list of string of tree hash identification
            @limit: size of items to retrieve
            @offset: start index number of listing
            @d1: string that represent first date to start listing, '2010-01-20'
            @d2: string that represent the last date to listing, '2010-01-21'
            @qw: list of words that must have on listing items
            @exportar: True or False to indicate the url will be dinamic or static
            @corpo: True or False if must retrive corpo field
        """
        self.request["exportar"] = exportar
        return self._getUltimosFilmes(hash=hash,
                                        limit=limit,
                                        offset=offset,
                                        d1=d1,
                                        d2=d2,
                                        qw=qw,
                                        exportar=exportar,
                                        render=1,
                                        corpo=corpo,
                                        sametree=sametree,
                                        samesite=samesite)
 

    @dbconnectionapp
    def _getUltimosFilmes(self, hash, limit=20, offset=0,
                                  d1=None, d2=None, qw=None,
                                  exportar=None, render=None,
                                  tags=[], corpo=None,
                                  sametree=None, samesite=None):
        """
            call _getListContent method portal
            to retrieve the content's tree came from the parameter hash.
            if the parameter corpo is True, more data will be retrieve from
            the content

            @hash: list of string of tree hash identification
            @limit: size of items to retrieve
            @offset: start index number of listing
            @d1: string that represent first date to start listing, '2010-01-20'
            @d2: string that represent the last date to listing, '2010-01-21'
            @qw: list of words that must have on listing items
            @exportar: True or False to indicate the url will be dinamic or static
            @render: True of False if the url must be complete or ssi include like
            @tags: list of strings to filter the content
            @corpo: True or False if must retrive corpo field

            >>> self._getUltimosFilmes(hash=['94169735419684109', '198413574648732'],
                                         corpo=1)
            {"res":[...], "qtde":10}
        """
        id_site_origin = getSiteByHost(self.id_site, self.request)
        if id_site_origin:
            id_site_origin = id_site_origin["id_site"]
            if id_site_origin == int(self.id_site):
                id_site_origin = None

        if type(hash) is not list:
            hash = [hash]

        site = getDadosSite(id_site=self.id_site,
                            request=self.request)
        base = site["base_html"]
        base_img = site["base_img"]

        items = self._getListContent(id_site=self.id_site,
                                      hash=hash,
                                      comentario=False,
                                      acesso=False,
                                      acesso24h=None,
                                      voto=False,
                                      keywords=qw,
                                      de=d1,
                                      ate=d2,
                                      tags=tags,
                                      limit=limit,
                                      offset=offset,
                                      render=render,
                                      sametree=sametree,
                                      samesite=samesite,
                                      id_site_origin=id_site_origin)
        itens = []
        idcs = []
        idcsd = {}
        items_ = [i for i in items["itens"] 
                                if idcs.append(str(i["id_conteudo"])) or 1]
        if idcs:
            for i in self.execSql("select_svgs",
                                  id_conteudos=buffer(",".join(idcs))):
                idcsd[i["id_conteudo"]] = i

        for i in items_:

            res = i["serialized"]()
            if idcsd.get(i["id_conteudo"]):
                try:
                    embed = res["dados"]["video"][0]["embed"] != ""
                except IndexError, e:
                    embed = False
                portal = Portal(self.id_site, self.request)
                rel = portal._getRelacionamentoConteudo(id_site=self.id_site,
                                                  schema=self.schema,
                                                  id_conteudo=i["id_conteudo"])
                galeria = False
                infografico = False
                for j in rel:
                    if j["meta_type"] == "foto":
                        galeria = True
                    elif j["meta_type"] == "infografico":
                        infografico = True
                i["audio"] = idcsd.get(i["id_conteudo"])["audio"]
                i["video"] = idcsd.get(i["id_conteudo"])["video"] or embed
                i["galeria"] = idcsd.get(i["id_conteudo"])["galeria"] or galeria
                i["infografico"] = infografico
            else:
                i["audio"] = None
                i["video"] = None
                i["galeria"] = None

            if corpo:
                if res:
                    corpo = self._formatarCorpo(corpo=res["dados"]["corpo"],
                                                fotos=res["dados"]["foto"],
                                                editor=res["dados"]["editor"],
                                                base_img=base_img)
                    i["corpo"] = corpo
                    i["titulo_original"] = res["dados"]["titulo_original"]
                    i["url_imdb"] = res["dados"]["url_imdb"]
                    i["diretor_nome"] = None
                    i["diretor_url_imdb"] = None
                    i["ator_nome"] = None
                    i["ator_url_imdb"] = None
                    i["cinema_nome"] = None
                    i["cinema_localizacao"] = None
                    i["cinema_endereco"] = None
                    i["cinema_fone"] = None

                    if res["dados"]["diretor"]:
                        for x in self.execSql("select_diretor_filme",
                                             id_conteudo=i["id_conteudo"]):
                            i["diretor_nome"] = x["nome"]
                            i["diretor_url_imdb"] = x["url_imdb"]
                            break

                    if res["dados"]["ator"]:
                        for x in self.execSql("select_ator_filme",
                                             id_conteudo=i["id_conteudo"]):
                            i["ator_nome"] = x["nome"]
                            i["ator_url_imdb"] = x["url_imdb"]
                            break

                    if res["dados"]["cinema"]:
                        for x in self.execSql("select_cinema_filme",
                                             id_conteudo=i["id_conteudo"]):
                            i["cinema_nome"] = x["nome"]
                            i["cinema_localizacao"] = x["localizacao"]
                            i["cinema_endereco"] = x["endereco"]
                            i["cinema_fone"] = x["fone"]
                            break

                    i["serialized"] = res

            itens.append(i)

        return {"res":itens, "qtde":items["qtde"]}


    @jsoncallback
    def getUltimosFilmesAcessados(self, hash, limit=20, offset=0,
                                          d1=None, d2=None, qw=None, exportar=1,
                                          sametree=None, samesite=None):
        """
            call _getUltimosFilmesAcessados to retrieve content with more views

            @hash: list of string of tree hash identification
            @limit: size of items to retrieve
            @offset: start index number of listing
            @d1: string that represent first date to start listing, '2010-01-20'
            @d2: string that represent the last date to listing, '2010-01-21'
            @qw: list of words that must have on listing items
            @exportar: True or False to indicate the url will be dinamic or static
        """
        self.request["exportar"] = exportar
        return self._getUltimosFilmesAcessados(hash=hash,
                                                 limit=limit,
                                                 offset=offset,
                                                 d1=d1,
                                                 d2=d2,
                                                 qw=qw,
                                                 exportar=exportar,
                                                 render=1,
                                                 sametree=sametree,
                                                 samesite=samesite)



    @dbconnectionapp
    def _getUltimosFilmesAcessados(self, hash, limit=20, offset=0,
                                           d1=None, d2=None, qw=None,
                                           exportar=1, render=None,
                                           sametree=None, samesite=None):
        """
            call _getListContent method portal
            to retrieve the content's tree came from the parameter hash
            with more views

            @hash: list of string of tree hash identification
            @limit: size of items to retrieve
            @offset: start index number of listing
            @d1: string that represent first date to start listing, '2010-01-20'
            @d2: string that represent the last date to listing, '2010-01-21'
            @qw: list of words that must have on listing items
            @exportar: True or False to indicate the url will be dinamic or static
            @render: True of False if the url must be complete or ssi include like
            @tags: list of strings to filter the content
            @corpo: True or False if must retrive corpo field

            >>> self._getUltimosFilmesAcessados(hash=['94169735419684109',
                                                  corpo=1)
            {"res":[...], "qtde":10}
        """
        id_site_origin = getSiteByHost(self.id_site, self.request)
        if id_site_origin:
            id_site_origin = id_site_origin["id_site"]
            if id_site_origin == int(self.id_site):
                id_site_origin = None

        if type(hash) is not list:
            hash = [hash]

        site = getDadosSite(id_site=self.id_site,
                            request=self.request)
        base = site["base_html"]

        items = self._getListContent(id_site=self.id_site,
                                      hash=hash,
                                      comentario=False,
                                      acesso=1,
                                      acesso24h=None,
                                      voto=False,
                                      keywords=qw,
                                      de=d1,
                                      ate=d2,
                                      limit=limit,
                                      offset=offset,
                                      render=render,
                                      sametree=sametree,
                                      samesite=samesite,
                                      id_site_origin=id_site_origin)

        itens = []
        idcs = []
        idcsd = {}
        items_ = [i for i in items["itens"] 
                                if idcs.append(str(i["id_conteudo"])) or 1]
        if idcs:
            for i in self.execSql("select_svgs",
                                  id_conteudos=buffer(",".join(idcs))):
                idcsd[i["id_conteudo"]] = i

        for i in items_:

            if idcsd.get(i["id_conteudo"]):
                embed = i["serialized"]()["dados"]["video"][0]["embed"] != ""
                portal = Portal(self.id_site, self.request)
                rel = portal._getRelacionamentoConteudo(id_site=self.id_site,
                                                  schema=self.schema,
                                                  id_conteudo=i["id_conteudo"])
                galeria = False
                infografico = False
                for j in rel:
                    if j["meta_type"] == "foto":
                        galeria = True
                    elif j["meta_type"] == "infografico":
                        infografico = True
                i["audio"] = idcsd.get(i["id_conteudo"])["audio"]
                i["video"] = idcsd.get(i["id_conteudo"])["video"] or embed
                i["galeria"] = idcsd.get(i["id_conteudo"])["galeria"] or galeria
                i["infografico"] = infografico
            else:
                i["audio"] = None
                i["video"] = None
                i["galeria"] = None

            itens.append(i)

        return {"res":itens, "qtde":items["qtde"]}


    @jsoncallback
    def getUltimosFilmesVotados(self, hash, limit=20, offset=0,
                                        d1=None, d2=None, qw=None, exportar=1,
                                        sametree=None, samesite=None):
        """
            call _getUltimosFilmesVotados to retrieve most voted content

            @hash: list of string of tree hash identification
            @limit: size of items to retrieve
            @offset: start index number of listing
            @d1: string that represent first date to start listing, '2010-01-20'
            @d2: string that represent the last date to listing, '2010-01-21'
            @qw: list of words that must have on listing items
            @exportar: True or False to indicate the url will be dinamic or static
        """
        self.request["exportar"] = exportar
        return self._getUltimosFilmesVotados(hash=hash,
                                               limit=limit,
                                               offset=offset,
                                               d1=d1,
                                               d2=d2,
                                               qw=qw,
                                               exportar=exportar,
                                               render=1,
                                               sametree=sametree,
                                               samesite=samesite)

 

    @dbconnectionapp
    def _getUltimosFilmesVotados(self, hash, limit=20, offset=0,
                                         d1=None, d2=None, qw=None,
                                         exportar=1, render=None,
                                         sametree=None, samesite=None):
        """
            call _getListContent method portal
            to retrieve the content's tree came from the parameter hash
            with more votes

            @hash: list of string of tree hash identification
            @limit: size of items to retrieve
            @offset: start index number of listing
            @d1: string that represent first date to start listing, '2010-01-20'
            @d2: string that represent the last date to listing, '2010-01-21'
            @qw: list of words that must have on listing items
            @exportar: True or False to indicate the url will be dinamic or static
            @render: True of False if the url must be complete or ssi include like

            >>> self._getUltimosFilmesVotafos(hash=['94169735419684109',
                                                corpo=1)
            {"res":[...], "qtde":10}
        """
        id_site_origin = getSiteByHost(self.id_site, self.request)
        if id_site_origin:
            id_site_origin = id_site_origin["id_site"]
            if id_site_origin == int(self.id_site):
                id_site_origin = None

        if type(hash) is not list:
            hash = [hash]

        site = getDadosSite(id_site=self.id_site,
                            request=self.request)
        base = site["base_html"]

        items = self._getListContent(id_site=self.id_site,
                                      hash=hash,
                                      comentario=False,
                                      acesso=None,
                                      acesso24h=None,
                                      voto=True,
                                      keywords=qw,
                                      de=d1,
                                      ate=d2,
                                      limit=limit,
                                      offset=offset,
                                      render=render,
                                      sametree=sametree,
                                      samesite=samesite,
                                      id_site_origin=id_site_origin)

        itens = []
        idcs = []
        idcsd = {}
        items_ = [i for i in items["itens"] 
                                if idcs.append(str(i["id_conteudo"])) or 1]
        if idcs:
            for i in self.execSql("select_svgs",
                                  id_conteudos=buffer(",".join(idcs))):
                idcsd[i["id_conteudo"]] = i

        for i in items_:

            if idcsd.get(i["id_conteudo"]):
                embed = i["serialized"]()["dados"]["video"][0]["embed"] != ""
                portal = Portal(self.id_site, self.request)
                rel = portal._getRelacionamentoConteudo(id_site=self.id_site,
                                                  schema=self.schema,
                                                  id_conteudo=i["id_conteudo"])
                galeria = False
                infografico = False
                for j in rel:
                    if j["meta_type"] == "foto":
                        galeria = True
                    elif j["meta_type"] == "infografico":
                        infografico = True
                i["audio"] = idcsd.get(i["id_conteudo"])["audio"]
                i["video"] = idcsd.get(i["id_conteudo"])["video"] or embed
                i["galeria"] = idcsd.get(i["id_conteudo"])["galeria"] or galeria
                i["infografico"] = infografico
            else:
                i["audio"] = None
                i["video"] = None
                i["galeria"] = None

            itens.append(i)

        return {"res":itens, "qtde":items["qtde"]}


    @jsoncallback
    def getUltimosFilmesComentados(self, hash, limit=20, offset=0,
                                           d1=None, d2=None, qw=None, exportar=1,
                                           sametree=None, samesite=None):
        """
        """
        self.request["exportar"] = exportar
        return self._getUltimosFilmesComentados(hash=hash,
                                                  limit=limit,
                                                  offset=offset,
                                                  d1=d1,
                                                  d2=d2,
                                                  qw=qw,
                                                  exportar=exportar,
                                                  render=1,
                                                  sametree=sametree,
                                                  samesite=samesite)


    @dbconnectionapp
    def _getUltimosFilmesComentados(self, hash, limit=20, offset=0,
                                            d1=None, d2=None, qw=None,
                                            exportar=1, render=None,
                                            sametree=None, samesite=None):
        """
        """
        id_site_origin = getSiteByHost(self.id_site, self.request)
        if id_site_origin:
            id_site_origin = id_site_origin["id_site"]
            if id_site_origin == int(self.id_site):
                id_site_origin = None

        if type(hash) is not list:
            hash = [hash]

        site = getDadosSite(id_site=self.id_site,
                            request=self.request)
        base = site["base_html"]

        items = self._getListContent(id_site=self.id_site,
                                      hash=hash,
                                      comentario=1,
                                      acesso=None,
                                      acesso24h=None,
                                      voto=None,
                                      keywords=qw,
                                      de=d1,
                                      ate=d2,
                                      limit=limit,
                                      offset=offset,
                                      render=render,
                                      sametree=sametree,
                                      samesite=samesite,
                                      id_site_origin=id_site_origin)

        itens = []
        idcs = []
        idcsd = {}
        items_ = [i for i in items["itens"] 
                                if idcs.append(str(i["id_conteudo"])) or 1]
        if idcs:
            for i in self.execSql("select_svgs",
                                  id_conteudos=buffer(",".join(idcs))):
                idcsd[i["id_conteudo"]] = i

        for i in items_:

            if idcsd.get(i["id_conteudo"]):
                embed = i["serialized"]()["dados"]["video"][0]["embed"] != ""
                portal = Portal(self.id_site, self.request)
                rel = portal._getRelacionamentoConteudo(id_site=self.id_site,
                                                  schema=self.schema,
                                                  id_conteudo=i["id_conteudo"])
                galeria = False
                infografico = False
                for j in rel:
                    if j["meta_type"] == "foto":
                        galeria = True
                    elif j["meta_type"] == "infografico":
                        infografico = True
                i["audio"] = idcsd.get(i["id_conteudo"])["audio"]
                i["video"] = idcsd.get(i["id_conteudo"])["video"] or embed
                i["galeria"] = idcsd.get(i["id_conteudo"])["galeria"] or galeria
                i["infografico"] = infografico
            else:
                i["audio"] = None
                i["video"] = None
                i["galeria"] = None

            itens.append(i)

        return {"res":itens, "qtde":items["qtde"]}



    @dbconnectionapp
    def maisUltimos(self, limit=20, offset=0, exportar=None, hash=[]):
        """
        """
        exportar = exportar or self.request.get("exportar")
        if not hash:
            hash = [i["hash"] for i in self.execSql("select_treeapp",
                                                    schema=self.schema)]

        return self._getUltimosFilmes(hash=hash,
                                        limit=limit,
                                        offset=offset,
                                        exportar=exportar)


    @dbconnectionapp
    def maisAcessados(self, limit=20, offset=0, exportar=None, hash=[]):
        """
        """
        exportar = exportar or self.request.get("exportar")
        if not hash:
            hash = [i["hash"] for i in self.execSql("select_treeapp",
                                                   schema=self.schema)]

        return self._getUltimosFilmesAcessados(hash=hash,
                                                 limit=limit,
                                                 offset=offset,
                                                 exportar=exportar)


    @dbconnectionapp
    def maisComentados(self, limit=20, offset=0, exportar=None, hash=[]):
        """
        """
        day = datetime.timedelta(days=2)
        today = datetime.date.today()
        yesterday = today - day

        exportar = exportar or self.request.get("exportar")
        if not hash:
            hash = [i["hash"] for i in self.execSql("select_treeapp",
                                                    schema=self.schema)]

        return self._getUltimosFilmesComentados(hash=hash,
                                                  limit=limit,
                                                  offset=offset,
                                                  exportar=exportar,
                                                  d1=yesterday.strftime("%d/%m/%Y"),
                                                  d2=today.strftime("%d/%m/%Y"))


    def getTags(self, limit=10):
        """
        """
        return self._getListTag(schema=self.schema,
                                 limit=int(limit))


    @dbconnectionapp
    def maisTag(self, tag, limit=5, exportar=None, offset=0, hash=[]):
        """
        """
        exportar = exportar or self.request.get("exportar")
        if not hash:
            hash = [i["hash"] for i in self.execSql("select_treeapp",
                                                    schema=self.schema)]

        return self._getUltimosFilmes(hash=hash,
                                        tags=[tag],
                                        limit=limit,
                                        offset=offset,
                                        exportar=exportar)


    @dbconnectionapp
    def maisFilme(self, limit=5, exportar=None, offset=0, hash=[]):
        """
        """
        exportar = exportar or self.request.get("exportar")
        if not hash:
            hash = [i["hash"] for i in self.execSql("select_treeapp",
                                                    schema=self.schema)]

        return self._getUltimosFilmes(hash=hash,
                                        tags=[],
                                        limit=limit,
                                        offset=offset,
                                        exportar=exportar)


    @dbconnectionapp
    def _ultimosAplicativo(self, offset=0, limit=25,
                                 exportar=None, render=None, dt=1):
        """
        """
        items = {"items":[], "qtde":0}
        exportar = self.request.get("exportar") or exportar
        items["qtde"] = self.execSql("select_ultimos_qtde").next()["qtde"]
        for i in self.execSql("select_ultimos",
                              offset=int(offset),
                              limit=int(limit)):
            i["url"] = self._getUrlByApp(env_site=self.id_site,
                                          schema=self.schema,
                                          id_conteudo=i["id_conteudo"],
                                          exportar=exportar,
                                          admin=render)
            ft = strptime(i["publicado_em"], "%d/%m/%Y %H:%M")
            if dt:
                i["datetime"] = lambda dt,ft=ft: strftime(dt, ft)
            items["items"].append(i)

        return items


    @jsoncallback
    def ultimosAplicativo(self, offset=0, limit=25):
        """
        """
        self.request["exportar"] = 1
        return self._ultimosAplicativo(offset=offset,
                                       limit=limit,
                                       dt=None,
                                       render=1)


    @dbconnectionapp
    def _UltimosApp(self, limit=50, offset=0, exportar=None):
        """
        """
        exportar = self.request.get("exportar") or exportar

        for i in self.execSql("select_ultimos_app",
                              schema=self.schema,
                              limit=int(limit),
                              offset=int(offset)):

            i["url"] = self._getUrlByApp(env_site=self.id_site,
                                          schema=self.schema,
                                          id_conteudo=i["id_conteudo"],
                                          exportar=exportar)
            yield i


    @dbconnectionapp
    def _maisUltimosApp(self, limit=50, offset=0, exportar=None,
                              dt=1, render=None, samesite=None):
        """
        """
        exportar = self.request.get("exportar") or exportar
 
        res = {"qtde":0, "res":[]} 
        for i in self.execSql("select_ultimos_app",
                              schema=self.schema,
                              limit=int(limit),
                              offset=int(offset)):

            i["url"] = self._getUrlByApp(env_site=self.id_site,
                                          schema=self.schema,
                                          id_conteudo=i["id_conteudo"],
                                          exportar=exportar,
                                          admin=render,
                                          samesite=samesite)
            if dt:
                i["datetime"] = lambda t, i=i["publicado_em"]:strftime(t, 
                                               strptime(i, "%Y-%m-%d %H:%M:%S"))
            res["res"].append(i)

        res["qtde"] = self.execSql("select_ultimos_app_qtde",
                                   schema=self.schema).next()["qtde"]

        return res


    @jsoncallback
    def maisUltimosApp(self, limit=50, offset=0):
        """
        """
        return self._maisUltimosApp(limit=limit,
                                    offset=offset,
                                    exportar=True,
                                    dt=None,
                                    render=1,
                                    samesite=1)


    @dbconnectionapp
    def UltimoDataEdicao(self, hash, data=None,
                       limit=50, offset=0, exportar=None):
        """
        """
        exportar = self.request.get("exportar") or exportar
        try:
            data = strptime(data, "%d/%m/%Y")
            data = strftime("%Y-%m-%d", data)
        except Exception, e:
            try:
                data = strptime(data, "%Y-%m-%d")
                data = strftime("%Y-%m-%d", data)
            except:
                data = None

        if not data:
            data = strftime("2099-%m-%d")

        if type(hash) is not list:
            hash = [hash]

        for i in hash:
            self.execSqlBatch("select_ultimo_data_edicao",
                              hash=i,
                              schema=self.schema,
                              data_edicao=data)

        for i in self.execSqlUnion(limit=int(limit),
                                   order="data_edicao DESC"):
            i["url"] = self._getUrlByApp(env_site=self.id_site,
                                          schema=self.schema,
                                          id_conteudo=i["id_conteudo"],
                                          exportar=exportar)
            yield i


    @dbconnectionapp
    def maisDataEdicao(self, hash, data=None,
                       limit=50, offset=0, exportar=None, render=None):
        """
        """
        exportar = self.request.get("exportar") or exportar
        try:
            data = strptime(data, "%Y-%m-%d")
            data = strftime("%Y-%m-%d", data)
        except Exception, e:
            data = None

        if not data:
            data = strftime("%Y-%m-%d")

        if type(hash) is not list:
            hash = [hash]

        for i in hash:
            self.execSqlBatch("select_data_edicao",
                              hash=i,
                              schema=self.schema,
                              data_edicao=data)

        for i in self.execSqlUnion(limit=int(limit),
                                   order="publicado_em DESC"):
            i["url"] = self._getUrlByApp(env_site=self.id_site,
                                          schema=self.schema,
                                          id_conteudo=i["id_conteudo"],
                                          exportar=exportar,
                                          admin=render)
            yield i


    @jsoncallback
    def maisDataEdicaoJx(self, hash, data=None,
                         limit=50, offset=0, exportar=None):
        """
        """
        exportar = exportar or self.request.get("exportar")
        return [i for i in self.maisDataEdicao(hash=hash,
                                               data=data,
                                               limit=limit,
                                               offset=offset,
                                               exportar=exportar,
                                               render=1)]
        
    @dbconnectionapp
    def _getAntProx(self, id_filme, publicado_em, exportar=None, render=None):
        """
           Returns a tuple with the previous and next content on the folder
        """
        p = strptime(publicado_em, "%d/%m/%Y %H:%M")
        publicado_em = strftime("%Y-%m-%d %H:%M:%S", p)
        prox = None
        ant = None
        for i in self.execSql("select_proximo", id_filme=id_filme,
                                                publicado_em=publicado_em,
                                                schema=self.schema):
            i["url"] = self._getUrlByApp(env_site=self.id_site,
                                          schema=self.schema,
                                          id_conteudo=i["id_conteudo"],
                                          exportar=exportar,
                                          admin=render)
            prox = i
        for i in self.execSql("select_anterior", id_filme=id_filme, 
                                                 publicado_em=publicado_em,
                                                 schema=self.schema):
            i["url"] = self._getUrlByApp(env_site=self.id_site,
                                          schema=self.schema,
                                          id_conteudo=i["id_conteudo"],
                                          exportar=exportar,
                                          admin=render)
            ant = i
        return ant, prox

    @dbconnectionapp
    @jsoncallback
    def votar(self, id_conteudo, nota):
        """
            Vota numa hipotese da enquete
        """
        if(id_conteudo and nota):
            block_voto = False
            id_rep = self.schema + id_conteudo
            response_headers = []

            if self.request.getCookie(id_rep):
                block_voto = True

            if not block_voto:
                self.execSqlu("update_filme_nota"+nota,
                             id_conteudo=int(id_conteudo))
                expires = (datetime.datetime.now() + datetime.timedelta(hours=24))
                self.request.setCookie(id_rep, "1")
                return 0
            else:
                return 1
        else:
            return 2

