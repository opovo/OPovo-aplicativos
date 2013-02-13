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
# sql.py cinema_opovo
# modificado por Eric Mesquita em 12/11/2012
#
select_campo = ("SELECT id_campo, nome, codigo FROM "
"rschemar.campo ORDER BY id_campo ASC")

select_campo_unico = ("SELECT nome, codigo FROM rschemar.campo "
"WHERE id_campo=%(id_campo)s")

select_conteudo_campos = ("SELECT CC.id_campo, CA.nome, CA.codigo "
"FROM rschemar.conteudo_campo CC "
"INNER JOIN rschemar.campo CA ON (CC.id_campo=CA.id_campo) "
"WHERE CC.id_conteudo=%(id_conteudo)i ORDER BY CA.id_campo ASC")

select_conteudo_cadastros = ("SELECT * "
"FROM rschemar.cadastro "
"WHERE id_conteudo=%(id_conteudo)i ORDER BY sequencial ASC")

select_conteudo_cadastro_vencedor = ("SELECT * "
"FROM rschemar.cadastro "
"WHERE id_conteudo=%(id_conteudo)i "
"AND sequencial=%(sequencial)i")

select_all_conteudo_cadastros = ("SELECT * "
"FROM rschemar.cadastro "
"WHERE id_conteudo=%(id_conteudo)i ORDER BY sequencial ASC")

select_cpf_cadastros = ("SELECT COUNT(*) FROM rschemar.cadastro "
"WHERE id_conteudo=%(id_conteudo)i AND cpf=%(cpf)s")

select_maxval_sequencial_conteudo_cadastros = ("SELECT MAX(sequencial) "
"FROM rschemar.cadastro WHERE id_conteudo=%(id_conteudo)i")

select_nextval_conteudo = ("SELECT NEXTVAL('rschemar.conteudo_id_conteudo_seq'::text) as id")

select_nextval_cadastro = ("SELECT NEXTVAL('rschemar.cadastro_id_cadastro_seq'::text) as id")

select_status_content = ("SELECT publicado FROM rschemar.conteudo "
"WHERE id_conteudo=%(id_conteudo)i")

select_dados = ("SELECT N.id_conteudo, N.titulo, N.cartola, N.descricao, N.editor, N.editor2, N.regulamento, "
"N.imagem_topo_list, N.imagem_rodape, N.imagem_bg_topo, N.imagem_bg_rodape, N.cor, N.cadastro_unico, N.vencedor, "
"to_char(N.expira_em, 'YYYY-MM-DD HH24:MI') as expira_em, "
"to_char(N.publicado_em, 'YYYY-MM-DD HH24:MI') as publicado_em, N.publicado, "
"to_char(N.atualizado_em, 'YYYY-MM-DD HH24:MI') as atualizado_em, "
"D.id_destaque, D.titulo as titulo_destaque, D.descricao as descricao_destaque, "
"D.img, D.img as imagem_destaque, D.peso as peso_destaque "
"FROM rschemar.conteudo N "
"LEFT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo) "
"WHERE N.id_conteudo=%(id_conteudo)i")

select_titulo = ("SELECT titulo FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i")

select_dublin_core = ("SELECT titulo, cartola, descricao, "
"to_char(atualizado_em, 'YYYY-MM-DD HH24:MI:SS') as atualizado_em, "
"to_char(publicado_em, 'YYYY-MM-DD HH24:MI:SS') as publicado_em "
"FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i")

select_conteudo = ("SELECT N.id_conteudo, N.titulo, N.cartola, N.descricao, N.editor, N.editor2, N.regulamento, "
"N.imagem_topo_list, N.imagem_rodape, N.imagem_bg_topo, N.imagem_bg_rodape, N.cor, N.cadastro_unico, N.vencedor, "
"to_char(N.atualizado_em, 'DD/MM/YYYY HH24:MI') as atualizado_em, "
"to_char(N.publicado_em, 'DD/MM/YYYY HH24:MI') as publicado_em, N.publicado, "
"D.id_destaque, D.titulo as titulo_destaque, D.descricao as descricao_destaque, "
"D.img, D.img as imagem_destaque, D.peso as peso_destaque "
"FROM rschemar.conteudo N "
"LEFT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo) "
"WHERE N.id_conteudo=%(id_conteudo)i")

insert_conteudo = ("INSERT INTO rschemar.conteudo (id_conteudo, titulo, cartola, "
"descricao, editor, editor2, regulamento, imagem_topo_list, imagem_rodape, imagem_bg_topo, imagem_bg_rodape, cor, cadastro_unico, vencedor, "
"publicado_em, atualizado_em, publicado) VALUES (%(id_conteudo)i, %(titulo)s,"
"%(cartola)s, %(descricao)s, %(editor)s, %(editor2)s, %(regulamento)s,%(imagem_topo_list)s, %(imagem_rodape)s, %(imagem_bg_topo)s, %(imagem_bg_rodape)s, "
"%(cor)s, %(cadastro_unico)s, %(vencedor)s, %(publicado_em)s, %(atualizado_em)s, %(publicado)s)")

insert_destaque  = ("INSERT INTO rschemar.destaque (id_conteudo, titulo, descricao, img, peso) VALUES "
"(%(id_conteudo)i, %(titulo)s, %(descricao)s, %(img)s, %(peso)i)")

insert_conteudo_campo = ("INSERT INTO rschemar.conteudo_campo (id_conteudo, "
"id_campo) VALUES (%(id_conteudo)d, %(id_campo)d)")

insert_cadastro = ("INSERT INTO rschemar.cadastro (id_cadastro, id_conteudo, sequencial, cpf, "
"rg, data_nascimento, nome, endereco, complemento, bairro, cep, email, profissao, faculdade, "
"curso, facebook, twitter, fone1, fone2, fone3, anexo, frase, opt_parceiro, "
"opt_opovo, data_hora_cadastro) VALUES (%(id_cadastro)i, %(id_conteudo)i, %(sequencial)i, %(cpf)s, %(rg)s, "
"%(data_nascimento)s, %(nome)s, %(endereco)s, %(complemento)s, %(bairro)s, %(cep)s, %(email)s, "
"%(profissao)s, %(faculdade)s, %(curso)s, %(facebook)s, %(twitter)s, %(fone1)s, %(fone2)s, %(fone3)s, %(anexo)s, "
"%(frase)s, %(opt_parceiro)s, %(opt_opovo)s, now())")

update_conteudo = ("UPDATE rschemar.conteudo SET titulo=%(titulo)s, cartola=%(cartola)s, "
"descricao=%(descricao)s, editor=%(editor)s, editor2=%(editor2)s, regulamento=%(regulamento)s, imagem_topo_list=%(imagem_topo_list)s, imagem_rodape=%(imagem_rodape)s, "
"imagem_bg_topo=%(imagem_bg_topo)s, imagem_bg_rodape=%(imagem_bg_rodape)s, cor=%(cor)s, cadastro_unico=%(cadastro_unico)s, vencedor=%(vencedor)s, "
"publicado_em=%(publicado_em)s, atualizado_em=%(atualizado_em)s, publicado=%(publicado)s "
"WHERE id_conteudo=%(id_conteudo)i")

delete_conteudo = ("DELETE FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i")

delete_destaque = ("DELETE FROM rschemar.destaque WHERE id_conteudo=%(id_conteudo)i")

delete_dados_conteudo = ("DELETE FROM rschemar.conteudo_campo WHERE id_conteudo=%(id_conteudo)d")

permissions = """
  GRANT USAGE ON SCHEMA rschemar TO %(user)s;
  GRANT SELECT ON rschemar.conteudo TO %(user)s;
  GRANT SELECT ON rschemar.campo TO %(user)s;
  GRANT SELECT ON rschemar.conteudo_campo TO %(user)s;
  GRANT SELECT, INSERT ON rschemar.cadastro TO %(user)s;
  GRANT SELECT ON rschemar.destaque TO %(user)s;
"""

permissions_admin = permissions

structure = """
  CREATE SCHEMA rschemar;
  
  CREATE TABLE rschemar.campo (
    id_campo SERIAL NOT NULL,
    nome VARCHAR NULL,
    codigo VARCHAR NULL,
    PRIMARY KEY(id_campo)
  );

  CREATE TABLE rschemar.conteudo (
    id_conteudo SERIAL NOT NULL,
    id_idioma INTEGER DEFAULT 102,
    titulo VARCHAR NOT NULL,
    cartola VARCHAR NULL,
    descricao VARCHAR NOT NULL,
    editor BOOL NULL DEFAULT 'False',
    editor2 BOOL NULL DEFAULT 'False',
    regulamento VARCHAR NULL,
    imagem_topo_list VARCHAR,
    imagem_rodape VARCHAR,
    imagem_bg_topo VARCHAR,
    imagem_bg_rodape VARCHAR,
    cor VARCHAR,
    cadastro_unico BOOLEAN DEFAULT 'False',
    vencedor VARCHAR NULL,
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
  
  CREATE TABLE rschemar.cadastro (
    id_cadastro SERIAL NOT NULL,
    id_conteudo INT NOT NULL,
    sequencial INT NOT NULL,
    nome VARCHAR NULL,
    cpf VARCHAR NULL,
    rg VARCHAR NULL,
    data_nascimento VARCHAR NULL,
    email VARCHAR NULL,
    endereco VARCHAR NULL,
    complemento VARCHAR NULL,
    bairro VARCHAR NULL,
    cep VARCHAR NULL,
    profissao VARCHAR NULL,
    faculdade VARCHAR NULL,
    curso VARCHAR NULL,
    facebook VARCHAR NULL,
    twitter VARCHAR NULL,
    fone1 VARCHAR NULL,
    fone2 VARCHAR NULL,
    fone3 VARCHAR NULL,
    frase VARCHAR NULL,
    anexo VARCHAR NULL,
    opt_opovo BOOLEAN DEFAULT 'False',
    opt_parceiro BOOLEAN DEFAULT 'False',
    data_hora_cadastro TIMESTAMP NULL,
    PRIMARY KEY(id_cadastro),
    FOREIGN KEY(id_conteudo)
      REFERENCES rschemar.conteudo(id_conteudo)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );
  CREATE INDEX rschemar_cadastro_id_conteudo_index ON rschemar.cadastro USING btree (id_conteudo);
  
  CREATE TABLE rschemar.conteudo_campo(
    id_conteudo INT NOT NULL,
    id_campo INT NOT NULL,
    FOREIGN KEY(id_conteudo)
      REFERENCES rschemar.conteudo(id_conteudo)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY(id_campo)
      REFERENCES rschemar.campo(id_campo)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );
  CREATE INDEX rschemar_conteudo_campo_id_conteudo_index ON rschemar.conteudo_campo USING btree (id_conteudo);

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
  
  INSERT INTO rschemar.campo (id_campo, nome, codigo) VALUES (1, 'nome', '<p><label for="nome" class="error">Nome:<span class=obrigatorio>*</span></label><input type="text" name="nome" id="nome" class="required"/></p>');
  INSERT INTO rschemar.campo (id_campo, nome, codigo) VALUES (2, 'cpf', '<p><label for="cpf" class="error">CPF:<span class=obrigatorio>*</span></label><input type="text" name="cpf" id="cpf" class="required" alt="cpf"/></p>');
  INSERT INTO rschemar.campo (id_campo, nome, codigo) VALUES (3, 'rg', '<p><label for="rg" class="error">RG:<span class=obrigatorio>*</span></label><input type="text" name="rg" id="rg" class="required" alt="num"/></p>');
  INSERT INTO rschemar.campo (id_campo, nome, codigo) VALUES (4, 'data_nascimento', '<p><label for="data_nascimento" class="error">Data de Nascimento:<span class=obrigatorio>*</span></label><input type="text" name="data_nascimento" id="data_nascimento" class="required" alt="date"/></p>');
  INSERT INTO rschemar.campo (id_campo, nome, codigo) VALUES (5, 'email', '<p><label for="email" class="error">E-mail:<span class=obrigatorio>*</span></label><input type="text" name="email" id="email" class="email required"/></p>');
  INSERT INTO rschemar.campo (id_campo, nome, codigo) VALUES (6, 'endereco', '<p><label for="endereco" class="error">Endereço:<span class=obrigatorio>*</span></label><input type="text" name="endereco" id="endereco" class="required"/></p>');
  INSERT INTO rschemar.campo (id_campo, nome, codigo) VALUES (7, 'complemento', '<p><label for="complemento" class="error">Complemento:</label><input type="text" name="complemento" id="complemento"/></p>');
  INSERT INTO rschemar.campo (id_campo, nome, codigo) VALUES (8, 'bairro', '<p><label for="bairro" class="error">Bairro:<span class=obrigatorio>*</span></label><input type="text" name="bairro" id="bairro" class="required"/></p>');
  INSERT INTO rschemar.campo (id_campo, nome, codigo) VALUES (9, 'cep', '<p><label for="cep" class="error">CEP:<span class=obrigatorio>*</span></label><input type="text" name="cep" id="cep" class="required" alt="cep"/></p>');
  INSERT INTO rschemar.campo (id_campo, nome, codigo) VALUES (10, 'profissao', '<p><label for="profissao" class="error">Profissão:<span class=obrigatorio>*</span></label><input type="text" name="profissao" id="profissao" class="required"/></p>');
  INSERT INTO rschemar.campo (id_campo, nome, codigo) VALUES (11, 'faculdade', '<p><label for="faculdade" class="error">Faculdade:<span class=obrigatorio>*</span></label><input type="text" name="faculdade" id="faculdade" class="required"/></p>');
  INSERT INTO rschemar.campo (id_campo, nome, codigo) VALUES (12, 'curso', '<p><label for="curso" class="error">Curso:<span class=obrigatorio>*</span></label><input type="text" name="curso" id="curso" class="required"/></p>');
  INSERT INTO rschemar.campo (id_campo, nome, codigo) VALUES (13, 'facebook', '<p><label for="facebook" class="error">Facebook:</label><input type="text" name="facebook" id="facebook"/></p>');
  INSERT INTO rschemar.campo (id_campo, nome, codigo) VALUES (14, 'twitter', '<p><label for="twitter" class="error">Tritter:</label><input type="text" name="twitter" id="twitter"/></p>');
  INSERT INTO rschemar.campo (id_campo, nome, codigo) VALUES (15, 'fone1', '<p><label for="fone1" class="error">Fone:<span class=obrigatorio>*</span></label><input type="text" name="fone1" id="fone1" class="required" alt="phone"/></p>');
  INSERT INTO rschemar.campo (id_campo, nome, codigo) VALUES (16, 'fone2', '<p><label for="fone2" class="error">Fone 2:</label><input type="text" name="fone2" id="fone2" alt="phone"/></p>');
  INSERT INTO rschemar.campo (id_campo, nome, codigo) VALUES (17, 'fone3', '<p><label for="fone3" class="error">Fone 3:</label><input type="text" name="fone3" id="fone3" alt="phone"/></p>');
  INSERT INTO rschemar.campo (id_campo, nome, codigo) VALUES (18, 'frase', '<p class="full frase"><label for="frase" class="error">Frase:<span class=obrigatorio>*</span></label><textarea name="frase" id="frase" rows="5" class="required"></textarea></p>');
  INSERT INTO rschemar.campo (id_campo, nome, codigo) VALUES (19, 'anexo', '<p class="full"><label for="anexo" class="error">Anexo:<span class=obrigatorio>*</span></label><input type="file" name="anexo" id="anexo" class="required"/><span>(Tamanho máximo do arquivo: 5Mb)</span></p>');
  INSERT INTO rschemar.campo (id_campo, nome, codigo) VALUES (20, 'opt_opovo', '<p class="full"><input type="checkbox" name="opt_opovo" id="opt_opovo" checked/><label class="fullCheck" for="opt_opovo">Quero ser informado sobre promoções e ofertas do Grupo de Comunicação O POVO.</label></p>'); 
  INSERT INTO rschemar.campo (id_campo, nome, codigo) VALUES (21, 'opt_parceiro', '<p class="full"><input type="checkbox" name="opt_parceiro" id="opt_parceiro" checked/><label class="fullCheck" for="opt_parceiro">Quero ser informado sobre promoções e ofertas de parceiros de Grupo de Comunicação OPOVO.</label></p>'); 
"""
