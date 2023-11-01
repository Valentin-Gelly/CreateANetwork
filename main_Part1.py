import time
import heapq
import threading

from Classes.bus import Bus
from Classes.stop import Stop
from Classes.road import Road
from Classes.people import People
from Classes.travel import Travel

listeRoute = []
listeRoute.append(Road('A', 'B', 10))
listeRoute.append(Road('A', 'C', 4))
listeRoute.append(Road('C', 'D', 12))
listeRoute.append(Road('C', 'E', 4))

dicRoad = {}

for road in listeRoute:
    if road.start not in dicRoad:
        dicRoad[road.start] = []
        dicRoad[road.start].append({road.stop: road.distance})
    else:
        dicRoad[road.start].append({road.stop: road.distance})
for road in listeRoute:
    if road.stop not in dicRoad:
        dicRoad[road.stop] = []
        dicRoad[road.stop].append({road.start: road.distance})
    else:
        dicRoad[road.stop].append({road.start: road.distance})

dicRoad2 = dicRoad
# print('dic2', dicRoad2)

listeBus = []
listeBus.append(Bus(10, 1, [1, 30], 'BACECA'))
listeBus.append(Bus(10, 1, [1, 30], 'DCEC'))
listeBus.append(Bus(10, 1, [1, 30], 'BED'))
listeBus.append(Bus(2, 1, [1, 10], 'AC'))

listeStop = []
listeStop.append(Stop('A'))
listeStop.append(Stop('B'))
listeStop.append(Stop('C'))
listeStop.append(Stop('D'))
listeStop.append(Stop('E'))


def recupDonnee(nameFile):
    listePeople = []
    with open(nameFile, 'r') as peoples:
        for people in peoples:
            infoPeople = people.split()

            for k in range(int(infoPeople[0])):
                nom = infoPeople[1] + '' + str(k).rjust(2, '0')
                heureDepart = infoPeople[2]
                trajetDepart = infoPeople[3]
                heureRetour = infoPeople[4]
                trajetRetour = infoPeople[5]
                listePeople.append(People(Travel(heureDepart, trajetDepart), Travel(heureRetour, trajetRetour), nom))
    lettreStop = []
    for stop in listeStop:
        lettreStop.append(stop.startRoads)
    for people in listePeople:
        depart = people.voyageAller.travel[0]
        arretDepart = lettreStop.index(depart)
        listeStop[arretDepart].addPeople(people)
        print(people.__str__())
    return listePeople


while True:
    try:
        nomChier = input('Nom du fichier des personnes : ')
        listePeople = recupDonnee(nomChier)
        break
    except FileNotFoundError:
        print("Le fichier n'existe pas")
    except ValueError:
        print("Le fichier n'est pas au bon format")
    except PermissionError:
        print("Vous n'avez pas les droits pour lire ce fichier")
    except IOError:
        print("Le fichier est introuvable")


#
# Permet la route entre les deux arret
# complexité : O(n)

def getIndexRoad(start, stop) -> Road:
    if start in dicRoad:
        for road in dicRoad[start]:
            if stop in road:
                return road[stop]


def dijkstra(graph2, start, end):
    graph = graph2
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]
    previous_nodes = {}

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue
        # boucle sur les voisins du noeud courant neigbor_info = [{voisin: distance}]
        for neighbor_info in graph[current_node]:
            neighbor_info_copy = dict(neighbor_info)
            neighbor, weight = neighbor_info_copy.popitem()
            distance = current_distance + weight
            # test si la distance est plus petite que la distance enregistré
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    path = []
    while end:
        path.insert(0, end)
        print(path)
        end = previous_nodes.get(end, None)

    return path


def dijkstraPeople(graph2, start, end, numTravel):
    if numTravel == 0:
        graph = graph2
        distances = {node: float('inf') for node in graph}
        distances[start] = 0
        priority_queue = [(0, start)]
        previous_nodes = {}

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            if current_distance > distances[current_node]:
                continue

            for neighbor_info in graph[current_node]:
                neighbor_info_copy = dict(neighbor_info)
                neighbor, weight = neighbor_info_copy.popitem()
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))

        path = []
        while end:
            path.insert(0, end)
            end = previous_nodes.get(end, None)
        return path
    else:
        graph = graph2
        distances = {node: float('inf') for node in graph}
        distances[start] = 0
        priority_queue = [(0, start)]
        previous_nodes = {}

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            if current_distance > distances[current_node]:
                continue

            for neighbor_info in graph[current_node]:
                neighbor_info_copy = dict(neighbor_info)
                neighbor, weight = neighbor_info_copy.popitem()
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))

        path = []
        while end:
            path.insert(0, end)
            end = previous_nodes.get(end, None)
        return path


for y, bus in enumerate(listeBus):
    for x, stop in enumerate(bus.travel):
        graph = dicRoad2
        if x + 1 < len(bus.travel):
            Parcours = dijkstra(graph, bus.travel[x], bus.travel[x + 1])

            listeEtape = [Parcours[i] + Parcours[i + 1] for i in range(len(Parcours) - 1)]
            for step in listeEtape:
                bus.allStepRaod.append(step)
                bus.nbStep += 1

# Permets de trouver les step d'une Personnes
for x, people in enumerate(listePeople):
    people.Firsttravel = dijkstraPeople(graph, people.voyageAller.travel[0], people.voyageAller.travel[1], 0)
    listeEtape = [people.Firsttravel[i] + people.Firsttravel[i + 1] for i in range(len(people.Firsttravel) - 1)]
    for step in listeEtape:
        people.firsttravelStep.append(step)
    people.Secondtravel = dijkstraPeople(graph, people.voyageRetour.travel[0], people.voyageRetour.travel[1], 1)
    listeEtape = [people.Secondtravel[i] + people.Secondtravel[i + 1] for i in range(len(people.Secondtravel) - 1)]
    for step in listeEtape:
        people.secondtravelStep.append(step)
    people.actualStep = people.firsttravelStep[0]
    print(people.nom, people.voyageAller.travel[0], people.voyageAller.travel[1], people.firsttravelStep)


def getIndexStop(nameStop):
    for stop in listeStop:
        if stop.startRoads == nameStop:
            return listeStop.index(stop)


def fillBus(bus, x):
    try:
        for people in listeStop[getIndexStop(bus.getPosition())].getWaitingQueue():
            if people.actualStep in bus.getNextStep() and int(
                    people.voyageActuel.hour) <= horloge and bus.position in bus.travel and people.actualStep[1] in bus.travel:
                bus.remplirUnePersonne(people)
                people.setPosition(bus.getPosition())
                listeStop[getIndexStop(bus.getPosition())].removePeople(people)
                return people

    except ValueError:
        null = 0


#
# Permet de faire descendre quelqu'un d'un bus

def unFillBus(bus, x):
    try:
        if len(bus.getPeople()) > 0:
            for people in bus.getPeople():
                if people.voyageActuel.getTravel()[1] == bus.getPosition():
                    bus.viderUnePersonne(people)
                    if people.changeVoyageActuel():
                        people.actualStep = people.secondtravelStep[0]
                        listeStop[getIndexStop(bus.getPosition())].addPeople(people)
                    else:
                        text = people.nom, " est arrivé chez lui, à l'arret : ", bus.getPosition()
                        fichier.write(people.nom + " est arrivé chez lui, à l'arret : " + bus.getPosition())
                elif people.actualStep != bus.getNextStep():
                    bus.viderUnePersonne(people)
                    if people.voyageActuel == people.voyageAller:
                        people.firsttravelStep.remove(people.actualStep)
                        people.actualStep = people.firsttravelStep[0]
                        listeStop[getIndexStop(bus.getPosition())].addPeople(people)
                    else:
                        people.secondtravelStep.remove(people.actualStep)
                        people.actualStep = people.secondtravelStep[0]
                        listeStop[getIndexStop(bus.getPosition())].addPeople(people)
                return people

    except ValueError:
        null = 0


#
# permety de savoir si une personne souhaite prendre le bus

def peopleWantTakeBus(bus, x):
    try:

        for people in listeStop[getIndexStop(bus.getPosition())].getWaitingQueue() :
            if people.actualStep in bus.getNextStep() and int(people.voyageActuel.hour) <= horloge and people.actualStep[1] in bus.travel:
                # print(people.nom + ' veut prendre le bus')
                return True
            else:
                return False
    except IndexError:
        null = 0


#
# Permet de savoir si quelqu'un veut descendre du bus

def peopleWantTakeDown(bus, x):
    try:
        if bus.getPeople():
            for people in bus.getPeople():
                # print(people.nom, people.actualStep, bus.getNextStep())
                if people.actualStep != bus.getNextStep():
                    return True
                else:
                    return False
    except IndexError:
        null = 0


#
# Fonction Principale :
#   Permet de faire circuler les bus
#   Permet de faire toutes les vérifications nécessaire pour faire monter, descendre, rester un passager dans le bus

def busIsInStop(bus, x):
    #
    # Le bus est à l'arret et voit si du monde veut descendre
    #
    if len(bus.getPosition()) == 1 and peopleWantTakeDown(bus, x):
        personne = unFillBus(bus, x)
        y = x + 1
        print("quelqu'un descend du bus n°", x + 1, " : ", personne.nom)
        fichier.write("quelqu'un descend du bus n°" + str(y) + " : " + personne.nom)

    #
    # le bus est plein à un arret
    #
    elif len(bus.getPosition()) == 1 and bus.getNbPersonnes() == bus.nbPlace and not peopleWantTakeDown(bus, x):
        # print("le bus est plein à un arret")
        # print("Le bus n°" + str(x + 1) + " est plein")
        bus.setPosition(bus.getNextStep())
        for people in bus.getPeople():
            people.setPosition(bus.getPosition())

    #
    # le bus n'est pas plein et il y a des personnes à l'arrêt
    #
    elif len(bus.getPosition()) == 1 and listeStop[getIndexStop(
            bus.getPosition())].getWaitingQueue() != [] and bus.getNbPersonnes() != bus.nbPlace and peopleWantTakeBus(
        bus, x) and bus.position in bus.travel:
        text = ""
        for people in listeStop[getIndexStop(bus.getPosition())].getWaitingQueue():
            text += str(people.voyageActuel) + ", "
        fillBus(bus, x)

    #
    # le bus n'est pas plein et il n'y a personne à l'arrêt
    #

    elif len(bus.getPosition()) == 1 and listeStop[getIndexStop(bus.getPosition())].getWaitingQueue() == []:
        bus.setPosition(bus.getNextStep())
        bus.distanceFromNextStop += bus.speedMetter
        for people in bus.getPeople():
            people.setPosition(bus.getPosition())


    elif len(bus.getPosition()) == 1 and bus.nbStep != len(bus.stepPassed) and not peopleWantTakeDown(bus, x):
        print(bus.position, bus.getNextStep())
        bus.setPosition(bus.getNextStep())
        for people in bus.getPeople():
            people.setPosition(bus.getPosition())
            if people.actualStep in people.firsttravelStep:
                people.nbStep += 1
            else:
                people.nbStep += 1

    #
    # le bus est en route
    #
    elif len(bus.getPosition()) == 2 and bus.distanceFromNextStop != getIndexRoad(bus.getPosition()[0],
                                                                                  bus.getPosition()[1]):
        if bus.timeInStep == bus.speedTime:
            bus.timeInStep = 0
            bus.distanceFromNextStop += bus.speedMetter
        else:
            bus.timeInStep += 1


    #
    # le bus est au niveau de l'arrêt suivant soit il est au terminus soit il est juste à un arret
    #
    elif len(bus.getPosition()) == 2 and bus.distanceFromNextStop == getIndexRoad(bus.getPosition()[0],
                                                                                  bus.getPosition()[1]):
        bus.stepPassed.append(bus.getPosition())
        if bus.getPosition()[1] == bus.terminus and bus.nbStep == len(bus.stepPassed):

            bus.distanceFromNextStop = 0

            bus.setPosition(bus.getPosition()[1])
            for people in bus.getPeople():
                people.setPosition(bus.getPosition())

            if len(bus.getPeople()) > 0:
                unFillBus(bus, x)

            bus.allStepRaod = bus.allStepRaod[::-1]
            for y, step in enumerate(bus.allStepRaod):
                bus.allStepRaod[y] = step[::-1]
            bus.travel = bus.travel[::-1]
            bus.terminus = bus.travel[bus.travel.index(bus.terminus) - 1]
            bus.stepPassed = []

        else:
            bus.distanceFromNextStop = 0
            bus.setPosition(bus.getPosition()[1])
            for people in bus.getPeople():
                people.setPosition(bus.getPosition())
            if len(bus.getPeople()) > 0 and peopleWantTakeDown(bus, x):
                unFillBus(bus, x)


def verifFinUnivers():
    for bus in listeBus:
        if bus.getPeople() != []:
            return False
    for stop in listeStop:
        if stop.getNbPeople() != 0:
            return False
    return True


#
# Boucle permettant de faire tourner le programme

horloge = 1

with open('log.txt', 'w') as fichier:
    fichier.write("")

while horloge != 100000 and not verifFinUnivers():
    with open('log.txt', 'a') as fichier:
        print("--------------------------------------------------")
        fichier.write("--------------------------------------------------\n")
        print("tempo : ", horloge)
        fichier.write("tempo : " + str(horloge) + "\n")
        for x, bus in enumerate(listeBus):
            busIsInStop(bus, x)

        horloge += 1
        print('\n')
        fichier.write("\n")
        print('\n')
        fichier.write("\n")
        for bus in listeBus:
            fichier.write(bus.getStateBus(dicRoad))
        print('\n')
        print('\n')
        for stop in listeStop:
            fichier.write(stop.getStopState())

        print("--------------------------------------------------")
        fichier.write("--------------------------------------------------\n")
        print('\n')
        fichier.write("\n")

print("Y'A QUELQU'UN ?")
print("Y'A PERSONNE !!!!!")
#
# def find_all_routes(routes, start, end, path=[]):
#     path = path + [start]
#     if start == end:
#         return [path]
#     if start not in routes:
#         return []
#     paths = []
#     for city_dict in routes[start]:
#         city = list(city_dict.keys())[0]
#         if city not in path:
#             new_paths = find_all_routes(routes, city, end, path)
#             for new_path in new_paths:
#                 paths.append(new_path)
#     return paths
#
# routes = {
#     'A': [{'B': 10}, {'C': 4}],
#     'C': [{'D': 12}, {'A': 4}, {'E': 4}],
#     'E': [{'C': 4}, {'D': 13}],
#     'B': [{'A': 10}],
#     'D': [{'C': 12}, {'E': 13}]
# }
#
# # Temps de chargement/déchargement par personne (en secondes)
# loading_time = 1
#
# # Maintenant, vous pouvez itérer sur chaque itinéraire pour calculer le temps d'attente au carré moyen
# def calculate_average_squared_wait_time(route):
#     global average_squared_wait_time, squared_wait_time
#     total_squared_wait_time = 0
#     for i in range(len(route) - 1):
#         # print("route",route)
#         #print("start_stop",route[i])
#         #print("end_stop",route[i+1])
#         start_stop = route[i]
#         end_stop = route[i + 1]
#
#         # Calcul de la distance entre les arrêts
#         try :
#             distance = int(routes[start_stop][0][end_stop])  # Insérez votre logique pour obtenir la distance entre les arrêts
#
#
#             # Calcul du temps de trajet entre les arrêts (en secondes)
#             travel_time = distance * (1 / 30)  # bus_speed est la vitesse du bus par seconde
#
#             # Nombre de passagers à faire monter/descendre à chaque arrêt
#             passengers_at_start = 25 # nb personnes à l'arrêt
#             passengers_at_end = 10 # nb Personnes dans le bus
#
#             # Calcul du temps de chargement/déchargement total à chaque arrêt
#             loading_time_at_start = loading_time * (passengers_at_start / 1) # temps de chargement pour toutes les personnes
#             loading_time_at_end = loading_time * (passengers_at_end / 1) # temps de déchargement pour toutes les personnes
#
#             # Calcul du temps d'attente au carré à chaque arrêt
#             squared_wait_time = (loading_time_at_start + travel_time + loading_time_at_end) ** 2
#             average_squared_wait_time = squared_wait_time / passengers_at_start
#
#         except KeyError:
#             # print("erreur")
#             average_squared_wait_time = 0
#             squared_wait_time = 0
#
#         return average_squared_wait_time, squared_wait_time
#
# # Choisissez l'itinéraire optimal avec le temps d'attente moyen au carré le plus bas
# best_route = None
# min_average_squared_wait_time = float('inf')
# min_squared_wait_time = float('inf')
#
# allPossibleRoutes = []
#
# all_cities = list(routes.keys())
# for start_city in all_cities:
#     for end_city in all_cities:
#         if start_city != end_city:
#             all_routes = find_all_routes(routes, start_city, end_city)
#             for route in all_routes:
#                 result = calculate_average_squared_wait_time(route)
#                 squared_wait_Time = result[1]
#                 average_squared_wait_time = result[0]
#                 if squared_wait_Time != 0 and average_squared_wait_time !=0:
#                     print(route,average_squared_wait_time, squared_wait_Time)
#                     i=0
#                     allPossibleRoutes.append([route,average_squared_wait_time, squared_wait_Time])
#                     if average_squared_wait_time < min_average_squared_wait_time  and  squared_wait_Time < min_squared_wait_time :
#                         min_average_squared_wait_time = average_squared_wait_time
#                         min_squared_wait_time = squared_wait_Time
#                         best_route = route
#
# for route in allPossibleRoutes:
#     for route2 in allPossibleRoutes:
#         if (set(route[0])==set(route2[0])):
#             allPossibleRoutes.remove(route2)
# print(allPossibleRoutes)
# print(best_route)
# # Maintenant, best_route contient l'itinéraire optimal avec le temps d'attente moyen au carré le plus bas en prenant en compte le temps de chargement/déchargement.
