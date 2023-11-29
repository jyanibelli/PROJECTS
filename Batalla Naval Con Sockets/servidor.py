import random
import re
import os
import socket
import threading
tablero = []
socketsJ = {}
contador = 0
barcosExistentes = dict()
barcos = [2,2,2,2,3,4]
ip = "0.0.0.0" 
puerto = 1026 
jugadores = 0
barcosJ = [2,2,2,2,2,2]
naranja = '\x1b[38;5;215m' #Colores ANSI
azul = '\x1b[38;5;21m'
rojo = '\x1b[38;5;124m'
verde = '\x1b[38;5;2m'
azulFondo = '\x1b[48;5;21m'
naranjaFondo = '\x1b[48;5;124m'
verdeFondo   = "\x1b[48;5;2m"
rojoFondo = '\x1b[48;5;124m'
escape = '\x1b[0m'
dictY = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,'I':8}
enCurso = False
nombreJug = {1:"",2:""}
def TableroJug(tableroJ):
    linea = "    1  2  3  4  5  6  7  8  9\n"
    linea = linea + '-'*30 + '\n'
    for a in dictY.keys():
        linea =  linea + '\n' + a
        for b in tableroJ[dictY[a]]:
            if(b[0] == 'B'):
                caracter = verdeFondo + b + escape
            if(b == 'E'):
                caracter = rojoFondo + b + escape
            elif(b == 'A'):
                caracter = azulFondo + ' ' + escape
            elif(b == ' ' or b == 'X'):
                caracter = b
            linea = linea + '  ' + caracter
        linea = linea + '\n'
    return linea

def generaBarcos():
    barco = 0
    contador = 0
    global tablerosJ
    global barcosJ
    global tablero
    tablerosJ = {}
    for a in range(0,9):
        tablero.append([])
        for b in range(0,9):
            tablero[a].append('A')
    while(barco != len(barcos)):
        x = random.randint(0,8-barcos[barco])
        y = random.randint(0,8)
        if(tablero[y][x-1][0] != 'B' and tablero[y][x+barcos[barco]][0] != 'B'):
            for a in range(x,x+barcos[barco]):
                tablero[y][a] = f'B{barco}'
            barcosExistentes[f'B{barco}'] = [barcos[barco],0,x,y]
            barco += 1
    l = list(barcosExistentes.keys())
    j1  = random.sample(l, len(barcos)//2)
    j2  = random.sample([i for i in l if i not in j1], len(barcos)//2)
    barcosJ.append(len(j1))
    barcosJ.append(len(j2))
    for c in range(1,3):
        tablerosJ[c] = []
        for d in range(0,9):
            tablerosJ[c].append([])
            for e in range(0,9):
                tablerosJ[c][d].append(' ')
    for a in j1:
        barcosExistentes[a][1] = 1 #Establecer los barcos de cada jugador.
        x = barcosExistentes[a][2]
        y = barcosExistentes[a][3]
        xFin = barcosExistentes[a][2] + barcosExistentes[a][0]
        for z in range(x,xFin):
            tablerosJ[1][y][z] = a

    for b in j2:
        barcosExistentes[b][1] = 2 #Establecer los barcos de cada jugador.
        x = barcosExistentes[b][2]
        y = barcosExistentes[b][3]
        xFin = barcosExistentes[b][2] + barcosExistentes[b][0] 
        for z in range(x,xFin):
            tablerosJ[2][y][z] = b #En el tablero de cada jugador solo podra ver sus barcos
        
def calcularDisparo(coord,j):                   
    y = dictY[coord[0]]
    x = int(coord[1])-1
    hit = tablero[y][x]
    if hit[0] == 'B':
        jugBarco = barcosExistentes[hit][1]
        if jugBarco == j: #Si le da a su propio barco (no tiene sentido)
           enviarMsg(f'{rojo}Le has pegado a tu propio barco!{escape}',j)
           pedirCoord(j)
        else:
            barcosExistentes[hit][0] -= 1
            tablero[y][x] = 'A'
            tablerosJ[j][y][x] = 'E' #Enemigo
            tablerosJ[jugBarco][y][x] = 'X'
            enviarMsg(f'{nombreJug[j]} te ha tocado el barco {hit}',jugBarco)
            enviarMsg(f'Has tocado el barco {hit} de {nombreJug[jugBarco]}',j)
            if barcosExistentes[hit][0] == 0:
                barcosJ[jugBarco-1] -= 1
                del barcosExistentes[hit]
                if barcosJ[jugBarco-1] == 0:
                    msgGlobal(f'Ha ganado el jugador {nombreJug[j]}')
                    enCurso = False
            return 1
    elif hit == 'A':
          enviarMsg(f'{azul}Agua{escape}',j)

def pedirCoord(j):
    try:
        msgGlobal(f"Le toca al jugador {j}")
        socketsJ[j].send('COR'.encode())
        data = socketsJ[j].recv(1024)
        calcularDisparo(data.decode(),j)
    except ConnectionResetError:
        enviarMsg(f'El jugador {nombreJug[j]} se ha desconectado. La partida terminó',int(not(j-1))+1)
        enCurso = False
    
def pedirCoords():
    for j in socketsJ:
        pedirCoord(j)
        
def syncTablero(j):
    try:
        t = TableroJug(tablerosJ[j])
        socketsJ[j].send(f'TAB:{t}'.encode())
    except ConnectionResetError:
        enviarMsg(f'El jugador {nombreJug[j]} se ha desconectado. La partida terminó',int(not(j-1))+1)
        enCurso = False
def syncTableros():
    for j in socketsJ:
        syncTablero(j)
def partida():
    global jugadores
    print('partida')
    enCurso = True
    generaBarcos()
    syncTableros()
    while(enCurso == True):
        pedirCoords()
        syncTableros()
    
def enviarMsg(msg,j):
    socketsJ[j].send(f'MSG:{msg}\n'.encode())
def msgGlobal(msg):
    for j in socketsJ:
        enviarMsg(msg,j)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, puerto))
        while jugadores < 2:
            s.listen()
            conn, addr = s.accept()
            jugadores += 1
            n = conn.recv(1024).decode()
            if n in nombreJug.values():
                conn.send('MSG: Nombre duplicado. Cambialo y vuelve a conectarte!'.encode())
                conn.close()
                jugadores -= 1
            else:
                nombreJug[jugadores] = n
                if jugadores == 1:
                     conn.send("MSG: Esperando al otro jugador".encode())
                socketsJ[jugadores] = conn
                msgGlobal(f"Jugador {jugadores}: Nueva conexión {addr}")
        partida()
            
            
        



      



