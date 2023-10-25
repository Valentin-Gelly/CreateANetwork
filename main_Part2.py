import time
import heapq
import threading

from Classes.bus import Bus
from Classes.stop import Stop
from Classes.road import Road
from Classes.people import People
from Classes.travel import Travel

listeRoute = []

dicRoad = {}
dicRoad2 = {}
#print('dic2', dicRoad2)

listeBus = []
listeBus.append(Bus(10, 1, [1, 30], 'BACECA'))
listeBus.append(Bus(10, 1, [1, 30], 'DCEC'))
listeBus.append(Bus(10, 1, [1, 30], 'BED'))
listeBus.append(Bus(2, 1, [1, 10], 'AC'))

listeStop = []



def recupDonneePersonnes(nameFile):
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
    return listePeople


def recupDonneeStop(nameFile):
    listeStop2 = []
    with open(nameFile, 'r') as stops:
        for stop in stops:
            infoStop = stop.split()
            listeStop2.append(infoStop[1])
            listeStop2.append(infoStop[2])
    listeStop2=list(set(listeStop2))
    listeStop = []
    for stop in listeStop2:
        print(stop)
        listeStop.append(Stop(stop))


    return listeStop


def recupDonneeRoute(nameFile):
    listeRoute = []
    with open(nameFile, 'r') as routes:
        for route in routes:
            infoRoute = route.split()
            print(infoRoute[1], infoRoute[2], infoRoute[3][:len(infoRoute[3]) - 1])
            listeRoute.append(Road(infoRoute[1], infoRoute[2], int(infoRoute[3][:len(infoRoute[3]) - 1])))

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

    print("dicRoad2", dicRoad2)

    return listeRoute


def recupDonneeBus(filename):
    compteur=0
    with open(filename, 'r') as bus:
        for n,line in enumerate(bus) :
            compteur+=1
            if n==0:
                nbBus = int(line[0])
            elif n==1:
                nbPlace = int(line[1])
            elif n==2:
                nbPersonnesPerSecond = int(line[2])
            elif n==3:
                nbMetterPerSecond = [int(line[2]),int(line[3])]
            if compteur == 4:
                listeBus.append(Bus(nbPlace, nbPersonnesPerSecond, nbMetterPerSecond, line[:len(line) - 1]))
                compteur=0
while True:
    try:
        nomFichierStop = input('Nom du fichier des arrêts/routes : ')
        listeStop = recupDonneeStop(nomFichierStop)
        listeRoute = recupDonneeRoute(nomFichierStop)
        break
    except FileNotFoundError:
        print("Le fichier n'existe pas")
    except ValueError:
        print("Le fichier n'est pas au bon format")
    except PermissionError :
        print("Vous n'avez pas les droits pour lire ce fichier")
    except IOError :
        print("Le fichier est introuvable")
dicRoad2 = dicRoad.copy()



while True:
    try:
        nomChier = input('Nom du fichier des personnes : ')
        listePeople = recupDonneePersonnes(nomChier)
        break
    except FileNotFoundError:
        print("Le fichier n'existe pas")
    except ValueError:
        print("Le fichier n'est pas au bon format")
    except PermissionError :
        print("Vous n'avez pas les droits pour lire ce fichier")
    except IOError :
        print("Le fichier est introuvable")


while True:
    try :
        nomFichierBus = input('Nom du fichier des bus : ')
        listeBus = recupDonneeBus(nomFichierBus)
        break
    except FileNotFoundError:
        print("Le fichier n'existe pas")
    except ValueError:
        print("Le fichier n'est pas au bon format")
    except PermissionError :
        print("Vous n'avez pas les droits pour lire ce fichier")
    except IOError :
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
    print(graph)
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    # print("graph", graph)
    priority_queue = [(0, start)]
    previous_nodes = {}

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor_info in graph[current_node]:
            # print("neighbor_info", neighbor_info)
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
    #print(bus.getStrTravel(), "bus.allStepRaod ", bus.allStepRaod, ' nbStep : ', bus.nbStep)

#
# Permet de savoir la distance entre deux arret
# complexité : O(n)
def getIndexStop(nameStop):
    for stop in listeStop:
        if stop.startRoads == nameStop:
            return listeStop.index(stop)

#
# Permet de faire monter quelqu'un dans un bus
# complexité : O(1)

def fillBus(bus, x):
    try:
        #print(bus.travel.index(listeStop[getIndexStop(bus.getPosition())].getWaitingQueue()[0].voyageActuel.travel[1]),
        #      'and', int(listeStop[getIndexStop(bus.getPosition())].getWaitingQueue()[0].voyageActuel.hour))
        if bus.travel.index(
                listeStop[getIndexStop(bus.getPosition())].getWaitingQueue()[0].voyageActuel.travel[1]) != -1 and int(
                listeStop[getIndexStop(bus.getPosition())].getWaitingQueue()[0].voyageActuel.hour) <= horloge:
            # print(listeStop[getIndexStop(bus.getPosition())].getWaitingQueue()[0].nom + ' trajet  : ' +listeStop[getIndexStop(bus.getPosition())].getWaitingQueue()[0].voyageAller.travel)
            # print('le bus n°' + str(x + 1) + ', au niveau de  : ' + bus.getPosition() + ', a  ' + str(
            # bus.getNbPersonnes()) + ' passagé(e)(s) : ', bus.remplirUnePersonne(listeStop[getIndexStop(bus.getPosition())].getWaitingQueue()[0]).nom)
            bus.remplirUnePersonne(listeStop[getIndexStop(bus.getPosition())].getWaitingQueue()[0])
            listeStop[getIndexStop(bus.getPosition())].getWaitingQueue()[0].setPosition(bus.getPosition())
            listeStop[getIndexStop(bus.getPosition())].removePeople(
                listeStop[getIndexStop(bus.getPosition())].getWaitingQueue()[0])

            # time.sleep(bus.timeReload)

    except ValueError:
        null = 0

#
# Permet de faire descendre quelqu'un d'un bus
# complexité : O(n)
def unFillBus(bus, x):
    try:
        if len(bus.getPeople()) > 0:
            y = 0
            # print(listeStop[getIndexStop(bus.getPosition())].getWaitingQueue()[0].nom + ' trajet  : ' +listeStop[getIndexStop(bus.getPosition())].getWaitingQueue()[0].voyageAller.travel)
            for people in bus.getPeople():
                if people.voyageActuel.getTravel()[1] == bus.getPosition():
                    bus.viderUnePersonne(people)
                    people.changeVoyageActuel()
                    listeStop[getIndexStop(bus.getPosition())].addPeople(people)
                    # print('le bus n°' + str(x + 1) + ', au niveau de  : ' + bus.getPosition() + ', a  ' + str(
                    # bus.getNbPersonnes()) + ' passagé(e)(s)')

                return people

    except ValueError:
        null = 0

#
# permety de savoir si une personne souhaite prendre le bus
# complexité : O(n)
def peopleWantTakeBus(bus, x):
    try:
        if listeStop[getIndexStop(bus.getPosition())].getWaitingQueue() != []:
            for people in listeStop[getIndexStop(bus.getPosition())].getWaitingQueue():
                # print(listeStop[getIndexStop(bus.getPosition())].getWaitingQueue())
                if people.voyageActuel.getTravel()[1] in bus.travel and int(people.voyageActuel.hour) <= horloge:
                    # print(people.nom + ' veut prendre le bus')
                    return True
                else:
                    return False
    except IndexError:
        null = 0

#
# Permet de savoir si quelqu'un veut descendre du bus
# complexité : O(n)
def peopleWantTakeDown(bus, x):
    try:
        if bus.getPeople():
            for people in bus.getPeople():
                if people.voyageActuel.getTravel()[1] == bus.getPosition():
                    return True
                else:
                    return False
    except IndexError:
        null = 0

#
# Fonction Principale :
#   Permet de faire circuler les bus
#   Permet de faire toutes les vérifications nécessaire pour faire monter, descendre, rester un passager dans le bus
#   complexité : O(n)

def busIsInStop(bus, x):
    #
    # Le bus est à l'arret et voit si du monde veut descendre
    #

    if len(bus.getPosition()) == 1 and peopleWantTakeDown(bus, x):
        # print("quelqu'un descend du bus : ", unFillBus(bus, x).nom)
        unFillBus(bus, x)
    #
    # le bus est plein à un arret
    #
    elif len(bus.getPosition()) == 1 and bus.getNbPersonnes() == bus.nbPlace:
        # print("Le bus n°" + str(x + 1) + " est plein")
        bus.setPosition(bus.getNextStep())
        for people in bus.getPeople():
            people.setPosition(bus.getPosition())

    #
    # le bus n'est pas plein et il y a des personnes à l'arrêt
    #

    elif len(bus.getPosition()) == 1 and listeStop[getIndexStop(
            bus.getPosition())].getWaitingQueue() != [] and bus.getNbPersonnes() != bus.nbPlace and peopleWantTakeBus(
            bus, x):
        # print("Le bus n°" + str(x + 1) + " n'est pas complet et il y a des personnes à l'arrêt " + bus.getPosition())
        # print(bus.allStepRaod)
        text = ""
        for people in listeStop[getIndexStop(bus.getPosition())].getWaitingQueue():
            text += str(people.voyageActuel) + ", "

        fillBus(bus, x)

    #
    # le bus n'est pas plein et il n'y a personne à l'arrêt
    #

    elif len(bus.getPosition()) == 1 and listeStop[getIndexStop(bus.getPosition())].getWaitingQueue() == []:
        # print("Le bus n°" + str(x + 1) + " n'est pas complet et il n'y a personne à l'arrêt" + bus.getPosition())
        bus.setPosition(bus.getNextStep())
        # print("Le bus n°" + str(x + 1) + " est au niveau de " + str(bus.getPosition()))
        bus.distanceFromNextStop += bus.speedMetter
        for people in bus.getPeople():
            people.setPosition(bus.getPosition())

    #
    # le bus est vide et personne ne veut monter
    #
    elif len(bus.getPosition()) == 1 and bus.position != bus.travel[len(bus.travel) - 1] and listeStop[getIndexStop(
            bus.getPosition())].getWaitingQueue() != [] and bus.getNbPersonnes() != bus.nbPlace and not peopleWantTakeBus(
            bus, x):
        # print("Le bus n°" + str(x + 1) + " est vide et personne ne veut monter ", bus.position)
        bus.setPosition(bus.getNextStep())


    #
    # le bus est au niveau d'un arrêt mais pas au terminus
    #
    elif len(bus.getPosition()) == 1 and bus.nbStep != len(bus.stepPassed):
        # print("Test Le bus n°" + str(x + 1) + " est au niveau de " + bus.getPosition())
        bus.setPosition(bus.getNextStep())
        for people in bus.getPeople():
            people.setPosition(bus.getPosition())
        if len(bus.getPeople()) > 0:
            unFillBus(bus, x)


    #
    # le bus est en route
    #
    elif len(bus.getPosition()) == 2 and bus.distanceFromNextStop != getIndexRoad(bus.getPosition()[0],
                                                                                  bus.getPosition()[1]):
        # print("Le bus n°" + str(x + 1) + " est au niveau de " + bus.getPosition() + " et est à " + str(bus.getDistanceFromNextStop()),"/",getIndexRoad(bus.getPosition()[0],bus.getPosition()[1]))
        if bus.timeInStep == bus.speedTime:
            bus.timeInStep = 0
            bus.distanceFromNextStop += bus.speedMetter
        else :
            bus.timeInStep += 1


    #
    # le bus est au niveau de l'arrêt suivant soit il est au terminus soit il est juste à un arret
    #
    elif len(bus.getPosition()) == 2 and bus.distanceFromNextStop == getIndexRoad(bus.getPosition()[0],
                                                                                  bus.getPosition()[1]):
        bus.stepPassed.append(bus.getPosition())
        # print(bus.travel , 'bus stepPassed : ', bus.stepPassed ,"/", bus.nbStep, '/', len(bus.stepPassed))
        if bus.getPosition()[1] == bus.terminus and bus.nbStep == len(bus.stepPassed):
            # print("Le bus n°" + str(x + 1) + " est au terminus")
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
            # print("Le bus n°" + str(x + 1) + " est au niveau de l'arret " + bus.getPosition()[1])
            bus.distanceFromNextStop = 0
            bus.setPosition(bus.getPosition()[1])
            for people in bus.getPeople():
                people.setPosition(bus.getPosition())
            if len(bus.getPeople()) > 0 and peopleWantTakeDown(bus, x):
                unFillBus(bus, x)


#
# Boucle permettant de faire tourner le programme

horloge = 1

while True:
    print("--------------------------------------------------")
    print("tempo : ", horloge)
    for x, bus in enumerate(listeBus):
        busIsInStop(bus, x)

    horloge += 1
    print('\n')
    print('\n')
    for bus in listeBus:
        bus.getStateBus(dicRoad)
    print('\n')
    print('\n')
    for stop in listeStop:
        stop.getStopState()

    print("--------------------------------------------------")
    print('\n')
    time.sleep(1)