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
# public.py novos_talentos_opovo
# modificado por Eric Mesquita em 17/12/2012
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
    @jsoncallback
    def addCadastro(self, id_conteudo, participou=None, edicao_participou=None, fase_participou=None,
                    nome_completo=None, cpf=None, idade=None, data_nascimento=None, local_nascimento=None, nacionalidade=None,
                    sexo=None, estado_civil=None, filhos=None, qtd_filhos=None, rua=None, numero=None, complemento=None,
                    bairro=None, cep=None, cidade=None, estado=None, fone_fixo=None, fone_celular=None, email_principal=None, 
                    email_alternativo=None, faculdade_cursa=None, semestre=None, inicio_curso=None, inicio_medio=None, 
                    conclusao_medio=None, instituicao_medio=None, estagia=None, trabalha=None, trabalha_opovo=None, 
                    setor_opovo=None, funcao_opovo=None, ativo_opovo=None, saida_opovo=None, portador=None, qual_necessidade=None, 
                    cursos_superiores=[], idiomas=[], cursos=[], estagios=[], empregos=[]):
        """
            cadastra participante
        """
        try:
            count_cpf = self.execSql("select_cpf_cadastros",
                                 id_conteudo=int(id_conteudo),
                                 cpf=cpf).next()['count']
            if(count_cpf):
                #cpf já cadastrado
                return 2
            id_cadastro = self.execSql("select_nextval_cadastro").next()["id"]
            
            try:
                idade = int(idade)
            except:
                idade = 0
                
            try:
                semestre = int(semestre)
            except:
                semestre = 0

            self.execSqlBatch("insert_cadastro",
                      id_cadastro=int(id_cadastro),
                      id_conteudo=int(id_conteudo),
                      participou=participou,
                      edicao_participou=edicao_participou,
                      fase_participou=fase_participou,
                      nome_completo=nome_completo,
                      cpf=cpf,
                      idade=idade,
                      data_nascimento=data_nascimento,
                      local_nascimento=local_nascimento,
                      nacionalidade=nacionalidade,
                      sexo=sexo,
                      estado_civil=estado_civil,
                      filhos=filhos,
                      qtd_filhos=qtd_filhos,
                      rua=rua,
                      numero=numero,
                      complemento=complemento,
                      bairro=bairro,
                      cep=cep,
                      cidade=cidade,
                      estado=estado,
                      fone_fixo=fone_fixo,
                      fone_celular=fone_celular,
                      email_principal=email_principal,
                      email_alternativo=email_alternativo,
                      faculdade_cursa=faculdade_cursa,
                      semestre=semestre,
                      inicio_curso=inicio_curso,
                      inicio_medio=inicio_medio,
                      conclusao_medio=conclusao_medio,
                      instituicao_medio=instituicao_medio,
                      estagia=estagia,
                      trabalha=trabalha,
                      trabalha_opovo=trabalha_opovo,
                      setor_opovo=setor_opovo,
                      funcao_opovo=funcao_opovo,
                      ativo_opovo=ativo_opovo,
                      saida_opovo=saida_opovo,
                      portador=portador,
                      qual_necessidade=qual_necessidade)
                      
            # cadastro cursos superiores
            for i in cursos_superiores:
                id_curso_superior = self.execSql("select_nextval_curso_superior").next()["id"]
                self.execSqlBatch("insert_curso_superior",
                      id_curso_superior=int(id_curso_superior),
                      id_cadastro=int(id_cadastro),
                      data_inicio=i['data_inicio'],
                      data_conclusao=i['data_conclusao'],
                      instituicao=i['instituicao'],
                      curso=i['curso'])
                      
            # cadastro idiomas
            for i in idiomas:
                id_idioma = self.execSql("select_nextval_idioma").next()["id"]
                self.execSqlBatch("insert_idioma",
                      id_idioma=int(id_idioma),
                      id_cadastro=int(id_cadastro),
                      idioma=i['idioma'],
                      grau_de_dominio=i['grau_de_dominio'])
                    
            # cadastro cursos
            for i in cursos:
                id_curso = self.execSql("select_nextval_curso").next()["id"]
                self.execSqlBatch("insert_curso",
                      id_curso=int(id_curso),
                      id_cadastro=int(id_cadastro),
                      data_inicio=i['data_inicio'],
                      data_conclusao=i['data_conclusao'],
                      instituicao=i['instituicao'],
                      curso=i['curso'])
                      
            # cadastro estagios
            for i in estagios:
                id_estagio = self.execSql("select_nextval_estagio").next()["id"]
                self.execSqlBatch("insert_estagio",
                      id_estagio=int(id_estagio),
                      id_cadastro=int(id_cadastro),
                      data_inicio=i['data_inicio'],
                      data_saida=i['data_saida'],
                      empresa=i['empresa'],
                      funcao=i['funcao'],
                      horario=i['horario'],
                      atual=i['atual'])
                      
            # cadastro empregos
            for i in empregos:
                id_emprego = self.execSql("select_nextval_emprego").next()["id"]
                self.execSqlBatch("insert_emprego",
                      id_emprego=int(id_emprego),
                      id_cadastro=int(id_cadastro),
                      data_inicio=i['data_inicio'],
                      data_saida=i['data_saida'],
                      empresa=i['empresa'],
                      funcao=i['funcao'],
                      horario=i['horario'],
                      atual=i['atual'])

            self.execSqlCommit()
            return 0
        except:
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
            soup = BeautifulSoup(conteudo["calendario"],
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
            conteudo["calendario"] = unquote( unicode(soup) )
        return conteudo
        
    @jsoncallback
    def getUltimoCurso(self, hash, limit=1, offset=0,
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
        return self._getUltimoCurso(hash=hash,
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
    def _getUltimoCurso(self, hash, limit=1, offset=0,
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