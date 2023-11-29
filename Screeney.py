import datetime
import os
import time
from tkinter import *
from tkinter import ttk

import pyautogui

def get_matieres():
    with open('liste_matieres.txt', 'r', encoding="utf-8") as f:
        m = f.read().split('\n')
        return [mat.upper() for mat in m]

def CreerDossierSauvegarde(ou, doss):
    nomEmplacementSauvegarde = f"{ou}/{doss}"
    if not os.path.exists(nomEmplacementSauvegarde):
        os.mkdir(nomEmplacementSauvegarde)
    return nomEmplacementSauvegarde


def SemblableFichier(fic, fic2):
    a = os.path.getsize(fic)
    b = os.path.getsize(fic2)
    diff = abs(a - b)
    print(diff)
    return (True, diff) if diff < 1000 else (False, diff)



def SupprimerFichier(path):
    if os.path.exists(path):
        os.remove(path)
    else:
        print(f"Impossible de supprimer le fichier {path} car il n'existe pas")


window = Tk()
window.title("SCREENEY")
window.iconphoto(False, PhotoImage(file='ico/icon.png'))
window.attributes('-topmost', 1)
window.geometry('310x240')

# lbl = Label(window, text="Hello")
# lbl.grid(column=0, row=0)
labelChoix = Label(window, text="Matières :")

listeMatieres = get_matieres()
listeMatieres.sort()
listeMatieres.append("Sélectionner")
listeCombo = ttk.Combobox(window, values=listeMatieres, state="readonly", justify='center', width=15)
listeCombo.current(len(listeMatieres) - 1)


def open_folder():
    nomMatiere = listeCombo.get()
    if nomMatiere != listeMatieres[-1]:
        nomEmplacementSauvegarde = CreerDossierSauvegarde(
            CreerDossierSauvegarde("H:/Desktop", "SCREENEY"), f"- {nomMatiere}"
        )

        path =  nomEmplacementSauvegarde
        path = path.replace('/','\\')

        print("open", path)
        if os.path.exists(path):
            command = f'explorer.exe {path}'
            os.system(command)


btn_open_dir = Button(window, text="📁", command=open_folder, width=3,
             height=1)
btn_open_dir.pack(padx=5, pady=4)

labelChoix.pack()
listeCombo.pack()


c = 0
ancienphoto = ""


def capturer():
    global c, ancienphoto


    nomMatiere = listeCombo.get()
    if nomMatiere != listeMatieres[-1]:
        nomEmplacementSauvegarde = CreerDossierSauvegarde(
            CreerDossierSauvegarde(
                CreerDossierSauvegarde("h:/Desktop", "SCREENEY"),
                f"- {nomMatiere.lower()}",
            ),
            datetime.datetime.now().strftime('%Y-%m-%d (%a)'),
        )

        comm = Comment.get()
        comm = comm.strip()
        if len(comm) > 0:
            comm = f' {comm}'

        myDatetime = datetime.datetime.now()
        nomFichier = myDatetime.strftime(f'%Y-%m-%d-%H%M%S{comm}')
        photo = f"{nomEmplacementSauvegarde}/{nomFichier}.png"

        # prendre photo
        pyautogui.screenshot(photo)
        print(f"#{str(c)}# {photo}")

        # pour les photo sauf la premiere
        if (c > 0):
            # si photo semblable a lancienne photo alors suprr photo
            semblable = SemblableFichier(photo, ancienphoto)
            if semblable[0]:
                print(f">>> PAREIL! {str(semblable[1])} # {photo} VS {ancienphoto}")
                label.config(text="Image similaire ! Je cala pas", fg='red')
                SupprimerFichier(photo)
            else:
                c += 1
                label.config(text=f"#{c} ▪ " + photo.split('/')[-1], fg='green')
                ancienphoto = photo

        else:
            c += 1
            label.config(text=f"#{c} ▪ " + photo.split('/')[-1], fg='green')
            ancienphoto = photo

        time.sleep(1)

def clicked():
    global value
    capturer()


btn = Button(window, text="Screen 📸", command=clicked, width=17,
             height=2)
btn.pack(padx=5, pady=10)


Comment = Entry(window, bd=3)
Comment.pack()

label = Label(window, text="")
label.pack()

cred = Label(window, text="Code by Mlamali Said Salimo.", font=("inherit", 8))
cred.pack(side='bottom')
window.mainloop()

