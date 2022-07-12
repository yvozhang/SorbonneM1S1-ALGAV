import math
import random
import time
import os

from graphviz import Digraph
from matplotlib import pyplot as plt

##################################    Partie I  Echauffement     ###################################


'''Question 1.2'''


def decomposition(num):
    listBi = []
    bi = format(num, "b")
    bi = str(bi)
    for i in bi:
        if i == "1":
            listBi.append(True)
        else:
            listBi.append(False)
    listBi.reverse()
    return listBi

#print(decomposition(38))

'''[False, True, True, False, False, True]'''


'''Question 1.3'''


def completion(liste, size):
    if size < len(liste):
        return liste[0:size]
    else:
        for i in range(len(liste), size):
            liste.append(False)
        return liste


# print(completion([False, True, True, False, False, True],4))
'''[False, True, True, False]'''
# print(completion([False, True, True, False, False, True],8))
'''[False, True, True, False, False, True, False, False]'''

'''Question 1.4'''


def table(x, n):
    liste1 = decomposition(x)
    liste2 = completion(liste1, n)
    return liste2

# print(table(38, 8))


'''[False, True, True, False, False, True, False, False]'''


##################################         Fin  Partie I         ###################################


###############################    Partie II  Arbre de décision et compression     ###########################


'''Question 2.5'''

class ArbreBinaire:
    def __init__(self, valeur, gauche=None, droit=None, lukaval=None):
        self.valeur = valeur
        self.lukaval = lukaval
        self.gauche = gauche
        self.droit = droit
        self.id = str(round(random.uniform(0, 1), 20))

    def insert_gauche(self, valeur):
        if self.gauche == None:
            self.droit = ArbreBinaire(valeur)
        else:
            new_node = ArbreBinaire(valeur)
            new_node.gauche = self.gauche
            self.gauche = new_node

    def insert_droit(self, valeur):
        if self.droit == None:
            self.droit = ArbreBinaire(valeur)
        else:
            new_node = ArbreBinaire(valeur)
            new_node.droit = self.droit
            self.droit = new_node

    def get_valeur(self):
        return self.valeur

    def get_gauche(self):
        return self.gauche

    def get_droit(self):
        return self.droit

    def get_id(self):
        return self.id

    def get_luka(self):
        return self.lukaval


#######fin de la classe########

'''Question 2.6'''


def cons_abr(liste):
    taille = len(liste)
    if taille == 1:
        return ArbreBinaire(liste[0])
    mid = taille // 2
    return ArbreBinaire("x" + str(int(math.log2(taille))), cons_abr(liste[:mid]), cons_abr(liste[mid:]))


'''Question 2.7'''


def luka(Noeud):
    if Noeud == None:
        return

    if Noeud.gauche != None:
        luka(Noeud.gauche)

    if Noeud.droit != None:
        luka(Noeud.droit)

    if not isinstance(Noeud.valeur, bool):
        Noeud.lukaval = str(Noeud.valeur) + "(" + str(Noeud.gauche.get_luka()) + ")" + "(" + str(
            Noeud.droit.get_luka()) + ")"
        # print(str(Noeud.valeur)+"("+str(Noeud.gauche.get_valeur())+")"+"("+str(Noeud.droit.get_valeur())+")")
    else :
        Noeud.lukaval = Noeud.valeur
    return Noeud


'''Question 2.8'''


def compression(dicNoeud,Noeud):
    tree = dicNoeud.get(Noeud.get_luka())

    if(tree == None):
        dicNoeud[Noeud.get_luka()] = Noeud
        if(not isinstance(Noeud.valeur,bool)):
            Noeud.gauche = compression(dicNoeud,Noeud.gauche)
            Noeud.droit = compression(dicNoeud,Noeud.droit)
        return Noeud
    else:
        return tree


'''Question 2.9'''

listN = []


def listNoeud(Noeud):
    if Noeud.get_gauche() == None:
        listN.append([Noeud,None,None])
    if Noeud.get_gauche() != None and [Noeud, Noeud.gauche, Noeud.droit] not in listN:
        listN.append([Noeud, Noeud.gauche, Noeud.droit])
        listNoeud(Noeud.get_gauche())
        listNoeud(Noeud.get_droit())


# Créer un ficher dot
def dot(Noeud):
    listNoeud(Noeud)
    path = os. getcwd()
    f = open(path+'/arbre.dot', "a")
    f.write("digraph test {\n")

    if len(listN) > 1:
        for node in listN:
            if node[1] != None:
                f.write(node[0].get_id() + "   [ label=\" " + node[0].valeur + " \"];\n")
                f.write(node[1].get_id() + "   [ label=\" " + str(node[1].valeur) + " \"];\n")
                f.write(node[2].get_id() + "   [ label=\" " + str(node[2].valeur) + " \"];\n")
                f.write(node[0].get_id() + " -> " + str(node[1].get_id()) + "   [ style=dashed  ];\n")
                f.write(node[0].get_id() + " -> " + str(node[2].get_id()) + "   [ style=solid  ];\n")
    else:
        for node in listN:
            f.write(node[0].get_id() + "   [ label=\" " + node[0].valeur + " \"];\n")
    f.write("}")

    f.close()


# Afficher le graph directement par python
def dot_py(Noeud):
    listNoeud(Noeud)
    #print(listN)
    dot = Digraph(name="Tree", comment="Tree graph", format="png")
    if len(listN)>1:
        for node in listN:
            if node[1] != None:
                dot.node(name=str(node[0].get_id()), label=str(node[0].valeur))
                dot.node(name=str(node[1].get_id()), label=str(node[1].valeur))
                dot.node(name=str(node[2].get_id()), label=str(node[2].valeur))
                dot.edge(str(node[0].get_id()), str(node[1].get_id()),_attributes={'style':'dotted'})
                dot.edge(str(node[0].get_id()), str(node[2].get_id()))
    else:
        for node in listN:
            dot.node(name=str(node[0].get_id()), label=str(node[0].valeur))

    print(dot.source)
    path = os. getcwd()
    dot.view(filename="graph_test", directory=path)
    dot.render(filename='graph_test', directory=path, view=True)


##################################         Fin  Partie II         ###################################


###############################    Partie III  Arbre de d ́ecision et ROBDD     ###########################

'''Question 3.10'''


def compression_bdd(Noeud):

    if isinstance(Noeud.lukaval,bool):
        return Noeud
    else:
        Noeud.gauche = compression_bdd(Noeud.gauche)
        Noeud.droit = compression_bdd(Noeud.droit)

        if(Noeud.gauche.get_id()==Noeud.droit.get_id()):
            return Noeud.get_droit()

        return Noeud


##################################         Fin  Partie III         ###################################





#################################          Partie TEST               #################################


'''TEST1 cons_arb()'''

'''
abd = cons_abr(table(38,8))
dot(abd)
dot_py(abd)
'''


'''TEST2 luka()'''
'''
abd = cons_abr(table(38,8))
luka(abd)
dot(abd)
dot_py(abd)
'''

'''TEST3 compression()'''
'''
abd = cons_abr(table(38,8))
luka(abd)
abd = compression({},abd)
dot(abd)
dot_py(abd)
'''

'''TEST4 compression_bdd()'''
'''
abd = cons_abr(table(38,8))
luka(abd)
abd = compression({},abd)
abd = compression_bdd(abd)
dot(abd)
dot_py(abd)
'''


##################################         Fin  Partie TEST         ###################################

#################################          Partie IV  Exprimental        #################################

nbNode=[]


def size(tree):
    if tree == None:
        return

    if tree.id not in nbNode:
        nbNode.append(tree.id)
    size(tree.get_gauche())
    size(tree.get_droit())

tableVertie=[]


def newTest1():
    resultDic = {}
    for value in range(0, 4):
        tableVertie.append(table(value, 2))
    for i in range(0, 4):
        nbNode.clear()
        tree = cons_abr(tableVertie[i])
        luka(tree)
        tree = compression({},tree)
        tree = compression_bdd(tree)  # transformer l'arbre en ROBDD
        size(tree)
        nbNoeud = len(nbNode)
        if nbNoeud in resultDic:  # resultDic.has_key(nbNoeud):
            resultDic[nbNoeud] = resultDic[nbNoeud] + 1
        else:
            resultDic[nbNoeud] = 1
    return resultDic


def newTest2():
    resultDic = {}
    for value in range(0, 16):
        tableVertie.append(table(value, 4))
    for i in range(0, 16):
        nbNode.clear()
        tree = cons_abr(tableVertie[i])
        luka(tree)
        tree = compression({},tree)
        tree = compression_bdd(tree)  # transformer l'arbre en ROBDD
        size(tree)
        nbNoeud = len(nbNode)
        if nbNoeud in resultDic:  # resultDic.has_key(nbNoeud):
            resultDic[nbNoeud] = resultDic[nbNoeud] + 1
        else:
            resultDic[nbNoeud] = 1
    return resultDic


def newTest3():
    resultDic = {}
    for value in range(0, 256):
        tableVertie.append(table(value, 8))
    for i in range(0, 256):
        nbNode.clear()
        tree = cons_abr(tableVertie[i])
        luka(tree)
        tree = compression({},tree)
        tree = compression_bdd(tree)  # transformer l'arbre en ROBDD
        size(tree)
        nbNoeud = len(nbNode)
        if nbNoeud in resultDic:  # resultDic.has_key(nbNoeud):
            resultDic[nbNoeud] = resultDic[nbNoeud] + 1
        else:
            resultDic[nbNoeud] = 1
    return resultDic


def newTest4():
    resultDic = {}
    for value in range(0, 65536):
        tableVertie.append(table(value, 16))
    for i in range(0, 65536):
        print(i)
        nbNode.clear()
        tree = cons_abr(tableVertie[i])
        luka(tree)
        tree = compression({},tree)
        tree = compression_bdd(tree)  # transformer l'arbre en ROBDD
        size(tree)
        nbNoeud = len(nbNode)
        if nbNoeud in resultDic:  # resultDic.has_key(nbNoeud):
            resultDic[nbNoeud] = resultDic[nbNoeud] + 1
        else:
            resultDic[nbNoeud] = 1
    return resultDic


def newTest5():
    resultDic = {}
    for simple in range(0, 500003):
        randomNum = random.randint(0,pow(2,32)-1)
        tableVertie.append(table(randomNum, 32))
    for i in range(0, 500003):
        print(i)
        nbNode.clear()
        tree = cons_abr(tableVertie[i])
        luka(tree)
        tree = compression({},tree)
        tree = compression_bdd(tree)  # transformer l'arbre en ROBDD
        size(tree)
        nbNoeud = len(nbNode)
        if nbNoeud in resultDic:  # resultDic.has_key(nbNoeud):
            resultDic[nbNoeud] = resultDic[nbNoeud] + 1
        else:
            resultDic[nbNoeud] = 1
    return resultDic


def newTest6():
    resultDic = {}
    for simple in range(0, 400003):
        randomNum = random.randint(0,pow(2,64)-1)
        tableVertie.append(table(randomNum, 64))
    for i in range(0, 400003):
        print(i)
        nbNode.clear()
        tree = cons_abr(tableVertie[i])
        luka(tree)
        tree = compression({},tree)
        tree = compression_bdd(tree)  # transformer l'arbre en ROBDD
        size(tree)
        nbNoeud = len(nbNode)
        if nbNoeud in resultDic:  # resultDic.has_key(nbNoeud):
            resultDic[nbNoeud] = resultDic[nbNoeud] + 1
        else:
            resultDic[nbNoeud] = 1
    return resultDic


def newTest7():
    resultDic = {}
    for simple in range(0, 486892):
        randomNum = random.randint(0,pow(2,128)-1)
        tableVertie.append(table(randomNum, 128))
    for i in range(0, 486892):
        print(i)
        nbNode.clear()
        tree = cons_abr(tableVertie[i])
        luka(tree)
        tree = compression({},tree)
        tree = compression_bdd(tree)  # transformer l'arbre en ROBDD
        size(tree)
        nbNoeud = len(nbNode)
        if nbNoeud in resultDic:  # resultDic.has_key(nbNoeud):
            resultDic[nbNoeud] = resultDic[nbNoeud] + 1
        else:
            resultDic[nbNoeud] = 1
    return resultDic


def newTest8():
    resultDic = {}
    for simple in range(0, 56343):
        randomNum = random.randint(0,pow(2,256)-1)
        tableVertie.append(table(randomNum, 256))
    for i in range(0, 56343):
        print(i)
        nbNode.clear()
        tree = cons_abr(tableVertie[i])
        luka(tree)
        tree = compression({},tree)
        tree = compression_bdd(tree)  # transformer l'arbre en ROBDD
        size(tree)
        nbNoeud = len(nbNode)
        if nbNoeud in resultDic:  # resultDic.has_key(nbNoeud):
            resultDic[nbNoeud] = resultDic[nbNoeud] + 1
        else:
            resultDic[nbNoeud] = 1
    return resultDic


def newTest9():
    resultDic = {}
    for simple in range(0, 94999):
        randomNum = random.randint(0,pow(2,512)-1)
        tableVertie.append(table(randomNum, 512))
    for i in range(0, 94999):
        print(i)
        nbNode.clear()
        tree = cons_abr(tableVertie[i])
        luka(tree)
        tree = compression({},tree)
        tree = compression_bdd(tree)  # transformer l'arbre en ROBDD
        size(tree)
        nbNoeud = len(nbNode)
        if nbNoeud in resultDic:  # resultDic.has_key(nbNoeud):
            resultDic[nbNoeud] = resultDic[nbNoeud] + 1
        else:
            resultDic[nbNoeud] = 1
    return resultDic


def newTest10():
    resultDic = {}
    for simple in range(0, 17975):
        randomNum = random.randint(0,pow(2,1024)-1)
        tableVertie.append(table(randomNum, 1024))
    for i in range(0, 17975):
        print(i)
        nbNode.clear()
        tree = cons_abr(tableVertie[i])
        luka(tree)
        tree = compression({},tree)
        tree = compression_bdd(tree)  # transformer l'arbre en ROBDD
        size(tree)
        nbNoeud = len(nbNode)
        if nbNoeud in resultDic:  # resultDic.has_key(nbNoeud):
            resultDic[nbNoeud] = resultDic[nbNoeud] + 1
        else:
            resultDic[nbNoeud] = 1
    return resultDic


def graphy_test_1():
    dicRes = newTest1()
    sorted(dicRes)
    keylist = dicRes.keys()
    newd = {}
    for key in sorted(keylist):
        newd[key] = dicRes[key]
    print(newd)
    all_keys = newd.keys()
    all_values = newd.values()

    plt.plot(list(all_keys), list(all_values), 'b-o')
    plt.xlabel("ROBDD node count for 1 variable")
    plt.ylabel("Number of Boolean functions")
    plt.grid()
    plt.axis([0, 4, 0, 5])
    plt.show()


def graphy_test_2():
    dicRes = newTest2()
    sorted(dicRes)
    keylist = dicRes.keys()
    newd = {}
    for key in sorted(keylist):
        newd[key] = dicRes[key]
    print(newd)
    all_keys = newd.keys()
    all_values = newd.values()

    plt.plot(list(all_keys), list(all_values), 'b-o')
    plt.xlabel("ROBDD node count for 2 variable")
    plt.ylabel("Number of Boolean functions")
    plt.grid()
    plt.axis([0, 6, 0, 10])
    plt.show()


def graphy_test_3():
    dicRes = newTest3()
    sorted(dicRes)
    keylist = dicRes.keys()
    newd = {}
    for key in sorted(keylist):
        newd[key] = dicRes[key]
    print(newd)
    all_keys = newd.keys()
    all_values = newd.values()

    plt.plot(list(all_keys), list(all_values), 'b-o')
    plt.xlabel("ROBDD node count for 3 variable")
    plt.ylabel("Number of Boolean functions")
    plt.grid()
    plt.axis([0, 10, 0, 100])
    plt.show()


def graphy_test_4():
    dicRes = newTest4()
    sorted(dicRes)
    keylist = dicRes.keys()
    newd = {}
    for key in sorted(keylist):
        newd[key] = dicRes[key]
    print(newd)
    all_keys = newd.keys()
    all_values = newd.values()

    plt.plot(list(all_keys), list(all_values), 'b-o')
    plt.xlabel("ROBDD node count for 4 variable")
    plt.ylabel("Number of Boolean functions")
    plt.grid()
    plt.axis([0, 12, 0, 25000])
    plt.show()


def graphy_test_5():
    dicRes = newTest5()
    sorted(dicRes)
    keylist = dicRes.keys()
    newd = {}
    for key in sorted(keylist):
        newd[key] = dicRes[key]
    print(newd)
    nbKey = list(newd.keys())
    print("unique size:"+str(len(nbKey)))
    all_keys = list(newd.keys())
    all_values = list(newd.values())
    all_values_new = [i * 8589 for i in all_values]

    plt.plot(all_keys, all_values_new, 'b-o')
    plt.xlabel("ROBDD node count for 5 variable")
    plt.ylabel("Number of Boolean functions")
    plt.grid()
    plt.axis([0, 20, 0, 2*pow(10, 9)])
    plt.show()


def graphy_test_6():
    dicRes = newTest6()
    sorted(dicRes)
    keylist = dicRes.keys()
    newd = {}
    for key in sorted(keylist):
        newd[key] = dicRes[key]
    print(newd)
    nbKey = list(newd.keys())
    print("unique size:"+str(len(nbKey)))
    all_keys = list(newd.keys())
    all_values = list(newd.values())
    all_values_new = [i * (pow(2, 64) / 400003) for i in all_values]

    plt.plot(all_keys, all_values_new, 'b-o')
    plt.xlabel("ROBDD node count for 6 variable")
    plt.ylabel("Number of Boolean functions")
    plt.grid()
    plt.axis([0, 35, 0, 5*pow(10,18)])
    plt.show()


def graphy_test_7():
    dicRes = newTest7()
    sorted(dicRes)
    keylist = dicRes.keys()
    newd = {}
    for key in sorted(keylist):
        newd[key] = dicRes[key]
    print(newd)
    nbKey = list(newd.keys())
    print("unique size:"+str(len(nbKey)))
    all_keys = list(newd.keys())
    all_values = list(newd.values())
    all_values_new = [i * 6.988 for i in all_values]

    plt.plot(all_keys, all_values_new, 'b-o')
    plt.xlabel("ROBDD node count for 7 variable")
    plt.ylabel("Number of Boolean functions(10^32)")
    plt.grid()
    plt.axis([0, 50, 0, 9*pow(10, 5)])
    plt.show()


def graphy_test_8():
    dicRes = newTest8()
    sorted(dicRes)
    keylist = dicRes.keys()
    newd = {}
    for key in sorted(keylist):
        newd[key] = dicRes[key]
    print(newd)
    nbKey = list(newd.keys())
    print("unique size:"+str(len(nbKey)))
    all_keys = list(newd.keys())
    all_values = list(newd.values())
    all_values_new = [i * 2.055  for i in all_values]

    plt.plot(all_keys, all_values_new, 'b-o')
    plt.xlabel("ROBDD node count for 8 variable")
    plt.ylabel("Number of Boolean functions(*10^72)")
    plt.grid()
    plt.axis([0, 90, 0, 3*pow(10,4)])
    plt.show()


def graphy_test_9():
    dicRes = newTest9()
    sorted(dicRes)
    keylist = dicRes.keys()
    newd = {}
    for key in sorted(keylist):
        newd[key] = dicRes[key]
    print(newd)
    nbKey = list(newd.keys())
    print("unique size:"+str(len(nbKey)))
    all_keys = list(newd.keys())
    all_values = list(newd.values())
    all_values_new = [i * 1.411363 for i in all_values]

    plt.plot(all_keys, all_values_new, 'b-o')
    plt.xlabel("ROBDD node count for 9 variable")
    plt.ylabel("Number of Boolean functions(*10^149)")
    plt.grid()
    plt.axis([0, 160, 0, 2.5*pow(10,4)])
    plt.show()


def graphy_test_10():
    dicRes = newTest10()
    sorted(dicRes)
    keylist = dicRes.keys()
    newd = {}
    for key in sorted(keylist):
        newd[key] = dicRes[key]
    print(newd)
    nbKey = list(newd.keys())
    print("unique size:"+str(len(nbKey)))
    all_keys = list(newd.keys())
    all_values = list(newd.values())
    all_values_new = [i * 1.000107 for i in all_values]

    plt.plot(all_keys, all_values_new, 'b-o')
    plt.xlabel("ROBDD node count for 10 variable")
    plt.ylabel("Number of Boolean functions(*10^304")
    plt.grid()
    plt.axis([0, 300, 0, 2*pow(10, 3)])
    plt.show()

##################################         Fin  Partie IV  Exprimental    ##############################

#################################          Partie  Exprimental  TEST     #################################

start =time.perf_counter()

# graphy_test_1()
# graphy_test_2()
# graphy_test_3()
# graphy_test_4()
# graphy_test_5()
# graphy_test_6()
# graphy_test_7()
# graphy_test_8()
# graphy_test_9()
# graphy_test_10()

end = time.perf_counter()

print('Running time: %s Seconds'%(end-start))
