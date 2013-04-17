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
from urllib import urlopen
from time import time, strftime, strptime
from publica.core.portal import Portal
from publica.admin.error import UserError
from publica.utils.json import encode
from publica.utils.decorators import serialize, dbconnectionplug,\
                                     Permission, logportal
from publica.utils.json import decode
from publica import settings

hasapp = False
haspage = False
haslist = False
hasportlet = False
title = "OPovo Impresso"
meta_type = "opovo_impresso"


class Plug:
    """
    """
    title = title
    meta_type = meta_type
    hasapp = hasapp
    haspage = haspage
    haslist = haslist
    schema = ""


    def __init__(self, id_site, id_plugin=None, request=None, dados={}):
        """
        """
        self.id_plugin = id_plugin
        self.id_site = id_site
        self.request = request
        if id_plugin and not dados:
            portal = Portal(id_site=self.id_site,
                            request=self.request)
            dados = portal._getDadosPlug(env_site=self.id_site,
                                         id_plugin=self.id_plugin)

        self.dados = dados


    def _install(self, title, id_site_, schema, **kargs):
        """Adiciona uma instancia do plugin
        """
        return {"titulo": title,
                "id_site": id_site_,
                "schema": schema}


    @serialize
    @Permission("ADM PLUG")
    def editPlug(self, title, id_site_, schema):
        """Edita os atributos do plugin
        """
        dados = {"titulo": title,
                 "id_site": id_site_,
                 "schema": schema}

        portal = Portal(id_site=self.id_site,
                        request=self.request)
        portal._editPlug(env_site=self.id_site,
                         id_plugin=self.id_plugin, 
                         title=title, 
                         dados=dados)

        return "Plugin configurado com sucesso"


    def _action(self, id_treeapp, schema, id_conteudo, link,
                      add=None, edit=None, delete=None, dados={}):
        """ this plugin does not have action on publishing
        """
        pass


    @serialize
    def actionWidget(self, **kargs):
        """ this plugin does not have action on content
        """
        pass
        

    # hurdle

    @dbconnectionplug
    def _getContent(self, year, month, day, page):
        """
        """
        ##select titulo, retranca from noticia_132346504881.conteudo
        ##where retranca like '2013_0603%17%' and publicado;
        day = str(day).zfill(2)
        month = str(month).zfill(2)
        page = str(page).zfill(2)
        data1 = "{0}-{1}-{2} 00:00".format(year, month, day)
        data2 = "{0}-{1}-{2} 23:59".format(year, month, day)

        #retranca = "{0}_{1}{2}%{3}%".format(year, day, month, page)
        retranca = "{0}_{1}{2}[a-zA-Z]*[0-9][0-9]{3}".format(year, day, month, page)

        return self.execSql("select_impresso_paginas",
                            schema=buffer("noticia_132346504881"),
                            data1=data1,
                            data2=data2,
                            retranca=retranca)



        


