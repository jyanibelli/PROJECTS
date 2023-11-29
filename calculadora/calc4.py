from tkinter import *
from tkinter import messagebox
from math import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
fuente = ('Terminal',15)
step = 8
fila = 4
start = 0
pad = 0
igual = False
integrando = False
global res
lastpad = 0
root = Tk()
res = ''
root.title('Calculadora')
root.geometry('365x280')
root.configure(background='white')
resultat = Entry(root, width = 100,font=fuente,fg='darkgreen')
resultat.grid(row = 1,column=0)
resultat.configure(state='readonly')
global tempStr
tempStr = ""
op = ['+','-','*','/','fact(','sqrt(','(',')','∫','x',',','.','^','sin(','cos(','C','AC','=','Π','tan(','%','e','log(','log2(']
resultat.configure(state='normal')
resultat.insert(0,'0')
resultat.configure(state='readonly')

def popDigit():
    global res
    resultat.configure(state='normal')
    resultat.delete(resultat.index(END)-1,END)
    res = res[:-1]
    if(len(resultat.get()) == 0):
        resultat.configure(state='normal')
        resultat.insert(0,'0')
        resultat.configure(state='readonly')

    resultat.configure(state='readonly')
def clearDisplay():
    global res
    resultat.configure(state='normal')
    resultat.delete(0,END)
    res = ''
    resultat.insert(0,'0')
    resultat.configure(state='readonly')
def afegirDigit(d):
    global igual
    global integrando
    global tempStr
    global res
    if igual == True:
        clearDisplay()
    if d == 'AC':
        clearDisplay()
        d = ''
    elif resultat.get() == '0':
        resultat.configure(state='normal')
        resultat.delete(0,END)
        resultat.configure(state='readonly')  
    if 'SYNTAX ERROR' not in resultat.get():
            if d == 'C':
                popDigit()
                d = ''
            elif d == '=':
                calcular()
                d = ''
            elif d == 'Π':
                d = str(pi)
                res = res + d
            elif d == 'e':
                d = str(e)
                res = res + str(e)
            else:   
                if str(d) == '∫':
                    integrando = True
                    tempStr = ""
                if integrando == True:
                    if(str(d) == '^'):
                        tempStr = tempStr + '**'
                    else:
                        tempStr = tempStr + str(d)
                    if tempStr.count(',') == 2 and d == ')':
                            integrando = False
                            tempStr = tempStr.replace('∫(',"integral('")
                            tempStr = tempStr.replace(',',"',",1)
                            res = res + tempStr
                else:
                    if(str(d) == '^'):
                        res = res + '**'
                    else:
                        res = res + str(d)

            resultat.configure(state='normal')
            resultat.insert(END,d)
            resultat.configure(state='readonly')
            igual=False

def fact(n):
    if n == 1:
        return 1
    else:
        res = n
        for a in range(n-1,1,-1):
            res *= a
        return res
def integral(funcion,xInicio,xFin):
    integral = 0
    cont = xInicio
    const = 0.0001
    while(cont <= xFin):
        func = funcion.replace('x',f'{cont}')
        integral += eval(f'({func})*{const}')
        cont += const
    funcion = funcion.replace('sin','np.sin')
    funcion = funcion.replace('cos','np.cos')
    funcion = funcion.replace('tan','np.tan')
    funcion = funcion.replace('sqrt','np.sqrt')
    x = np.linspace(1, xFin+1, 1000)
    plt.plot(x, eval(f'{funcion}'))
    plt.axhline(color = 'blue')
    plt.fill_between(x,eval(f'{funcion}'), where = [(x > xInicio) and (x < xFin) for x in x])
    plt.text(2, 15, integral)
    plt.show()
    return integral
        
        
    
def calcular():
    try:
        global igual
        exp = eval(res)
        clearDisplay()
        resultat.configure(state='normal')
        resultat.insert(0,exp)
        resultat.configure(state='readonly')
        igual = True
    except ZeroDivisionError:
        clearDisplay()
        resultat.configure(state='normal')
        resultat.insert(0,"ERROR: DIV POR CERO")
        resultat.configure(state='readonly')
    except:
        clearDisplay()
        resultat.configure(state='normal')
        resultat.insert(0,"SYNTAX ERROR")
        resultat.configure(state='readonly')

for a in range(0,len(op)):
    if(a % step == 0 and a != 0):
        fila += 1
        lastpad = 0
    lastpad =(a%step)*45
    Button(root, text=f'{op[a]}',width=5,height=2,command=lambda x=a: afegirDigit(op[x])).grid(row=fila,padx=lastpad,sticky=W,pady=5)



for a in range(0,10):
    if a % step == 0:
        fila += 1
    Button(root, text=f'{a}',width=5,height=2,command=lambda x=a: afegirDigit(x)).grid(row=fila,padx=(a%step)*45,sticky=W,pady=5)





        
root.mainloop()


    
