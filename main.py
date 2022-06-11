from tkinter import *
from tkinter import messagebox #"import *" importe pas messagebox
from tkinter.colorchooser import askcolor
from random import choice

import sys
sys.path.insert(0, './assets')
from webcolors_min import *

def victoire(colonne,ligne,tableau):
    """
    Fonction vérifiant si la pièce placé amène à la victoire.
    Prends comme entrée la colonne et la ligne de la pièce à verifier, 
    ainsi que le tableau du jeu
    La fonction vérifie d'abord vers le bas si 3 autres pièce y sont
    La fonction ensuite vérifie l'horizontal. Elle commence par regarder elle 
    même puis les pièces à droite, avant de passer aux pièces à gauche
    Elle vérifie ensuite les horizontal sur le même principe, 
    d'abord l'horizontal qui va de bas à gauche jusqu'à en haut à gauche.
    Puis elle vérifie l'horizontal qui va de haut à gauche jusqu'à bas à droite

    On exclue dans les tests ce qui peut amené à un comportement anormal comme 
    une ligne ou une colonne plus large que prévu ou négative,
    ainsi qu'un tableau pas formatter correctement
    >>> #Vertical
    >>> victoire(3,3,[[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [2, 2, 2, 0, 0, 0], [1, 1, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
    True
    >>> #Horizontal
    >>> victoire(3,0,[[1, 2, 0, 0, 0, 0], [1, 2, 0, 0, 0, 0], [1, 2, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
    True
    >>> #Diagonal droite
    >>> victoire(3,3,[[1, 0, 0, 0, 0, 0], [2, 1, 0, 0, 0, 0], [2, 2, 1, 0, 0, 0], [2, 2, 2, 1, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0]])
    True
    >>> #Diagonal gauche
    >>> victoire(0,3,[[2, 2, 2, 1, 0, 0], [2, 2, 1, 0, 0, 0], [2, 1, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0]])
    True
    >>> #Rien (la majorité du temps)
    >>> victoire(4,3,[[2, 1, 2, 0, 0, 0], [2, 2, 1, 2, 0, 0], [1, 1, 1, 0, 0, 0], [1, 2, 2, 1, 0, 0], [1, 2, 1, 2, 0, 0], [2, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
    False
    """
    verifier = tableau[colonne][ligne]
    try:
        compteur=0
        #Verifier hauteur
        #Pièce -> Bas
        ligneencours=ligne
        while tableau[colonne][ligneencours]==verifier and ligneencours>=0:
            compteur+=1
            ligneencours-=1
        if compteur >= 4:
            return True

        #Verification horizontal
        #Pièce -> Droite
        compteur = 0
        colonneencours=colonne
        while tableau[colonneencours][ligne]==verifier and colonneencours>=0:
            compteur+=1
            colonneencours-=1
        colonneencours=colonne+1 #+1 permet d'exclure la pièce qu'on vérifie (sinon compté en double)
        #Pièce -> Gauche
        while tableau[colonneencours if colonneencours!=7 else 0][ligne]==verifier and colonneencours<7:
            compteur+=1
            colonneencours+=1
        if compteur >= 4:
            return True

        
        #Vérification diagonal droite
        compteur = 0
        colonneencours=colonne
        ligneencours=ligne
        #Pièce -> Bas à gauche
        while tableau[colonneencours][ligneencours]==verifier and colonneencours>=0 and ligneencours>=0:
            compteur+=1
            colonneencours-=1
            ligneencours-=1
        colonneencours=colonne+1
        #Pièce -> Haut à droite
        colonneencours=colonne+1
        ligneencours=ligne+1
        while tableau[colonneencours if colonneencours!=7 else 0][ligneencours if ligneencours!=6 else 0]==verifier and colonneencours<7 and ligneencours<6:
            compteur+=1
            colonneencours+=1
            ligneencours+=1
        if compteur >= 4:
            return True
        
        #Vérification diagonal gauche
        compteur = -1
        colonneencours=colonne
        ligneencours=ligne
        #Pièce -> Haut à gauche
        while tableau[colonneencours][ligneencours if ligneencours!=6 else 0]==verifier and colonneencours>=0 and ligneencours<6:
            compteur+=1
            colonneencours-=1
            ligneencours+=1
        colonneencours=colonne+1
        colonneencours=colonne
        ligneencours=ligne
        #Pièce -> Bas à droite
        while tableau[colonneencours if colonneencours!=7 else 0][ligneencours]==verifier and colonneencours<7 and ligneencours>=0:
            compteur+=1
            colonneencours+=1
            ligneencours-=1 
        if compteur >= 4:
            return True
        return False
    except IndexError:
        #Si erreur, merci de me prévenir avec si possible un screen de comment sont placés les pièces
        import traceback
        print(f"erreur de vérification : ligne = {ligneencours}, colonne = {colonneencours}\n\nerreur détaillé :\n{traceback.format_exc()}")
    

def animation():
    """
    Permet de jouer l'animation de déplacement de lettre.
    Impossible de faire une boucle for car le programme déplace l'image instantanément
    et la fonction sleep du module time n'est pas bien compatible avec tkinter.
    La seul fonction que j'ai trouvé est d'utiliser ".after()" permettant de après un temps donnée d'executer une fonction
    """
    global blocage
    global piece
    global objectif
    global img
    if "piece" in globals(): #Quand la fonction est réexécuter après le .after()
        piece+=3 #Incrémente de 3(pour bouger l'image de de 3 pixel)
    else: #Quand la fonction est exécuter pour la première fois
        blocage=True #Permet de dire au programme que l'animation commence (permet de bloquer la modification de touche)
        objectif = 500-(100*ligne) #Dit là où la pièce doit aller
        piece=0 # Met l'image à sa position de départ normal
        img = place(piece,colonne,color) #Place la première image

    canvas.delete(img) #Supprime l'image
    img = place(piece,colonne,color) #Pour la replacer à sa nouvelle position

    if piece <= objectif: #Permet de faire ma boucle for
        win.after(1,animation) #Réexécute la fonction toute les milisecondes, permet un effet fluide

    else: #Quand la boucle est fini
        canvas.delete(img)
        img = place(objectif,colonne,color) #Replace l'image à la bonne positition, le piece +3 ayant tendance à dépasser l'objectif
        blocage=False #Dit au programme que l'animation est fini
        del piece #Supprime piece pour la prochaine animation

def place(piece, colonne, couleur):
    """
    Fonction servant à placer les pièces sur le terrain
    """
    if couleur == color1:
        img = canvas.create_oval(colonne*100+5, piece+8, 94+colonne*100,94+piece-2, fill=color1hex, outline="")
    else: 
        img = canvas.create_oval(colonne*100+5, piece+8, 94+colonne*100,94+piece-2, fill=color2hex, outline="")
    return img

def quelLigne(colonne,tableau):
    """
    Indique à quel ligne la pièce doit être placé (en comptant à partir de 0)
    pour ne pas écrasé une autre pièce dans la colonne.
    Retourne -1 si la colonne est déjà remplis
    Chaque colonne est indépendante les une des autres dans cette fonction

    >>> quelLigne(1, [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
    0
    >>> quelLigne(1, [[0, 0, 0, 0, 0, 0], [2, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
    2
    >>> quelLigne(1, [[0, 0, 0, 0, 0, 0], [2, 1, 2, 1, 2, 1], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
    -1
    >>> quelLigne(2, [[2, 0, 0, 0, 0, 0], [2, 1, 2, 1, 2, 1], [0, 0, 0, 0, 0, 0], [1, 2, 1, 2, 1, 2], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
    0
    """
    for i in range(6):
        if tableau[colonne][i] == 0:
            return i
    return -1 #Si aucun 0 est disponible 

def click(event,tableau, egalite, inputType):
    """
    Gère le déroulement du jeu,
    s'active lorsque le joueur presse la barre espace ou le clic gauche
    Dû au fait qu'il n'y a pas la possibilité de return une value,
    il faut tout mettre en global, à part les listes qui sont lié, merci python !
    """
    global endgame
    if not blocage and not endgame:
        # Global pour animation
        global ligne
        global colonne
        global color
        
        #Gestion des controles par clavier
        global gameArrow
        global gameArrowOnScreen
        if inputType=="souris":
            colonne = event.x//100
            if colonne==7:
                return
            if "gameArrow" in globals():
                del(gameArrow)
                keyboardCanvas.delete(gameArrowOnScreen)
        else:
            if "gameArrow" in globals():
                colonne = gameArrow-1 #gameArrow fonctionne en comptant à partir de 1, permet donc de compter à partir de 0
            else:
                return
 
        ligne = quelLigne(colonne, tableau)

        if ligne!=-1:
            animation()
            tableau[colonne][ligne] = 1 if color == color2 else 2
            if victoire(colonne,ligne,tableau):
                endgame=True
                color = color2 if color == color1 else color1
                turn.config(text=f"Joueur {color.capitalize()} a gagné !", fg=color1hex if color==color1 else color2hex)
                return 
            win.config(bg=color1hex if color==color1 else color2hex)
            turn.config(text=f"Au tour du joueur {color.capitalize()}", fg=color1hex if color==color1 else color2hex)
            color = color2 if color == color1 else color1
            if ligne==5:
                egalite[colonne] = 1
                if not 0 in egalite:
                    turn.config(text="Egalité", fg="blue")

def move(evt):
    """
    Gère le déplacement de la flèche
    gameArrow correspond à l'emplacement flèche
    gameArrowOnScreen correspond à l'image sur le Canvas
    """
    global gameArrow
    global gameArrowOnScreen
    to = evt.keysym
    if "gameArrow" in globals():
        keyboardCanvas.delete(gameArrowOnScreen)
        if to == "Left" and gameArrow > 1: #Empeche que la flèche sorte de l'écran
            gameArrow+=-1    
        elif to == "Right" and gameArrow <= 6: #Empeche que la flèche sorte de l'écran
            gameArrow+=1        
        gameArrowOnScreen = keyboardCanvas.create_image((gameArrow*100)-50,100,image=arrow, anchor="s")
    else:
        gameArrow = 4
        gameArrowOnScreen = keyboardCanvas.create_image((gameArrow*100)-50,100,image=arrow, anchor="s")
        

def jeu():
    """
    Fonction préparant le jeu (variable et 1er joueur)
    Supprime les données de la partie précédente si il y a
    """
    global color
    global blocage,endgame
    
    egalite = [0 for _ in range(7)]
    #7 colonnes utiliser par le jeu, la 8ème, inutile, 
    #sert uniquement dans la fonction victoire et est 
    #normalement inaccessible à l'utilisateur
    tableau = [[0 for _ in range(6)] for _ in range(7)] 
    canvas.delete("all")
    keyboardCanvas.delete("all")
    blocage = endgame = False
    
    [canvas.create_line(100*i, 0, 100*i, 600, width=10) for i in range(1,7)] #Hauteur
    [canvas.create_line(0,i*100 , 700, i*100, width=15) for i in range(1,7)] #Largeur

    color = choice([color2,color1])
    turn.config(text=f"Au tour du joueur {color.capitalize()}", fg=color1hex if color==color1 else color2hex)
    win.config(bg=color1hex if color==color1 else color2hex)
    color = color2 if color == color1 else color1
    win.bind('<Button-1>', lambda evt: click(evt, tableau,egalite, "souris"))
    win.bind('<space>', lambda evt: click(evt, tableau, egalite, "espace"))
    win.bind('<Left>' , lambda evt: move(evt))
    win.bind('<Right>', lambda evt: move(evt))


def restart():
    """
    Pourquoi cette fonction ?

    Cette fonction crée une latence de 22ms afin que si une animation est en cours, elle a le temps de se terminer
    Permet d'éviter un bug qui fait que si une pièce tombe avec l'animation et que une nouvelle partie est lancé,
    la pièce reste sur le terrain, provoquant un bug visuel
    """
    win.after(22,jeu) 

#Guide
def guideAnim():
    """
    Permet d'animer les gif (pas possible par défaut normalement)
    """
    global souris, souris2
    global fleche, fleche2

    if "souris" in globals():
        canvasFen.delete(souris)
        canvasFen.delete(fleche)
        if "souris2" in globals():
            canvasFen.delete(souris2)
            canvasFen.delete(fleche2)
        del(fleche,souris)
        souris2 = canvasFen.create_image(250,600,image=imgSouris2, anchor="s")
        fleche2 = canvasFen.create_image(750,500,image=imgFleche1, anchor="s")
    else:
        souris = canvasFen.create_image(250,600,image=imgSouris1, anchor="s")
        fleche = canvasFen.create_image(750,500,image=imgFleche2, anchor="s")

    fen.after(1000,guideAnim) #toutes les 1sec change l'image


def guide():
    """
    Crée une fenêtre pour montrer aux joueurs comment jouer.
    """
    global fen
    global canvasFen
    fen = Toplevel(win)
    fen.title ("Guide Puissance 4")
    fen.geometry("1000x750")
    fen.attributes('-topmost', 'true')
    fen.resizable (width = False , height = False)
    fen.grab_set()
    
    canvasFen = Canvas(fen, width=1000, height=750)
    plus      = Label(fen, text="+",justify= "center", font="Arial, 50", fg="#4e4e4e")
    guideHaut = Label(fen, text ="Deux manières de jouer :", justify="center", font="Arial 32")
    compris   = Button(fen, text="Compris !", bg="Green", font="Arial,32", command=lambda:fen.destroy())

    canvasFen.place(x=0, y=0)
    plus.place(x="600",y="500")
    guideHaut.place(x=0,y=0,width=1000, height=100)
    compris.place(x=350, y=665,width=300, height=75)
    
    canvasFen.create_image(750,500,image=imgFleche1, anchor="s")
    canvasFen.create_image(250,600,image=imgSouris2, anchor="s")
    canvasFen.create_image(800,600,image=imgSpace, anchor="s")
    
    canvasFen.create_line (500, 100, 500, 650, dash=(15,5),width= 5) #Fonctionne mal selon l'OS

    guideAnim()
    fen.mainloop()

def setting():
    """
    Fenêtre permettant de changer le nom du joueur, ainsi que la couleur de ses jetons.
    """
    settings = Toplevel(win)
    settings.title ("Paramètre")
    settings.geometry("400x275")
    settings.resizable (width = False , height = False)
    settings.grab_set()
    roue = PhotoImage(file = "./assets/roue.gif")
    
    def userColor(requested_colour):
        """
        Fonction permettant de trouver la couleur choisi par le joueur (passe de l'hexadécimal au nom)
        Utilise le module webcolors. Si le joueur n'a pas le module d'installé sur son pc, cette fonction ne sera pas accessible.
        Webcolors ne marche qu'avec des hexadécimal précis. Cette fonction a pour but de trouver la couleur la plus proche.
        Webcolors est également seulement en anglais, les couleurs seront donc en anglais (possibilité de palier à ça en 
        utilisant un module de traduction, mais nécessite un accès un internet, ou un module de traduction offline mais lourd)

        >>> userColor("#FF0000") #Majuscule
        'red'
        >>> userColor("#ff0000") #Minuscule
        'red'
        >>> #Mais également :
        >>> userColor("#ef1010")
        'red'
        >>> userColor("#00FF00")
        'lime'
        >>> userColor("#0000FF")
        'blue'
        >>> userColor("#ffa500")
        'orange'
        >>> #Nom de couleur complexe
        >>> userColor('#31ceab')
        'lightseagreen'

        >>> userColor("#FFFFFF")
        'white'
        >>> userColor("#000000")
        'black'
        """
        requested_colour = hex_to_rgb(requested_colour) #Convertie l'hex en entrée en tuple RGB 
        min_colours = {} #Crée un dictionnaire vide
        for hexcouleur, nom in CSS3_HEX_TO_NAMES.items(): # Boucle la longueur du dictionnaire (146 fois, webcolors version 1.11.1)
            r_c, g_c, b_c = hex_to_rgb(hexcouleur) #Convertie l'hex du dictionnaire en tuple RGB 
            rd = (r_c - requested_colour[0]) ** 2 #Calcule la différence entre les couleurs du dictionnaire CSS3_HEX_TO_NAMES et la couleur chercher
            gd = (g_c - requested_colour[1]) ** 2
            bd = (b_c - requested_colour[2]) ** 2
            min_colours[(rd + gd + bd)] = nom #Met la somme des différences des couleurs dans le dictionnaire crée au début
        return min_colours[min(min_colours.keys())] #Retourne la valeur la plus petite du dictionnaire; la valeur la plus proche

    def hexcheck(data):
        """
        Fonction s'executant à chaque caractère entrée dans les cases destiné à entrer la couleur hexadécimal choisi
        Si le caractère entrée n'est pas un hex, supprime le caractère.
        Remplace également les minuscules par des majuscule
        Bloque le nombre de caractère à 6 
        """
        nb = data[1]
        sv = data[0].get().upper()
        position = hexcolor[nb].index(INSERT)
        if not len(sv)==0:
            if not sv[position-1] in "0123456789ABCDEF" or len(sv)>6:
                position-=1
                hexcolor[nb].delete(0,"end")
                sv = sv[:position]+sv[position+1:]
                hexcolor[nb].insert(0,sv)
            else:
                hexcolor[nb].delete(0,"end")
                hexcolor[nb].insert(0,sv)

            if len(sv)==6:
                canvasColor[nb].delete("ALL")
                canvasColor[nb].create_oval(2, 2, 98,98, fill="#"+sv, outline="")
            hexcolor[nb].icursor(position)

    def pickcolor(player):
        """
        Permet de choisir une couleur dans une interface graphique et de la mettre dans l'entrée
        """
        color = askcolor()
        if not color[0]==None:
            hexcolor[player].delete(0,"end")
            hexcolor[player].insert(0,color[1][1:])


    def namecheck(data):
        """
        Permet de bloquer le nombre de caractère dans les cases où il faut mettre son nom à 8 caractères max
        Empêche pas les caractères Unicode long
        """
        username = data[0].get()
        nb = data[1]
        if len(username) > 8:
            userNameColor[nb].delete(0,"end")
            username = username[:-1]
            userNameColor[nb].insert(0,username)


    def finished():
        """
        Déclencher lorsque le bouton est appuyé.
        Permet d'enregistrer les paramètres et de recommencer une nouvelle partie. 
        """
        global color1,color2,color1hex,color2hex
        #Empêche les deux joueurs d'avoir la même couleur
        if len(hexcolorVAR["1"].get())==6 and len(hexcolorVAR["2"].get())==6 and hexcolorVAR["1"].get()==hexcolorVAR["2"].get():
            messagebox.showwarning("Attention !", "Les deux joueurs ont la même couleur !") #Empeche pas les joueurs d'avoir deux couleurs très proche
            return
        if len(userNameColorVAR["1"].get())>0 and len(userNameColorVAR["2"].get())>0 and userNameColorVAR["1"].get()==userNameColorVAR["2"].get():
            messagebox.showwarning("Attention !", "Les deux joueurs ont le même nom !")
            return
        # Si aucun nom n'est entrée et que les couleurs sont trop proche (module webcolors renvoient le même nom), oblige le joueur à entrer un nom
        if (len(userNameColorVAR["1"].get())==0 and len(userNameColorVAR["2"].get())==0):
            if userColor("#"+hexcolorVAR["1"].get() if len(hexcolorVAR["1"].get()) == 6 else "ff0000" )==userColor("#"+hexcolorVAR["2"].get() if len(hexcolorVAR["2"].get())==6 else "#f3c200"):
                messagebox.showwarning("Attention !", "Les deux joueurs ont une couleur trop proche !\nMerci de prendre des couleurs plus éloigné ou de mettre des noms personnalisés.")
                return
            
        #Si les vérifications précédentes sont passées, alors demande aux joueurs si ils sont sûr
        if messagebox.askyesno("Sauvegarder","Changer la couleur fait recommencer la partie. Continer ?"):
            color1hex= "#"+hexcolorVAR["1"].get() if len(hexcolorVAR["1"].get())==6 else "#ff0000"
            color2hex= "#"+hexcolorVAR["2"].get() if len(hexcolorVAR["2"].get())==6 else "#f3c200"
            color1= userColor(color1hex) if len(userNameColorVAR["1"].get())==0 else userNameColorVAR["1"].get()
            color2 = userColor(color2hex) if len(userNameColorVAR["2"].get())==0 else userNameColorVAR["2"].get()
            jeu() # Relance une nouvelle partie
            settings.destroy() #Détruit la fenêtre de configuration de couleur 

    #Création de l'interface et des variables pour les entrées
    canvasSettings = Canvas(settings,width=400, height=200)

    canvasColor = {}
    canvasColor["1"] = Canvas(settings,width=100,height=100)
    canvasColor["2"] = Canvas(settings,width=100,height=100)

    textColorSet1 = Label(settings,text="Couleur en HEX :")
    textColorSet2 = Label(settings,text="Couleur en HEX :")
    textColorSetName1 = Label(settings,text="Nom du joueur :")
    textColorSetName2 = Label(settings,text="Nom du joueur :")

    hexcolorVAR={}
    hexcolorVAR["1"] = StringVar()
    hexcolorVAR["2"] = StringVar()

    userNameColorVAR={}
    userNameColorVAR["1"] = StringVar()
    userNameColorVAR["2"] = StringVar()

    hexcolorVAR["1"].trace("w", lambda name, index, mode, hexcolor1VAR=(hexcolorVAR["1"],"1"): hexcheck(hexcolor1VAR))
    hexcolorVAR["2"].trace("w", lambda name, index, mode, hexcolor2VAR=(hexcolorVAR["2"],"2"): hexcheck(hexcolor2VAR))
    userNameColorVAR["1"].trace("w", lambda name, index, mode, userNameColor1VAR=(userNameColorVAR["1"],"1"): namecheck(userNameColor1VAR))
    userNameColorVAR["2"].trace("w", lambda name, index, mode, userNameColor2VAR=(userNameColorVAR["2"],"2"): namecheck(userNameColor2VAR))

    hexcolor = {}
    hexcolor["1"] = Entry(settings, textvariable=hexcolorVAR["1"])
    hexcolor["2"] = Entry(settings, textvariable=hexcolorVAR["2"])
    userNameColor = {}
    userNameColor["1"] = Entry(settings, textvariable=userNameColorVAR["1"])
    userNameColor["2"] = Entry(settings, textvariable=userNameColorVAR["2"])

    picker1 = Button(settings, image=roue,command=lambda:pickcolor("1"))
    picker2 = Button(settings, image=roue,command=lambda:pickcolor("2"))
    finishedButton = Button(settings,text="Enregistrer",font=("Arial,24"),command=finished)

    canvasColor["1"].create_oval(2, 2, 98,98, fill="red", outline="")
    canvasColor["2"].create_oval(2, 2, 98,98, fill="#f3c200", outline="")
    canvasSettings.create_line (200, 0, 200, 350, dash=(15,5),width= 5)

    textColorSet1.place(x=37.5,y=130)
    textColorSet2.place(x=237.5,y=130)
    textColorSetName1.place(x=37.5,y=170)
    textColorSetName2.place(x=237.5,y=170)
    hexcolor["1"].place(x=37.5,y=150)
    hexcolor["2"].place(x=237.5,y=150)
    userNameColor["1"].place(x=37.5,y=190)
    userNameColor["2"].place(x=237.5,y=190)
    canvasColor["1"].place(x=50,y=0)
    canvasColor["2"].place(x=250,y=0)
    canvasSettings.place(x=0,y=0)
    picker1.place(x=170,y=150,width=20, height=20)
    picker2.place(x=370,y=150,width=20, height=20)
    finishedButton.place(x=150,y=225)

    #Bloque la possibilité de coller, évite la possibilité de pouvoir écrire autre chose que des HEX ou d'outrepasser la limite de caractère.
    hexcolor["1"].bind('<Control-v>', lambda e: 'break')
    hexcolor["2"].bind('<Control-v>', lambda e: 'break')
    userNameColor["1"].bind('<Control-v>', lambda e: 'break')
    userNameColor["2"].bind('<Control-v>', lambda e: 'break')

    settings.mainloop()

#Fenêtre
win = Tk()
win.config(width=715,height=800,relief="groove",bd=5)
win.title ("Puissance 4")
win.geometry("715x800") #Cette dimension pose problème sur petits écrans
win.resizable (width = False , height = False)
menubar = Menu(win)

canvas = Canvas(win, width=700, height=600, bg='ivory')
keyboardCanvas= Canvas(win, width=700, height=100, bg='#e1e1d7')
turn = Label(win,justify= "center", font= ("Arial","34", "bold"))
win.config(menu=menubar)

menubar.add_command(label="Recommencer une nouvelle partie !", command=restart)
menubar.add_command(label="Comment Jouer ?", command=guide)
menubar.add_command(label="Paramètres", command=setting)
keyboardCanvas.place(x=0, y=100)
canvas.place(x=0, y=200)
turn.place(x=0,y=0,width=704,height=100)

color1="red"
color1hex="#ff0000"
color2="gold"
color2hex="#f3c200"

#Images
arrow      = PhotoImage(file = "./assets/arrow.gif")
imgSpace   = PhotoImage(file = "./assets/spacebar.gif")
imgSouris1 = PhotoImage(file = "./assets/guide.gif")
imgSouris2 = PhotoImage(file = "./assets/guide.gif" , format="gif -index 1") #Récupère la deuxième image du gif
imgFleche1 = PhotoImage(file = "./assets/fleche.gif")
imgFleche2 = PhotoImage(file = "./assets/fleche.gif", format="gif -index 1")

jeu()
win.mainloop()