from institut import *
import random
nombres = ['Juan','Pedro','Manuel','Ernesto','Daniel']
apellidos = ['Perez','Rodriguez','Martinez','Hernandez']
materiasEjemplo = ['Matematicas','Historia','Tecnologia','Informatica','Musica']
def omplirDades():
    for b in range(0,len(materiasEjemplo)):
        afegirMateria(Materia(f'M{b}',materiasEjemplo[b]))
    for a in range(0,20):
        afegirAlumne(Alumne(f'A{a}',random.choice(nombres),random.choice(apellidos),f'{random.randint(1,30)}/{random.randint(1,12)}/{random.randint(1990,2005)}')) #Generar l'alumne
        for b in range(0,random.randint(0,len(materiasEjemplo))): #Matricular l'alumne
            matriculaAlumne(f'A{a}',f'M{b}')
            posarNota(f'A{a}',f'M{b}',random.randint(0,10))

alumnes.clear()
materies.clear()
