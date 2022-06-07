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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def init():
    analyzer = model.newAnalyzer()
    return analyzer
# Funciones para la carga de datos

def loadServices(analyzer, servicesfile):
    servicesfile = cf.data_dir + servicesfile
    fh = open(servicesfile, encoding="utf-8")
    input_file = csv.DictReader(fh, delimiter=",")
    
    for trip in input_file:
        if (trip['Start Station Id'] != None and trip['Start Station Id'] != '' and
            trip['End Station Id'] != None and trip['End Station Id'] != '' and 
            trip['Trip  Duration'] != None and trip['Trip  Duration'] != '' and
            trip['Bike Id'] != None and trip['Bike Id'] != '' and
            trip['Start Station Id'] != trip['End Station Id'] and
            float(trip['Trip  Duration']) > 0):
            model.addTrip(analyzer, trip)
            model.addAllStations(analyzer, trip)
        analyzer['total_viajes']+=1
    
    return analyzer 

def optionThree(analyzer):
    datos = model.optionThree(analyzer)          
    return datos

def optionFive(analyzer):
    componentes = model.optionFive(analyzer)
    return componentes
    
def optionSix(analyzer, origen, destino):
    return model.optionSix(analyzer, origen, destino)

def optionSeven(analyzer, fecha_inicial, fecha_final):
    return model.optionSeven(analyzer, fecha_inicial, fecha_final)

def optionEight(analyzer, bike_id):
    return model.optionEight(analyzer, bike_id)

def optionNine(analyzer, nombre_estacion, fecha_inicial, fecha_final):
    return model.optionNine(analyzer, nombre_estacion, fecha_inicial, fecha_final)



# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def totalStations(analyzer):
    "Total de estaciones de bicicleta"
    return model.totalStations(analyzer)

def totalConnections(analyzer):
    """
    Total de enlaces entre las paradas
    """
    return model.totalConnections(analyzer)

def getVertices(analyzer):
    """
    Retorna lista con los vertices
    """
    return model.getVertices(analyzer)

def getTotalViajes(analyzer):
    return analyzer['total_viajes']

def getStationsMap(analyzer):
    return analyzer['stations']

def getGraph(analyzer):
    return analyzer['connections']

def connectedComponents(analyzer):
    return model.connectedComponents(analyzer)