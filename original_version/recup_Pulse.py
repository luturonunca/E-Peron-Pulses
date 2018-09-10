# -*- coding: iso-8859-1 -*-
import time
start = time.time()
import os
import math
import csv
import numpy as np
import scipy as sci
import matplotlib as mpl
import matplotlib.pyplot as pl
import matplotlib.patches as patches
import matplotlib.path as path
import random as rand
import datetime as dt
import pyfits
import pickle
from jdutil import * #librairie pour convertir des dates (JD, MJD, date, etc..)
############################################################################
#                Input à paramétrer manuellement (pour l'instant)
############################################################################
carte = 'Q6'
YYYY = '2016'
MM = '07'
DD = '25'
file_name = '2016-7-25_20-40-29_P_HOURS'
date_file = YYYY+'-'+MM+'-'+DD
table1='Data_'+carte+'/'+date_file+'/'+file_name+'_'+carte
nblignes = 0
fd = open(table1, 'r') # 'r' pour reading = mode lecture
for line in fd:
    nblignes = nblignes + 1
fd.close()

# initialisation de la table de données

data = []
#Initialisation du timer

timer = time.time()

# lecture des données dans le fichier
print "lecture du fichier", table1 
lecfi = csv.reader(open(table1,'r'),skipinitialspace = 'true',delimiter='\t') # delimiter = caractÃ¨re utilisÃ© pour sÃ©parer les diffÃ©rentes valeurs

# remplissage des données du fichier pulse dans la variable data

i = 0
for co in lecfi:
    data.append(co[0])
    i = i+1

# Analyse de chaque ligne de données (on extrait le trigger time, le T_start et T_end du pulse)
lignes = []
print "Temps de lecture fichier (s) :", time.time()-timer
print "Nombre de lignes a traiter : ", len(data)
timer = time.time()
print "Etape 1 : nettoyage des elements non chiffres (,),' ',[ et ]"
# Etape 1 on nettoie les éléments non importants : (, ),' ',[,]
for k in range(len(data)-1):
    ligne = list(data[k])# on lit ligne par ligne
      
    i=0
    while (i<len(ligne)):
        a = ligne[i]# on analyse les caratères présents dans la ligne 
        if a=='(' or a==')' or a==' ':# or a=='[' or a==']':# on supprimme les "mauvais caratères"
            #print "bad = ",a
            del ligne[i]
        #print "la ligne est maintenant",ligne
        i=i+1
        #print "i = ",i
    lignes.append(ligne)    
    k = k+1 

print "Temps de process Etape 1 (s) :", time.time()-timer
timer = time.time()
# Etape 2 on extrait les données (maximum 9 data : trigger time + 4* FE & RE time)
Trig_time = []
RE0_time = []
FE0_time = []
RE1_time = []
FE1_time = []
RE2_time = []
FE2_time = []
RE3_time = []
FE3_time = []
print "Etape 2 : extraction des donnees (maximum 9 data : trigger time + 4* FE & RE time)" 

for i in range(len(lignes)):
    a = lignes[i]
    Trig_time_list = []
    RE0_time_list = []
    FE0_time_list = []
    RE1_time_list = []
    FE1_time_list = []
    RE2_time_list = []
    FE2_time_list = []
    RE3_time_list = []
    FE3_time_list = []
    index_data = 0
    ind_RE0 = 0
    peak0 = 1
    ind_RE1 = 0
    peak1 = 1
    ind_RE2 = 0
    peak2 = 1
    ind_RE3 = 0
    peak3 = 1
    for k in range(len(a)):
        # data 1 Trigger time
        if a[k]!=',' and index_data==0:
            Trig_time_list.append(a[k])
        # The RE0 time    
        elif a[k]!=',' and index_data ==1:
            if (a[k]!='[' and a[k]!=']') and ind_RE0<=1 and peak0==1:
                RE0_time_list.append(a[k])
            elif (a[k]!='[' and a[k]!=']') and ind_RE0<=1 and peak0!=1:
                RE0_time_list.append( a[k])
            elif ind_RE0==1 and a[k]==']':
                RE0_time_list.append('-1')
                FE0_time_list.append('-1')
                index_data = index_data+1
            else:        
                ind_RE0 = ind_RE0+1
        # The FE0 time
        elif a[k]!=',' and index_data ==2 and peak0==1:
            if a[k]!=']':
                FE0_time_list.append(a[k])
        elif a[k]!=',' and index_data ==2 and peak0!=1:
            if a[k]!=']':
                FE0_time_list.append( a[k])
                 
        # Come back to fill RE0 if multiple pulse        
        elif a[k]=='(' and index_data ==3:
            index_data = index_data-2
            ind_RE0 = 0
            peak0 = peak0+1
            # put ; to separate the pulses
            RE0_time_list.append(';') 
            FE0_time_list.append(';') 
        # The RE1 time         
        elif a[k]!=',' and index_data ==3:
            if a[k]!='[' and a[k]!=']' and ind_RE1<=1 and peak1==1:
                RE1_time_list.append(a[k])
            elif (a[k]!='[' and a[k]!=']') and ind_RE1<=1 and peak1!=1:
                RE1_time_list.append(a[k])
            elif ind_RE1==1 and a[k]==']':
                RE1_time_list.append('-1')
                FE1_time_list.append('-1')
                index_data = index_data+1
            else:        
                ind_RE1 = ind_RE1+1
        # The FE1 time
        elif a[k]!=',' and index_data ==4:
            if a[k]!=']':
                FE1_time_list.append(a[k])
        elif a[k]!=',' and index_data ==4 and peak1!=1:
            if a[k]!=']':
                FE1_time_list.append( a[k])
        
        # Come back to fill RE1 if multiple pulse        
        elif a[k]=='(' and index_data ==5:
            index_data = index_data-2
            ind_RE1 = 0   
            peak1 = peak1+1   
            # put ; to separate the pulses
            RE1_time_list.append(';') 
            FE1_time_list.append(';')          
        # The RE2 time         
        elif a[k]!=',' and index_data ==5:
            if a[k]!='[' and a[k]!=']' and ind_RE2<=1 and peak2==1:
                RE2_time_list.append(a[k])
            elif (a[k]!='[' and a[k]!=']') and ind_RE2<=1 and peak2!=1:
                RE2_time_list.append(a[k])
            elif ind_RE2==1 and a[k]==']':
                RE2_time_list.append('-1')
                FE2_time_list.append('-1')
                index_data = index_data+1
            else:        
                ind_RE2 = ind_RE2+1
        # The FE2 time
        elif a[k]!=',' and index_data ==6:
            if a[k]!=']':
                FE2_time_list.append(a[k])
        elif a[k]!=',' and index_data ==6 and peak2!=1:
            if a[k]!=']':
                FE2_time_list.append( a[k])
         
        # Come back to fill RE2 if multiple pulse        
        elif a[k]=='(' and index_data ==7:
            index_data = index_data-2
            ind_RE2 = 0  
            peak2 = peak2+1 
            # put ; to separate the pulses
            RE2_time_list.append(';') 
            FE2_time_list.append(';')          
               
        # The RE3 time         
        elif a[k]!=',' and index_data ==7:
            if a[k]!='[' and a[k]!=']' and ind_RE3<=1 and peak3==1:
                RE3_time_list.append(a[k])
            elif (a[k]!='[' and a[k]!=']') and ind_RE3<=1 and peak3!=1:
                RE3_time_list.append( a[k])
            elif ind_RE3==1 and a[k]==']':
                RE3_time_list.append('-1')
                FE3_time_list.append('-1')
                index_data = index_data+1
            else:        
                ind_RE3 = ind_RE3+1
        # The FE3 time
        elif a[k]!=',' and index_data ==8 and peak3==1:
            if a[k]!=']':
                FE3_time_list.append(a[k])
        elif a[k]!=',' and index_data ==8 and peak3!=1:
            if a[k]!=']':
                FE3_time_list.append( a[k])
        
        # Come back to fill RE3 if multiple pulse        
        elif a[k]=='(' and index_data ==9:
            index_data = index_data-2
            ind_RE3 = 0
            peak3 = peak3+1
            # put ; to separate the pulses
            RE3_time_list.append(';') 
            FE3_time_list.append(';') 
            
        else:
            index_data = index_data+1
            
    Trig_time.append(float(''.join(Trig_time_list)))
    RE0_time.append(''.join(RE0_time_list))
    FE0_time.append(''.join(FE0_time_list))       
    RE1_time.append(''.join(RE1_time_list))
    FE1_time.append(''.join(FE1_time_list))
    RE2_time.append(''.join(RE2_time_list))
    FE2_time.append(''.join(FE2_time_list))
    RE3_time.append(''.join(RE3_time_list))
    FE3_time.append(''.join(FE3_time_list))
#print "la ligne est",RE0_time
print "Temps de process Etape 2 (s) :", time.time()-timer
timer = time.time()
# Etape 3 : On réécrit le fichier en tenant compte des potentiels multipulses/channel
# On va traiter les multipulses de la manière suivante : 
# Si une channel a plusieurs pulses on sépare ces pulses et on les écrit ligne par ligne.
# On a donc qu'un pulse/channel par ligne de fichier mais avec la même date de trigger pour les multipulses

Trig_time_multi = []
RE0_time_multi = []
FE0_time_multi = []
RE1_time_multi = []
FE1_time_multi = []
RE2_time_multi = []
FE2_time_multi = []
RE3_time_multi = []
FE3_time_multi = []
print "Etape 3 : Rearrangement des donnees. On tient compte des multi-pulses"
# Boucle sur tout les événements
for i in range(len(RE0_time)):
    RE0_time_tmp = RE0_time[i]    
    RE1_time_tmp = RE1_time[i]
    RE2_time_tmp = RE2_time[i]
    RE3_time_tmp = RE3_time[i]
    index_peak0 = []
    index_peak1 = []
    index_peak2 = []
    index_peak3 = []
# On sépare les multi pulse RE   
    while RE0_time_tmp.find(';')!=-1:
        i0 = RE0_time_tmp.find(';')
        index_peak0.append(i0)
        RE0_time_tmp = list(RE0_time_tmp)
        RE0_time_tmp[0:i0+1] = []
        RE0_time_tmp = "".join(RE0_time_tmp)
    while RE1_time_tmp.find(';')!=-1:
        i1 = RE1_time_tmp.find(';')
        index_peak1.append(i1)
        RE1_time_tmp = list(RE1_time_tmp)
        RE1_time_tmp[0:i1+1] = []
        RE1_time_tmp = "".join(RE1_time_tmp)
    while RE2_time_tmp.find(';')!=-1:
        i2 = RE2_time_tmp.find(';')
        index_peak2.append(i2)
        RE2_time_tmp = list(RE2_time_tmp)
        RE2_time_tmp[0:i2+1] = []
        RE2_time_tmp = "".join(RE2_time_tmp)
    while RE3_time_tmp.find(';')!=-1:
        i3 = RE3_time_tmp.find(';')
        index_peak3.append(i3)
        RE3_time_tmp = list(RE3_time_tmp)
        RE3_time_tmp[0:i3+1] = []
        RE3_time_tmp = "".join(RE3_time_tmp)
        
    RE0_time_tmp = RE0_time[i]
    RE1_time_tmp = RE1_time[i]
    RE2_time_tmp = RE2_time[i]
    RE3_time_tmp = RE3_time[i]
    if index_peak0 == [] and index_peak1 == [] and index_peak2 == [] and index_peak3 == []:
        Trig_time_multi.append(Trig_time[i])
        RE0_time_multi.append(RE0_time_tmp)
        RE1_time_multi.append(RE1_time_tmp)
        RE2_time_multi.append(RE2_time_tmp)
        RE3_time_multi.append(RE3_time_tmp)
    else:            
        k = max([len(index_peak0),len(index_peak1), len(index_peak2), len(index_peak3)]) # nbre maximum de pic obtenu dans 1 des 4 channel
        ind = 0
        while ind<=k: # boucle sur le nombre max de pic
            
            # si pas de RE0 applique RE0=-1 (default value)
            if RE0_time_tmp == [] and ind==0:
                Trig_time_multi.append(Trig_time[i])
                RE0_time_multi.append(-1)
            
            # si plus de pulse dans CH0 applique RE0=-1
            elif RE0_time_tmp == [] and ind>0:
                Trig_time_multi.append(Trig_time[i])
                RE0_time_multi.append(-1)
            # si 1 seul pulse dans CH0 prend sa valeur et la supprime de la liste 
            # (on appliquera ensuite RE0=-1 s'il y a eu plus de 1 pulse dans les autres channels)  
            elif RE0_time_tmp != [] and index_peak0 == [] and ind==0:
                Trig_time_multi.append(Trig_time[i])
                RE0_time_multi.append(RE0_time_tmp)
                RE0_time_tmp = []
                
            # si plusieurs pulses dans CH0 prend leurs valeurs et les suppriment de la liste 
            # (on appliquera ensuite RE0=-1 s'il y a eu plus de pulses dans les autres channels que CH0)
            elif ind<len(index_peak0):
                Trig_time_multi.append(Trig_time[i])
                RE0_time_tmp = list(RE0_time_tmp)
                RE0_time_multi.append("".join(RE0_time_tmp[0:index_peak0[ind]]))
                RE0_time_tmp[0:index_peak0[ind]+1] = []
                RE0_time_tmp = "".join(RE0_time_tmp)
                
            # si plusieurs pulses dans CH0 prend la dernière valeur restante et la supprime de la liste 
            # (on appliquera ensuite RE0=-1 s'il y a eu plus de 1 pulse dans les autres channel)
            elif RE0_time_tmp != [] and ind==len(index_peak0):
                Trig_time_multi.append(Trig_time[i])
                RE0_time_multi.append(RE0_time_tmp)
                RE0_time_tmp = []
            
            # On applique le même schéma pour CH1 
            if RE1_time_tmp == [] and ind==0:
                RE1_time_multi.append(-1)
                
            elif RE1_time_tmp == [] and ind>0:
                RE1_time_multi.append(-1)
                
            elif RE1_time_tmp != [] and index_peak1 == [] and ind==0:
                RE1_time_multi.append(RE1_time_tmp)
                RE1_time_tmp = []
            elif ind<len(index_peak1):
                RE1_time_tmp = list(RE1_time_tmp)
                RE1_time_multi.append("".join(RE1_time_tmp[0:index_peak1[ind]]))
                RE1_time_tmp[0:index_peak1[ind]+1] = []
                RE1_time_tmp = "".join(RE1_time_tmp)
            
            elif RE1_time_tmp != [] and ind==len(index_peak1):
                RE1_time_multi.append(RE1_time_tmp)
                RE1_time_tmp = []
            
            # On applique le même schéma pour CH2
            if RE2_time_tmp == [] and ind==0:
                RE2_time_multi.append(-1)
                
            elif RE2_time_tmp == [] and ind>0:
                RE2_time_multi.append(-1)
                
            elif RE2_time_tmp != [] and index_peak2 == [] and ind==0:
                RE2_time_multi.append(RE2_time_tmp)
                RE2_time_tmp = []
            elif ind<len(index_peak2):
                RE2_time_tmp = list(RE2_time_tmp)
                RE2_time_multi.append("".join(RE2_time_tmp[0:index_peak2[ind]]))
                RE2_time_tmp[0:index_peak2[ind]+1] = []
                RE2_time_tmp = "".join(RE2_time_tmp)
            
            elif RE2_time_tmp != [] and ind==len(index_peak2):
                RE2_time_multi.append(RE2_time_tmp)
                RE2_time_tmp = []
            
            # On applique le même schéma pour CH3
            if RE3_time_tmp == [] and ind==0:
                RE3_time_multi.append(-1)
                
            elif RE3_time_tmp == [] and ind>0:
                RE3_time_multi.append(-1)
                
            elif RE3_time_tmp != [] and index_peak3 == [] and ind==0:
                RE3_time_multi.append(RE3_time_tmp)
                RE3_time_tmp = []
            elif ind<len(index_peak3):
                RE3_time_tmp = list(RE3_time_tmp)
                RE3_time_multi.append("".join(RE3_time_tmp[0:index_peak3[ind]]))
                RE3_time_tmp[0:index_peak3[ind]+1] = []
                RE3_time_tmp = "".join(RE3_time_tmp)
            
            elif RE3_time_tmp != [] and ind==len(index_peak3):
                RE3_time_multi.append(RE3_time_tmp)
                RE3_time_tmp = []
                
                
            ind = ind+1
            
    # On sépare les multi pulse FE  et on reproduit le même schéma que pour les RE 
    FE0_time_tmp = FE0_time[i]    
    FE1_time_tmp = FE1_time[i]
    FE2_time_tmp = FE2_time[i]
    FE3_time_tmp = FE3_time[i]
    index_peak0 = []
    index_peak1 = []
    index_peak2 = []
    index_peak3 = []
    while FE0_time_tmp.find(';')!=-1:
        i0 = FE0_time_tmp.find(';')
        index_peak0.append(i0)
        FE0_time_tmp = list(FE0_time_tmp)
        FE0_time_tmp[0:i0+1] = []
        FE0_time_tmp = "".join(FE0_time_tmp)
    while FE1_time_tmp.find(';')!=-1:
        i1 = FE1_time_tmp.find(';')
        index_peak1.append(i1)
        FE1_time_tmp = list(FE1_time_tmp)
        FE1_time_tmp[0:i1+1] = []
        FE1_time_tmp = "".join(FE1_time_tmp)
    while FE2_time_tmp.find(';')!=-1:
        i2 = FE2_time_tmp.find(';')
        index_peak2.append(i2)
        FE2_time_tmp = list(FE2_time_tmp)
        FE2_time_tmp[0:i2+1] = []
        FE2_time_tmp = "".join(FE2_time_tmp)
    while FE3_time_tmp.find(';')!=-1:
        i3 = FE3_time_tmp.find(';')
        index_peak3.append(i3)
        FE3_time_tmp = list(FE3_time_tmp)
        FE3_time_tmp[0:i3+1] = []
        FE3_time_tmp = "".join(FE3_time_tmp)
        
    FE0_time_tmp = FE0_time[i]
    FE1_time_tmp = FE1_time[i]
    FE2_time_tmp = FE2_time[i]
    FE3_time_tmp = FE3_time[i]
    if index_peak0 == [] and index_peak1 == [] and index_peak2 == [] and index_peak3 == []:
        FE0_time_multi.append(FE0_time_tmp)
        FE1_time_multi.append(FE1_time_tmp)
        FE2_time_multi.append(FE2_time_tmp)
        FE3_time_multi.append(FE3_time_tmp)
    else:            
        k = max([len(index_peak0),len(index_peak1), len(index_peak2), len(index_peak3)]) # nbre maximum de pic obtenu dans 1 des 4 channel
        ind = 0
        while ind<=k: # boucle sur le nombre max de pic
            
            # si pas de FE0 applique FE0=-1 (default value)
            if FE0_time_tmp == [] and ind==0:
                FE0_time_multi.append(-1)
            
            # si plus de pulse dans CH0 applique FE0=-1
            elif FE0_time_tmp == [] and ind>0:
                FE0_time_multi.append(-1)
            # si 1 seul pulse dans CH0 prend sa valeur et la supprime de la liste 
            # (on appliquera ensuite FE0=-1 s'il y a eu plus de 1 pulse dans les autres channels)  
            elif FE0_time_tmp != [] and index_peak0 == [] and ind==0:
                FE0_time_multi.append(FE0_time_tmp)
                FE0_time_tmp = []
                
            # si plusieurs pulses dans CH0 prend leurs valeurs et les suppriment de la liste 
            # (on appliquera ensuite FE0=-1 s'il y a eu plus de pulses dans les autres channels que CH0)
            elif ind<len(index_peak0):
                FE0_time_tmp = list(FE0_time_tmp)
                FE0_time_multi.append("".join(FE0_time_tmp[0:index_peak0[ind]]))
                FE0_time_tmp[0:index_peak0[ind]+1] = []
                FE0_time_tmp = "".join(FE0_time_tmp)
                
            # si plusieurs pulses dans CH0 prend la dernière valeur restante et la supprime de la liste 
            # (on appliquera ensuite FE0=-1 s'il y a eu plus de 1 pulse dans les autres channel)
            elif FE0_time_tmp != [] and ind==len(index_peak0):
                FE0_time_multi.append(FE0_time_tmp)
                FE0_time_tmp = []
            
            # On applique le même schéma pour CH1 
            if FE1_time_tmp == [] and ind==0:
                FE1_time_multi.append(-1)
                
            elif FE1_time_tmp == [] and ind>0:
                FE1_time_multi.append(-1)
                
            elif FE1_time_tmp != [] and index_peak1 == [] and ind==0:
                FE1_time_multi.append(FE1_time_tmp)
                FE1_time_tmp = []
            elif ind<len(index_peak1):
                FE1_time_tmp = list(FE1_time_tmp)
                FE1_time_multi.append("".join(FE1_time_tmp[0:index_peak1[ind]]))
                FE1_time_tmp[0:index_peak1[ind]+1] = []
                FE1_time_tmp = "".join(FE1_time_tmp)
            
            elif FE1_time_tmp != [] and ind==len(index_peak1):
                FE1_time_multi.append(FE1_time_tmp)
                FE1_time_tmp = []
            
            # On applique le même schéma pour CH2
            if FE2_time_tmp == [] and ind==0:
                FE2_time_multi.append(-1)
                
            elif FE2_time_tmp == [] and ind>0:
                FE2_time_multi.append(-1)
                
            elif FE2_time_tmp != [] and index_peak2 == [] and ind==0:
                FE2_time_multi.append(FE2_time_tmp)
                FE2_time_tmp = []
            elif ind<len(index_peak2):
                FE2_time_tmp = list(FE2_time_tmp)
                FE2_time_multi.append("".join(FE2_time_tmp[0:index_peak2[ind]]))
                FE2_time_tmp[0:index_peak2[ind]+1] = []
                FE2_time_tmp = "".join(FE2_time_tmp)
            
            elif FE2_time_tmp != [] and ind==len(index_peak2):
                FE2_time_multi.append(FE2_time_tmp)
                FE2_time_tmp = []
            
            # On applique le même schéma pour CH3
            if FE3_time_tmp == [] and ind==0:
                FE3_time_multi.append(-1)
                
            elif FE3_time_tmp == [] and ind>0:
                FE3_time_multi.append(-1)
                
            elif FE3_time_tmp != [] and index_peak3 == [] and ind==0:
                FE3_time_multi.append(FE3_time_tmp)
                FE3_time_tmp = []
            elif ind<len(index_peak3):
                FE3_time_tmp = list(FE3_time_tmp)
                FE3_time_multi.append("".join(FE3_time_tmp[0:index_peak3[ind]]))
                FE3_time_tmp[0:index_peak3[ind]+1] = []
                FE3_time_tmp = "".join(FE3_time_tmp)
            
            elif FE3_time_tmp != [] and ind==len(index_peak3):
                FE3_time_multi.append(FE3_time_tmp)
                FE3_time_tmp = []
                
                
            ind = ind+1
print "Temps de process Etape 3 (s) :", time.time()-timer
                
# Etape 4 : On calcule la largeur de chaque pulse 
Pulse_Width0 = []
Pulse_Width1 = []
Pulse_Width2 = []
Pulse_Width3 = []
print "Etape 4 : Calcul de la largeur de chaque pulse"
for i in range(len(Trig_time_multi)):
    Pulse_Width0.append(float(FE0_time_multi[i])-float(RE0_time_multi[i]))
    Pulse_Width1.append(float(FE1_time_multi[i])-float(RE1_time_multi[i]))          
    Pulse_Width2.append(float(FE2_time_multi[i])-float(RE2_time_multi[i]))
    Pulse_Width3.append(float(FE3_time_multi[i])-float(RE3_time_multi[i]))

print "Temps de process Etape 4 (s) :", time.time()-timer
timer = time.time()
# Etape 5 : On modifie la colonne Trigger time pour avoir des dates absolues en JD 
print "Etape 5 : Calcul des Trigger time en Jour Julien JD2000"
date_start = date_to_jd(int(YYYY),int(MM),int(DD))
Time_JD = []
k = 0
for i in range(len(Trig_time_multi)-1):
    if Trig_time_multi[i+1]+1000<=Trig_time_multi[i]:
        date_start = date_start+1
        Time_JD.append(date_start+Trig_time_multi[i]/86400)
        k = k+1
    else:
        Time_JD.append(date_start+Trig_time_multi[i]/86400)

print "Temps de process Etape 5 (s) :", time.time()-timer
# Etape 6 : Ecriture du fichier ASCII facilement déchiffrable par n'importe quel soft
timer = time.time()
print "Etape 6 : Reecriture des donnees dans un fichier PulseYYYYMMDD_Q#.txt."

fichier1=open('Data_'+carte+'/'+date_file+'/Pulse'+YYYY+MM+DD+'_'+carte+'.txt','w')
fichier1.write("Time (JD2000)"+"\t"+"RE0_time (ns)"+"\t"+"FE0_time (ns)"+"\t"+"RE1_time (ns)"+"\t"+"FE1_time (ns)"+"\t"+"RE2_time (ns)"+"\t"+"FE2_time (ns)"+
               "\t"+"RE3_time (ns)"+"\t"+"FE3_time (ns)"+"\n"+"Pulse_Width0 (ns)"+"\t"+"Pulse_Width1 (ns)"+"\t"+"Pulse_Width2 (ns)"+"\t"+"Pulse_Width3 (ns)"+"\t"+"QN card"+"\n")
for i in range(len(Time_JD)) :
    fichier1.write(str('{:.20}'.format(Time_JD[i]))+"\t"+str(RE0_time_multi[i])+"\t"+str(FE0_time_multi[i])+"\t"+str(RE1_time_multi[i])+"\t"+str(FE1_time_multi[i])+
                 "\t"+str(RE2_time_multi[i])+"\t"+str(FE2_time_multi[i])+"\t"+str(RE3_time_multi[i])+"\t"+str(FE3_time_multi[i])+"\t"+str(Pulse_Width0[i])+"\t"+
                 str(Pulse_Width1[i])+"\t"+str(Pulse_Width2[i])+"\t"+str(Pulse_Width3[i])+"\t"+carte+"\n") 
    #fichier1.write(str(Trig_time_multi[i])+"\t"+str(RE0_time_multi[i])+str(FE0_time_multi[i])+"\n") 
fichier1.close()

print "Temps de process Etape 6 (s) :", time.time()-timer
print "Fin de traitement fichier"
end = time.time()
print "temp total = {0:.2f} s".format(end-start)

