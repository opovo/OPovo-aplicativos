# coding: utf-8
#
# Copyright 2009 Prima Tech Informatica Ltda.
#
# Licensed under the Environ License, Version 1.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.presslab.com.br/licenses/ENVIRON-LICENSE-1.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

select_impresso_paginas = ("SELECT id_conteudo, titulo, retranca, "
"corpo, descricao "
"FROM %(schema)s.conteudo WHERE retranca  ~* %(retranca)s AND "
"publicado=True AND publicado_em >= %(data1)s AND  publicado_em <= %(data2)s AND"
"(publicado_em <= now() AND (expira_em > now() OR expira_em IS NULL))")



