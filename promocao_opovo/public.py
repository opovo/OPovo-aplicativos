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
from publica import settings
from publica.admin.exchange import getDadosSite, getSiteByHost
from publica.utils.json import encode, decode
from publica.utils.decorators import dbconnectionapp, serialize, jsoncallback
from publica.utils.BeautifulSoup import BeautifulSoup
from urllib import splitquery, splitvalue, unquote, quote


class Public(object):

    """
        public class of methods of this content
    """

    @dbconnectionapp
    def getConteudoCamposCustom(self, id_conteudo):
        """
            returns all campos custom from conteudo

            >>> self._getCampo()
            <generator>
        """
        return [i for i in self.execSql("select_conteudo_campos_custom", id_conteudo=int(id_conteudo))]

    @dbconnectionapp
    @jsoncallback
    def addCadastro(self, id_conteudo, cpf=None, rg=None, data_nascimento=None, nome=None,
                    endereco=None, complemento=None, bairro=None, cep=None, email=None,
                    profissao=None, faculdade=None, curso=None, facebook=None, twitter=None, fone1=None, fone2=None,
                    fone3=None, anexo=None, frase=None, opt_midia=None, opt_leitor=None, opt_cenario=None, opt_conhecimento=None,
                    opt_parceiro=None, opt_opovo=None, cadastro_campos_custom={}):
        """
            cadastra participante da promocao
        """
        try:
            conteudo = self._getConteudoPublicado(id_conteudo=id_conteudo)
            for i in conteudo['campos']:
                if (i['nome'] != 'complemento' and i['nome'] != 'fone2' and i['nome'] != 'fone3' and i['nome'] != 'opt_parceiro' and i['nome'] != 'opt_opovo' and i['nome'] != 'facebook' and i['nome'] != 'twitter' and i['nome'] != 'opt_conhecimento'):
                    if not eval(i['nome']):
                        #algum campo não for preenchido
                        return 3
            
            if(conteudo['cadastro_unico']):
                count_cpf = self.execSql("select_cpf_cadastros",
                                     id_conteudo=int(id_conteudo),
                                     cpf=cpf).next()['count']
                if(count_cpf):
                    #cpf já cadastrado
                    return 2
            id_cadastro = self.execSql("select_nextval_cadastro").next()["id"]

            sequencial = self.execSql("select_maxval_sequencial_conteudo_cadastros",
                                 id_conteudo=int(id_conteudo)).next()['max']
            if(sequencial):
                sequencial = int(sequencial)+1
            else:
                sequencial = 1
            self.execSqlBatch("insert_cadastro",
                      id_cadastro=int(id_cadastro),
                      id_conteudo=int(id_conteudo),
                      sequencial=int(sequencial),
                      cpf=cpf,
                      rg=rg,
                      data_nascimento=data_nascimento,
                      nome=nome,
                      endereco=endereco,
                      complemento=complemento,
                      bairro=bairro,
                      cep=cep,
                      email=email,
                      profissao=profissao,
                      faculdade=faculdade,
                      curso=curso,
                      facebook=facebook,
                      twitter=twitter,
                      fone1=fone1,
                      fone2=fone2,
                      fone3=fone3,
                      anexo=anexo,
                      frase=frase,
                      opt_midia=opt_midia,
                      opt_leitor=opt_leitor,
                      opt_cenario=opt_cenario,
                      opt_conhecimento=opt_conhecimento,
                      opt_parceiro=opt_parceiro,
                      opt_opovo=opt_opovo)
            
            #adicionar campos_custom
            if(cadastro_campos_custom):
                for i in cadastro_campos_custom:
                    if(isinstance(cadastro_campos_custom[i], (list))):
                        valor = ""
                        for j in cadastro_campos_custom[i]:
                            valor += j+' '
                        cadastro_campos_custom[i] = valor
                    self.execSqlBatch("insert_cadastro_campos_custom",
                              id_cadastro=int(id_cadastro),
                              id_campos_custom=int(i),
                              valor=cadastro_campos_custom[i])
            self.execSqlCommit()
            return 0
        except:
            #erro tente novamente
            return 1
            
    def _formatarCorpo(self, corpo, editor=None):
        """
            format text body with the photos related to the content
        """
        if not corpo:
            corpo = ""
        if not editor:
            corpo = corpo.replace("\n", "<br/>")
        return corpo
        
    @dbconnectionapp
    def _getConteudoPublicado(self, id_conteudo=None, mkl=None):
        """
            returns the data from a news content

            @mkl: overwrites de default render method of links

            >>> self._getConteudoPublicado(id_filme=1)
            {'id_conteudo':, 'titulo':, 'cartola':, 'descricao':, 'editor':,
             'regulamento':, 'imagem_topo_list':, 'imagem_rodape':, 'cor':, 'cadastro_unico':,
             'publicado_em':, 'publicado':, 'atualizado_em':, "
             'id_destaque':, 'titulo_destaque':, 'descricao_destaque':,
             'imagem_destaque':, 'titulo_tree':, 'breadcrump':}
        """
        conteudo = None
        for conteudo in self.execSql("select_dados",
                                    id_conteudo=int(id_conteudo)):
            break

        if conteudo:
            soup = BeautifulSoup(conteudo["regulamento"],
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
            conteudo["regulamento"] = unquote( unicode(soup) )
            
            soup = BeautifulSoup(conteudo["descricao"],
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
            conteudo["descricao"] = unquote( unicode(soup) )
            conteudo["campos"] = [i for i in self.execSql("select_conteudo_campos",
                                                        id_conteudo=int(conteudo["id_conteudo"]))]
        return conteudo
        
    @jsoncallback
    def getUltimasPromocoes(self, hash, limit=20, offset=0,
                                 d1=None, d2=None, qw=None,
                                 exportar=1, corpo=None,
                                 sametree=None, samesite=None):
        """
            call _getUltimasPromocoes method to return list of content
            
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
        return self._getUltimasPromocoes(hash=hash,
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
    def _getUltimasPromocoes(self, hash, limit=20, offset=0,
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

            >>> self._getUltimasNoticias(hash=['94169735419684109', '198413574648732'],
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
        for i in items_:
            i['dados'] = self._getConteudoPublicado(id_conteudo=i["id_conteudo"])    

        return items_