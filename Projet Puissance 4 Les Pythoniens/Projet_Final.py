# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 11:12:52 2020

@author: Michelle Hatoum
"""	
import time
import math
import random
import numpy as np
#%%
        
ia = 2
humain = 1
tour_ia=0
tour_humain=1
NB_COLONNES = 12
NB_LIGNES = 6
TAILLE_FENETRE = 4
VIDE = 0
CRED = '\33[31m'
CEND = '\033[0m'
CBLUE   = '\33[34m'

#%% Fonctions utiles

def est_tour_gagnant(s, joueur):
	# Horizontales
	for c in range(NB_COLONNES-3):
		for r in range(NB_LIGNES):
			if s[r][c] == joueur and s[r][c+1] == joueur and s[r][c+2] == joueur and s[r][c+3] == joueur:
				return True

	# Verticales
	for c in range(NB_COLONNES):
		for r in range(NB_LIGNES-3):
			if s[r][c] == joueur and s[r+1][c] == joueur and s[r+2][c] == joueur and s[r+3][c] == joueur:
				return True

	# Diagonales positives
	for c in range(NB_COLONNES-3):
		for r in range(NB_LIGNES-3):
			if s[r][c] == joueur and s[r+1][c+1] == joueur and s[r+2][c+2] == joueur and s[r+3][c+3] == joueur:
				return True

	# Diagonales négatives
	for c in range(NB_COLONNES-3):
		for r in range(3, NB_LIGNES):
			if s[r][c] == joueur and s[r-1][c+1] == joueur and s[r-2][c+2] == joueur and s[r-3][c+3] == joueur:
				return True 
            
	result = 0
	for i in range(NB_LIGNES):
		for j in range(NB_COLONNES):
			if s[i][j]==0:
				result+=1

	if result==0:
		return True
    

def est_noeud_terminal(s):
	return est_tour_gagnant(s, humain) or est_tour_gagnant(s, ia)

def evaluer_fenetre(fenetre, joueur):
	score = 0
	adversaire = humain
	if joueur == humain:
		adversaire = ia

	if fenetre.count(joueur) == 4:
		score += 100
	if fenetre.count(joueur) == 3 and fenetre.count(VIDE) == 1:
		score += 5
	if fenetre.count(joueur) == 2 and fenetre.count(VIDE) == 2:
		score += 2
	if fenetre.count(adversaire) == 4:
		score -= 15
	if fenetre.count(adversaire) == 3 and fenetre.count(VIDE) == 1:
		score -= 5
	if fenetre.count(joueur) == 3 and fenetre.count(adversaire) == 1:
		score -= 10
	return score
        
def score_position(s, joueur):
	score = 0

	#on modifie le score selon les pions dans la colonne centrale
	centre_array = [int(i) for i in list(s[:, NB_COLONNES//2])]
	centre_count = centre_array.count(joueur)
	score += centre_count * 3

	#on modifie le score selon les pions dans chaque ligne
	for r in range(NB_LIGNES):
		ligne_array = [int(i) for i in list(s[r,:])]
		for c in range(NB_COLONNES-3):
			fenetre = ligne_array[c:c+TAILLE_FENETRE]
			score += evaluer_fenetre(fenetre, joueur)

	#on modifie le score selon les pions dans chque colonne
	for c in range(NB_COLONNES):
		col_array = [int(i) for i in list(s[:,c])]
		for r in range(NB_LIGNES-3):
			fenetre = col_array[r:r+TAILLE_FENETRE]
			score += evaluer_fenetre(fenetre, joueur)

	#on modifie le score selon les pions dans chaque diagonale 
	for r in range(NB_LIGNES-3):
		for c in range(NB_COLONNES-3):
			fenetre = [s[r+i][c+i] for i in range(TAILLE_FENETRE)]
			score += evaluer_fenetre(fenetre, joueur)

	for r in range(NB_LIGNES-3):
		for c in range(NB_COLONNES-3):
			fenetre = [s[r+3-i][c+i] for i in range(TAILLE_FENETRE)]
			score += evaluer_fenetre(fenetre, joueur)

	return score


def Actions(s):       
	actions = []
	for col in range(NB_COLONNES):
		if s[NB_LIGNES-1][col] == VIDE:
			actions.append(col)
	return actions
        
def Affichage(grille):
    for i in reversed(range(NB_LIGNES)):
        print(" | ",end=' ')
        for j in range(NB_COLONNES):
            if(grille[i][j]==1):
                print(CBLUE+'0'+CEND,end=' ')
            elif grille[i][j]==2:
                print(CRED+'0'+CEND,end=' ')
            else:
                print(" ",end=' ')
            print(" | ",end=' ')
        print()
    print(" | ",end=' ')
    for i in range(NB_COLONNES):
        print("_",end=" ")
        print(" | ",end=' ')
    print()
    print(" | ",end=' ')
    for i in range(1,NB_COLONNES+1):
        print(i,end=" ")
        if i>9:
            print("| ",end=' ')
        else:
            print(" | ",end=' ')
    print()
    
        
def prochaine_ligne_vide(s, col):
	for r in range(NB_LIGNES):
		if s[r][col] == VIDE:
			return r
        
def grille_apres_jeu(s, row, col, joueur):
	s[row][col] = joueur
    
def somme(liste):
    _somme = 0
    for i in liste:
        _somme = _somme + i
    return _somme

def moyenne(liste):
    return somme(liste)/len(liste)

#%%Minimax
def AlphaBeta(s,depth,alpha,beta,joueurAMaximiser):
	actions = Actions(s)
	est_terminal = est_noeud_terminal(s)
	if depth == 0 or est_terminal:
		if est_terminal:
			if est_tour_gagnant(s, ia):
				return (None, 100000000000000)
			elif est_tour_gagnant(s, humain):
				return (None, -10000000000000)
			else: # GameOver
				return (None, 0)
		else: # à la prof 0
			return (None, score_position(s, ia))
	if joueurAMaximiser:
		value = -math.inf
		colonne = random.choice(actions)
		for col in actions:
			ligne = prochaine_ligne_vide(s, col)
			b_copy = s.copy()
			grille_apres_jeu(b_copy, ligne, col, ia)
			nouveau_score = AlphaBeta(b_copy, depth-1, alpha, beta, False)[1]
			if nouveau_score > value:
				value = nouveau_score
				colonne = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return colonne, value

	else: # tour du joueur à minimiser
		value = math.inf
		colonne = random.choice(actions)
		for col in actions:
			ligne = prochaine_ligne_vide(s, col)
			b_copy = s.copy()
			grille_apres_jeu(b_copy, ligne, col, humain)
			nouveau_score = AlphaBeta(b_copy, depth-1, alpha, beta, True)[1]
			if nouveau_score < value:
				value = nouveau_score
				colonne = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return colonne, value
#%%Jeu
def Jeu():
    grille = np.zeros((NB_LIGNES,NB_COLONNES),dtype=int)
    temps = []
    game_over = False
    tour = 1
    
    while not game_over and tour <= 72 :
        if tour % 2 != 0:#Tour de l'IA
            start_time=time.time()
            col = AlphaBeta(grille, 4, -math.inf, math.inf, True)[0]
            print("temps d'exécution : "+str(time.time()-start_time))
            temps.append(time.time()-start_time)
            print( "La moyenne d'execution est : " + str(moyenne(temps)))
            #temps.append(time.time()-start_time)
            print("\nL'IA a joué en "+ str(col+1) + "\n" )
            if grille[NB_LIGNES-1][col] == VIDE:
                ligne = prochaine_ligne_vide(grille,col)
                grille_apres_jeu(grille,ligne,col,ia)
                Affichage(grille)
                tour += 1
            if est_tour_gagnant(grille, ia):
                game_over=True
                print("BIEN JOUE L'IA C'EST NOUS LES PATRONS !")
        else :
            print('liste des actions possibles :')
            print([i+1 for i in Actions(grille)])
            print('Que voulez vous jouer ?')
            while True:
                col=int(input('numéro de la colonne =')) - 1
                if col in Actions(grille):
                    break
            #start_time=time.time()
            #col = AlphaBeta(grille, 4, -math.inf, math.inf, True)[0]
            #print("temps d'exécution : "+str(time.time()-start_time))
            ligne = prochaine_ligne_vide(grille,col)
            grille_apres_jeu(grille,ligne,col,humain)
            #Affichage(grille)
            tour += 1
            if est_tour_gagnant(grille, humain):
                Affichage(grille)
                game_over = True
                print("bv mais match retour tt dsuite ca va pas ou quoi")
    if tour == 73 and game_over==False:
        Affichage(grille)
        print("Egalité, on a enfin trouvé aussi fort que nous")
    

Jeu()