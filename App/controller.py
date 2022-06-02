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
archivo_viajes = "Bikeshare // Bikeshare-ridership-2021-utf8-small.csv"

# Inicialización del Catálogo de libros
def init():
    analyzer = model.newAnalyzer()
    return analyzer

# Funciones para la carga de datos
def loadData(analyzer,archivo):
    archivo = cf.data_dir + archivo_viajes
    input_file = csv.DictReader(open(archivo, encoding='utf-8'))
    num_entry = 0
    for viaje in input_file: 
        if len(viaje["Start Station Name"]) == 0 or len(viaje["End Station Name"]) == 0 or len(viaje["Bike Id"]):
            num_entry +=1 
            continue
        else: 
            model.agregarViaje(analyzer,viaje)
    return analyzer,num_entry

def totalConexiones(analyzer):
    return model.totalConexiones(analyzer)

def totalParadas(analyzer): 
    return model.totalParadas(analyzer)

def viajesTotales(analyzer):
    return model.viajesTotales(analyzer)

def posiciones(analyzer):
    return model.posiciones(analyzer)

def getInfo1(analyzer):
    return model.getInfo1(analyzer)

def getInfo2(analyzer,estacion_inicial,disponibilidad,minimo_paradas,estaciones):
    return model.getInfo2(analyzer,estacion_inicial,disponibilidad,minimo_paradas,estaciones)

def getInfo3(analyzer,nombre_origen, nombre_final):
    return model.getInfo3(analyzer,nombre_origen, nombre_final)

def getInfo4(analyzer,fecha_inicial, fecha_final):
    return model.getInfo4(analyzer,fecha_inicial,fecha_final)

def getInfo5(analyzer,bicicleta, fecha_inicial, fecha_final):
    return model.getInfo5(analyzer,bicicleta, fecha_inicial,fecha_final)

def getInfo6(analyzer,nombre_estacion):
    return model.getInfo6(analyzer,nombre_estacion)
    
# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
