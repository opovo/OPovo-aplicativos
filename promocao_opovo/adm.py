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
# modificado por Eric Mesquita em 12/11/2012
#
from time import time, strftime, strptime
from urllib import unquote
from publica.admin.error import UserError
from publica.utils.json import encode
from publica.utils.decorators import serialize, dbconnectionapp,\
                                     Permission

class Adm(object):
    """
    """

    @dbconnectionapp
    def _getCampo(self):
        """
            returns all campos

            >>> self._getCampo()
            <generator>
        """
        return self.execSql("select_campo") 
        
    @dbconnectionapp
    def _getConteudoCampos(self, id_conteudo):
        """
            returns all campos from conteudo

            >>> self._getCampo()
            <generator>
        """
        return self.execSql("select_conteudo_campos",
                             id_conteudo=int(id_conteudo))

    @dbconnectionapp
    def _getConteudoCadastros(self, id_conteudo):
        """
            returns all cadastros from conteudo

            >>> self._getCampo()
            <generator>
        """
        retorno = []
        cadastros = [i for i in self.execSql("select_conteudo_cadastros",
                             id_conteudo=int(id_conteudo))]
        campos = [i for i in self._getConteudoCampos(id_conteudo=id_conteudo)]
        for i in cadastros:
            cadastro = {}
            for j in campos:
                cadastro[j['nome']] = i[j['nome']]
            cadastro['sequencial'] = i['sequencial']
            cadastro['data_hora_cadastro'] = i['data_hora_cadastro']
            retorno.append(cadastro)
        return retorno
        
    @dbconnectionapp
    def _getConteudoCadastroVencedor(self, id_conteudo, sequencial):
        """
            returns all cadastros from conteudo

            >>> self._getCampo()
            <generator>
        """
        cadastros = [i for i in self.execSql("select_conteudo_cadastro_vencedor",
                             id_conteudo=int(id_conteudo),
                             sequencial=int(sequencial))]
        if (cadastros):
            campos = [i for i in self._getConteudoCampos(id_conteudo=id_conteudo)]
            cadastro = {}
            for j in campos:
                cadastro[j['nome']] = cadastros[0][j['nome']]
            cadastro['sequencial'] = cadastros[0]['sequencial']
            return cadastro
        else:
            return None

    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def addConteudo(self, id_site, id_treeapp, id_aplicativo,
                          titulo, descricao, regulamento, imagem_topo_list, 
                          publicado_em, campos=[], cartola=None, editor=None, editor2=None, imagem_rodape=None, imagem_bg_topo=None, 
                          imagem_bg_rodape=None, cor=None, cadastro_unico=None, vencedor=None, atualizado_em=None, publicado=None,
                          titulo_destaque=None, descricao_destaque=None,
                          imagem_destaque=None, peso_destaque=None,
                          relacionamento=[], tags="", permissao=None,
                          exportar_xml=None, exportar_json=None,
                          exportar=None):
        """
        """
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
            p = strptime(atualizado_em, "%d/%m/%Y %H:%M")
            atualizado_em = strftime("%Y-%m-%d %H:%M", p)
        except ValueError, e:
           atualizado_em = None

        # inserir conteudo
        id_conteudo = self.execSql("select_nextval_conteudo").next()["id"]
        
        # imagens
        imagem_topo_list = self._addFile(arquivo=imagem_topo_list,
                                         id_conteudo=id_conteudo,
                                         schema=self.schema,
                                         dt=dt)
        if(imagem_rodape):
            imagem_rodape = self._addFile(arquivo=imagem_rodape,
                                          id_conteudo=id_conteudo,
                                          schema=self.schema,
                                          dt=dt)
        if(imagem_bg_topo):
            imagem_bg_topo = self._addFile(arquivo=imagem_bg_topo,
                                          id_conteudo=id_conteudo,
                                          schema=self.schema,
                                          dt=dt)
        if(imagem_bg_rodape):
            imagem_bg_rodape = self._addFile(arquivo=imagem_bg_rodape,
                                          id_conteudo=id_conteudo,
                                          schema=self.schema,
                                          dt=dt)
                                          
        editor = True if editor else False
        editor2 = True if editor2 else False
        
        self.execSqlBatch("insert_conteudo",
                          id_conteudo=id_conteudo,
                          titulo=titulo,
                          cartola=cartola,
                          descricao=descricao,
                          editor=editor,
                          editor2=editor2,
                          regulamento=regulamento,
                          imagem_topo_list=imagem_topo_list,
                          imagem_rodape=imagem_rodape,
                          imagem_bg_topo=imagem_bg_topo,
                          imagem_bg_rodape=imagem_bg_rodape,
                          cor=cor,
                          cadastro_unico=cadastro_unico,
                          vencedor=vencedor,
                          publicado_em=publicado_em,
                          atualizado_em=atualizado_em,
                          publicado=publicado)
                          
        # adicionar campos
        for t in campos:
            self.execSqlBatch("insert_conteudo_campo", 
                              id_conteudo=id_conteudo,
                              id_campo=int(t))

        # inserindo os destaques
        dados_destaque = []
        if titulo_destaque or imagem_destaque or descricao_destaque:
            imagem_destaque = self._addFile(arquivo=imagem_destaque,
                                             id_conteudo=id_conteudo,
                                             schema=self.schema,
                                             dt=dt)
            if not imagem_destaque:
                imagem_destaque = None

            try:
                peso_destaque = int(peso_destaque)
            except:
                peso_destaque = 0

            self.execSqlBatch("insert_destaque", 
                              id_conteudo=id_conteudo,
                              titulo=titulo_destaque,
                              descricao=descricao_destaque,
                              img=imagem_destaque,
                              peso=peso_destaque)

        self.execSqlCommit()

        # acoes para o portal
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
                               atualizado_em=atualizado_em,
                               titulo_destaque=titulo_destaque,
                               descricao_destaque=descricao_destaque,
                               imagem_destaque=imagem_destaque,
                               tags=tags,
                               permissao=permissao,
                               relacionamento=relacionamento,
                               dados=dados)

        if exportar_xml or exportar_json or exportar:

            self._addLog("Novo conteudo cadastrado e publicado '%s'" % titulo)
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

            return ("Promo&ccedil;&atilde;o cadastrada com sucesso! "
                    "Publica&ccedil;&atilde;o iniciada.")

        self._addLog("Nova promo&ccedil;&atilde;o cadastrada '%s'" % titulo)
        return "Promo&ccedil;&atilde;o cadastrada com sucesso."


    @dbconnectionapp
    @Permission("PERM APP")
    def _getConteudo(self, id_conteudo):
        """
        """
        for i in self.execSql("select_conteudo",
                              id_conteudo=int(id_conteudo)):
            return i


    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def editConteudo(self, id_conteudo, id_site, id_treeapp, id_aplicativo,
                          titulo, descricao, regulamento, imagem_topo_list, 
                          publicado_em, campos=[], cartola=None, editor=None, editor2=None, imagem_rodape=None, imagem_bg_topo=None, 
                          imagem_bg_rodape=None, cor=None, cadastro_unico=None, vencedor=None, atualizado_em=None, publicado=None,
                          titulo_destaque=None, descricao_destaque=None,
                          imagem_destaque=None, peso_destaque=None,
                          relacionamento=[], tags="", permissao=None,
                          exportar_xml=None, exportar_json=None,
                          exportar=None):
        """
        """
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
            p = strptime(atualizado_em, "%d/%m/%Y %H:%M")
            atualizado_em = strftime("%Y-%m-%d %H:%M", p)
        except ValueError, e:
           atualizado_em = None


        # deletar conteudo tabela destaques ou outras tabelas
        self.execSqlBatch("delete_destaque",
                          id_conteudo=int(id_conteudo))
                          
        self.execSqlBatch("delete_dados_conteudo",
                          id_conteudo=int(id_conteudo))
                          
        # imagens
        imagem_topo_list = self._addFile(arquivo=imagem_topo_list,
                                         id_conteudo=id_conteudo,
                                         schema=self.schema,
                                         dt=dt)
        if(imagem_rodape):
            imagem_rodape = self._addFile(arquivo=imagem_rodape,
                                          id_conteudo=id_conteudo,
                                          schema=self.schema,
                                          dt=dt)
        if(imagem_bg_topo):
            imagem_bg_topo = self._addFile(arquivo=imagem_bg_topo,
                                          id_conteudo=id_conteudo,
                                          schema=self.schema,
                                          dt=dt)
        if(imagem_bg_rodape):
            imagem_bg_rodape = self._addFile(arquivo=imagem_bg_rodape,
                                          id_conteudo=id_conteudo,
                                          schema=self.schema,
                                          dt=dt)

        editor = True if editor else False
        editor2 = True if editor2 else False

        self.execSqlBatch("update_conteudo",
                          id_conteudo=int(id_conteudo),
                          titulo=titulo,
                          cartola=cartola,
                          descricao=descricao,
                          editor=editor,
                          editor2=editor2,
                          regulamento=regulamento,
                          imagem_topo_list=imagem_topo_list,
                          imagem_rodape=imagem_rodape,
                          imagem_bg_topo=imagem_bg_topo,
                          imagem_bg_rodape=imagem_bg_rodape,
                          cor=cor,
                          cadastro_unico=cadastro_unico,
                          vencedor=vencedor,
                          publicado_em=publicado_em,
                          atualizado_em=atualizado_em,
                          publicado=publicado)
                          
        # adicionar campos
        for dir in campos:
            self.execSqlBatch("insert_conteudo_campo",
                              id_conteudo=int(id_conteudo),
                              id_campo=int(dir))

        # inserindo os destaques
        dados_destaque = []
        if titulo_destaque or imagem_destaque or descricao_destaque:
            imagem_destaque = self._addFile(arquivo=imagem_destaque,
                                             id_conteudo=id_conteudo,
                                             schema=self.schema,
                                             dt=dt)
            if not imagem_destaque:
                imagem_destaque = None

            try:
                peso_destaque = int(peso_destaque)
            except:
                peso_destaque = 0

            self.execSqlBatch("insert_destaque", 
                              id_conteudo=int(id_conteudo),
                              titulo=titulo_destaque,
                              descricao=descricao_destaque,
                              img=imagem_destaque,
                              peso=peso_destaque)

        self.execSqlCommit()

        # acoes para o portal
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
                                atualizado_em=atualizado_em,
                                titulo_destaque=titulo_destaque,
                                descricao_destaque=descricao_destaque,
                                imagem_destaque=imagem_destaque,
                                permissao=permissao,
                                tags=tags,
                                relacionamento=relacionamento,
                                dados=dados)

        if exportar_xml or exportar_json or exportar:

            self._addLog("Promo&ccedil;&atilde;o '%s' editada e publicada" % titulo)
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

            return ("Promo&ccedil;&atilde;o editada com sucesso! "
                    "Publica&ccedil;&atilde;o iniciada.")

        self._addLog("Promo&ccedil;&atilde;o editada '%s'" % titulo)
        return "Promo&ccedil;&atilde;o editada com sucesso."



