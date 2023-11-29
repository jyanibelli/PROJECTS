from tkinter import *
from tkinter import messagebox
large_font = ('Verdana',15)
step = 3
fila = 4
start = 0
pad = 0
igual = False
root = Tk()
root.title('Calculadora')
root.geometry('250x300')
resultat = Entry(root, width = 100,font=large_font)
resultat.grid(row = 1,column=0)
resultat.configure(state='readonly')
op = ['+','-','*','/'] 

def popDisplay():
    resultat.configure(state='normal')
    resultat.delete(resultat.index(END)-1,END)
    resultat.configure(state='readonly')
def clearDisplay():
    resultat.configure(state='normal')
    resultat.delete(0,END)    
    resultat.configure(state='readonly')
def afegirDigit(d): #En aquest cas no ha fet falta fer servir el metode d'afegirOperacio, tots fan servir el mateix metode ja que s'evalua el resultat a la pantalla
    global igual
    if igual == True:
        clearDisplay()
    resultat.configure(state='normal')
    resultat.insert(END,d)
    resultat.configure(state='readonly')
    igual=False
    
def calcular():
    try:
        global igual
        exp = resultat.get()
        res = eval(exp)
        clearDisplay()
        resultat.configure(state='normal')
        resultat.insert(0,res)
        resultat.configure(state='readonly')
        igual = True
    except SyntaxError:
        clearDisplay()
        resultat.configure(state='normal')
        resultat.insert(0,"Syntax Error")
        resultat.configure(state='readonly')
    except ZeroDivisionError:
        clearDisplay()
        resultat.configure(state='normal')
        resultat.insert(0,"ERR:DIV POR CERO")
        resultat.configure(state='readonly')
            

for a in range(0,10):
    if a % step == 0:
        fila += 1
    lastpad = (a%step)*45
    Button(root, text=f'{a}',width=5,command=lambda x=a: afegirDigit(x)).grid(row=fila,padx=lastpad,sticky=W,pady=5)
lastpad = 0
for a in range(0,len(op)):
    Button(root, text=f'{op[a]}',width=5,command=lambda x=a: afegirDigit(op[x])).grid(row=4,padx=lastpad,sticky=W,pady=5)
    lastpad += 45
Button(root, text=f'=',width=5,command=lambda: calcular()).grid(row=fila,padx=45,sticky=W,pady=5)


bNet = Button(root, text="⌫ Borrar digito",width=15,command=lambda: popDisplay())
bNet.grid(row=fila+1,sticky=W)
bDisp = Button(root, text="⎚ Limpiar display",width=15,command=lambda: clearDisplay())
bDisp.grid(row=fila+2,sticky=W)
        
root.mainloop()


    
