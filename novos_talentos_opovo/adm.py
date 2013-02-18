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
# adm.py novos_talentos_opovo
# modificado por Eric Mesquita em 17/12/2012
#
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
    def _getAllProvas(self):
        """
            returns all provas

            >>> self._getAllProvas()
            <generator>
        """
        return self.execSql("select_all_provas") 
        
    @dbconnectionapp
    def _getConteudoProvas(self, id_conteudo):
        """
            returns all provas from conteudo

            >>> self._getConteudoProvas()
            <generator>
        """
        return self.execSql("select_conteudo_provas",
                             id_conteudo=int(id_conteudo))

    @dbconnectionapp
    def _getConteudoCadastros(self, id_conteudo):
        """
            returns all cadastros from conteudo

            >>> self._getConteudoCadastros()
            <generator>
        """
        return self.execSql("select_conteudo_cadastros",
                             id_conteudo=int(id_conteudo))
        
    @dbconnectionapp
    def _getConteudoCadastrosSelecionados(self, id_conteudo):
        """
            returns all cadastros selecionados from conteudo

            >>> self._getConteudoCadastrosSelecionados()
            <generator>
        """
        return self.execSql("select_conteudo_cadastros_selecionados",
                             id_conteudo=int(id_conteudo))
                             
    @dbconnectionapp
    def _getCadastroCursosSuperiores(self, id_cadastro):
        """
            returns all cursos superiores from cadastro

            >>> self._getCadastroCursosSuperiores()
            <generator>
        """
        return self.execSql("select_cadastro_cursos_superiores",
                             id_cadastro=int(id_cadastro))
                             
    @dbconnectionapp
    def _getCadastroIdiomas(self, id_cadastro):
        """
            returns all idiomas from cadastro

            >>> self._getCadastroIdiomas()
            <generator>
        """
        return self.execSql("select_cadastro_idiomas",
                             id_cadastro=int(id_cadastro))

    @dbconnectionapp
    def _getCadastroCursos(self, id_cadastro):
        """
            returns all cursos from cadastro

            >>> self._getCadastroCursos()
            <generator>
        """
        return self.execSql("select_cadastro_cursos",
                             id_cadastro=int(id_cadastro))
                             
    @dbconnectionapp
    def _getCadastroEstagios(self, id_cadastro):
        """
            returns all estagios from cadastro

            >>> self._getCadastroEstagios()
            <generator>
        """
        return self.execSql("select_cadastro_estagios",
                             id_cadastro=int(id_cadastro))
                             
    @dbconnectionapp
    def _getCadastroEmpregos(self, id_cadastro):
        """
            returns all empregos from cadastro

            >>> self._getCadastroEmpregos()
            <generator>
        """
        return self.execSql("select_cadastro_empregos",
                             id_cadastro=int(id_cadastro))

    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def addConteudo(self, id_site, id_treeapp, id_aplicativo,
                          titulo, publicado_em, descricao=[], arquivo=[], editor=None, calendario=None, foto_galeria=None, foto_interna=None, 
                          legenda_foto_interna=None, destaque_capa=None, andamento=None, atualizado_em=None, publicado=None,
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
        if(foto_galeria):
            foto_galeria = self._addFile(arquivo=foto_galeria,
                                          id_conteudo=id_conteudo,
                                          schema=self.schema,
                                          dt=dt)
        if(foto_interna):
            foto_interna = self._addFile(arquivo=foto_interna,
                                          id_conteudo=id_conteudo,
                                          schema=self.schema,
                                          dt=dt)
                                          
        editor = True if editor else False
        
        self.execSqlBatch("insert_conteudo",
                          id_conteudo=id_conteudo,
                          titulo=titulo,
                          editor=editor,
                          calendario=calendario,
                          foto_galeria=foto_galeria,
                          foto_interna=foto_interna,
                          legenda_foto_interna=legenda_foto_interna,
                          destaque_capa=destaque_capa,
                          andamento=andamento,
                          publicado_em=publicado_em,
                          atualizado_em=atualizado_em,
                          publicado=publicado)
                          
        # adicionar provas
        if descricao or arquivo:
            for p in range(len(descricao)):
                id_prova = self.execSql("select_nextval_prova").next()["id"]
                descricao_prova = descricao[p]
                arquivo_prova = arquivo[p]
            
                if(arquivo_prova):
                    arquivo_prova = self._addFile(arquivo=arquivo_prova,
                                              id_conteudo=id_conteudo,
                                              schema=self.schema,
                                              dt=dt)
                                          
                self.execSqlBatch("insert_prova", 
                                  id_prova=int(id_prova), 
                                  id_conteudo=int(id_conteudo),
                                  descricao=descricao_prova,
                                  arquivo=arquivo_prova)

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

            return ("Curso cadastrado com sucesso! "
                    "Publica&ccedil;&atilde;o iniciada.")

        self._addLog("Novo curso cadastrado '%s'" % titulo)
        return "Curso cadastrado com sucesso."


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
    def editConteudo(self, id_site, id_treeapp, id_aplicativo, id_conteudo, 
                          titulo, publicado_em, descricao=[], arquivo=[], selecionado=[], editor=None, calendario=None, foto_galeria=None, foto_interna=None, 
                          legenda_foto_interna=None, destaque_capa=None, andamento=None, atualizado_em=None, publicado=None,
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
                          
        self.execSqlBatch("delete_prova",
                          id_conteudo=int(id_conteudo))

        self.execSqlBatch("update_conteudo_cadastros_desselecionados",
                          id_conteudo=int(id_conteudo))

        # imagens
        if(foto_galeria):
            foto_galeria = self._addFile(arquivo=foto_galeria,
                                          id_conteudo=id_conteudo,
                                          schema=self.schema,
                                          dt=dt)
        if(foto_interna):
            foto_interna = self._addFile(arquivo=foto_interna,
                                          id_conteudo=id_conteudo,
                                          schema=self.schema,
                                          dt=dt)

        editor = True if editor else False

        self.execSqlBatch("update_conteudo",
                          id_conteudo=int(id_conteudo),
                          titulo=titulo,
                          editor=editor,
                          calendario=calendario,
                          foto_galeria=foto_galeria,
                          foto_interna=foto_interna,
                          legenda_foto_interna=legenda_foto_interna,
                          destaque_capa=destaque_capa,
                          andamento=andamento,
                          publicado_em=publicado_em,
                          atualizado_em=atualizado_em,
                          publicado=publicado)
                          
        # adicionar provas
        if descricao or arquivo:
            for p in range(len(descricao)):
                id_prova = self.execSql("select_nextval_prova").next()["id"]
                descricao_prova = descricao[p]
                arquivo_prova = arquivo[p]
            
                if(arquivo_prova):
                    arquivo_prova = self._addFile(arquivo=arquivo_prova,
                                              id_conteudo=id_conteudo,
                                              schema=self.schema,
                                              dt=dt)
                                          
                self.execSqlBatch("insert_prova", 
                                  id_prova=int(id_prova), 
                                  id_conteudo=int(id_conteudo),
                                  descricao=descricao_prova,
                                  arquivo=arquivo_prova)

        # selecionados
        if selecionado:
            for p in range(len(selecionado)):
                self.execSqlBatch("update_cadastro_selecionado", 
                                  id_cadastro=int(selecionado[p]))
                

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

            self._addLog("Curso '%s' editado e publicado" % titulo)
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

            return ("Curso editado com sucesso! "
                    "Publica&ccedil;&atilde;o iniciada.")

        self._addLog("Curso editado '%s'" % titulo)
        return "Curso editado com sucesso."

    def exportaXls(self, id_conteudo):
        n = self._getConteudo(id_conteudo)
        titulo = n['titulo'].replace(' ', '').replace('ª', '').lower()
        cadastros = [i for i in self._getConteudoCadastros(id_conteudo=id_conteudo)]
        array1 = ['id_cadastro', 'id_conteudo', 'nome_completo', 'idade', 'data_nascimento', 'cpf', 'local_nascimento', 'nacionalidade', 'sexo', 'estado_civil', 'filhos', 'qtd_filhos', 'rua', 'numero', 'complemento', 'bairro', 'cep', 'cidade', 'estado', 'fone_fixo', 'fone_celular', 'email_principal', 'email_alternativo', 'faculdade_cursa', 'semestre', 'inicio_curso']
        array2 = ['inicio_medio', 'conclusao_medio', 'instituicao_medio']
        array3 = ['trabalha_opovo', 'setor_opovo', 'funcao_opovo', 'ativo_opovo', 'saida_opovo', 'participou', 'edicao_participou', 'fase_participou', 'portador', 'qual_necessidade', 'selecionado', 'data_hora_cadastro']
        arrayCs = ['id_curso_superior', 'data_inicio', 'data_conclusao', 'instituicao', 'curso']
        arrayId = ['id_idioma', 'idioma', 'grau_de_dominio']
        arrayC =  ['id_curso', 'data_inicio', 'data_conclusao', 'instituicao', 'curso']
        arrayEs =  ['id_estagio', 'atual', 'data_inicio', 'data_saida', 'empresa', 'funcao', 'horario']
        arrayEm =  ['id_emprego', 'atual', 'data_inicio', 'data_saida', 'empresa', 'funcao', 'horario']
        wb = Workbook()
        ws0 = wb.add_sheet('Participantes', cell_overwrite_ok=True)
        row_number=1
        for row in cadastros:
            id_cadastro = row['id_cadastro']
            column_num=0
            for item in array1:
                ws0.write(0,column_num,self.decoder(item))
                ws0.write(row_number,column_num,self.decoder(row[item]))
                column_num=column_num+1
            cs = [i for i in self._getCadastroCursosSuperiores(id_cadastro=id_cadastro)]
            for i in range(0,4):
                for item in arrayCs:
                    ws0.write(0,column_num,self.decoder(item))
                    try:
                        ws0.write(row_number,column_num,self.decoder(cs[i][item]))
                    except:
                        pass
                    column_num=column_num+1
            for item in array2:
                ws0.write(0,column_num,self.decoder(item))
                ws0.write(row_number,column_num,self.decoder(row[item]))
                column_num=column_num+1
            id = [i for i in self._getCadastroIdiomas(id_cadastro=id_cadastro)]
            for i in range(0,4):
                for item in arrayId:
                    ws0.write(0,column_num,self.decoder(item))
                    try:
                        ws0.write(row_number,column_num,self.decoder(id[i][item]))
                    except:
                        pass
                    column_num=column_num+1
            c = [i for i in self._getCadastroCursos(id_cadastro=id_cadastro)]
            for i in range(0,4):
                for item in arrayC:
                    ws0.write(0,column_num,self.decoder(item))
                    try:
                        ws0.write(row_number,column_num,self.decoder(c[i][item]))
                    except:
                        pass
                    column_num=column_num+1
            ws0.write(0,column_num,self.decoder('estagia'))
            ws0.write(row_number,column_num,self.decoder(row['estagia']))
            column_num=column_num+1
            es = [i for i in self._getCadastroEstagios(id_cadastro=id_cadastro)]
            for i in range(0,4):
                for item in arrayEs:
                    ws0.write(0,column_num,self.decoder(item))
                    try:
                        ws0.write(row_number,column_num,self.decoder(es[i][item]))
                    except:
                        pass
                    column_num=column_num+1
            ws0.write(0,column_num,self.decoder('trabalha'))
            ws0.write(row_number,column_num,self.decoder(row['trabalha']))
            column_num=column_num+1
            em = [i for i in self._getCadastroEmpregos(id_cadastro=id_cadastro)]
            for i in range(0,4):
                for item in arrayEm:
                    ws0.write(0,column_num,self.decoder(item))
                    try:
                        ws0.write(row_number,column_num,self.decoder(em[i][item]))
                    except:
                        pass
                    column_num=column_num+1
            for item in array3:
                ws0.write(0,column_num,self.decoder(item))
                ws0.write(row_number,column_num,self.decoder(row[item]))
                column_num=column_num+1
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