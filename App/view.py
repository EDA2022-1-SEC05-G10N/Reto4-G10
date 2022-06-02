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
archivo_viajes = "Bikeshare // Bikeshare-ridership-2021-utf8-small.csv"
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

def print_info_carga():
    print('Total de viajes: ')
    print('Total de vertices del grafo: ')
    print('Total de arcos del grafo: ')
    print('Primeros 5 y ultimos 5 vertices cargados: ')
    for vertice in lt.iterator(lista_vertices):
        print(vertice['id'])
        print(vertice['name'])
        print(vertice['n_viajes'])


catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Inicializando....")
        cont = controller.init()

    elif int(inputs[0]) == 2:
        print("Cargando informacion de viajes....")
        x, numentry = controller.loadData(cont,archivo_viajes)
        num_edges = controller.totalConexiones(cont,archivo_viajes)
        num_vertices = controller.totalParadas(cont)
        num_viajes = controller.viajesTotales(cont)
        primeras_y_ultimas, size = controller.posiciones(cont)
        carga(numentry,num_edges,num_vertices,num_viajes,primeras_y_ultimas)
        print(size)

    elif int(inputs[0]) == 3:
        print("Requerimiento 1")
        info1 = controller.getInfo1(cont)
        printReq1(info1)

    elif int(inputs[0]) == 4:
        print("Requerimiento 2")
        estacion_inicial = input("Ingrese la estación de origen: ")
        disponibilidad = input("Ingrese su disponibilidad: ")
        minimo_paradas = int(input("Ingrese el numero minimo de paradas: "))
        estaciones = int(input("Ingrese el numero de rutas de respuesta: "))
        info2 = controller.getInfo2(cont,estacion_inicial,disponibilidad,minimo_paradas,estaciones)
        printReq2(info2)

    elif int(inputs[0]) == 5:
        print("Requerimiento 3 ")
        nombre_origen = input("Ingrese el nombre de la estación origen: ")
        nombre_destino = input("ingrese el nombre de la estación destino: ")
        info3 = controller.getInfo3(cont,nombre_origen,nombre_destino)
        printReq3(info3)
    
    elif int(inputs[0]) == 6: 
        print("Requerimiento 4")
        fecha_inicial = input("Ingrese la fecha inicial (formato MM/DD/AA)")
        fecha_final = input("Ingrese la fecha final (formato MM/DD/AA)")
        info4 = controller.getInfo4(cont,fecha_inicial,fecha_final)
        printReq4(info4)
    
    elif int(inputs[0]) == 7: 
        print("Requerimiento 5 ")
        bicicleta = int(input("Ingrese el identificador de la bicicleta: "))
        fechaa_inicial = input("Ingrese la fecha inicial (formato MM/DD/AA)")
        fechaa_final = input("Ingrese la fecha final (formato MM/DD/AA)")
        info5 = controller.getInfo5(cont,bicicleta,fechaa_inicial,fechaa_final)
        printReq5(info5)
    
    elif int(nputs[0]) == 8:
        print("Requerimiento 6")
        nombre_estacion = input("Ingrese el nombre de la estación")
        info6= controller.getInfo6(cont,nombre_estacion)
        printReq6(info6)
   
    else:
        sys.exit(0)
sys.exit(0)
