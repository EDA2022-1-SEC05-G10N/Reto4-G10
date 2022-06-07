"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 """
import sys
import config
import threading
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import stack
from DISClib.ADT import graph as gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
assert config


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

servicefile = 'Bikeshare-ridership-2021-utf8-small.csv'

def printMenu():
    print("Bienvenido")
    print("1- Inicializar analizador")
    print("2- Cargar información en el catálogo")
    print("3- Comprar bicicletas para las estaciones con más viajes de origen")
    print("4- Planear paseos turísticos por la ciudad")
    print("5- Reconocer los componentes fuertemente conectados")
    print("6- Planear una ruta rápida para el usuario")
    print("7- Reportar rutas en un rango de fechas para los usuarios anuales")
    print("8- Planear el mantenimiento preventivo de bicicletas")
    print("9- La estación más frecuentada por los visitantes")

def optionTwo(cont):
    print("\nCargando Informacion de Bikeshare.....")
    controller.loadServices(cont, servicefile)
    numedges = controller.totalConnections(cont)
    numvertex = controller.totalStations(cont)
    print('Total de viajes: '+str(controller.getTotalViajes(cont)))
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    print('Los primeros y ultimos 5 vertices del grafo: ')
    lista_vertices = controller.getVertices(cont)
    mapa_estaciones = controller.getStationsMap(cont)
    grafo = controller.getGraph(cont)

    i = 0
    while i<lt.size(lista_vertices):
        i+=1
        print(str(i)+')' )
        vertex = lt.getElement(lista_vertices, i)
        submapa = m.get(mapa_estaciones, vertex)['value']
        print("     "+'ID de la estacion: '+m.get(submapa, 'station id')['value'])
        print("     "+'Nombre de la estacion '+m.get(submapa, 'station name')['value'])
        print("     "+'# Viajes de salida '+str(m.get(submapa, 'out trips')['value']))
        print("     "+'# Viajes de llegada '+str(m.get(submapa, 'in trips')['value']))
        print("     "+'Rutas de entrada '+str(gr.indegree(grafo, vertex)))
        print("     "+'Rutas de salida '+str(gr.outdegree(grafo, vertex)))
        if i==5:
            print('       .......')
            print('       .......')
            print('       .......')            
            i=lt.size(lista_vertices)-5
        
def optionThree(cont):
    lista = controller.optionThree(cont)
    i = 0
    while i<lt.size(lista):
        i+=1
        vertex = lt.getElement(lista, i)
        print(str(i)+')')
        print("     "+'ID de la estacion: '+str(vertex[0]))
        print("     "+'Nombre de la estacion: '+vertex[1])
        print("     "+'Viajes de salida: '+str(vertex[2]))
        if i == 5:       
            i=lt.size(lista)

def optionFour(cont):
    return None

def optionFive(cont):
    print('     El numero de componentes conectados es: '+str(controller.connectedComponents(cont)))
    componentes = controller.optionFive(cont)

    mapa_aux = m.newMap(maptype='PROBING')

    ids_componente = m.valueSet(componentes['idscc'])
    for id1 in lt.iterator(ids_componente):
        if not m.contains(mapa_aux, id1):
            m.put(mapa_aux, id1, 1)
        else:
            valor = m.get(mapa_aux, id1)['value']
            m.put(mapa_aux, id1, valor+1)

    i = 0
    while i<controller.connectedComponents(cont):
        i+=1
        print(' Componente '+str(i)+' # de estaciones: '+str(m.get(mapa_aux, i)['value']))
        #if i == 3:
            #i=controller.connectedComponents(cont)-3
            

def optionSix(cont, origen, destino):
    ruta = controller.optionSix(cont, origen, destino)
    
    ruta_real = lt.newList('ARRAY_LIST')
    total_cost = 0
    for i in lt.iterator(ruta):        
        total_cost += i['weight']
        lt.addFirst(ruta_real, i)

    print('Tiempo total que tomara el recorrido: '+str(total_cost))
    
    a = 1
    for i in lt.iterator(ruta_real):
        print(str(a)+')')
        print('     Estaciones: '+i['vertexA']+' -> '+i['vertexB'])
        print('     Tiempo: '+str(i['weight']))
        a+=1


def optionSeven(cont, fecha_inicial, fecha_final):
    controller.optionSeven(cont, fecha_inicial, fecha_final)


def optionEight(cont, bike_id):
    controller.optionEight(cont, bike_id)

def optionNine(cont, nombre_estacion, fecha_inicial, fecha_final):
    controller.optionNine(cont, nombre_estacion, fecha_inicial, fecha_final)



"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    
    if int(inputs[0]) == 1:
        print("Inicializando")
        cont = controller.init()

    elif int(inputs[0]) == 2:
        optionTwo(cont)

    elif int(inputs[0]) == 3:
        optionThree(cont)
    
    elif int(inputs[0]) == 4:
        optionFour(cont)

    elif int(inputs[0]) == 5:
        optionFive(cont)

    elif int(inputs[0]) == 6:
        origen = input('Ingrese el nombre de la estacion origen')
        destino = input('Ingrese el nombre de la estacion destino')
        optionSix(cont, origen, destino)

    elif int(inputs[0]) == 7:
        fecha_inicial = input('Ingrese fecha inicial formato m/d/a')
        fecha_final = input('Ingrese fecha final formato m/d/a')
        optionSeven(cont, fecha_inicial, fecha_final)

    elif int(inputs[0]) == 8:
        bike_id = str(float(input('Ingrese el ID de la bicicleta que quiere buscar')))
        optionEight(cont, bike_id)

    elif int(inputs[0]) == 9:
        nombre_estacion = input('Ingrese el nombre de la estacion')
        fecha_inicial = input('Ingrese la fecha inicial')
        fecha_final = input('Ingrese la fecha final')
        optionNine(cont, nombre_estacion, fecha_inicial, fecha_final)

    else:
        sys.exit(0)
sys.exit(0)