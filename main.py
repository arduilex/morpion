from tkinter import *
from tkinter.messagebox import *
from tkinter.colorchooser import *
from random import randint

# Procédure grille() qui trace 8 lignes avec la méthode .create_line()
def grille():
    index = [[0, 1], [1, 0]]    # Permet d'inerser les x et y
    for k in range(2):
        for i in range(4):
            xy = [[4, 184], [60*i+4, 60*i+4]]
            x0 = xy[index[k][0]][0]
            y0 = xy[index[k][1]][0]
            x1 = xy[index[k][0]][1]
            y1 = xy[index[k][1]][1]
            can.create_line(x0, y0, x1, y1, width=5, fill='#33A8D1', cap='round')

# Procédure reset() qui réinitialise le morpion en effaçant tout les canevas 
def reset():
    global joueur, joueurStart, l_cases, l_colorJoueur, l_nom, stop
    l_cases = [0]*9
    stop = 0
    joueur = joueurStart
    can.delete(ALL)
    grille()
    if var_name_j2.get() == 'IA#3.1' and joueur == 2:
        IA_play()
    else:
        lab_gain.configure(text=l_nom[joueur-1]+", tu commences !", bg=l_colorJoueur[joueur-1])

# Fonction qui retourne 1 si un alignement horizontale, verticale, ou diagonale de 3 cases est détecté sinon retourne 0 
def gagner():
    global l_cases, l_indexGagner
    for l in l_indexGagner:
        if l_cases[l[0]] == l_cases[l[1]] and l_cases[l[0]] == l_cases[l[2]] and l_cases[l[0]] != 0:
            x0, y0 = transforme(l[0])
            x1, y1 = transforme(l[2])
            forme('ligne', x0, y0, x1, y1)
            return 1
    return 0

# Fonctionqui transforme case en x et y
def transforme(case):
    global l_position
    # Pour comprendre ces boucles voir feuille "gestion xy opti" 
    for i in range(3):
        for j in range(3):
            if 3*i+j == case:
                return l_position[j], l_position[i]  #return x, y

# Procédure qui actualise les variables de Tkinter avec la variables score
def afficheScore(score):
    var_score_j1.set(str(score[0]))
    var_score_j2.set(str(score[1]))

def forme(nom, x0, y0, x1, y1):
    global l_colorJoueur, joueur
    r = 20
    if nom == 'cercle':
        can.create_oval(x0-r, y0-r, x1+r, y1+r, outline =l_colorJoueur[1], width=5)
    elif nom == 'croix':
        can.create_line(x0-r, y0-r, x1+r, y1+r, fill=l_colorJoueur[0], width=5)
        can.create_line(x0-r, y0+r, x1+r, y1-r, fill=l_colorJoueur[0], width=5)
    elif nom == 'ligne':
        can.create_line(x0, y0, x1, y1, fill=l_colorJoueur[joueur-1], width=9, cap='round')

# Procédure clic() avec le paramètre souris qui contient les abscisse et ordonnée du clic de la souris sur la fenêtre
def clic(souris):
    global joueur, joueurStart, l_nom, l_cases, l_colorJoueur, l_position, score, stop
    if stop == 0:
        # Fonction qui retourne l'index du nombre le plus petit de la liste mise en argument
        def minIndex(liste):
            mini = 0
            for i in range(len(liste)):
                if liste[i] < liste[mini]:
                    mini = i
            return mini
        # Fonction qui calcul la distance positive entre le point souris et les 3 points de la liste l_position
        # Ensuite grâce à la fonction minIndex() les index de x et y en sont déduit
        def proche(souris):
            liste = []
            for i in l_position:
                liste.append(abs(i-souris))
            return minIndex(liste)
        if var_name_j2.get() == 'IA#3.1' and joueur == 2:
            index_x = proche(souris[0])
            index_y = proche(souris[1])
        else:
            index_x = proche(souris.x)
            index_y = proche(souris.y)
        case = 3*index_y+index_x
        x = l_position[index_x]
        y = l_position[index_y]
        if l_cases[case] == 0:
            l_cases[case] = joueur
            if joueur == 2:
                joueurTemp = 1
                forme('cercle', x, y, x, y)
            else:
                joueurTemp = 2
                forme('croix', x, y, x, y)
            if gagner():
                stop = 1
                lab_gain.configure(text=l_nom[joueur-1]+" a gagné :D", bg=l_colorJoueur[joueur-1])
                score[joueur-1] += 1
                afficheScore(score)
                joueurStart = joueurTemp
            elif l_cases.count(0) == 0:
                stop = 1
                joueurStart = joueurTemp
                lab_gain.configure(text="Match nul !", bg='#3D8BDE')
            else:
                joueur = joueurTemp
                lab_gain.configure(text=l_nom[joueur-1]+" c'est à toi !", bg=l_colorJoueur[joueur-1])
                if var_name_j2.get() == 'IA#3.1' and joueur == 2:
                    IA_play()
        elif l_cases.count(0) != 0:
            lab_gain.configure(text="Tu ne peux pas jouer sur cette case", bg="orange")

#L'ordinateur joue, ses coups sont calculer en fonction de la dispositions du Morpion
def IA_play():
    def analyse(mode):
        global l_indexGagner
        l_analyse = [['gagner', 'défense', 'attaque'], 
                     [[2, 1],    [1, 1],    [2, 2]] ]
        case_joueur = l_analyse[1][l_analyse[0].index(mode)][0]
        case_libre = l_analyse[1][l_analyse[0].index(mode)][1]
        for gagner in l_indexGagner:
            l_case_joueur = []
            for case in gagner:
                l_case_joueur.append(l_cases[case])
            if l_case_joueur.count(0) == case_libre and l_case_joueur.count(case_joueur) == (3-case_libre):
                case = gagner[l_case_joueur.index(0)]
                return case
        return 'rien'
    def stratégie():
        global l_cases
        ordre = ['gagner', 'défense', 'attaque']
        #défense
        for mode in ordre:
            case = analyse(mode)
            if type(case) == int:
                if mode == 'attaque':
                    if randint(0, 1):
                        return case
                else:
                    return case
        #Si rien n'a marché -> au pif
        index = []
        for i in range(len(l_cases)):
            if l_cases[i] == 0:
                index.append(i)
        case = index[randint(0, len(index)-1)]
        return case
    x, y = transforme(stratégie())
    clic([x, y])


# Initialisation des listes et varialbes 
l_position = [34, 94, 154]
l_indexGagner = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
l_colorJoueur = ['#00FFB2', '#FF00FF']
score = [0, 0]  # L'index 0 correspond au score du joueur 1 et l'index 1 à celui du joueur 2
l_nom = ['']*2

#Vérification qu'une saisie à bien été faite
def verif():
    if var_name_j1.get():
        if var_name_j2.get() and lab1.cget('text') == 'GO':
            morpionGame()
        elif lab1.cget('text') == 'VS':
            joueur2()
        else:
            showerror("Erreur", "Veuillez entrer un nom !")
    else:
        showerror("Erreur", "Veuillez entrer un nom !")
# Positionnement des widget avec la méthode .pack)
def start():
    frame_titre.pack()
    lab_titre.pack()
    frame_entry.pack()
    lab_nom.pack()
    entry_nom.pack(side=LEFT, padx=10)
    bout_color.pack(side=LEFT)
    frame_choix.pack()
    lab1.pack()
    bout1.pack(side=LEFT, padx=4)
    bout2.pack(side=LEFT, pady=5, padx=6)
def joueur2():
    global joueur, l_colorJoueur
    joueur = 2
    frame_entry.configure(bg='#F4B2FA', padx=23)
    lab_nom.configure(text="Nom du 2e joueur :", fg=l_colorJoueur[1], bg='#F4B2FA')
    entry_nom.configure(textvariable=var_name_j2, bg=l_colorJoueur[1])
    bout_color.configure(bg=l_colorJoueur[1])
    frame_choix.configure(bg='#AEF6B8', padx=50)
    lab1.configure(text="GO", fg='#41A846', bg='#AEF6B8')
    bout1.configure(text="Retour", bg='#F8452D', command=retour, cursor='left_side')
    bout2.configure(text="C'est parti !", bg="#41A846", command=verif, cursor='right_side ')
def retour():
    global l_colorJoueur
    frame_entry.configure(bg='#AEF6B8', padx=34)
    lab_nom.configure(text="Entre ton nom :", fg=l_colorJoueur[0], bg='#AEF6B8')
    entry_nom.configure(textvariable=var_name_j1, bg=l_colorJoueur[0])
    bout_color.configure(bg=l_colorJoueur[0])
    frame_choix.configure(bg='#F4B2FA', padx=47)
    lab1.configure(text="VS", fg='#BA136C', bg='#F4B2FA')
    bout1.configure(text="Ordinateur", bg='#9938BD', command=activeIA, cursor='iron_cross')
    bout2.configure(text="Joueur 2", bg=l_colorJoueur[1], command=verif, cursor='circle')
def activeIA():
    global joueur, l_colorJoueur
    if var_name_j1.get():
        l_colorJoueur[1] = '#9938BD'
        joueur = 1
        var_name_j2.set("IA#3.1")
        morpionGame()
    else:
        showerror("Erreur", "Veuillez entrer un nom !")
def morpionGame():
    global l_nom, joueurStart
    frame_titre.pack_forget()
    lab_titre.pack_forget()
    frame_entry.pack_forget()
    frame_choix.pack_forget()
    can.bind("<Button-1>", clic)    # Gestion des clics de souris
    can.pack()
    lab_gain.pack()
    frame_score.pack()
    lab_score_j1.pack(side=LEFT, padx=3, pady=5)
    lab_score_sep.pack(side=LEFT)
    lab_score_j2.pack(side=LEFT, padx=3, pady=5)
    frame_button.pack(padx=19)
    bout_quit.pack(side=LEFT, padx=10)
    bout_retry.pack(side=LEFT, padx=10, pady=10)
    lab_score_j1.configure(bg=l_colorJoueur[0])
    lab_score_j2.configure(bg=l_colorJoueur[1])
    l_nom[0] = var_name_j1.get()
    l_nom[1] = var_name_j2.get()
    joueurStart = joueur
    afficheScore(score)
    reset()
#Procédure qui ouvre une palette de couleur 
def palette():
    global l_colorJoueur
    if lab1.cget('text') == "GO":
        colorIndex = 1
    else:
        colorIndex = 0
    tuple_color = askcolor(color=l_colorJoueur[colorIndex])
    if tuple_color[1]:
        l_colorJoueur[colorIndex] = tuple_color[1]
        if colorIndex == 0:
            retour()
        else:
            joueur2()

# Création des différents widget avec Tkinter tel que des boutons, des étiquettes, des canevas...
fen = Tk()  # Fenêtre principale
fen.title("Morpion")
# Fenêtre morpionn game
can = Canvas(fen, width = 189, height =189, bg ='#F0F0F0')
lab_gain = Label(fen)
frame_score = Frame(fen, padx=10)
var_score_j1 = StringVar()
var_score_j2 = StringVar()
lab_score_j1 = Label(frame_score, textvariable=var_score_j1, font=('Courier New Greek', 14, 'bold'), fg='#FFFFFF')
lab_score_sep = Label(frame_score, text="VS", font=('Courier New Greek', 14, 'bold'), fg='#33A8D1')
lab_score_j2 = Label(frame_score, textvariable=var_score_j2, font=('Courier New Greek', 14, 'bold'), fg='#FFFFFF')
frame_button = Frame(fen)
bout_retry = Button(frame_button, text="Recommencer", bg="#41A846",  command = reset, cursor='exchange')
bout_quit = Button(frame_button, text="Quitter", bg="#F8452D", command = fen.destroy, cursor='pirate')

# Fenêtre Acceuil / J1
frame_titre = Frame(fen, padx=7, bg='#D6F8F7')
lab_titre = Label(frame_titre, text="Bienvenue sur\n le jeu Morpion !", font=('Cooper Black', 19, 'bold'), fg='#1E95E3', bg='#D6F8F7')
var_name_j1 = StringVar()
var_name_j2 = StringVar()
frame_entry = Frame(fen, padx=34, pady=10, bg='#AEF6B8')
lab_nom = Label(frame_entry, text="Entre ton nom :", font=('Gill Sans MT', 15, 'bold'), fg=l_colorJoueur[0], bg='#AEF6B8')
entry_nom = Entry(frame_entry, textvariable=var_name_j1, width=20, bg=l_colorJoueur[0])
img_color = PhotoImage(file='color.png')
bout_color = Button(frame_entry, image=img_color, command=palette, bg=l_colorJoueur[0])
frame_choix = Frame(fen, padx=47, bg='#F4B2FA')
lab1 = Label(frame_choix, text="VS", font=('Cooper Black', 30, 'bold'), fg='#BA136C', bg='#F4B2FA')
bout1 = Button(frame_choix, text="Ordinateur", bg='#9938BD', command=activeIA, cursor='iron_cross')
bout2 = Button(frame_choix, text="Joueur 2", bg=l_colorJoueur[1], command=verif, cursor='circle')
start()
fen.mainloop()

# Note: alterne joueur si match nul + compréhension IA#3.1 + 1/2 chance d'utiliser attaque
# bug entrer un nom cliquer sur joueur 2, retour, enlever nom, pas de détection de non remplissage 
# --> problème dans la fonction retour()
#Couleur:
#  j1 #00FFB2
#  j2 #FF00FF
