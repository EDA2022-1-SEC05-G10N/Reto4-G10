"""
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


'''
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf'''

import config
from DISClib.ADT import graph as gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import dfs as dfs 
from DISClib.Algorithms.Graphs import bfs as bfs 
from DISClib.Utils import error as error
from DISClib.Algorithms.Sorting import mergesort as mergesort
from datetime import datetime
assert config

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newAnalyzer():
    try:
        analyzer = {
            'stations': None,
            'connections': None,
            'components': None,
            'paths': None,
            'search': None,
        }

        analyzer['total_viajes'] = 0

        analyzer['lista viajes'] = lt.newList('ARRAY_LIST')

        analyzer['stations'] = m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)
        
        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareStopIds)
        analyzer['tiempos'] = m.newMap(maptype='PROBING')

        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para agregar informacion al catalogo

def addTrip(analyzer, trip):
    datos_viaje = [0,0,0,0,0,0,0]
    datos_viaje[0] = trip['Trip Id']
    datos_viaje[1] = trip['Trip  Duration']
    datos_viaje[2] = datetime.strptime(trip['Start Time'][0:10], "%m/%d/%Y")
    datos_viaje[3] = trip['Bike Id']
    datos_viaje[4] = trip['User Type']
    datos_viaje[5] = trip['Start Station Name']
    datos_viaje[6] = trip['End Station Name']

    lt.addLast(analyzer['lista viajes'], datos_viaje)




def addAllStations(analyzer, trip):
    try:
        origin = trip['Start Station Name']
        origin_id = trip['Start Station Id']
        destination = trip['End Station Name']
        destination_id = trip['End Station Id']

        #agregar vertices LISTO
        addStation(analyzer, origin, origin_id, 'out')
        addStation(analyzer, destination, destination_id, 'in')

        #sacar el tiempo LISTO
        time = float(trip['Trip  Duration'])

        #armar string trayecto
        trayecto = origin+'/'+destination
        #cada vez que un usuario hace este trayecto, se actualizar el promedio de tiempos
        actualizar_tiempos(analyzer, trayecto, time)
        tiempo_promedio_total = m.get(analyzer['tiempos'], trayecto)['value'][0]

        edge = gr.getEdge(analyzer['connections'], origin, destination)
        if edge is None:
            gr.addEdge(analyzer['connections'], origin, destination, tiempo_promedio_total)
        else:
            edge['weight'] = tiempo_promedio_total

        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addAllStations')

def addStation(analyzer, station_name, station_id, in_out):
    if not gr.containsVertex(analyzer['connections'], station_name):
        gr.insertVertex(analyzer['connections'], station_name)

        submapa=m.newMap(maptype='PROBING')
        m.put(submapa, 'station name', station_name)
        m.put(submapa, 'station id', station_id)
        out_trips = 0
        in_trips = 0
        m.put(submapa, 'out trips', out_trips)
        m.put(submapa, 'in trips', in_trips)

        m.put(analyzer['stations'], station_name, submapa)
    


    submapa = m.get(analyzer['stations'], station_name)['value']
    out_trips = m.get(submapa, 'out trips')['value']    
    in_trips = m.get(submapa, 'in trips')['value']
    if in_out == 'out':
        out_trips+=1
    if in_out == 'in':
        in_trips+=1
    m.put(submapa, 'out trips', out_trips)
    m.put(submapa, 'in trips', in_trips)

    m.put(analyzer['stations'], station_name, submapa)
    return analyzer

def actualizar_tiempos(analyzer, trayecto, time):
    mapa=analyzer['tiempos']
    entry = m.get(mapa, trayecto)
    if entry is None:
        tupla = [time, 1]
        m.put(mapa, trayecto, tupla)
                
    else:        
        nuevo_promedio = (((entry['value'][0])*(entry['value'][1]))+time)/(entry['value'][1]+1)
        nueva_tupla = [nuevo_promedio, entry['value'][1]+1]
        m.put(mapa, trayecto, nueva_tupla)

    return analyzer



def optionThree(analyzer):
    vertices = m.valueSet(analyzer['stations'])
    lista_mejor = lt.newList('ARRAY_LIST')
    for i in lt.iterator(vertices):
        tupla = [0,0,0]
        tupla[0] = m.get(i, 'station id')['value']
        tupla[1] = m.get(i, 'station name')['value']
        tupla[2] = m.get(i, 'out trips')['value']
        lt.addLast(lista_mejor, tupla)

    lista_mejor2 = mergesort.sort(lista_mejor, cmpVerticesByOutTrips)
    
    return lista_mejor2
    

def optionFive(analyzer):
    componentes = scc.KosarajuSCC(analyzer['connections'])
    return componentes



def optionSix(analyzer, origen, destino):
    existe1 = gr.containsVertex(analyzer['connections'], origen)
    existe2 = gr.containsVertex(analyzer['connections'], destino)

    if existe1 and existe2:    
        analyzer['paths'] = djk.Dijkstra(analyzer['connections'], origen)
        
        if djk.hasPathTo(analyzer['paths'], destino):
            path = djk.pathTo(analyzer['paths'], destino)
            return path
        else:
            return 'no hay ruta entre los vertices'


def optionSeven(analyzer, fecha_inicial, fecha_final):
    lista_viajes = analyzer['lista viajes']
    lista_ordenada = mergesort.sort(lista_viajes, cmpViajesPorFecha)

    fecha_inicial = datetime.strptime(fecha_inicial, "%m/%d/%Y")
    fecha_final = datetime.strptime(fecha_final, "%m/%d/%Y")

    mayor = busqueda_lineal(lista_ordenada, fecha_final, 'max')
    menor = busqueda_lineal(lista_ordenada, fecha_inicial, 'min')

    #print('menor'+str(menor)+str(lt.getElement(lista_ordenada, menor)[2]))
    #print('mayor'+str(mayor)+str(lt.getElement(lista_ordenada, mayor)[2]))
    
    trips_en_rango = lt.subList(lista_ordenada, menor, (mayor-menor))    

    mapa_estaciones_origen = m.newMap(maptype='PROBING')
    mapa_estaciones_destino = m.newMap(maptype='PROBING')
    total_tiempo = 0
    
    for trip in lt.iterator(trips_en_rango):
        total_tiempo += float(trip[1])

        if not m.contains(mapa_estaciones_origen, trip[5]):
            m.put(mapa_estaciones_origen, trip[5], 1)
        else:
            valor = m.get(mapa_estaciones_origen, trip[5])['value']
            m.put(mapa_estaciones_origen, trip[5], valor+1)

        if not m.contains(mapa_estaciones_destino, trip[6]):
            m.put(mapa_estaciones_destino, trip[6], 1)
        else:
            valor = m.get(mapa_estaciones_destino, trip[6])['value']
            m.put(mapa_estaciones_destino, trip[6], valor+1)


    estaciones_origen = m.keySet(mapa_estaciones_origen)
    
    maximo1 = 0
    maxima_estacion1 = lt.newList('ARRAY_LIST')
    for estacion in lt.iterator(estaciones_origen):
        if m.get(mapa_estaciones_origen, estacion)['value'] > maximo1:
            maximo1 = m.get(mapa_estaciones_origen, estacion)['value']
            lt.addLast(maxima_estacion1, estacion)

    maximo2 = 0
    maxima_estacion2 = lt.newList('ARRAY_LIST')
    estaciones_destino = m.keySet(mapa_estaciones_destino)
    for estacion in lt.iterator(estaciones_destino):
        if m.get(mapa_estaciones_destino, estacion)['value'] > maximo2:
            maximo2 = m.get(mapa_estaciones_destino, estacion)['value']
            lt.addLast(maxima_estacion2, estacion)


    print('     Total viajes entre fechas: '+str(lt.size(trips_en_rango)))
    print('     Total de tiempo invertido en los viajes: '+str(total_tiempo))
    print('     Estaciones origen mas frecuentadas: '+str(maximo1)+' veces')
    for estacion in lt.iterator(maxima_estacion1):
        print("          "+estacion)
    print('     Estaciones destino mas frecuentadas: '+str(maximo2)+' veces')
    for estacion in lt.iterator(maxima_estacion2):
        print("          "+estacion)

def optionEight(analyzer, bike_id):


    contador_viajes_bici = 0
    contador_horas_bici = 0

    lista_viajes = analyzer['lista viajes']
    for trip in lt.iterator(lista_viajes):
        if trip[3] == bike_id:
            contador_viajes_bici += 1
            contador_horas_bici += float(trip[1])

    print('Total de viajes de la bici: '+str(contador_viajes_bici))
    print('Total de horas en la bici: '+str(contador_horas_bici))


def optionNine(analyzer, nombre_estacion, fecha_inicial, fecha_final):
    lista_viajes = analyzer['lista viajes']
    lista_ordenada = mergesort.sort(lista_viajes, cmpViajesPorFecha)

    fecha_inicial = datetime.strptime(fecha_inicial, "%m/%d/%Y")
    fecha_final = datetime.strptime(fecha_final, "%m/%d/%Y")

    mayor = busqueda_lineal(lista_ordenada, fecha_final, 'max')
    menor = busqueda_lineal(lista_ordenada, fecha_inicial, 'min')
    
    trips_en_rango = lt.subList(lista_ordenada, menor, (mayor-menor))    

    trips_salieron = lt.newList('ARRAY_LIST')
    trips_llegaron = lt.newList('ARRAY_LIST')
    for trip in lt.iterator(trips_en_rango):
        if trip[5] == nombre_estacion:
            lt.addLast(trips_salieron, trip)
        if trip[6] == nombre_estacion:
            lt.addLast(trips_llegaron, trip)


    print('     Total de viajes que iniciaron en esta estacion: '+str(lt.size(trips_salieron)))
    print('     Total de viajes que terminaron en esta estacion: '+str(lt.size(trips_llegaron)))
    
    lissta = mergesort.sort(trips_salieron, cmpTripsByDuration)
    maxtrip = lt.lastElement(lissta)
    print('     Viaje de mayor duracion: ')
    print('          '+'ID: '+str(maxtrip[0]))
    print('          '+'Estacion salida: '+str(maxtrip[5]))
    print('          '+'Estacion llegada: '+str(maxtrip[6]))
    print('          '+'Duracion: '+str(maxtrip[1]))        
    

    lista_aux = trips_salieron

    estaciones_de_llegada = m.newMap(maptype='PROBING')
    
    for trip in lt.iterator(lista_aux):
        if m.contains(estaciones_de_llegada, trip[6]):
            n_actualizado = m.get(estaciones_de_llegada, trip[6])['value']+1
            m.put(estaciones_de_llegada, trip[6], n_actualizado)    
        else:
            m.put(estaciones_de_llegada, trip[6], 1)


    keys_estaciones = m.keySet(estaciones_de_llegada)
    
    maximoN = 0
    for key in lt.iterator(keys_estaciones):
        if m.get(estaciones_de_llegada, key)['value'] > maximoN:
            maximoN = m.get(estaciones_de_llegada, key)['value']
        #print('     Name: '+key+' frecuencia: '+str(m.get(estaciones_de_llegada, key)['value']))


    print('     Estaciones donde terminaron la mayoria de viajes que iniciaron en esta estacion:')
    for key in lt.iterator(keys_estaciones):
        if m.get(estaciones_de_llegada, key)['value'] == maximoN:
            print('          Nombre: '+key+' Frecuencia: '+str(maximoN))

# Funciones para creacion de datos

# Funciones de consulta
def totalStations(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['connections'])


def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['connections'])

def getVertices(analyzer):
    return gr.vertices(analyzer['connections'])

def connectedComponents(analyzer):
    analyzer['components'] = scc.KosarajuSCC(analyzer['connections'])
    return scc.connectedComponents(analyzer['components'])


# Funciones utilizadas para comparar elementos dentro de una lista
def compareStopIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1


def cmpVerticesByOutTrips(vertice1, vertice2):
    if vertice1[2] > vertice2[2]:
        return 1
    else: 
        return 0

def cmpViajesPorFecha(viaje1, viaje2):
    if viaje1[2] < viaje2[2]:
        return 1
    else:
        return 0

def cmpTripsByDuration(trip1, trip2):
    if trip1[1] > trip2[1]:
        return 1
    else:
        return 0

# Funciones de ordenamiento

def busqueda_lineal(lista, x, criterio)->int:
    
    if criterio == 'min':
        a = 1
    else:
        a = lt.size(lista)
        
    for i in range(1,lt.size(lista),1):
        if lt.getElement(lista,a)[2] == x:
            return a
        else:
            if criterio == 'min':
                a+=1
            elif criterio == 'max':
                a-=1
    return 0