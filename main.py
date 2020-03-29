# Cette version est un bonus, seule l'ordinateur peut jouer (contre lui même)
from tkinter import *
from tkinter.messagebox import *
from random import randint
import time

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
    global joueur, joueur_perdu, l_cases, l_colorJoueur, l_nom, stop
    print('\n----------------\n### RESTART ###\n----------------', end='')
    l_cases = [0]*9
    stop = 0
    joueur = joueur_perdu
    can.delete(ALL)
    grille()
    IA_play()

# Fonction qui retourne 1 si un alignement horizontale, verticale, ou diagonale de 3 cases est détecté sinon retourne 0 
def gagner():
    global l_cases, l_indexGagner
    for l in l_indexGagner:
        if l_cases[l[0]] == l_cases[l[1]] and l_cases[l[0]] == l_cases[l[2]] and l_cases[l[0]] != 0:
            x0, y0 = transforme(l[0])
            x1, y1 = transforme(l[2])
            forme('trait', x0, y0, x1, y1)
            return 1
    return 0

# Fonctionqui transforme N en x et y
def transforme(N):
    global l_position
    # Pour comprendre ces boucles voir feuille "gestion xy opti" 
    for i in range(3):
        for j in range(3):
            if 3*i+j == N:
                return l_position[j], l_position[i]  #return x, y

# Procédure qui actualise les variables de Tkinter avec la variables score
def afficheScore(score):
    var_score_j1.set(str(score[0]))
    var_score_j2.set(str(score[1]))

def forme(nom, x0, y0, x1, y1):
    global l_colorJoueur, l_colorWin, joueur
    r = 20
    if nom == 'cercle':
        can.create_oval(x0-r, y0-r, x1+r, y1+r, outline =l_colorJoueur[1], width=5)
    elif nom == 'croix':
        can.create_line(x0-r, y0-r, x1+r, y1+r, fill=l_colorJoueur[0], width=5)
        can.create_line(x0-r, y0+r, x1+r, y1-r, fill=l_colorJoueur[0], width=5)
    else:
        can.create_line(x0, y0, x1, y1, fill=l_colorWin[joueur-1], width=9, cap='round')

# Procédure clic() avec le paramètre souris qui contient les abscisse et ordonnée du clic de la souris sur la fenêtre
def clic(souris):
    global joueur, joueur_perdu, l_nom, l_cases, l_colorJoueur, l_position, score, stop
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
        
        index_x = proche(souris[0])
        index_y = proche(souris[1])
        case = 3*index_y+index_x
        x = l_position[index_x]
        y = l_position[index_y]
        if l_cases[case] == 0:
            l_cases[case] = joueur
            if joueur == 2:
                temp = 1
                forme('cercle', x, y, x, y)
            else:
                temp = 2
                forme('croix', x, y, x, y)
            if gagner():
                stop = 1
                lab_gain.configure(text=l_nom[joueur-1]+" a gagné :D", bg=l_colorJoueur[joueur-1])
                score[joueur-1] += 1
                afficheScore(score)
                joueur = temp
                joueur_perdu = joueur
            elif l_cases.count(0) == 0:
                stop = 1
                lab_gain.configure(text="Match nul !", bg='#3D8BDE')
                joueur = temp
            else:
                joueur = temp
                lab_gain.configure(text=l_nom[joueur-1]+" c'est à toi !", bg=l_colorJoueur[joueur-1])

def IA_play():
    global stop, joueur
    if not(stop):
        print('\nJoueur n°',joueur,'\n',l_cases, sep='')
        def analyse(mode):
            global l_indexGagner, joueur
            if mode == 'défense':
                if joueur == 1:
                    valeur = 2
                else:
                    valeur = 1
                countLibre = 1
            elif mode == 'attaque':
                valeur = joueur
                countLibre = 2
            elif mode == 'gagner':
                valeur = joueur
                countLibre = 1
            for i in l_indexGagner:
                l_casesValeur = []
                for j in i:
                    l_casesValeur.append(l_cases[j])
                if l_casesValeur.count(0) == countLibre and l_casesValeur.count(valeur) == 3-countLibre:
                    n = i[l_casesValeur.index(0)]
                    print(i, '=', l_casesValeur, " ->",mode,"! N =", n)
                    return n
            return 'rien'
        def stratégie():
            global l_cases
            ordre = ['gagner', 'défense', 'attaque']
            #défense
            for mode in ordre:
                case = analyse(mode)
                if type(case) == int:
                    return case
            #Si rien n'a marché -> au pif
            index = []
            for i in range(len(l_cases)):
                if l_cases[i] == 0:
                    index.append(i)
            case = index[randint(0, len(index)-1)]
            print("-> RANDOM ! N =",case, )
            return case
        x, y = transforme(stratégie())
        print('Position [ x=', x, 'y=', y, ']')
        clic([x, y])



# Initialisation des listes et varialbes 
l_position = [34, 94, 154]
l_indexGagner = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
l_colorJoueur = ['#00FFB2', '#FF00FF']
l_colorWin = ['#3AB892', '#973A97']
score = [0, 0]  # L'index 0 correspond au score du joueur 1 et l'index 1 à celui du joueur 2
l_nom = ['IA#1', "IA#2"]
joueur = 2
joueur_perdu = joueur

def start():
    global l_nom
    can.pack()
    lab_gain.pack()
    frame_score.pack()
    lab_score_j1.pack(side=LEFT, padx=3, pady=5)
    lab_score_sep.pack(side=LEFT)
    lab_score_j2.pack(side=LEFT, padx=3, pady=5)
    frame_button.pack(padx=19)
    bout_quit.pack(side=LEFT, padx=10)
    bout_retry.pack(side=LEFT, padx=10, pady=10)
    afficheScore(score)
    reset()

# Création des différents widget avec Tkinter tel que des boutons, des étiquettes, des canevas...
fen = Tk()  # Fenêtre principale
fen.title("Morpion")
# Fenêtre morpionn game
can = Canvas(fen, width = 189, height =189, bg ='#F0F0F0')
lab_gain = Label(fen)
frame_score = Frame(fen, padx=10)
var_score_j1 = StringVar()
var_score_j2 = StringVar()
lab_score_j1 = Label(frame_score, textvariable=var_score_j1, font=('Courier New Greek', 14, 'bold'), bg='#00FFB2', fg='#FFFFFF')
lab_score_sep = Label(frame_score, text="VS", font=('Courier New Greek', 14, 'bold'), fg='#33A8D1')
lab_score_j2 = Label(frame_score, textvariable=var_score_j2, font=('Courier New Greek', 14, 'bold'), bg='#FF00FF', fg='#FFFFFF')
frame_button = Frame(fen)
bout_retry = Button(frame_button, text="Suivant", bg="#41A846",  command = IA_play)
bout_quit = Button(frame_button, text="Recommencer", bg="#F8452D", command = reset, cursor='exchange')


start()
fen.mainloop()

# Note: IA 3.0 défensive + attaque ! 
#Couleur:
#  j1 #00FFB2
#  j2 #FF00FF
