from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from institut import *
import pandas as pd
import matplotlib.pyplot as plt
from tkinter.filedialog import asksaveasfilename
from omplir import *
#Añadir alumnos: Hecho
#Añadir materias: Hecho (falta validar inputs)
#Matricular alumnos: Hecho
#Ver/modificar alumnos: A medias
#Poner notas: Hecho
#Desmatricular: Hecho
ventana = Tk()
ventana.geometry("650x100")
botoAlumne = Button(ventana,text="🧍 Afegir alumne",command = lambda: afegirAlumneGrafic(),width=50) #hecho
botoAlumne.grid(row = 0, column = 0)
botoAlumne = Button(ventana,text="📚 Afegir materia",command = lambda:afegirMateriaGrafic(),width=50) #hecho
botoAlumne.grid(row = 0, column = 1)
botoAlumne = Button(ventana,text="📚🧍 Matricular alumne",command = lambda:matricularAlumneGrafic(),width=50) #hecho
botoAlumne.grid(row = 1, column = 0)
botoAlumne = Button(ventana,text="📚🧍 Posar nota a alumne", command= lambda:posarNotaGrafic(),width=50) #hecho
botoAlumne.grid(row = 1, column = 1)
botoDesmatricular = Button(ventana,text="📚🧍 Desmatricular alumne", command= lambda:desmatricularAlumneGrafic(),width=50) #hecho
botoDesmatricular.grid(row = 2, column = 0)
botoVeure = Button(ventana,text="🧍 Veure/modificar alumnes", command= lambda:veureAlumnes(),width=50) #medio hecho
botoVeure.grid(row = 2, column = 1)
botoVeure = Button(ventana,text="📚 Veure/modificar materies", command= lambda:veureMateries(),width=50) #medio hecho
botoVeure.grid(row = 3, column = 0)
omplirDades()


def veureAlumnes():
    finAlumne = Toplevel(ventana)
    treeview = Treeview(finAlumne,columns=("Nom", "Cognom", "Data Naixement","Nota mitjana"))
    for columna in treeview['columns']:
         treeview.column(columna, anchor=CENTER)
    treeview.heading("#0", text="Codi")
    treeview.heading("Nom", text="Nom")
    treeview.heading("Cognom", text="Cognom")
    treeview.heading("Data Naixement", text="Data Naixement")
    treeview.heading("Nota mitjana", text="Nota mitjana")
    treeview.grid(row=0, column =0)
    Button(finAlumne,text="Esborrar alumne",command=lambda: esborrarAluGrafic()).grid(row=1,column=1)
    Button(finAlumne,text="Generar informe d'alumne",command = lambda: generarInformeAlu()).grid(row=1,column=0)
    def carregaAlumnes():
        for i in treeview.get_children():
            treeview.delete(i)
        alumnesTree = obtenirAlumnes()
        for a in alumnesTree:
            media = calcularMitjanaAlumne(a.Codi)
            if media == None:
                media = "--"
            else:
                media = f'{media:<.2f}'
            treeview.insert("",END,text = a.Codi,values=(a.Nom,a.Cognom,a.DataNaixement,media))
    carregaAlumnes()
    def generarInformeAlu():
        id = treeview.focus()
        if id:
            item = treeview.item(id)
            informeAlu = Toplevel(ventana)
            Label(informeAlu, text=f"Informe de l'alumne {item['text']}-{item['values'][0]} {item['values'][1]}").grid(row = 0, column = 0)
            Button(informeAlu,text="🗎 PDF",command=lambda:treeViewPDF(treeMateria)).grid(row=2,column=0)
            Button(informeAlu,text="Grafica",command=lambda:graficar()).grid(row=2,column=1)
            treeMateria = Treeview(informeAlu,columns=("Materia","Nota"))
            treeMateria.heading("Materia",text="Materia")
            treeMateria.heading("Nota",text="Nota")
            treeMateria.column("Nota",anchor=CENTER)
            treeMateria['show'] = 'headings'
            treeMateria.grid(row=1,column=0)
            materiesAlumne = obtenirMateriesNoms(item['text'])
            if materiesAlumne != None:
                for a in range(0,len(materiesAlumne[0])):
                    nota = obtenirNota(item['text'],materiesAlumne[0][a])
                    treeMateria.insert("",END,text = materiesAlumne[0][a],values=(materiesAlumne[1][a],nota))
                listaAprobats = []
                for b in treeMateria.get_children():
                    listaAprobats.append(float(treeMateria.item(b)['values'][1]))
                aprobados = aprobats(listaAprobats)
                treeMateria.insert("",END,text="",values=("","",""))
                treeMateria.insert("",END,text="",values=("Assignatures aprobades",f"{int(aprobados[0]):<}",f"{aprobados[1]:<.2f}%"))
                treeMateria.insert("",END,text = a,values=("Mitjana",item['values'][3]))
            def graficar():
                if materiesAlumne != None:
                    notas = [len(listaAprobats)-aprobados[0],aprobados[0]]
                    nombres = ["Suspeses","Assignatures aprobades"]
                    plt.pie(notas, labels=nombres,autopct="%0.1f %%")
                    plt.axis("equal")
                    plt.show()

    def esborrarAluGrafic():
        id = treeview.focus()
        item = treeview.item(id)
        confirmar = messagebox.askyesno(parent=finAlumne,title='Confirmació',message=f"Segur que desitges esborrar l'alumne {item['text']} - {item['values'][0]} {item['values'][1]}?")
        if id and confirmar:
            eliminarAlumne(item['text'])
            carregaAlumnes()

    def editarAlumne(*args):
        item = treeview.item(treeview.focus())
        print(item)
        editarAlumne = Toplevel(finAlumne)
        entryNom = Entry(editarAlumne, text=item['values'][0])
        entryCognom = Entry(editarAlumne, text=item['values'][1])
        entryDataNaixement = Entry(editarAlumne, text=item['values'][2])
        entryNom.grid(row=0,column=1)
        entryNom.delete(0, END)
        entryCognom.delete(0, END)
        entryDataNaixement.delete(0, END)
        entryNom.insert(0,item['values'][0])
        entryCognom.insert(0,item['values'][1])
        entryDataNaixement.insert(0,item['values'][2])
        Label(editarAlumne, text="Nom:").grid(row=0,column=0)
        entryCognom.grid(row=1,column=1)
        Label(editarAlumne, text="Cognom:").grid(row=1,column=0)
        entryDataNaixement.grid(row=2,column=1)
        Label(editarAlumne, text="Data Naixement:").grid(row=2,column=0)
        Label(editarAlumne, text="Per guardar els canvis, presiona ENTER").grid(row=3,column=1)
        def validar(*args):
            if(modificarAlumne(item['text'],entryNom.get(), entryCognom.get(),entryDataNaixement.get())):
                editarAlumne.destroy()
                carregaAlumnes()
            else:
                messagebox.showerror(parent=editarAlumne,title="Error",message="La data de naixement no té el format esperat (DD/MM/YYYY)")
        editarAlumne.bind("<Return>", validar)

    treeview.bind("<Double-1>", editarAlumne)

def veureMateries():
    finMateries = Toplevel(ventana)
    treeview = Treeview(finMateries,columns= ("Nom", "Mitjana"))
    treeview.heading("#0", text="Codi")
    treeview.heading("Nom", text="Nom")
    treeview.heading("Mitjana", text="Mitjana")
    treeview.grid(row=0, column =0)
    for columna in treeview['columns']:
        treeview.column(columna, anchor=CENTER)
    Button(finMateries,text="Esborrar materia",command=lambda: esborrarMatGrafic()).grid(row=1,column=1)
    Button(finMateries,text="Generar report de materia",command=lambda: generarReportMateria()).grid(row=1,column=0)
    def esborrarMatGrafic():
        id = treeview.focus()
        item = treeview.item(id)
        confirm = messagebox.askyesno(parent=finMateries,title='Confirmació',
                    message=f"Segur que desitjes esborrar la materia {item['text']} - {item['values'][0]}?")
        if id and confirm:
            eliminarMateria(item['text'])
            carregaMateries()
    def carregaMateries():
        for i in treeview.get_children():
            treeview.delete(i)
        for a in obtenirMateries():
            media = calcularMitjanaMateria(a.Codi)
            treeview.insert("",END,text = a.Codi,values=(a.Nom,f'{media:<.2f}'))
    def generarReportMateria():
        finReport = Toplevel(finMateries)
        treeReport = Treeview(finReport,columns= ("Nom","Cognom", "Nota"))
        treeReport.heading("#0", text="Codi")
        treeReport.heading("Nom", text="Nom")
        treeReport.heading("Cognom", text="Cognom")
        treeReport.heading("Nota", text="Nota")
        treeReport.grid(row=0,column=0)
        Button(finReport,text="🗎 PDF",command=lambda:treeViewPDF(treeReport)).grid(row=1,column=0)
        Button(finReport,text="Graficar",command=lambda:graficar()).grid(row=1,column=1)
        for columna in treeReport['columns']:
            treeReport.column(columna, anchor=CENTER)
        id = treeview.focus()
        if id:
            item = treeview.item(id)
            print(item['values'])
            alumnesMateria = obtenirAlumnesMateria(item['text'])
            if alumnesMateria != None:
                for a in alumnesMateria:
                    treeReport.insert("",END,text=a[0].Codi,values=(a[0].Nom,a[0].Cognom,a[1]))
                listaAprobats = []
                for b in treeReport.get_children():
                    listaAprobats.append(float(treeReport.item(b)['values'][2]))
                aprobados = aprobats(listaAprobats)
                treeReport.insert("",END,text="",values=("","",""))
                treeReport.insert("",END,text="",values=("Aprobats",f"{int(aprobados[0]):<}",f"{aprobados[1]:<.2f}%"))
                treeReport.insert("",END,text="",values=("Mitjana","",item['values'][1]))
            def graficar():
                if alumnesMateria != None:
                    notas = [len(listaAprobats)-aprobados[0],aprobados[0]]
                    nombres = ["Alumnes suspesos","Alumnes aprobats"]
                    plt.pie(notas, labels=nombres,autopct="%0.1f %%")
                    plt.axis("equal")
                    plt.show()
                

    carregaMateries()

    def editarMateria(*args):
        item = treeview.item(treeview.focus())
        print(item)
        editarMateria = Toplevel(finMateries)
        entryCodi = Entry(editarMateria)
        entryNom = Entry(editarMateria)
        entryCodi.grid(row=0,column=1)
        entryNom.grid(row=1,column=1)
        entryNom.delete(0, END)
        entryCodi.delete(0, END)
        entryCodi.insert(0,item['text'])
        entryNom.insert(0,item['values'][0])
        Label(editarMateria, text="Codi:").grid(row=0,column=0)
        Label(editarMateria, text="Nom:").grid(row=1,column=0)
        Label(editarMateria, text="Per guardar els canvis, presiona ENTER").grid(row=2,column=1)
        def validar(*args):
            nouCodi = entryCodi.get()
            codiAntic = item['text']
            nouNom = entryNom.get()
            if modificarMateria(codiAntic,nouCodi,nouNom):
                carregaMateries()
                editarMateria.destroy()
            else:
                messagebox.showerror(parent=finMateries,title="Error",message="No s'ha pogut modificar la materia (el nou codi ja correspon a una altra matèria existent?)")
                
        editarMateria.bind("<Return>", validar)
            
    treeview.bind("<Double-1>", editarMateria)
def treeViewPDF(treeview):
            archivo =  asksaveasfilename(filetypes=[("Archivo PDF", ".pdf")],defaultextension=".pdf")
            if archivo:
                columnas = {x:[] for x in treeview['columns']}
                for a in treeview.get_children():
                    i = 0
                    for b in columnas.keys():
                        columnas[b].append(treeview.item(a)['values'][i])
                        i += 1
                dataframe = pd.DataFrame.from_dict(columnas)
                print(dataframe)
                fig, ax = plt.subplots()
                fig.patch.set_visible(False)
                ax.axis('off')
                table = ax.table(cellText=dataframe.values, colLabels=dataframe.columns, loc='center',cellLoc = 'center')
                fig.tight_layout()
                try:
                    plt.savefig(archivo, bbox_inches='tight')
                except:
                    messagebox.showinfo(message="Has de posar el nom del fitxer sense extensió!", title="Error")
                    treeViewPDF()

            
def afegirAlumneGrafic():
    def validacio():
        match afegirAlumne(Alumne(codi.get(),nom.get(),cognom.get(),dataNaixement.get())):
            case 2:
                messagebox.showerror(message="L'alumne està duplicat (ja existeix un alumne amb aquest codi)",title="Error")
            case 1:
                messagebox.showinfo(message="Alumne afegit amb exit",title="Informació")
            case 0:
                messagebox.showerror(message="La data de naixement no coincideix amb el format esperat (DD/MM/YYYY)",title="Error")
    finestraAlumne = Toplevel(ventana)
    codi = Entry(finestraAlumne,width=20)
    Label(finestraAlumne, text="Codi: ").grid(row=0,column=0)
    codi.grid(row=0,column=1)
    nom = Entry(finestraAlumne,width=20)
    Label(finestraAlumne, text="Nom: ").grid(row=1,column=0)
    nom.grid(row=1,column=1)
    cognom = Entry(finestraAlumne,width=20)
    Label(finestraAlumne, text="Cognom: ").grid(row=2,column=0)
    cognom.grid(row=2,column=1)
    dataNaixement = Entry(finestraAlumne,width=20)
    Label(finestraAlumne, text="Data Naixement: ").grid(row=3,column=0)
    dataNaixement.grid(row=3,column=1)
    botoAlumne = Button(finestraAlumne,text="Afegir",width=15,command=lambda: validacio())
    botoAlumne.grid(row = 4, column = 1,sticky='')


def afegirMateriaGrafic():
    def validacio():
        if afegirMateria(Materia(codi.get(),nom.get())):
            messagebox.showinfo(parent = finestraMateria, message=f"Materia {codi.get()}-{nom.get()} afegida correctament",title="Informació")
        else:
            messagebox.showerror(parent = finestraMateria, message=f"La materia {codi.get()}-{nom.get()} està duplicada (ja existeix una materia amb el mateix codi)",title="Error")

    finestraMateria= Toplevel(ventana)
    codi = Entry(finestraMateria,width=20)
    Label(finestraMateria, text="Codi: ").grid(row=0,column=0)
    codi.grid(row=0,column=1)
    nom = Entry(finestraMateria,width=20)
    Label(finestraMateria, text="Nom: ").grid(row=1,column=0)
    nom.grid(row=1,column=1)
    botoMateria = Button(finestraMateria,text="Afegir",width=15,command=lambda: validacio())
    botoMateria.grid(row = 2, column = 1,sticky='')
def matricularAlumneGrafic():
    materiesAlumne = [[],[]]
    alumnesLista = obtenirAlumnesNoms()
    def validacio():
        opcioMat = desplegableMateries.current()
        opcioAlu = desplegableAlumnes.current()
        a = matriculaAlumne(alumnesLista[0][opcioAlu],materiesAlumne[0][opcioMat])
        match(a):
            case 0:
                messagebox.showerror(parent = finestraMatricular, message="L'alumne o la materia no existeixen",title="Error")
            case 1:
                messagebox.showinfo(parent = finestraMatricular, message=f'Alumne {alumnesLista[1][opcioAlu]} matriculat amb exit de {materiesAlumne[1][opcioMat]} ',title="Informació")
            case 2:
                messagebox.showerror(parent = finestraMatricular, message=f'Alumne {alumnesLista[1][opcioAlu]} ja esta matriculat de {materiesAlumne[1][opcioMat]} ',title="Error")
    finestraMatricular = Toplevel(ventana)
    finestraMatricular.title('Matricular alumne')
    desplegableMateries = Combobox(finestraMatricular,state="readonly",values=materiesAlumne[1])
    Label(finestraMatricular, text="Materia: ").grid(row=0,column=0)
    desplegableMateries.grid(row=0,column=1)
    desplegableAlumnes = Combobox(finestraMatricular,state="readonly",values=alumnesLista[1])
    Label(finestraMatricular, text="Alumne: ").grid(row=1,column=0,pady=15)
    desplegableAlumnes.grid(row=1,column=1,pady=15)
    botoMatricular = Button(finestraMatricular,text="Matricular",width=15,command=lambda: validacio())
    botoMatricular.grid(row = 2, column = 1,sticky='')
    def obtenirMateriesNMGrafic(*args):
        materiesAlumne.clear()
        seleccio = desplegableAlumnes.current()
        mat = obtenirMateriesNM(alumnesLista[0][seleccio])
        materiesAlumne.append(mat[0])
        materiesAlumne.append(mat[1])
        desplegableMateries['values'] = materiesAlumne[1]
    desplegableAlumnes.bind("<<ComboboxSelected>>",obtenirMateriesNMGrafic) #NM = No matriculat

def posarNotaGrafic():
    finestraNota = Toplevel(ventana)
    finestraNota.title('Posar nota a alumne')
    alumnesLista = obtenirAlumnesNoms()
    materiesLista = [[],[]]
    def obtenirMateriesAlumne(self):
        materiesLista.clear()
        nota.delete(0,END)
        seleccio = desplegableAlumnes.current()
        desplegableMateries.set("")
        if seleccio != -1:
            mat = obtenirMateriesNoms(alumnesLista[0][seleccio])
            materiesLista.append(mat[0])
            materiesLista.append(mat[1])
            print(materiesLista)
            desplegableMateries['values'] = materiesLista[1]
    def getNota(self):
        nota.delete(0,END)
        seleccioMateria = desplegableMateries.current()
        seleccioAlumne = desplegableAlumnes.current()
        if seleccioMateria >= 0 and seleccioAlumne >= 0:
            notaNumerica = obtenirNota(alumnesLista[0][seleccioAlumne],materiesLista[0][seleccioMateria])
            if notaNumerica == None:
                nota.insert(0,"No té")
            else:
                nota.insert(0,notaNumerica)
    def actualitzarNota():
        seleccioMateria = desplegableMateries.current()
        seleccioAlumne = desplegableAlumnes.current()
        notaNum = nota.get()
        if seleccioMateria >= 0 and seleccioAlumne >= 0:
            codiAlumne = alumnesLista[0][seleccioAlumne]
            codiMateria = materiesLista[0][seleccioMateria]
            if posarNota(codiAlumne,codiMateria,notaNum):
                messagebox.showinfo( parent = finestraNota, message=f"Nota de l'alumne {alumnesLista[1][seleccioAlumne]} en {materiesLista[1][seleccioMateria]} actualitzada a {notaNum}",title="Informació")
            else:
                messagebox.showerror(parent = finestraNota, message="La nota ha de ser un numèric comprès entre 0-10.",title="Error")  
           


    
    nota = Entry(finestraNota,width=5)
    nota.grid(row = 2, column = 1,sticky = 'W',pady=10)
    Label(finestraNota,text="Nota:").grid(row=2,column = 0)
    desplegableMateries = Combobox(finestraNota,state="readonly")
    desplegableMateries.grid(row = 1, column = 1,pady=10)
    Label(finestraNota,text="Materia:").grid(row=1,column = 0)
    desplegableAlumnes = Combobox(finestraNota,state="readonly",values=alumnesLista[1])
    desplegableAlumnes.grid(row = 0, column = 1,pady=10)
    Label(finestraNota,text="Alumne:").grid(row=0,column = 0)
    desplegableAlumnes.bind("<<ComboboxSelected>>",obtenirMateriesAlumne)
    desplegableMateries.bind("<<ComboboxSelected>>",getNota)
    Button(finestraNota,text="Canviar",command=lambda: actualitzarNota()).grid(row=3,column=1)
   
def desmatricularAlumneGrafic():
    finestraDesmatricular = Toplevel(ventana)
    materiesAlumne = []
    alumneCodi = obtenirAlumnesNoms() #Emplenar la llista d'alumnes
    def obtenirMateriesAlumne(*args):
        materiesAlumne.clear()
        seleccio = desplegableAlumnes.current()
        desplegableMateries.set("")
        if seleccio != -1:
            print(alumneCodi)
            mat = obtenirMateriesNoms(alumneCodi[0][seleccio])
            materiesAlumne.append(mat[0])
            materiesAlumne.append(mat[1])
            print(materiesAlumne)
            desplegableMateries['values'] = materiesAlumne[1]
    def desmatricularGrafic():
        alumne = desplegableAlumnes.current()
        materia = desplegableMateries.current()
        if alumne >= 0 and materia >= 0:
            if desmatriculaAlumne(alumneCodi[0][alumne], materiesAlumne[0][materia]):
                messagebox.showinfo(parent = finestraDesmatricular, message=f"Alumne {alumneCodi[1][alumne]} desmatriculat amb èxit de {materiesAlumne[1][materia]}",title="Informació")
                obtenirMateriesAlumne()
            else:
                messagebox.showerror(parent = finestraDesmatricular,message="No s'ha pogut desmatricular l'alumne",title="Error")

    desplegableAlumnes = Combobox(finestraDesmatricular,state="readonly",values=alumneCodi[1])
    Label(finestraDesmatricular,text = "Alumne:").grid(row=1,column=0)
    desplegableAlumnes.bind("<<ComboboxSelected>>",obtenirMateriesAlumne)
    print(materiesAlumne)
    desplegableMateries = Combobox(finestraDesmatricular,state="readonly")
    Label(finestraDesmatricular,text = "Materia:").grid(row=0,column=0)
    desplegableMateries.grid(row = 0, column = 1)
    desplegableAlumnes.grid(row = 1, column = 1)
    Button(finestraDesmatricular,text="Desmatricular",command = lambda: desmatricularGrafic()).grid(row=2,column=1)
    

            
            
    
ventana.mainloop()

