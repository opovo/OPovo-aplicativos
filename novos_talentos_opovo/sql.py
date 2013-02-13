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
# sql.py novos_talentos_opovo
# modificado por Eric Mesquita em 10/12/2012
#

select_all_provas = ("SELECT * "
"FROM rschemar.prova "
"ORDER BY id_conteudo ASC")

select_conteudo_provas = ("SELECT * "
"FROM rschemar.prova "
"WHERE id_conteudo=%(id_conteudo)i ORDER BY id_prova ASC")

select_conteudo_cadastros = ("SELECT * "
"FROM rschemar.cadastro "
"WHERE id_conteudo=%(id_conteudo)i ORDER BY nome_completo ASC")

select_cpf_cadastros = ("SELECT COUNT(*) FROM rschemar.cadastro "
"WHERE id_conteudo=%(id_conteudo)i AND cpf=%(cpf)s")

select_conteudo_cadastros_selecionados = ("SELECT * "
"FROM rschemar.cadastro "
"WHERE id_conteudo=%(id_conteudo)i "
"AND selecionado = TRUE "
"ORDER BY id_cadastro ASC")

select_cadastro_cursos_superiores = ("SELECT * "
"FROM rschemar.curso_superior "
"WHERE id_cadastro=%(id_cadastro)i ORDER BY id_curso_superior ASC")

select_cadastro_idiomas = ("SELECT * "
"FROM rschemar.idioma "
"WHERE id_cadastro=%(id_cadastro)i ORDER BY id_idioma ASC")

select_cadastro_cursos = ("SELECT * "
"FROM rschemar.curso "
"WHERE id_cadastro=%(id_cadastro)i ORDER BY id_curso ASC")

select_cadastro_estagios = ("SELECT * "
"FROM rschemar.estagio "
"WHERE id_cadastro=%(id_cadastro)i ORDER BY id_estagio ASC")

select_cadastro_empregos = ("SELECT * "
"FROM rschemar.emprego "
"WHERE id_cadastro=%(id_cadastro)i ORDER BY id_emprego ASC")

select_nextval_prova = ("SELECT NEXTVAL('rschemar.prova_id_prova_seq'::text) as id")

select_nextval_conteudo = ("SELECT NEXTVAL('rschemar.conteudo_id_conteudo_seq'::text) as id")

select_nextval_cadastro = ("SELECT NEXTVAL('rschemar.cadastro_id_cadastro_seq'::text) as id")

select_nextval_curso_superior = ("SELECT NEXTVAL('rschemar.curso_superior_id_curso_superior_seq'::text) as id")

select_nextval_idioma = ("SELECT NEXTVAL('rschemar.idioma_id_idioma_seq'::text) as id")

select_nextval_curso = ("SELECT NEXTVAL('rschemar.curso_id_curso_seq'::text) as id")

select_nextval_estagio = ("SELECT NEXTVAL('rschemar.estagio_id_estagio_seq'::text) as id")

select_nextval_emprego = ("SELECT NEXTVAL('rschemar.emprego_id_emprego_seq'::text) as id")

select_status_content = ("SELECT publicado FROM rschemar.conteudo "
"WHERE id_conteudo=%(id_conteudo)i")

select_dados = ("SELECT N.id_conteudo, N.titulo, N.calendario, N.foto_galeria, "
"N.foto_interna, N.legenda_foto_interna, N.destaque_capa, N.andamento, N.editor, "
"to_char(N.expira_em, 'YYYY-MM-DD HH24:MI') as expira_em, "
"to_char(N.publicado_em, 'YYYY-MM-DD HH24:MI') as publicado_em, N.publicado, "
"to_char(N.atualizado_em, 'YYYY-MM-DD HH24:MI') as atualizado_em, "
"D.id_destaque, D.titulo as titulo_destaque, D.descricao as descricao_destaque, "
"D.img, D.img as imagem_destaque, D.peso as peso_destaque "
"FROM rschemar.conteudo N "
"LEFT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo) "
"WHERE N.id_conteudo=%(id_conteudo)i")

select_titulo = ("SELECT titulo FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i")

select_dublin_core = ("SELECT titulo, calendario, "
"to_char(atualizado_em, 'YYYY-MM-DD HH24:MI:SS') as atualizado_em, "
"to_char(publicado_em, 'YYYY-MM-DD HH24:MI:SS') as publicado_em "
"FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i")

select_conteudo = ("SELECT N.id_conteudo, N.titulo, N.calendario, N.foto_galeria, "
"N.foto_interna, N.legenda_foto_interna, N.destaque_capa, N.andamento, N.editor, "
"to_char(N.atualizado_em, 'DD/MM/YYYY HH24:MI') as atualizado_em, "
"to_char(N.publicado_em, 'DD/MM/YYYY HH24:MI') as publicado_em, N.publicado, "
"D.id_destaque, D.titulo as titulo_destaque, D.descricao as descricao_destaque, "
"D.img, D.img as imagem_destaque, D.peso as peso_destaque "
"FROM rschemar.conteudo N "
"LEFT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo) "
"WHERE N.id_conteudo=%(id_conteudo)i")

insert_conteudo = ("INSERT INTO rschemar.conteudo (id_conteudo, titulo, editor, "
"calendario, foto_galeria, foto_interna, legenda_foto_interna, destaque_capa, andamento, "
"publicado_em, atualizado_em, publicado) VALUES (%(id_conteudo)i, %(titulo)s, %(editor)s, "
"%(calendario)s, %(foto_galeria)s, %(foto_interna)s, %(legenda_foto_interna)s, %(destaque_capa)s, "
"%(andamento)s, %(publicado_em)s, %(atualizado_em)s, %(publicado)s)")

insert_destaque  = ("INSERT INTO rschemar.destaque (id_conteudo, titulo, descricao, img, peso) VALUES "
"(%(id_conteudo)i, %(titulo)s, %(descricao)s, %(img)s, %(peso)i)")

insert_prova = ("INSERT INTO rschemar.prova (id_prova, id_conteudo, descricao, arquivo) VALUES "
"(%(id_prova)d, %(id_conteudo)d, %(descricao)s, %(arquivo)s)")

insert_cadastro = ("INSERT INTO rschemar.cadastro (id_cadastro, id_conteudo, participou, edicao_participou, "
"fase_participou, nome_completo, cpf, idade, data_nascimento, local_nascimento, nacionalidade, sexo, estado_civil, "
"filhos, qtd_filhos, rua, numero, complemento, bairro, cep, cidade, estado, fone_fixo, fone_celular, email_principal, "
"email_alternativo, faculdade_cursa, semestre, inicio_curso, inicio_medio, conclusao_medio, instituicao_medio, estagia, "
"trabalha, trabalha_opovo, setor_opovo, funcao_opovo, ativo_opovo, saida_opovo, portador, qual_necessidade, data_hora_cadastro) "
"VALUES (%(id_cadastro)i, %(id_conteudo)i, %(participou)s, %(edicao_participou)s, %(fase_participou)s, %(nome_completo)s, %(cpf)s, "
"%(idade)i, %(data_nascimento)s, %(local_nascimento)s, %(nacionalidade)s, %(sexo)s, %(estado_civil)s, %(filhos)s, "
"%(qtd_filhos)s, %(rua)s, %(numero)s, %(complemento)s, %(bairro)s, %(cep)s, %(cidade)s, %(estado)s, %(fone_fixo)s, "
"%(fone_celular)s, %(email_principal)s, %(email_alternativo)s, %(faculdade_cursa)s, %(semestre)i, %(inicio_curso)s, "
"%(inicio_medio)s, %(conclusao_medio)s, %(instituicao_medio)s, %(estagia)s, %(trabalha)s, %(trabalha_opovo)s, %(setor_opovo)s, "
"%(funcao_opovo)s, %(ativo_opovo)s, %(saida_opovo)s, %(portador)s, %(qual_necessidade)s, now())")

insert_curso_superior = ("INSERT INTO rschemar.curso_superior (id_curso_superior, id_cadastro, data_inicio, "
"data_conclusao, instituicao, curso) VALUES (%(id_curso_superior)i, %(id_cadastro)i, %(data_inicio)s, "
"%(data_conclusao)s, %(instituicao)s, %(curso)s)")

insert_idioma = ("INSERT INTO rschemar.idioma (id_idioma, id_cadastro, idioma, "
"grau_de_dominio) VALUES (%(id_idioma)i, %(id_cadastro)i, %(idioma)s, %(grau_de_dominio)s)")

insert_curso = ("INSERT INTO rschemar.curso (id_curso, id_cadastro, data_inicio, "
"data_conclusao, instituicao, curso) VALUES (%(id_curso)i, %(id_cadastro)i, %(data_inicio)s, "
"%(data_conclusao)s, %(instituicao)s, %(curso)s)")

insert_estagio = ("INSERT INTO rschemar.estagio (id_estagio, id_cadastro, data_inicio, "
"data_saida, empresa, funcao, horario, atual) VALUES (%(id_estagio)i, %(id_cadastro)i, %(data_inicio)s, "
"%(data_saida)s, %(empresa)s, %(funcao)s, %(horario)s, %(atual)s)")

insert_emprego = ("INSERT INTO rschemar.emprego (id_emprego, id_cadastro, data_inicio, "
"data_saida, empresa, funcao, horario, atual) VALUES (%(id_emprego)i, %(id_cadastro)i, %(data_inicio)s, "
"%(data_saida)s, %(empresa)s, %(funcao)s, %(horario)s, %(atual)s)")

update_conteudo = ("UPDATE rschemar.conteudo SET titulo=%(titulo)s, editor=%(editor)s, "
"calendario=%(calendario)s, foto_galeria=%(foto_galeria)s, foto_interna=%(foto_interna)s, "
"legenda_foto_interna=%(legenda_foto_interna)s, destaque_capa=%(destaque_capa)s, andamento=%(andamento)s, "
"publicado_em=%(publicado_em)s, atualizado_em=%(atualizado_em)s, publicado=%(publicado)s "
"WHERE id_conteudo=%(id_conteudo)i")

update_cadastro_selecionado = ("UPDATE rschemar.cadastro SET selecionado = TRUE "
"WHERE id_cadastro=%(id_cadastro)i")

update_conteudo_cadastros_desselecionados = ("UPDATE rschemar.cadastro SET selecionado = FALSE "
"WHERE id_conteudo=%(id_conteudo)i")

delete_conteudo = ("DELETE FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i")

delete_destaque = ("DELETE FROM rschemar.destaque WHERE id_conteudo=%(id_conteudo)i")

delete_prova = ("DELETE FROM rschemar.prova WHERE id_conteudo=%(id_conteudo)i")

delete_cadastro = ("DELETE FROM rschemar.cadastro WHERE id_conteudo=%(id_conteudo)i")

delete_curso_superior = ("DELETE FROM rschemar.curso_superior WHERE id_cadastro=%(id_cadastro)i")

delete_idioma = ("DELETE FROM rschemar.idioma WHERE id_cadastro=%(id_cadastro)i")

delete_curso = ("DELETE FROM rschemar.curso WHERE id_cadastro=%(id_cadastro)i")

delete_estagio = ("DELETE FROM rschemar.estagio WHERE id_cadastro=%(id_cadastro)i")

delete_emprego = ("DELETE FROM rschemar.emprego WHERE id_cadastro=%(id_cadastro)i")

permissions = """
  GRANT USAGE ON SCHEMA rschemar TO %(user)s;
  GRANT SELECT ON rschemar.conteudo TO %(user)s;
  GRANT SELECT ON rschemar.prova TO %(user)s;
  GRANT SELECT, INSERT ON rschemar.cadastro TO %(user)s;
  GRANT SELECT, INSERT ON rschemar.curso_superior TO %(user)s;
  GRANT SELECT, INSERT ON rschemar.idioma TO %(user)s;
  GRANT SELECT, INSERT ON rschemar.curso TO %(user)s;
  GRANT SELECT, INSERT ON rschemar.estagio TO %(user)s;
  GRANT SELECT, INSERT ON rschemar.emprego TO %(user)s;
  GRANT SELECT ON rschemar.destaque TO %(user)s;
"""

permissions_admin = permissions

structure = """
  CREATE SCHEMA rschemar;

  CREATE TABLE rschemar.conteudo (
    id_conteudo SERIAL NOT NULL,
    id_idioma INTEGER DEFAULT 102,
    titulo VARCHAR NOT NULL,
    editor BOOL NULL DEFAULT 'False',
    calendario VARCHAR NULL,
    foto_galeria VARCHAR NULL,
    foto_interna VARCHAR NULL,
    legenda_foto_interna VARCHAR NULL,
    destaque_capa VARCHAR NULL,
    andamento CHAR DEFAULT 'I',
    publicado BOOL NOT NULL DEFAULT 'False',
    expira_em TIMESTAMP NULL,
    publicado_em TIMESTAMP NOT NULL,
    atualizado_em TIMESTAMP NULL,
    exportado BOOLEAN DEFAULT 'False',
    PRIMARY KEY(id_conteudo)
  );
  CREATE INDEX rschemar_conteudo_publicado_index ON rschemar.conteudo USING btree (publicado);
  CREATE INDEX rschemar_conteudo_publicado_em_index ON rschemar.conteudo USING btree (publicado_em);
  CREATE INDEX rschemar_conteudo_expira_em_index ON rschemar.conteudo USING btree (expira_em);
  
  CREATE TABLE rschemar.prova (
    id_prova SERIAL NOT NULL,
    id_conteudo INT NOT NULL,
    descricao VARCHAR NULL,
    arquivo VARCHAR NULL,
    PRIMARY KEY(id_prova),
    FOREIGN KEY(id_conteudo)
      REFERENCES rschemar.conteudo(id_conteudo)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );
  CREATE INDEX rschemar_prova_id_conteudo_index ON rschemar.prova USING btree (id_conteudo);

  
  CREATE TABLE rschemar.cadastro (
    id_cadastro SERIAL NOT NULL,
    id_conteudo INT NOT NULL,
    participou VARCHAR NOT NULL,
    edicao_participou VARCHAR NULL,
    fase_participou VARCHAR NULL,
    nome_completo VARCHAR NOT NULL,
    cpf VARCHAR NOT NULL,
    idade INT NOT NULL,
    data_nascimento VARCHAR NOT NULL,
    local_nascimento VARCHAR NOT NULL,
    nacionalidade VARCHAR NOT NULL,
    sexo VARCHAR NOT NULL,
    estado_civil VARCHAR NOT NULL,
    filhos VARCHAR NOT NULL,
    qtd_filhos VARCHAR NULL,
    rua VARCHAR NOT NULL,
    numero VARCHAR NOT NULL,
    complemento VARCHAR NULL,
    bairro VARCHAR NOT NULL,
    cep VARCHAR NOT NULL,
    cidade VARCHAR NOT NULL,
    estado VARCHAR NOT NULL,
    fone_fixo VARCHAR NOT NULL,
    fone_celular VARCHAR NOT NULL,
    email_principal VARCHAR NOT NULL,
    email_alternativo VARCHAR NULL,
    faculdade_cursa VARCHAR NOT NULL,
    semestre INT NOT NULL,
    inicio_curso VARCHAR NOT NULL,
    inicio_medio VARCHAR NOT NULL,
    conclusao_medio VARCHAR NOT NULL,
    instituicao_medio VARCHAR NOT NULL,
    estagia VARCHAR NOT NULL,
    trabalha VARCHAR NOT NULL,
    trabalha_opovo VARCHAR NOT NULL,
    setor_opovo VARCHAR NULL,
    funcao_opovo VARCHAR NULL,
    ativo_opovo VARCHAR NULL,
    saida_opovo VARCHAR NULL,
    portador VARCHAR NOT NULL,
    qual_necessidade VARCHAR NULL,
    data_hora_cadastro TIMESTAMP NULL,
    selecionado BOOL NULL DEFAULT 'False',
    PRIMARY KEY(id_cadastro),
    FOREIGN KEY(id_conteudo)
      REFERENCES rschemar.conteudo(id_conteudo)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );
  CREATE INDEX rschemar_cadastro_id_conteudo_index ON rschemar.cadastro USING btree (id_conteudo);
  
  CREATE TABLE rschemar.curso_superior (
    id_curso_superior SERIAL NOT NULL,
    id_cadastro INT NOT NULL,
    data_inicio VARCHAR NOT NULL,
    data_conclusao VARCHAR NOT NULL,
    instituicao VARCHAR NOT NULL,
    curso VARCHAR NOT NULL,
    PRIMARY KEY(id_curso_superior),
    FOREIGN KEY(id_cadastro)
      REFERENCES rschemar.cadastro(id_cadastro)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );
  CREATE INDEX rschemar_curso_superior_id_cadastro_index ON rschemar.curso_superior USING btree (id_cadastro);
  
  CREATE TABLE rschemar.idioma (
    id_idioma SERIAL NOT NULL,
    id_cadastro INT NOT NULL,
    idioma VARCHAR NOT NULL,
    grau_de_dominio INT NOT NULL,
    PRIMARY KEY(id_idioma),
    FOREIGN KEY(id_cadastro)
      REFERENCES rschemar.cadastro(id_cadastro)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );
  CREATE INDEX rschemar_idioma_id_cadastro_index ON rschemar.idioma USING btree (id_cadastro);
  
  CREATE TABLE rschemar.curso (
    id_curso SERIAL NOT NULL,
    id_cadastro INT NOT NULL,
    data_inicio VARCHAR NOT NULL,
    data_conclusao VARCHAR NOT NULL,
    instituicao VARCHAR NOT NULL,
    curso VARCHAR NOT NULL,
    PRIMARY KEY(id_curso),
    FOREIGN KEY(id_cadastro)
      REFERENCES rschemar.cadastro(id_cadastro)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );
  CREATE INDEX rschemar_curso_id_cadastro_index ON rschemar.curso USING btree (id_cadastro);
  
  CREATE TABLE rschemar.estagio (
    id_estagio SERIAL NOT NULL,
    id_cadastro INT NOT NULL,
    data_inicio VARCHAR NOT NULL,
    data_saida VARCHAR NULL,
    empresa VARCHAR NOT NULL,
    funcao VARCHAR NOT NULL,
    horario VARCHAR NOT NULL,
    atual VARCHAR NOT NULL,
    PRIMARY KEY(id_estagio),
    FOREIGN KEY(id_cadastro)
      REFERENCES rschemar.cadastro(id_cadastro)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );
  CREATE INDEX rschemar_estagio_id_cadastro_index ON rschemar.estagio USING btree (id_cadastro);
  
  CREATE TABLE rschemar.emprego (
    id_emprego SERIAL NOT NULL,
    id_cadastro INT NOT NULL,
    data_inicio VARCHAR NOT NULL,
    data_saida VARCHAR NULL,
    empresa VARCHAR NOT NULL,
    funcao VARCHAR NOT NULL,
    horario VARCHAR NOT NULL,
    atual VARCHAR NOT NULL,
    PRIMARY KEY(id_emprego),
    FOREIGN KEY(id_cadastro)
      REFERENCES rschemar.cadastro(id_cadastro)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );
  CREATE INDEX rschemar_emprego_id_cadastro_index ON rschemar.emprego USING btree (id_cadastro);

  CREATE TABLE rschemar.destaque (
    id_destaque SERIAL NOT NULL,
    id_conteudo INT NOT NULL,
    titulo VARCHAR NULL,
    descricao VARCHAR NULL,
    img VARCHAR NULL,
    peso INT NULL,
    PRIMARY KEY(id_destaque),
    FOREIGN KEY(id_conteudo)
      REFERENCES rschemar.conteudo(id_conteudo)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );
  CREATE INDEX rschemar_destaque_id_conteudo_index ON rschemar.destaque USING btree (id_conteudo);
"""
