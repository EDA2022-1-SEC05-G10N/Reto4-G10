﻿"""
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

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Comprar bicicletas para las estaciones con más viajes de origen")
    print("3- Planear paseos turísticos por la ciudad")
    print("4- Reconocer los componentes fuertemente conectados")
    print("5- Planear una ruta rápida para el usuario")
    print("6- Reportar rutas en un rango de fechas para los usuarios anuales")
    print("7- Planear el mantenimiento preventivo de bicicletas")
    print("8- La estación más frecuentada por los visitantes")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")

    elif int(inputs[0]) == 2:
        pass
    elif int(inputs[0]) == 3:
        nombre = input("Ingrese el nombre de la estación de inicio: ")
        disponibilidad = input("Ingrese la disponibilidad para el paseo: ")
        num_min_est = input("Ingrese el numero minimo de estaciones de parada para la ruta")
        max_num = input("Ingrese el maximo numero de rutas de respuesta")
    elif int(inputs[0]) == 4:
        pass
    elif int(inputs[0]) == 5:
        nombre_origen = input("Ingrese el nombre de la estación origen: ")
        nombre_destino = input("ingrese el nombre de la estación destino: ")
    else:
        sys.exit(0)
sys.exit(0)
