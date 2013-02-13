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
# modificado por Eric Mesquita em 01/10/2012
#
select_status_content = ("SELECT publicado FROM rschemar.conteudo WHERE "
"id_conteudo=%(id_conteudo)i")

select_conteudo = ("SELECT C.id_conteudo, C.titulo, C.publicado, C.publicado_em, "
"C.expira_em, D.titulo as titulo_destaque, D.descricao as descricao_destaque, "
"D.img as imagem_destaque "
"FROM rschemar.conteudo C "
"LEFT JOIN rschemar.destaque D ON(C.id_conteudo=D.id_conteudo) "
"ORDER BY C.id_conteudo")

select_genero = ("SELECT id_genero, nome FROM "
"rschemar.genero ORDER BY nome")

select_genero_unico = ("SELECT nome FROM rschemar.genero "
"WHERE id_genero=%(id_genero)s")

select_censura = ("SELECT id_censura, nome FROM "
"rschemar.censura ORDER BY nome")

select_censura_unico = ("SELECT nome FROM rschemar.censura "
"WHERE id_censura=%(id_censura)s")

select_status = ("SELECT id_status, nome FROM "
"rschemar.status ORDER BY nome")

select_status_unico = ("SELECT nome FROM rschemar.status "
"WHERE id_status=%(id_status)s")

select_diretor_unico = ("SELECT nome, url_imdb FROM rschemar.diretor "
"WHERE id_diretor=%(id_diretor)s")

select_diretor_unico_nome = ("SELECT id_diretor, nome, url_imdb FROM "
"rschemar.diretor WHERE nome=%(nome)s")

select_diretor = ("SELECT id_diretor, nome, url_imdb FROM rschemar.diretor "
"ORDER BY nome")

select_ator_unico = ("SELECT nome, url_imdb FROM rschemar.ator "
"WHERE id_ator=%(id_ator)s")

select_ator_unico_nome = ("SELECT id_ator, nome, url_imdb FROM "
"rschemar.ator WHERE nome=%(nome)s")

select_ator = ("SELECT id_ator, nome, url_imdb FROM rschemar.ator "
"ORDER BY nome")

select_cinema_unico = ("SELECT nome, localizacao, endereco, fone FROM rschemar.cinema "
"WHERE id_cinema=%(id_cinema)s")

select_cinema_unico_nome = ("SELECT id_cinema, nome, localizacao, endereco, fone FROM "
"rschemar.cinema WHERE nome=%(nome)s")

select_cinema = ("SELECT id_cinema, nome, localizacao, endereco, fone FROM rschemar.cinema "
"ORDER BY nome")

select_nextval_filme = ("SELECT NEXTVAL('rschemar.conteudo_id_conteudo_seq'::text) as id")

select_nextval_diretor = ("SELECT NEXTVAL('rschemar.diretor_id_diretor_seq'::text) as id")

select_nextval_ator = ("SELECT NEXTVAL('rschemar.ator_id_ator_seq'::text) as id")

select_nextval_cinema = ("SELECT NEXTVAL('rschemar.cinema_id_cinema_seq'::text) as id")

select_titulo = ("SELECT titulo FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i")

select_filme = ("SELECT N.id_conteudo, N.titulo, N.titulo_original, N.url_imdb, "
"N.descricao, N.id_genero, N.id_censura, N.id_status, N.editor, N.corpo, N.video, N.audio, N.galeria, "
"to_char(N.expira_em, 'DD/MM/YYYY HH24:MI') as expira_em, "
"to_char(N.publicado_em, 'DD/MM/YYYY HH24:MI') as publicado_em, N.publicado, "
"to_char(N.data_edicao, 'DD/MM/YYYY') as data_edicao, "
"to_char(N.atualizado_em, 'DD/MM/YYYY') as atualizado_em, "
"D.id_destaque, D.titulo as titulo_destaque, D.descricao as descricao_destaque, "
"D.img, D.img as imagem_destaque, D.peso as peso_destaque, G.nome as genero, C.nome as censura, S.nome as status "
"FROM rschemar.conteudo N "
"LEFT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo) "
"LEFT JOIN rschemar.genero G ON(N.id_genero=G.id_genero) "
"LEFT JOIN rschemar.censura C ON(N.id_censura=C.id_censura) "
"LEFT JOIN rschemar.status S ON(N.id_status=S.id_status) "
"WHERE N.id_conteudo=%(id_conteudo)i")

select_filme_dados = ("SELECT N.id_conteudo, N.titulo, N.titulo_original, N.url_imdb, "
"N.descricao, N.id_genero, N.id_censura, N.id_status, N.editor, N.corpo, N.video, N.audio, N.galeria, "
"to_char(N.expira_em, 'YYYY-MM-DD HH24:MI') as expira_em, "
"to_char(N.publicado_em, 'YYYY-MM-DD HH24:MI') as publicado_em, N.publicado, "
"to_char(N.data_edicao, 'YYYY-MM-DD') as data_edicao, to_char(N.atualizado_em, 'YYYY-MM-DD') as atualizado_em, "
"D.id_destaque, D.titulo as titulo_destaque, D.descricao as descricao_destaque, "
"D.img, D.img as imagem_destaque, D.peso as peso_destaque, G.nome as genero, C.nome as censura, S.nome as status "
"FROM rschemar.conteudo N "
"LEFT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo) "
"LEFT JOIN rschemar.genero G ON(N.id_genero=G.id_genero) "
"LEFT JOIN rschemar.censura C ON(N.id_censura=C.id_censura) "
"LEFT JOIN rschemar.status S ON(N.id_status=S.id_status) "
"WHERE N.id_conteudo=%(id_conteudo)i")

select_filme_destaque = ("SELECT titulo, descricao, img FROM rschemar.destaque "
"WHERE id_conteudo=%(id_conteudo)i")

select_filme_fotos = ("SELECT id_foto, arquivo, arquivo_grande, alinhamento, "
"credito, legenda, descricao, link FROM rschemar.foto WHERE id_conteudo=%(id_conteudo)d "
"ORDER BY id_foto ASC")

select_filme_fotos_ad = ("SELECT * "
"FROM rschemar.foto_ad WHERE id_conteudo=%(id_conteudo)d ORDER BY id_foto ASC")

select_videos = ("SELECT id_video, embed FROM rschemar.video WHERE "
"id_conteudo=%(id_conteudo)i ORDER BY id_video ASC")

select_filme_diretores = ("SELECT FD.id_diretor, FD.id_conteudo, D.nome, D.url_imdb "
"FROM rschemar.conteudo_diretor FD "
"INNER JOIN rschemar.diretor D ON (FD.id_diretor=D.id_diretor) "
"WHERE FD.id_conteudo=%(id_conteudo)i ORDER BY FD.ordem ASC")

select_filme_atores = ("SELECT FA.id_ator, FA.id_conteudo, A.nome, A.url_imdb "
"FROM rschemar.conteudo_ator FA "
"INNER JOIN rschemar.ator A ON (FA.id_ator=A.id_ator) "
"WHERE FA.id_conteudo=%(id_conteudo)i ORDER BY FA.ordem ASC")

select_sessoes_busca = ("SELECT FC.id_conteudo, FC.horarios, CO.titulo, FC.id_cinema, CI.nome, CI.localizacao, CI.endereco, CI.fone "
"FROM rschemar.conteudo_cinema FC "
"LEFT JOIN rschemar.conteudo CO on CO.id_conteudo = FC.id_conteudo "
"LEFT JOIN rschemar.cinema CI on CI.id_cinema = FC.id_cinema "
"LEFT JOIN rschemar.foto fo on fo.id_conteudo = FC.id_conteudo "
"WHERE CO.id_status != 5 "
"AND CO.publicado = TRUE "
"AND FC.ativo = TRUE")

select_filmes_ativos = ("SELECT CO.id_conteudo, CO.id_censura, CO.id_genero, CO.id_status, CO.titulo, CO.descricao, CO.corpo, "
"CO.nota1, CO.nota2, CO.nota3, CO.nota4, CO.nota5, CO.titulo_original, CO.url_imdb, CE.nome as censura, GE.nome as genero, SE.nome as status "
"FROM rschemar.conteudo_cinema FC "
"LEFT JOIN rschemar.conteudo CO on CO.id_conteudo = FC.id_conteudo "
"LEFT JOIN rschemar.censura CE on CE.id_censura = CO.id_censura "
"LEFT JOIN rschemar.genero GE on GE.id_genero = CO.id_genero "
"LEFT JOIN rschemar.status SE on SE.id_status = CO.id_status "
"WHERE CO.id_status != 5 "
"AND FC.ativo = TRUE "
"AND CO.publicado = TRUE "
"GROUP BY CO.id_conteudo, CE.nome, GE.nome, SE.nome")

select_filmes_por_genero = ("SELECT CO.id_conteudo, CO.id_censura, CO.id_genero, CO.id_status, CO.titulo, CO.descricao, CO.corpo, "
"CO.titulo_original, CO.url_imdb, CE.nome as censura, GE.nome as genero, SE.nome as status "
"FROM rschemar.conteudo_cinema FC "
"LEFT JOIN rschemar.conteudo CO on CO.id_conteudo = FC.id_conteudo "
"LEFT JOIN rschemar.censura CE on CE.id_censura = CO.id_censura "
"LEFT JOIN rschemar.genero GE on GE.id_genero = CO.id_genero "
"LEFT JOIN rschemar.status SE on SE.id_status = CO.id_status "
"WHERE CO.id_genero = %(id_genero)i "
"AND CO.id_conteudo != %(id_conteudo)i "
"AND CO.publicado = TRUE "
"GROUP BY CO.id_conteudo, CE.nome, GE.nome, SE.nome "
"ORDER BY CO.id_conteudo DESC "
"LIMIT 4")

select_filme_cinemas = ("SELECT FC.id_cinema, FC.id_conteudo, FC.sala, FC.horarios, "
"FC.legendado, FC.tresd, FC.ativo, C.nome, C.localizacao, C.endereco, C.fone "
"FROM rschemar.conteudo_cinema FC "
"INNER JOIN rschemar.cinema C ON (FC.id_cinema=C.id_cinema) "
"WHERE FC.id_conteudo=%(id_conteudo)i ORDER BY FC.ordem ASC")

select_filme_cinemas_ativos = ("SELECT FC.id_cinema, FC.id_conteudo, FC.sala, FC.horarios, "
"FC.legendado, FC.tresd, FC.ativo, C.nome, C.localizacao, C.endereco, C.fone "
"FROM rschemar.conteudo_cinema FC "
"INNER JOIN rschemar.cinema C ON (FC.id_cinema=C.id_cinema) "
"LEFT JOIN rschemar.conteudo CO on CO.id_conteudo = FC.id_conteudo "
"WHERE FC.id_conteudo=%(id_conteudo)i "
"AND CO.id_status != 5 "
"AND FC.ativo = TRUE "
"ORDER BY FC.ordem ASC")

select_filme_publicado = ("SELECT N.id_conteudo, N.titulo, N.titulo_original, N.url_imdb, N.descricao, "
"N.id_genero, N.id_censura, N.id_status, N.editor, N.corpo, "
"N.nota1, N.nota2, N.nota3, N.nota4, N.nota5, "
"N.video, N.audio, N.galeria, to_char(N.publicado_em, 'DD/MM/YYYY HH24:MI') as publicado_em, N.publicado, "
"to_char(N.atualizado_em, 'DD/MM/YYYY HH24:MI') as atualizado_em, "
"D.id_destaque, D.titulo as titulo_destaque, D.descricao as descricao_destaque, D.img as imagem_destaque, "
"T.titulo as titulo_tree, CC.breadcrump "
"FROM rschemar.conteudo N "
"INNER JOIN envsite.conteudo CC ON(N.id_conteudo=CC.id_conteudo) "
"INNER JOIN envsite.treeapp T ON(CC.id_treeapp=T.id_treeapp) "
"LEFT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo) "
"WHERE N.id_conteudo=%(id_conteudo)i AND "
"CC.id_aplicativo=(SELECT id_aplicativo FROM envsite.aplicativo WHERE schema='rschemar')")

select_filme_publicado_ultimo = ("SELECT N.id_conteudo, N.titulo, N.titulo_original, N.url_imdb, N.descricao, N.id_genero, N.id_censura, N.id_status, N.editor, N.corpo, "
"N.nota1, N.nota2, N.nota3, N.nota4, N.nota5, "
"N.video, N.audio, N.galeria, to_char(N.publicado_em, 'DD/MM/YYYY HH24:MI') as publicado_em, N.publicado, "
"to_char(N.atualizado_em, 'DD/MM/YYYY HH24:MI') as atualizado_em, "
"D.id_destaque, D.titulo as titulo_destaque, D.descricao as descricao_destaque, D.img as imagem_destaque, "
"T.titulo as titulo_tree, CC.breadcrump "
"FROM rschemar.conteudo N "
"INNER JOIN envsite.conteudo CC ON(N.id_conteudo=CC.id_conteudo) "
"INNER JOIN envsite.treeapp T ON(CC.id_treeapp=T.id_treeapp) "                                   
"LEFT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo) "
"WHERE (N.expira_em > now() OR expira_em IS NULL) "
"AND N.publicado_em <= now() AND N.publicado='True' AND "
"CC.id_aplicativo=(SELECT id_aplicativo FROM envsite.aplicativo WHERE schema='rschemar')"
"ORDER BY N.publicado_em DESC LIMIT 1 ")

select_diretor_filme = ("SELECT D.id_diretor, D.nome, D.url_imdb FROM rschemar.conteudo_diretor FD "
"INNER JOIN rschemar.diretor D ON(FD.id_diretor=D.id_diretor) "
"WHERE FD.id_conteudo=%(id_conteudo)i ORDER BY FD.ordem ")

select_ator_filme = ("SELECT A.id_ator, A.nome, A.url_imdb FROM rschemar.conteudo_ator FA "
"INNER JOIN rschemar.ator A ON(FA.id_ator=A.id_ator) "
"WHERE FA.id_conteudo=%(id_conteudo)i ORDER BY FA.ordem ")

select_cinema_filme = ("SELECT C.id_cinema, C.nome, C.localizacao, C.endereco, C.fone, "
" FC.sala, FC.horarios, FC.legendado, FC.tresd, FC.ativo "
"FROM rschemar.conteudo_cinema FC "
"INNER JOIN rschemar.cinema C ON(FC.id_cinema=C.id_cinema) "
"WHERE FC.id_conteudo=%(id_conteudo)i ORDER BY FC.ordem ")

select_svg = ("SELECT audio, video, galeria FROM rschemar.conteudo WHERE "
"id_conteudo=%(id_conteudo)i")

select_svgs = ("SELECT id_conteudo, audio, video, galeria FROM "
"rschemar.conteudo WHERE id_conteudo IN (%(id_conteudos)s)")

select_dublin_core = ("SELECT titulo, descricao, corpo, "
"to_char(atualizado_em, 'YYYY-MM-DD HH24:MI:SS') as atualizado_em, "
"to_char(publicado_em, 'YYYY-MM-DD HH24:MI:SS') as publicado_em "
"FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i")

select_treeapp = ("SELECT C.id_treeapp, T.hash FROM envsite.conteudo C "
"INNER JOIN envsite.treeapp T ON(C.id_treeapp=T.id_treeapp) "
"WHERE C.id_aplicativo=(SELECT id_aplicativo FROM envsite.aplicativo WHERE schema=%(schema)s) "
"GROUP BY C.id_treeapp, T.hash")

select_data_edicao = ("SELECT C.data_edicao, C.id_conteudo, C.titulo, C.publicado_em, C.descricao, CC.breadcrump as breadcrumb, C.titulo_original "
"FROM rschemar.conteudo C "
"INNER JOIN envsite.conteudo CC ON(C.id_conteudo=CC.id_conteudo) "
"INNER JOIN envsite.treeapp T ON(CC.id_treeapp=T.id_treeapp) "
"WHERE CC.id_aplicativo=(SELECT id_aplicativo FROM envsite.aplicativo WHERE schema=%(schema)s) "
"AND C.data_edicao=%(data_edicao)s AND C.publicado AND C.publicado_em <= now() AND "
"(C.expira_em > now() OR C.expira_em IS NULL) AND T.hash=%(hash)s")

select_ultimo_data_edicao = ("SELECT C.data_edicao, C.id_conteudo, C.titulo, C.publicado_em "
"FROM rschemar.conteudo C "
"INNER JOIN envsite.conteudo CC ON(C.id_conteudo=CC.id_conteudo) "
"INNER JOIN envsite.treeapp T ON(CC.id_treeapp=T.id_treeapp) "
"WHERE CC.id_aplicativo=(SELECT id_aplicativo FROM envsite.aplicativo WHERE schema=%(schema)s) "
"AND C.data_edicao<%(data_edicao)s AND C.publicado AND C.publicado_em <= now() AND "
"(C.expira_em > now() OR C.expira_em IS NULL) AND T.hash=%(hash)s")

select_ultimos_app = ("SELECT C.id_conteudo, C.titulo, to_char(C.publicado_em, 'HH24:MI') as hora, "
"to_char(C.publicado_em, 'DD/MM/YYYY') as data, C.publicado_em "
"FROM rschemar.conteudo C "
"WHERE C.publicado AND C.publicado_em <= now() AND "
"(C.expira_em > now() OR C.expira_em IS NULL) "
"ORDER BY C.publicado_em DESC "
"LIMIT %(limit)i OFFSET %(offset)i")

select_ultimos_app_qtde = ("SELECT count(1) as qtde FROM rschemar.conteudo C "
"WHERE C.publicado AND C.publicado_em <= now() AND "
"(C.expira_em > now() OR C.expira_em IS NULL) ")

select_ultimos_app_acesso24h = ("SELECT C.id_conteudo, C.titulo, to_char(C.publicado_em, 'HH24:MI') as hora, "
"to_char(C.publicado_em, 'DD/MM/YYYY') as data "
"FROM rschemar.conteudo C "
"INNER JOIN envsite.conteudo CC ON(C.id_conteudo=CC.id_conteudo) "
"WHERE C.publicado AND C.publicado_em <= now() AND "
"(C.expira_em > now() OR C.expira_em IS NULL) AND "
"C.publicado_em >= (now() - interval '48 hours') AND "
"CC.id_aplicativo=(SELECT id_aplicativo FROM envsite.aplicativo WHERE schema='rschemar') AND "
"CC.acesso > 0 "
"ORDER BY C.publicado_em DESC "
"LIMIT %(limit)i OFFSET %(offset)i")

select_ultimo_data_edicao = ("SELECT C.data_edicao, C.id_conteudo, C.titulo, C.publicado_em "
"FROM rschemar.conteudo C "
"INNER JOIN envsite.conteudo CC ON(C.id_conteudo=CC.id_conteudo) "
"INNER JOIN envsite.treeapp T ON(CC.id_treeapp=T.id_treeapp) "
"WHERE CC.id_aplicativo=(SELECT id_aplicativo FROM envsite.aplicativo WHERE schema=%(schema)s) "
"AND C.data_edicao<%(data_edicao)s AND C.publicado AND C.publicado_em <= now() AND "
"(C.expira_em > now() OR C.expira_em IS NULL) AND T.hash=%(hash)s")

select_ultimos = ("SELECT N.id_conteudo, N.titulo, N.titulo_original, N.descricao, "
"N.video, N.audio, N.galeria, to_char(N.publicado_em, 'DD/MM/YYYY HH24:MI') as publicado_em, N.publicado, "
"to_char(N.atualizado_em, 'DD/MM/YYYY HH24:MI') as atualizado_em, "
"D.id_destaque, D.titulo as titulo_destaque, D.descricao as descricao_destaque, D.img as imagem_destaque "
"FROM rschemar.conteudo N "
"LEFT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo) "
"WHERE (N.expira_em > now() OR expira_em IS NULL) "
"AND N.publicado_em <= now() AND N.publicado='True' "
"ORDER BY N.publicado_em DESC LIMIT %(limit)i OFFSET %(offset)i ")

select_ultimos_qtde = ("SELECT count(1) as qtde FROM rschemar.conteudo N "
"LEFT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo) "
"WHERE (N.expira_em > now() OR expira_em IS NULL) "
"AND N.publicado_em <= now() AND N.publicado='True' ")

select_proximo = ("SELECT id_conteudo, titulo, titulo_original, publicado_em "
"FROM rschemar.conteudo WHERE publicado_em >= %(publicado_em)s "
"AND id_conteudo IN (SELECT id_conteudo FROM envsite.conteudo WHERE "
"id_treeapp=(SELECT id_treeapp FROM envsite.conteudo WHERE "
"id_conteudo=%(id_filme)s AND id_aplicativo=(SELECT id_aplicativo "
"FROM envsite.aplicativo WHERE schema=%(schema)s))) "
"AND publicado_em <= NOW() AND (publicado_em <> %(publicado_em)s "
"OR id_conteudo > %(id_filme)s) AND publicado = TRUE "
"ORDER BY publicado_em, id_conteudo LIMIT 1")

select_anterior = ("SELECT id_conteudo, titulo, titulo_original, publicado_em "
"FROM rschemar.conteudo WHERE publicado_em <= %(publicado_em)s "
"AND id_conteudo IN (SELECT id_conteudo FROM envsite.conteudo WHERE "
"id_treeapp=(SELECT id_treeapp FROM envsite.conteudo WHERE "
"id_conteudo=%(id_filme)s AND id_aplicativo=(SELECT id_aplicativo "
"FROM envsite.aplicativo WHERE schema=%(schema)s))) "
"AND publicado_em <= NOW() AND (publicado_em <> %(publicado_em)s "
"OR id_conteudo < %(id_filme)s) AND publicado = TRUE "
"ORDER BY publicado_em DESC, id_conteudo DESC LIMIT 1")

select_content_retranca = ("SELECT id_conteudo, publicado_em FROM "
"rschemar.conteudo WHERE retranca=%(retranca)s")

insert_diretor = ("INSERT INTO rschemar.diretor (nome, url_imdb) VALUES "
"(%(nome)s, %(url_imdb)s)")

insert_diretori = ("INSERT INTO rschemar.diretor (id_diretor, nome, url_imdb) "
"VALUES (%(id_diretor)i, %(nome)s, %(url_imdb)s)")

insert_ator = ("INSERT INTO rschemar.ator (nome, url_imdb) VALUES "
"(%(nome)s, %(url_imdb)s)")

insert_atori = ("INSERT INTO rschemar.ator (id_ator, nome, url_imdb) "
"VALUES (%(id_ator)i, %(nome)s, %(url_imdb)s)")

insert_cinema = ("INSERT INTO rschemar.cinema (nome, localizacao, endereco, fone) VALUES "
"(%(nome)s, %(localizacao)s, %(endereco)s, %(fone)s)")

insert_cinemai = ("INSERT INTO rschemar.cinema (id_cinema, nome, localizacao, endereco, fone) "
"VALUES (%(id_cinema)i, %(nome)s, %(localizacao)s, %(endereco)s, %(fone)s)")

insert_filme = ("INSERT INTO rschemar.conteudo (id_conteudo, "
"titulo, titulo_original, url_imdb, descricao, id_genero, id_censura, id_status, "
"corpo, publicado_em, expira_em, publicado, editor, video, "
"audio, galeria, data_edicao) VALUES "
"(%(id_conteudo)d, %(titulo)s, %(titulo_original)s, %(url_imdb)s, "
"%(descricao)s, %(id_genero)i, %(id_censura)i, %(id_status)i, %(corpo)s, %(publicado_em)s, "
"%(expira_em)s, %(publicado)s, %(editor)s, %(video)s, "
"%(audio)s, %(galeria)s, %(data_edicao)s)")

insert_filme_diretor = ("INSERT INTO rschemar.conteudo_diretor (id_conteudo, "
"id_diretor, ordem) VALUES (%(id_conteudo)d, %(id_diretor)d, %(ordem)i)")

insert_filme_ator = ("INSERT INTO rschemar.conteudo_ator (id_conteudo, "
"id_ator, ordem) VALUES (%(id_conteudo)d, %(id_ator)d, %(ordem)i)")

insert_filme_cinema = ("INSERT INTO rschemar.conteudo_cinema (id_conteudo, "
"id_cinema, sala, horarios, legendado, tresd, ativo, ordem) VALUES "
"(%(id_conteudo)d, %(id_cinema)d, %(sala)s, %(horarios)s, %(legendado)s, "
"%(tresd)s, %(ativo)s, %(ordem)i)")

insert_foto_filme = ("INSERT INTO rschemar.foto (id_conteudo, arquivo, "
"arquivo_grande, alinhamento, credito, legenda, descricao, link) "
"VALUES (%(id_conteudo)d, %(arquivo)s, %(arquivo_grande)s, %(alinhamento)s, "
"%(credito)s, %(legenda)s, %(descricao)s, %(link)s)")

insert_foto_filme_ad = ("INSERT INTO rschemar.foto_ad (id_conteudo, "
"foto_antes, foto_depois, alinhamento, credito_antes, credito_depois, "
"legenda, link) VALUES (%(id_conteudo)d, %(foto_antes)s, %(foto_depois)s, "
"%(alinhamento)s, %(credito_antes)s, %(credito_depois)s, "
"%(legenda)s, %(link)s)")

insert_video = ("INSERT INTO rschemar.video (id_conteudo, embed) VALUES "
"(%(id_conteudo)i, %(embed)s)")

insert_destaque = ("INSERT INTO rschemar.destaque (id_conteudo, titulo, "
"descricao, img, peso) VALUES (%(id_conteudo)i, %(titulo)s, "
"%(descricao)s, %(img)s, %(peso)i)")

delete_diretor = ("DELETE FROM rschemar.diretor WHERE id_diretor=%(id_diretor)i")

delete_ator = ("DELETE FROM rschemar.ator WHERE id_ator=%(id_ator)i")

delete_cinema = ("DELETE FROM rschemar.cinema WHERE id_cinema=%(id_cinema)i")

delete_filme = ("DELETE FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i")

delete_dados_filme = ("DELETE FROM rschemar.foto WHERE id_conteudo=%(id_conteudo)d; "
"DELETE FROM rschemar.foto_ad WHERE id_conteudo=%(id_conteudo)d;"
"DELETE FROM rschemar.video WHERE id_conteudo=%(id_conteudo)d; "
"DELETE FROM rschemar.conteudo_diretor WHERE id_conteudo=%(id_conteudo)d; "
"DELETE FROM rschemar.conteudo_ator WHERE id_conteudo=%(id_conteudo)d; "
"DELETE FROM rschemar.conteudo_cinema WHERE id_conteudo=%(id_conteudo)d; ")

delete_destaque = ("DELETE FROM rschemar.destaque WHERE id_destaque=%(id_destaque)i")

update_diretor = ("UPDATE rschemar.diretor SET nome=%(nome)s, url_imdb=%(url_imdb)s "
"WHERE id_diretor=%(id_diretor)s")

update_ator = ("UPDATE rschemar.ator SET nome=%(nome)s, url_imdb=%(url_imdb)s "
"WHERE id_ator=%(id_ator)s")

update_cinema = ("UPDATE rschemar.cinema SET nome=%(nome)s, localizacao=%(localizacao)s, endereco=%(endereco)s, fone=%(fone)s "
"WHERE id_cinema=%(id_cinema)s")

update_filme = ("UPDATE rschemar.conteudo SET titulo=%(titulo)s, "
"titulo_original=%(titulo_original)s, url_imdb=%(url_imdb)s, descricao=%(descricao)s, "
"id_genero=%(id_genero)i, id_censura=%(id_censura)i, id_status=%(id_status)i, corpo=%(corpo)s, "
"publicado_em=%(publicado_em)s, expira_em=%(expira_em)s, "
"publicado=%(publicado)s, atualizado_em=%(atualizado_em)s, "
"editor=%(editor)s, video=%(video)s, audio=%(audio)s, "
"galeria=%(galeria)s, data_edicao=%(data_edicao)s WHERE id_conteudo=%(id_conteudo)i")

update_filme_nota1 = ("UPDATE rschemar.conteudo SET nota1=nota1+1 "
"WHERE id_conteudo=%(id_conteudo)i")

update_filme_nota2 = ("UPDATE rschemar.conteudo SET nota2=nota2+1 "
"WHERE id_conteudo=%(id_conteudo)i")

update_filme_nota3 = ("UPDATE rschemar.conteudo SET nota3=nota3+1 "
"WHERE id_conteudo=%(id_conteudo)i")

update_filme_nota4 = ("UPDATE rschemar.conteudo SET nota4=nota4+1 "
"WHERE id_conteudo=%(id_conteudo)i")

update_filme_nota5 = ("UPDATE rschemar.conteudo SET nota5=nota5+1 "
"WHERE id_conteudo=%(id_conteudo)i")

update_destaque = ("UPDATE rschemar.destaque SET titulo=%(titulo)s, "
"descricao=%(descricao)s, img=%(img)s, peso=%(peso)i "
"WHERE id_conteudo=%(id_conteudo)i")

update_retranca = ("UPDATE rschemar.conteudo SET retranca=%(retranca)s "
"WHERE id_conteudo=%(id_conteudo)i")

permissions = """
  GRANT USAGE ON SCHEMA rschemar TO %(user)s;
  GRANT SELECT, UPDATE ON rschemar.conteudo TO %(user)s;
  GRANT SELECT ON rschemar.foto TO %(user)s;
  GRANT SELECT ON rschemar.foto_ad TO %(user)s;
  GRANT SELECT ON rschemar.diretor TO %(user)s;
  GRANT SELECT ON rschemar.ator TO %(user)s;
  GRANT SELECT ON rschemar.cinema TO %(user)s;
  GRANT SELECT ON rschemar.conteudo_diretor TO %(user)s;
  GRANT SELECT ON rschemar.conteudo_ator TO %(user)s;
  GRANT SELECT ON rschemar.conteudo_cinema TO %(user)s;
  GRANT SELECT ON rschemar.destaque TO %(user)s;
  GRANT SELECT ON rschemar.genero TO %(user)s;
  GRANT SELECT ON rschemar.censura TO %(user)s;
  GRANT SELECT ON rschemar.status TO %(user)s;
  GRANT SELECT ON rschemar.video TO %(user)s;
"""

permissions_admin = permissions

structure = """
  CREATE SCHEMA rschemar;

  CREATE TABLE rschemar.genero (
    id_genero SERIAL NOT NULL,
    nome VARCHAR NULL,
    PRIMARY KEY(id_genero)
  );

  CREATE TABLE rschemar.censura (
    id_censura SERIAL NOT NULL,
    nome VARCHAR NULL,
    PRIMARY KEY(id_censura)
  );  

  CREATE TABLE rschemar.status (
    id_status SERIAL NOT NULL,
    nome VARCHAR NULL,
    PRIMARY KEY(id_status)
  );  
  
  CREATE TABLE rschemar.diretor (
    id_diretor SERIAL NOT NULL,
    nome VARCHAR NOT NULL UNIQUE,
    url_imdb VARCHAR NOT NULL,
    PRIMARY KEY(id_diretor)
  );
  
  CREATE TABLE rschemar.ator (
    id_ator SERIAL NOT NULL,
    nome VARCHAR NOT NULL UNIQUE,
    url_imdb VARCHAR NOT NULL,
    PRIMARY KEY(id_ator)
  );
  
  CREATE TABLE rschemar.cinema (
    id_cinema SERIAL NOT NULL,
    nome VARCHAR NOT NULL UNIQUE,
    localizacao VARCHAR NOT NULL,
    endereco VARCHAR NOT NULL,
    fone VARCHAR NOT NULL,
    PRIMARY KEY(id_cinema)
  );

  CREATE TABLE rschemar.conteudo (
    id_conteudo SERIAL NOT NULL,
    id_idioma INTEGER DEFAULT 102,
    id_genero INT NOT NULL,
    id_censura INT NOT NULL,
    id_status INT NOT NULL,
    titulo VARCHAR NOT NULL,
    titulo_original VARCHAR NULL,
    url_imdb VARCHAR NULL,
    descricao VARCHAR NULL,
    editor BOOL NULL DEFAULT 'False',
    corpo VARCHAR NOT NULL,
    nota1 INT NOT NULL DEFAULT 0,
    nota2 INT NOT NULL DEFAULT 0,
    nota3 INT NOT NULL DEFAULT 0,
    nota4 INT NOT NULL DEFAULT 0,
    nota5 INT NOT NULL DEFAULT 0,
    video BOOL NOT NULL DEFAULT 'False',
    audio BOOL NOT NULL DEFAULT 'False',
    galeria BOOL NULL DEFAULT 'False',
    publicado BOOL NOT NULL DEFAULT 'False',
    expira_em TIMESTAMP NULL,
    publicado_em TIMESTAMP NOT NULL,
    atualizado_em TIMESTAMP NULL,
    data_edicao DATE NULL,
    retranca VARCHAR NULL,
    exportado BOOLEAN DEFAULT 'False',
    PRIMARY KEY(id_conteudo),
    FOREIGN KEY(id_genero)
      REFERENCES rschemar.genero(id_genero)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY(id_censura)
      REFERENCES rschemar.censura(id_censura)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY(id_status)
      REFERENCES rschemar.status(id_status)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );
  CREATE INDEX rschemar_conteudo_id_genero_index ON rschemar.conteudo USING btree (id_genero);
  CREATE INDEX rschemar_conteudo_id_censura_index ON rschemar.conteudo USING btree (id_censura);
  CREATE INDEX rschemar_conteudo_id_status_index ON rschemar.conteudo USING btree (id_status);
  CREATE INDEX rschemar_conteudo_publicado_index ON rschemar.conteudo USING btree (publicado);
  CREATE INDEX rschemar_conteudo_publicado_em_index ON rschemar.conteudo USING btree (publicado_em);
  CREATE INDEX rschemar_conteudo_expira_em_index ON rschemar.conteudo USING btree (expira_em);
  CREATE INDEX rschemar_conteudo_data_edicao_index ON rschemar.conteudo USING btree (data_edicao);
  CREATE INDEX rschemar_conteudo_data_edicao_index_plus on rschemar.conteudo USING BTREE (data_edicao, publicado_em) WHERE data_edicao IS NOT NULL;

  CREATE TABLE rschemar.conteudo_diretor(
    id_conteudo INT NOT NULL,
    id_diretor INT NOT NULL,
    ordem INT NULL,
    FOREIGN KEY(id_conteudo)
      REFERENCES rschemar.conteudo(id_conteudo)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY(id_diretor)
      REFERENCES rschemar.diretor(id_diretor)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );
  CREATE INDEX rschemar_conteudo_diretor_id_conteudo_index ON rschemar.conteudo_diretor USING btree (id_conteudo);
  
  CREATE TABLE rschemar.conteudo_ator(
    id_conteudo INT NOT NULL,
    id_ator INT NOT NULL,
    ordem INT NULL,
    FOREIGN KEY(id_conteudo)
      REFERENCES rschemar.conteudo(id_conteudo)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY(id_ator)
      REFERENCES rschemar.ator(id_ator)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );
  CREATE INDEX rschemar_conteudo_ator_id_conteudo_index ON rschemar.conteudo_ator USING btree (id_conteudo);

  CREATE TABLE rschemar.conteudo_cinema(
    id_conteudo INT NOT NULL,
    id_cinema INT NOT NULL,
    sala VARCHAR NOT NULL,
    horarios VARCHAR NOT NULL,
    legendado CHAR DEFAULT 'L',
    tresd BOOLEAN DEFAULT 'True',
    ativo BOOLEAN DEFAULT 'True',
    ordem INT NULL,
    FOREIGN KEY(id_conteudo)
      REFERENCES rschemar.conteudo(id_conteudo)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY(id_cinema)
      REFERENCES rschemar.cinema(id_cinema)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );
  CREATE INDEX rschemar_conteudo_cinema_id_conteudo_index ON rschemar.conteudo_cinema USING btree (id_conteudo);
  
  CREATE TABLE rschemar.foto (
    id_foto SERIAL NOT NULL,
    id_conteudo INT NOT NULL,
    arquivo VARCHAR NOT NULL,
    arquivo_grande VARCHAR NULL,
    alinhamento VARCHAR NOT NULL,
    credito VARCHAR NULL,
    legenda VARCHAR NULL,
    descricao VARCHAR NULL,
    link VARCHAR NULL,
    PRIMARY KEY(id_foto),
    FOREIGN KEY(id_conteudo)
      REFERENCES rschemar.conteudo(id_conteudo)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );
  CREATE INDEX rschemar_foto_id_conteudo_index ON rschemar.foto USING btree (id_foto);
  
  CREATE TABLE rschemar.foto_ad (
    id_foto SERIAL NOT NULL,
    id_conteudo INT NOT NULL,
    foto_antes VARCHAR NOT NULL,
    foto_depois VARCHAR NOT NULL,
    alinhamento VARCHAR NOT NULL,
    credito_antes VARCHAR NULL,
    credito_depois VARCHAR NULL,
    legenda VARCHAR NULL,
    link VARCHAR NULL,
    PRIMARY KEY(id_foto),
    FOREIGN KEY(id_conteudo)
      REFERENCES rschemar.conteudo(id_conteudo)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );
  CREATE INDEX rschemar_foto_ad_id_conteudo_index ON rschemar.foto_ad USING btree (id_foto);

  CREATE TABLE rschemar.video (
    id_video SERIAL NOT NULL,
    id_conteudo INT NOT NULL,
    embed VARCHAR NOT NULL,
    PRIMARY KEY(id_video),
    FOREIGN KEY(id_conteudo)
      REFERENCES rschemar.conteudo(id_conteudo)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );
  CREATE INDEX rschemar_video_id_conteudo_index ON rschemar.video USING btree (id_video);

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

  INSERT INTO rschemar.genero (id_genero, nome) VALUES (1, 'Ação');
  INSERT INTO rschemar.genero (id_genero, nome) VALUES (2, 'Animacação');
  INSERT INTO rschemar.genero (id_genero, nome) VALUES (3, 'Aventura');
  INSERT INTO rschemar.genero (id_genero, nome) VALUES (4, 'Chanchada');
  INSERT INTO rschemar.genero (id_genero, nome) VALUES (5, 'Cinema catástrofe');
  INSERT INTO rschemar.genero (id_genero, nome) VALUES (6, 'Comédia');
  INSERT INTO rschemar.genero (id_genero, nome) VALUES (7, 'Comédia romântica');
  INSERT INTO rschemar.genero (id_genero, nome) VALUES (8, 'Comédia dramática');
  INSERT INTO rschemar.genero (id_genero, nome) VALUES (9, 'Comédia de ação');
  INSERT INTO rschemar.genero (id_genero, nome) VALUES (10, 'Cult');
  INSERT INTO rschemar.genero (id_genero, nome) VALUES (11, 'Documentários');
  INSERT INTO rschemar.genero (id_genero, nome) VALUES (12, 'Drama');
  INSERT INTO rschemar.genero (id_genero, nome) VALUES (13, 'Espionagem');
  INSERT INTO rschemar.genero (id_genero, nome) VALUES (14, 'Fantasia');
  INSERT INTO rschemar.genero (id_genero, nome) VALUES (15, 'Faroeste');
  INSERT INTO rschemar.genero (id_genero, nome) VALUES (16, 'Ficção científica');
  INSERT INTO rschemar.genero (id_genero, nome) VALUES (17, 'Franchise/Séries');
  INSERT INTO rschemar.genero (id_genero, nome) VALUES (18, 'Guerra');
  INSERT INTO rschemar.genero (id_genero, nome) VALUES (19, 'Musical');
  INSERT INTO rschemar.genero (id_genero, nome) VALUES (20, 'Filme noir');
  INSERT INTO rschemar.genero (id_genero, nome) VALUES (21, 'Policial');
  INSERT INTO rschemar.genero (id_genero, nome) VALUES (22, 'Romance');
  INSERT INTO rschemar.genero (id_genero, nome) VALUES (23, 'Suspense');
  INSERT INTO rschemar.genero (id_genero, nome) VALUES (24, 'Terror');
  INSERT INTO rschemar.genero (id_genero, nome) VALUES (25, 'Trash');

  INSERT INTO rschemar.censura (id_censura, nome) VALUES (1, 'Livre');
  INSERT INTO rschemar.censura (id_censura, nome) VALUES (2, '10 anos');
  INSERT INTO rschemar.censura (id_censura, nome) VALUES (3, '12 anos');
  INSERT INTO rschemar.censura (id_censura, nome) VALUES (4, '14 anos');
  INSERT INTO rschemar.censura (id_censura, nome) VALUES (5, '16 anos');
  INSERT INTO rschemar.censura (id_censura, nome) VALUES (6, '18 anos');
  
  INSERT INTO rschemar.status (id_status, nome) VALUES (1, 'Pré-estreia');
  INSERT INTO rschemar.status (id_status, nome) VALUES (2, 'Estreia');
  INSERT INTO rschemar.status (id_status, nome) VALUES (3, 'Mostra');
  INSERT INTO rschemar.status (id_status, nome) VALUES (4, 'Em cartaz');
  INSERT INTO rschemar.status (id_status, nome) VALUES (5, 'Fora de cartaz');
  
  INSERT INTO rschemar.cinema (id_cinema, nome, localizacao, endereco, fone) VALUES (1, 'Arcoíris Aldeota', '1', 'Av. Dom Luiz, 500 Fortaleza-CE', '(85) 3458-1212');
  INSERT INTO rschemar.cinema (id_cinema, nome, localizacao, endereco, fone) VALUES (2, 'Arcoíris Del Paseo', '1', 'Av. Santos Dumont, 3131 Fortaleza–CE', '(85) 3456-5500');
  INSERT INTO rschemar.cinema (id_cinema, nome, localizacao, endereco, fone) VALUES (3, 'Arcoplex - Dom Luís', '1', 'Av. Dom Luís, 1200 Fortaleza–CE', '(85) 4011-5999');
  INSERT INTO rschemar.cinema (id_cinema, nome, localizacao, endereco, fone) VALUES (4, 'Centerplex - Via Sul', '1', 'Av. Washington Soares, 4335 Fortaleza-CE', '(85) 4003-9365');
  INSERT INTO rschemar.cinema (id_cinema, nome, localizacao, endereco, fone) VALUES (5, 'Centro Cultural Luiz Severiano Ribeiro', '1', 'Rua Major Facundo, 500 Fortaleza-CE', '(85) 3253-3332');
  INSERT INTO rschemar.cinema (id_cinema, nome, localizacao, endereco, fone) VALUES (6, 'Cine Benfica', '1', 'Av. Carapinima, 2200 Fortaleza-CE', '(85) 3243-1000');
  INSERT INTO rschemar.cinema (id_cinema, nome, localizacao, endereco, fone) VALUES (7, 'Espaço Unibanco', '1', 'Rua Dragão do Mar, 81 Fortaleza-CE', '(85) 3219-2641');
  INSERT INTO rschemar.cinema (id_cinema, nome, localizacao, endereco, fone) VALUES (8, 'Multiplex UCI Ribeiro - Iguatemi', '1', 'Av. Washington Soares, 85 Fortaleza-CE', '(85) 3477-3560');
  INSERT INTO rschemar.cinema (id_cinema, nome, localizacao, endereco, fone) VALUES (9, 'North Shopping', '1', 'Av. Bezerra de Meneses, 2450 Fortaleza-CE', '(85) 3404-3000');
  INSERT INTO rschemar.cinema (id_cinema, nome, localizacao, endereco, fone) VALUES (10, 'Cine Cariri', '2', 'Avenida Padre Cícero, 2555 Juazeiro do Norte-CE', '(88) 3572-9333');
  INSERT INTO rschemar.cinema (id_cinema, nome, localizacao, endereco, fone) VALUES (11, 'Cinema Francisco Lucena', '3', 'Rua Erbas Cavalcante Pinheiro, 50 Limoeiro do Norte–CE', '(88) 3423-2638');
  INSERT INTO rschemar.cinema (id_cinema, nome, localizacao, endereco, fone) VALUES (12, 'North Shopping Maracanaú', '4', 'Av. Senador Carlos Jereissati, 100 Maracanaú-CE', '(85) 3311-9300');
  INSERT INTO rschemar.cinema (id_cinema, nome, localizacao, endereco, fone) VALUES (13, 'Cine Renato Aragão', '5', 'Avenida John Sanford, 1800 Sobral-CE', '(88) 3614-2521');
"""
