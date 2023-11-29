import socket
import pickle
import os
import re
os.system('color') # Para que funcionen los colores ANSI
naranja = '\x1b[38;5;215m' #Colores ANSI
azul = '\x1b[38;5;21m'
rojo = '\x1b[38;5;124m'

azulFondo = '\x1b[48;5;21m'
naranjaFondo = '\x1b[48;5;124m'

data = "."
HOST = "127.0.0.1" 
PORT = 1026
dictY = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,'I':8}
def confirmar():
     a  = input("Empezar partida (Si/No): ")
     if a in ("Si","No"):
        s.send(a.encode())
     else:
         confirmar()
def pedirCoords():
     a  = input("Coordenadas (letra y numero): ")
     if(re.match('^[A-I][1-9]$',a)):
        s.send(a.encode())
     else:
         print("Formato: coordenada X, coordenada Y")
         pedirCoords()
               

    
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
     def conectar():
          a = input("Host: ")
          b = input("Puerto: ")
          c = input("Nombre: ")
          s.connect((a, int(b)))
          s.send(c.encode())
     try:
          conectar()
          while data:
                data = s.recv(1024)
                if(data):
                    data = data.decode()
                    if data == "C":
                          confirmar()
                    if "COR" in data:
                         pedirCoords()
                    else:
                         spliteado = data.split(':')
                         if spliteado[0] == 'MSG' or spliteado[0] == 'TAB':
                              print(spliteado[1])

     except TimeoutError:
          print("No se pudo establecer conexión!")
          
       
   
         



