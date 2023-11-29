from tkinter import *
from tkinter import messagebox
import re
def operacio(op):
    
        try:
            float(entN1.get())
            float(entN2.get())
            res = str(eval(op))
            entRes.configure(state = 'normal')
            entRes.delete(0, END)
            entRes.insert(0,res)
            entRes.configure(state = 'readonly')
        except ValueError:
            messagebox.showwarning("Error","N1 i N2 han de ser numeros!")
        except ZeroDivisionError:
           messagebox.showwarning("Error","No es pot dividir per zero!")
        except SyntaxError:
            messagebox.showwarning("Error","Treu els zeros del principi/final!")


    

    
    
finestra = Tk()

lbN1 = Label(finestra,text='N1')
lbN1.grid(row=0,column=0,ipadx=0)

lbN2 = Label(finestra,text='N2')
lbN2.grid(row=1,column=0,ipadx=0)

lbRes = Label(finestra,text='Resultat')
lbRes.grid(row=2,padx=0)

entN1 = Entry(finestra)
entN1.grid(row=0,column=1,columnspan=4)

entN2 = Entry(finestra)
entN2.grid(row=1,column=1,columnspan=4)

entRes = Entry(finestra)
entRes.grid(row=2,column=1,columnspan=4)
entRes.configure(state='readonly')

btSortir = Button(finestra,text='Sortir')
btSortir.grid(row=3, column = 0, sticky=W)

btSum = Button(finestra,text='+',command=lambda: operacio(f'{entN1.get()}+{entN2.get()}'))
btSum.grid(row=3,column = 1, padx = 0,sticky=W)

btResta = Button(finestra,text='-',command=lambda: operacio(f'{entN1.get()}-{entN2.get()}'))
btResta.grid(row=3, column = 2, sticky=W)

btMult = Button(finestra,text='*',command=lambda: operacio(f'{entN1.get()}*{entN2.get()}'))
btMult.grid(row=3, column = 3, sticky=W)

btDiv = Button(finestra,text='/',command=lambda: operacio(f'{entN1.get()}/{entN2.get()}'))
btDiv.grid(row=3, column = 4, sticky=W)
finestra.geometry('200x150')
finestra.mainloop()
