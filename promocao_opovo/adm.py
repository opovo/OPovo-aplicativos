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
import random
from publica import settings
from xlwt import *
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
            cadastro['id_cadastro'] = i['id_cadastro']
            cadastro['data_hora_cadastro'] = i['data_hora_cadastro']
            retorno.append(cadastro)
        return retorno
        
    @dbconnectionapp
    def _getConteudoCamposCustom(self, id_conteudo):
        """
            returns all campos custom from conteudo

            >>> self._getCampo()
            <generator>
        """
        return self.execSql("select_conteudo_campos_custom",
                             id_conteudo=int(id_conteudo))

    @dbconnectionapp
    def _getCamposCustomItensMultiescolha(self, id_campos_custom):
        """
            returns all campos custom from conteudo

            >>> self._getCampo()
            <generator>
        """
        return self.execSql("select_campos_custom_itens_multiescolha",
                             id_campos_custom=int(id_campos_custom))

    @dbconnectionapp
    def _getCadastroCamposCustom(self, id_cadastro):
        """
            returns all campos custom from conteudo

            >>> self._getCampo()
            <generator>
        """
        return self.execSql("select_cadastro_campos_custom",
                             id_cadastro=int(id_cadastro))

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
                          publicado_em, campos=[], 
                          cc_nome_campo=[], cc_tipo_campo=[], cc_full_width=[], cc_obrigatorio=[], cc_qtd_itens=[], im_value=[], 
                          cartola=None, editor=None, editor2=None, imagem_rodape=None, imagem_bg_topo=None,
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

        # adicionar campos_custom
        contador_itens = 0
        for ncc in range(len(cc_nome_campo)):
            if(cc_nome_campo[ncc] and cc_tipo_campo[ncc]):
                id_campo_custom = self.execSql("select_nextval_campos_custom").next()["id"]
                full_width = True if cc_full_width[ncc] else False
                obrigatorio = True if cc_obrigatorio[ncc] else False
                cc_attr_id_name_campo = ''.join(e for e in cc_nome_campo[ncc].lower() if e.isalnum())+"_"+str(id_campo_custom)
                self.execSqlBatch("insert_campos_customi",
                              id_campos_custom=id_campo_custom,
                              id_conteudo=id_conteudo,
                              nome_campo=cc_nome_campo[ncc],
                              attr_id_name_campo=cc_attr_id_name_campo,
                              tipo_campo=cc_tipo_campo[ncc],
                              full_width=full_width,
                              obrigatorio=obrigatorio,
                              ordem=ncc+1)
                # adicionar itens_multiescolha
                for nim in range(int(cc_qtd_itens[ncc])):
                    if(im_value[contador_itens]):
                      self.execSqlBatch("insert_itens_multiescolha",
                                    id_campos_custom=id_campo_custom,
                                    value=im_value[contador_itens],
                                    ordem=nim+1)
                    contador_itens += 1

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
                          publicado_em, campos=[], 
                          cc_nome_campo=[], cc_tipo_campo=[], cc_full_width=[], cc_obrigatorio=[], cc_qtd_itens=[], im_value=[],  
                          cartola=None, editor=None, editor2=None, imagem_rodape=None, imagem_bg_topo=None, 
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

        # adicionar campos_custom
        contador_itens = 0
        for ncc in range(len(cc_nome_campo)):
            if(cc_nome_campo[ncc] and cc_tipo_campo[ncc]):
                id_campo_custom = self.execSql("select_nextval_campos_custom").next()["id"]
                full_width = True if cc_full_width[ncc] else False
                obrigatorio = True if cc_obrigatorio[ncc] else False
                cc_attr_id_name_campo = ''.join(e for e in cc_nome_campo[ncc].lower() if e.isalnum())+"_"+str(id_campo_custom)
                self.execSqlBatch("insert_campos_customi",
                              id_campos_custom=id_campo_custom,
                              id_conteudo=int(id_conteudo),
                              nome_campo=cc_nome_campo[ncc],
                              attr_id_name_campo=cc_attr_id_name_campo,
                              tipo_campo=cc_tipo_campo[ncc],
                              full_width=full_width,
                              obrigatorio=obrigatorio,
                              ordem=ncc+1)
                # adicionar itens_multiescolha
                for nim in range(int(cc_qtd_itens[ncc])):
                    if(im_value[contador_itens]):
                      self.execSqlBatch("insert_itens_multiescolha",
                                    id_campos_custom=id_campo_custom,
                                    value=im_value[contador_itens],
                                    ordem=nim+1)
                    contador_itens += 1

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

    def exportaXls(self, id_conteudo):
        n = self._getConteudo(id_conteudo)
        titulo = n['titulo'].replace(' ', '').lower()
        titulo = unicode(titulo, errors="ignore")
        titulo = ''.join(e for e in titulo if e.isalnum())
        cadastros = [i for i in self._getConteudoCadastros(id_conteudo=id_conteudo)]
        campos = [i for i in self._getConteudoCampos(id_conteudo=id_conteudo)]
        wb = Workbook()
        ws0 = wb.add_sheet('Participantes', cell_overwrite_ok=True)
        row_number=1
        for row in cadastros:
            column_num=0
            ws0.write(0,column_num,self.decoder("sequencial"))
            ws0.write(row_number,column_num,self.decoder(row['sequencial']))
            column_num=column_num+1
            for item in campos:
                ws0.write(0,column_num,self.decoder(item['nome']))
                ws0.write(row_number,column_num,self.decoder(row[item['nome']]))
                column_num=column_num+1
            ws0.write(0,column_num,self.decoder("data_hora_cadastro"))
            ws0.write(row_number,column_num,self.decoder(row['data_hora_cadastro']))
            row_number=row_number+1
        wb.save("{0}/ns{1}/arquivos/app/{2}/{3}.xls".format(str(settings.PATH_FILES),
                                                              str(self.id_site),
                                                              self.schema,
                                                              titulo))

    def decoder(self, val):
        """
        """
        try:
            val = val.decode(settings.GLOBAL_ENCODING) 
        except:
            pass
        return val