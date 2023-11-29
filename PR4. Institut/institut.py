from datetime import *

#Variables Globals
#alumnes és un diccionari que tindrà com a Key el codi de l'alumne, i com a Value al propi alumne
alumnes={}
#materies és un diccionari que tindrà com a Key el codi de la materia i com a value la pròpia matèria
materies={}


#Classes
class Alumne:
    def __init__(self,Codi:str,Nom:str,Cognom:str,DataNaixement:date):
        self.Codi=Codi
        self.Nom=Nom
        self.Cognom=Cognom
        self.DataNaixement=DataNaixement
        #self.Materies és un diccionari que tindrà com a Key el codi de MAtèria, i com a value la nota que ha tret l'alumnes de la matèria
        self.Materies={}
class Materia:
    def __init__(self,Codi:str,Nom:str):
        self.Codi=Codi
        self.Nom=Nom
        #self.Alumnes és una llista que contindrà els alumnes que estan matriculats de cada matèria. Han de ser els alumnes(Clss Alumne), no els codis d'alumnes
        self.Alumnes=[]

#Funcions que heu de programar
def nouAlumne():
    #Ha de demanar les dades d'un alumne, crea-lo i retornar una variable de la classe Alumne
    codi = input("Codi: ")
    nom = input("Nom: ")
    cognom = input("Cognom: ")
    datanaixement = datetime.strptime(input("Data Naixement: "), '%d/%m/%Y')
    alu =  Alumne(codi,nom,cognom,datanaixement)
    return alu
def obtenirMateriesNoms(codiAlumne:str):
     codisMateries = []
     nomsMateries = []
     if len(alumnes[codiAlumne].Materies) > 0:
         for a in alumnes[codiAlumne].Materies.keys():
            codisMateries.append(a)
            nomsMateries.append(f'{a}-{materies[a].Nom}')
         return [codisMateries,nomsMateries]
def calcularMitjanaAlumne(codiAlumne:str):
    media = 0
    longitud = len(alumnes[codiAlumne].Materies)
    if longitud > 0:
        for a in alumnes[codiAlumne].Materies.values():
            media += a
        media = media / longitud
        return media
    else:
        return None
def aprobats(llista): #Cantidad y porcentaje de aprobados de una lista de notas cualquiera
     lenTotal = len(llista)
     listaAprobados = list(filter(lambda x: x >= 5, llista))
     print(listaAprobados)
     lenAprobados = len(listaAprobados)
     return [lenAprobados,(lenAprobados/lenTotal)*100]

     
def calcularMitjanaMateria(codiMateria:str):
    media = 0
    longitud = len(materies[codiMateria].Alumnes)
    if longitud > 0:
        for a in materies[codiMateria].Alumnes:
            media += a.Materies[codiMateria]
        media /= longitud
        return media
    


def obtenirAlumnesNoms(): #Usado en tkinter (para menus desplegables)
    codisAlumnes = []
    nomsAlumnes = []
    for a in alumnes.keys():  
        codisAlumnes.append(a)
        nomsAlumnes.append(f'{a}-{alumnes[a].Nom} {alumnes[a].Cognom}')
    return [codisAlumnes,nomsAlumnes]
def obtenirAlumnes(): #Retorna una lista de todos los objetos Alumne del diccionario
    alumnesLista = []
    for a in alumnes.values():  
        alumnesLista.append(a)
    return alumnesLista

def obtenirNota(codiAlumne:str, codiMateria:str):
    if estaMatriculat(codiAlumne,codiMateria):
        return alumnes[codiAlumne].Materies[codiMateria]
    else:
        return None
def obtenirMateries():
    materiesLista = []
    for a in materies.values():
        materiesLista.append(a)
    return materiesLista
def obtenirMateriesNM(codiAlumne:str): #NM = No matriculado, usado para la funcion de matricular alumnos a materias (no aparecen las que ya esta matriculado)
    materiesLista = obtenirMateries()
    materiesNM = [[],[]]
    for a in materiesLista:
        if not estaMatriculat(codiAlumne,a.Codi):
            materiesNM[0].append(a.Codi)
            materiesNM[1].append(f'{a.Codi}-{a.Nom}') 
    return materiesNM
def obtenirAlumnesMateria(codiMateria:str):
    listaAlumnes = []
    for a in materies[codiMateria].Alumnes:
        listaAlumnes.append([a,a.Materies[codiMateria]])
    return listaAlumnes

def novaMateria():
    #Metode per crear una materia
    codi = input("Codi: ")
    nom = input("Nom: ")
    mat =  Materia(codi,nom)
    return mat
def modificarAlumne(codiAlumne:str, nouNom:str,nouCognom:str,novaDataNaix:str):
    try:
        datetime.strptime(novaDataNaix, '%d/%m/%Y')
        alumnes[codiAlumne].DataNaixement = novaDataNaix
        alumnes[codiAlumne].Nom = nouNom
        alumnes[codiAlumne].Cognom = nouCognom
        return 1
    except:
        return 0
def modificarMateria(codiMateria:str, nouCodi:str, nouNom:str):
    if codiMateria != nouCodi: #Si queremos cambiar el codigo de materia, se quitan todos los alumnos de la antigua y se ponen en la nueva.
        if nouCodi in materies: #Evitar duplicados
            return 0
        else:
            for alumne in materies[codiMateria].Alumnes:
                alumne.Materies[nouCodi] = alumne.Materies.pop(codiMateria)
            materies[nouCodi] = materies.pop(codiMateria)
            materies[nouCodi].Nom = nouNom
            materies[nouCodi].Codi = nouCodi
    else:
        materies[codiMateria].Nom = nouNom
    return 1



def afegirAlumne(a:Alumne):
    #Afegirà l'alumne a al diccionari alumnes
    if a.Codi in alumnes:
        return 2
    else:
        try:
            alumnes[a.Codi] = a
            datetime.strptime(a.DataNaixement, '%d/%m/%Y')
            return 1
        except:
            return 0
        
    

def afegirMateria(m:Materia):
    #Afegirà la materia m al diccionaru materies
    if m.Codi in materies:
        return 0
    else:
        materies[m.Codi] = m
        return 1



def eliminarAlumne(codiAlumne:str):
    #Ha de eliminar-lo de totes les materies que estigui matriculat
    for materia in alumnes[codiAlumne].Materies.keys():
        i = materies[materia].Alumnes.index(alumnes[codiAlumne])
        materies[materia].Alumnes.pop(i)
    #Elimina del diccionary alumnes, l'alumne que té com a codi codiAlumne
    alumnes.pop(codiAlumne)
    


def eliminarMateria(codiMateria:str):
    #Eliminar la materia amb codiMateria del diccionari materies,
    #i també del diccionari a.materies de tots els alumnes que estaven matriculats d'aquella matèria
    for alumne in materies[codiMateria].Alumnes:
        alumne.Materies.pop(codiMateria)
    materies.pop(codiMateria)
    


def matriculaAlumne(codiAlumne:str,codiMateria:str):
    #agafarà l'alumne a, que té com a codi codiAlumne del dicc alumnes
    #agafarà la materia m, que té com a codi codiMateria del dicc materies
    #afegirà el coidiMateria a alumne a, per tant, l'afegirà al diccionai a.Materies, amb value buit, el value serà la nota
    #afegirà l'alumne a la materia m, l'afegirà a la llista m.Alumnes
    #Tot l'anterior sempre comprovant que existeixen l'alumne i la materia
    if codiAlumne in alumnes and codiMateria in materies:
        if estaMatriculat(codiAlumne,codiMateria):
            return 2
        else:
            materies[codiMateria].Alumnes.append(alumnes[codiAlumne])
            alumnes[codiAlumne].Materies[codiMateria] = None
            return 1
    else:
        return 0


def estaMatriculat(codiAlumne:str,codiMateria:str):
    if codiMateria in alumnes[codiAlumne].Materies and alumnes[codiAlumne] in materies[codiMateria].Alumnes:
        return True
    else:
        return False
def desmatriculaAlumne(codiAlumne:str,codiMateria:str):
    #Ha de fer el contrari que el métode anterior
    if codiAlumne in alumnes and codiMateria in materies and estaMatriculat(codiAlumne,codiMateria):
            i = materies[codiMateria].Alumnes.index(alumnes[codiAlumne])
            materies[codiMateria].Alumnes.pop(i)
            alumnes[codiAlumne].Materies.pop(codiMateria)
            return 1
    else:
        return 0

def posarNota(codiAlumne:str,codiMateria:str,nota):
    try:
        nota = float(nota)
        if not (nota >= 0 and nota <= 10):
            return 0
        elif estaMatriculat(codiAlumne,codiMateria):
            alumnes[codiAlumne].Materies[codiMateria] = nota
            return 1 #Exito
        else:
            return 2 #No matriculado
    except:
        return 0 #La nota no es numerica

def mostrarNotesMateria(codiMateria:str):
    #Li passarem el codi d'una Matèria i ens mostrarà per pantalla un llistat amb les següents columnes:
    #Nom Materia CodiAlumne NomAlumne Nota
    #Si l'alumne no té nota, mostrarà 2 guionets --
    if codiMateria in materies:
        print (f'{"Materia":<15} {"Codi_Alumne":>10} {"Nom_Alumne":>10} {"Nota":>2}')
        nomMateria = materies[codiMateria].Nom
        for alumne in materies[codiMateria].Alumnes:
            nota = alumne.Materies[codiMateria] if alumne.Materies[codiMateria] else "--"
            print(f'{nomMateria:<15} {alumne.Codi:>10} {alumne.Nom:>10} {nota:>4}')
        return "--------------------------------------------------------------------"
    else:
        return 0

def mostrarNotesAlumne(codiAlumne:str):
    #Li passarem el codi d'un alumne i ens mostrarà per pantalla un llistat amb les següents columnes:
    #Nom Materia  Nota
    #Si l'alumne no té nota, mostrarà 2 guionets --
    if codiAlumne in alumnes:
        print (f'{"Materia":<15} {"Codi_Alumne":>10} {"Nom_Alumne":>10} {"Nota":>3}')
        nomAlumne = alumnes[codiAlumne].Nom
        codiAlumne = alumnes[codiAlumne].Codi
        for materia in alumnes[codiAlumne].Materies.keys():
            if alumnes[codiAlumne].Materies[materia]:
                nota = alumnes[codiAlumne].Materies[materia]
            else:
                nota = "--"
            print(f'{materies[materia].Nom:<15} {codiAlumne:>10} {nomAlumne:>10} {nota:>5}')
    else:
        return 0
