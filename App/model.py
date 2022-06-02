0"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import graph as gr 
from DISClib.Algorithms.Graphs import scc 
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import dfs as dfs
from DISClib.Algorithms.Graphs import bfs as bfs 
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.ADT import stack as st
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf
from datetime import date, datetime

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newAnalyzer():
        analyzer = {
            "estaciones": None, 
            "connections": None, 
            "components": None, 
            "paths": None, 
            "search": None,
        }

        analyzer["estaciones"] = mp.newMap(numelements= 61031,
                                            maptype = "CHAINING",
                                            comparefunction = None)
        analyzer["bikes"] = mp.newMap(numelements = 61031,
                                        maptype = "CHAINING",
                                        comparefunction = None)
        analyzer["id_estaciones"] = mp.newMap(numelements = 61031,
                                            maptype = "CHAINING",
                                            comparefunction = comparar_id_estaciones)
        analyzer["conexiones"] = gr.newGraph(datastructure = "ADJ_LIST",
                                            directed = True
                                            size = 14000,
                                            compare_function = comparar_id_estaciones)
        analyzer["lista_de_conexiones"] = lt.newList("ARRAY_LIST")
        analyzer["estaciones_iniciales"] = mp.newMap(numelements = 61031,
                                                    maytype = "CHAINING",
                                                    comparefunction = None)
        analyzer["tiempo"] = mp.newMap(numelements = 61031,
                                       maptype = "CHAINING",
                                        comparefunction = comparar_id_estaciones)
        analyzer["fechas_iniciales"] = om.newMap(omaptype = "RBT",
                                                comparefunction = comparar_fechas)
        analyzer["paradas"] = mp.newMap(numelements = 61031,
                                                    maytype = "CHAINING",
                                                    comparefunction = None) 

        return analyzer

# Funciones para agregar informacion al catalogo
def agregarConexionesEstaciones(analyzer,viaje):
    inicio = str(viaje["Start Station Id"])
    fin = str(int(float(viaje["End Station Id"])))
    agregarParada(analyzer,inicio)
    agregarParada(analyzer,fin)
    edge = gr.getEdge(analyzer["conexiones"],inicio,fin)
    if edge is None: 
        recorrido = inicio + fin 
        lst_rec = mp.get(analyzer["time"],recorrido)["value"]
        tiempo_rec = sum(lst_rec)
        viajes = len(lst_rec)
        tiempo_promedio = tiempo_rec / viajes
        agregarConexion(analyzer,inicio,fin,tiempo_promedio)
    return analyzer

def agregarParada(analyzer,estacion_id):
    if not gr.containsVertex(analyzer["conexiones"],estacion_id):
            gr.insertVertex(analyzer["conexiones"],estacion_id)
    return analyzer

def agregarConexion(analyzer,inicio,fin,tiempo_promedio):
    edge = gr.getEdge(analyzer["conexiones"],inicio,fin)
    if edge is None: 
        gr.addEgde(analyzer["conexiones"],inicio,fin,tiempo_promedio)
    return analyzer


# Funciones para creacion de datos
#cargar elementos req 1 
def cargar_estaciones_inicio(analyzer, bicicleta):
    estaciones = analyzer["estaciones_iniciales"]
    id_estacion = bicicleta["Start Station Id"]
    nombre = crear_nombre_estacion(bicicleta["Start Station Name"])
    llave = id_estacion + "-" + nombre
    tipo_usuario = bicicleta["User Type"]
    if not mp.contains(estaciones,llave):
        diccionario_estaciones = {"id_estacion":id_estacion, 
                                "nombre":nombre,
                                "total_viajes":0,
                                "Casual Member":0,
                                "Annual Member": 0}
    else:
        diccionario_estaciones = mp.get(estaciones,llave)
        diccionario_estaciones = me.getValue(diccionario_estaciones)
    diccionario_estaciones["total_viajes"] +=1
    diccionario_estaciones[tipo_usuario]
    mp.put(estaciones,llave, diccionario_estaciones)

    return analyzer

        
#FUNCIONES REQUERIMIENTOS 

#REQUERIMIENTO 1 
def más_viajes(analyzer):
    est = mp.valueSet(analyzer["estaciones_iniciales"])
    lst = lt.newList("ARRAY_LIST")
    for estacion in lt.iterator(est):
        llave = estacion["id_estacion"] + "-" + estacion["nombre"]
        try:
            outdegree = gr.outdegree(analyzer["conexiones"],llave)
        except:
            outdegree = 0 
        estacion["Out Degree"] = 0 
        lt.addLast(lst,estacion)

def getInfo1(analyzer):
    return analyzer 

def getInfo2(analyzer,estacion_inicial,estacion_final):
    analyzer["paths"] = djk.Dijkstra(analyzer["conexiones"],7543.0)
    caminos_existentes = analyzer["paths"]

    lst_paradas = analyzer["lista_de_conexiones"]
    route_index = mp.newMap(numelements = 14000,
                            maptype="PROBING")
    for parada in lt.iterator(lst_paradas):
        existe_cam = hasPath(caminos_existentes,parada["stop_id"])
        if existe_cam:
            camino = minimunCostPath(caminos_existentes,parada["stop_id"])
            num_estaciones = st.size(camino)
            if num_estaciones != 0:
                costo = djk.distTo(caminos_existentes,parada["stop_id"])
                orden = lt.newList(datastructure="ARRAY_LIST")
                for camino_parada in lt.iterator(camino):
                    vertice1 = camino_parada["vertexA"]
                    vertice2 = camino_parada["vertexB"]
                    nombre1 = mp.get(analyzer["paradas"],vertice1)
                    nomb1 = me.getValue(nombre1)["station_name"]
                    nombre2 = mp.get(analyzer["paradas"],vertice2)
                    nomb2 = me.getValue(nombre2)["station_name"]
                    informacion_final = (vertice1,nomb1),(vertice2,nomb2)
                    lt.addLast(orden,informacion_final)
                entry = {
                    "orden":orden,
                    "tiempo": costo,
                    "num_estaciones": num_estaciones
                }
                mp.put(route_index,stop["stop_id"],entry)
    key_set = lista_llaves(route_index)
    caminos_finales = lt.newList(datastructure="ARRAY_LIST")
    for llave in key_set:
        info1 = mp.get(route_index,llave)
        info1_f = me.getValue(info1)
        if info1_f["num_estacion"] >= minstops: 
            


    return analyzer

def getInfo3(analyzer)


def totalParadas(analyzer):
    return gr.numVertices(analyzer["conexiones"])

def totalConexiones(analyzer):
    return gr.numEdges(analyzer["conexiones"])

# Funciones de consulta
def crear_nombre_estacion(estacion):
    if estacion == " ":
        return "desconocido"
    else:
        return estacion 

def connectedComponents(analyzer):
    analyzer["components"] = scc.KosajaruSCC(analyzer["connections"])
    return scc.connectedComponents(analyzer["components"]) 

def minimumCostPaths(analyzer,initialStation):
    analyzer["paths"] = djk.Dijkstra(analyzer["connections"],initialStation)
    return analyzer

def hasPath(analyzer,destStation):
    return djk.hasPathTo(analyzer["paths"],destStation)

def minimunCostPath(analyzer,destStation):
    path = djk.pathTo(analyzer["paths"],destStation)
    return path 

def searchPaths(analyzer,initialStation,method):
    if method == "dfs":
        analyzer["search"] = dfs.DepthFirstSearch(analyzer["connections"],initialStation)
    elif method == "bfs":
        analyzer["search"] = bfs.BreadhtFisrtSearch(analyzer["connections"],initialStation)
    return analyzer

def hasSearchPath(analyzer,destStation,method):
    if method == "dfs":
        camino = dfs.hasPathTo(analyzer["search"],destStation)
        return camino 
    elif method == "bfs":
        camino = bfs.hasPathTo(analyzer["search"],destStation)
        return camino 

def searchPathTo(analyzer,destStation,method):
    if method == "dfs":
        path = dfs.pathTo(analyzer["search"],destStation)
    elif method == "bfs":
        path = bfs.pathTo(analyzer["search"],destStation)
    return path 

def totalStops(analyzer):
    return gr.numVertices(analyzer["connections"])

def totalConnections(analyzer):
    return gr.numEdges(analyzer["connections"])

def servedRoutes(analyzer):
    lastvert = mp.keySet(analyzer["estaciones"])
    maxvert = None 
    maxdeg = 0 
    for vert in lt.iterator(lastvert):
        lstroutes = mp.get(analyzer["estaciones",vert])["value"]
        degree = lt.size(lstroutes)
        if (degree > maxdeg):
            maxvert = vert
            maxdeg = degree 
    return maxvert, maxdeg


# Funciones utilizadas para comparar elementos dentro de una lista
def comparar_id_estaciones(estacion_id,entry):
    if type(entry) is dict: 
        entry_estacion = me.getKey(entry)
        if estacion_id == entry_estacion: 
            return 0
        elif estacion_id > entry_estacion: 
            return 1
        else: 
            return -1

def compareStopsIds(estacion,valor_estacion):
    estacion_llave = valor_estacion["key"]
    if (estacion == estacion_llave):
        return 0 
    elif (estacion > estacion_llave):
        return 1 
    else: 
        return -1

def comparar_fechas(fecha1,fecha2):
    fecha_1 = datetime.strptime("%Y-%m-%d","%H-%M-%S")
    fecha_2 = datetime.strptime("%Y-%m-%d","%H-%M-%S")
    if fecha_1 == fecha_2:
        return 0 
    elif fecha_1 > fecha_2:
        return -1 

    
def compareroutes(route1,route2):
    if (route1 == route2):
        return 0 
    elif (route1 > route2):
        return 1 
    else: 
        return -1 

# Funciones de ordenamiento
