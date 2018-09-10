# -*- coding: iso-8859-1 -*-
"""
recup_pulse.py
version : 2.0
author : arturo.nunez@lam.fr
for the E-Peron project
a bit faster 
incorporated Etapes 1,2,3 -> Etape 1 now
generalized reading of data file
for now only accounts for double coincidence
but in a generel manner for the 2 to 4fold 
distributions
note: ignoring tripel concidences for now
Sorry for the bilingual comments.
"""
import time
start = time.time()
import os
import sys
import numpy as np
import StringIO
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
###########################################################################
#                                 some functions 
############################################################################



def lineread(l):
    """
    read line by line and in case of
    double peak in line reprints  peaks from 
    other channel with the second peak
    * if nothing in channel prints -1 for 
    both, rising and falling time.
    * igonres triple peak (for now)
    * ignores double-double peak (for now)

    input = cleaned line from DAQ file no '[',']','(' or ')'
            should be in line, only comma separated values
    output = line with following format
             t,R_ch0,F_ch0,R_ch1,F_ch1,R_ch2,F_ch2,R_ch3,F_ch3
             prints -1,-1 if channel is not present

    """
    row = l.split(',')
    doublePeak = -1
    if row[2]!='':CH0 = row[2]+','+row[3]
    else: CH0 = '-1,-1'

    if  len(row)==17:#one peak each
        if row[6]=='':ch1=False
        if row[10]=='':ch2=False
        if row[14]=='':ch3=False
        
        if row[6]!='':CH1 = row[6]+','+row[7]
        else: CH1 = '-1,-1'
        if row[10]!='':CH2 = row[10]+','+row[11]
        else: CH2 = '-1,-1'
        if row[14]!='':CH3 = row[14]+','+row[15]
        else: CH3 = '-1,-1'
        line = row[0]+','+CH0+','+CH1+','+CH2+','+CH3
        return line
    elif len(row)==19:#one with two peaks
        if row[10]==row[14]:
            #2peak either in CH0 or in CH1
            if row[12]!='':CH2 = row[12]+','+row[13]
            else: CH2 = '-1,-1'
            if row[16]!='':CH3 = row[16]+','+row[17]
            else: CH3 = '-1,-1'
            if row[4]==row[10]:
                #2peak in CH1
                doublePeak = 1
                if row[6]!='':CH1 = row[6]+','+row[7]
                else: CH1 = '-1,-1'
                extraCH = row[8]+','+row[9]
            elif row[6]==row[10]:
                #peak in CH0
                doublePeak = 0
                if row[8]!='':CH1 = row[8]+','+row[8]
                else: CH1 = '-1,-1'
                extraCH = row[4]+','+row[5]
        elif row[4]==row[8]:
            #2peak either in CH2 or in CH3
            if row[6]!='':CH1 = row[6]+','+row[7]
            else: CH1 = '-1,-1'
            if row[10]!='':CH2 = row[10]+','+row[11]
            else: CH2 = '-1,-1'
            if row[8]==row[14]:
                #2peak in CH2
                doublePeak = 2
                if row[16]!='':CH3 = row[16]+','+row[17]
                else: CH3 = '-1,-1'
                extraCH = row[12]+','+row[13]
            elif row[8]==row[12]:
                #peak in CH3
                doublePeak = 3
                if row[14]!='':CH3 = row[14]+','+row[15]
                else: CH3 = '-1,-1'
                extraCH = row[16]+','+row[17]
        line = row[0]+','+CH0+','+CH1+','+CH2+','+CH3
        if doublePeak==0:
            line +=" \n"+row[0]+','+extraCH+','+CH1+','+CH2+','+CH3
        if doublePeak==1:
            line +=" \n"+row[0]+','+CH0+','+extraCH+','+CH2+','+CH3
        if doublePeak==2:
            line +=" \n"+row[0]+','+CH0+','+CH1+','+extraCH+','+CH3
        if doublePeak==0:
            line +=" \n"+row[0]+','+CH0+','+CH1+','+CH2+','+extraCH
        return line 
    else:return 0


###########################################################################
#                                main sequence 
############################################################################



#########################################################################
print "Etape 1 : nettoyage des donnees"
timer = time.time()
now = time.time()
# massive cleaning of file to make it into a csv-ish file
rawtable = open(table1).read().replace('(','') # eliminates '(' characteres
rawtable = rawtable.replace(')','') # eliminates ')' characteres
rawtable = rawtable.replace('[]',',,,') # changes '[' to '-' will be useful
rawtable = rawtable.replace('[',',') # changes '[' to ','
rawtable = rawtable.replace(']',',') # changes ']' to ','
# now creates clean data array
bylines  = (str(StringIO.StringIO(rawtable).getvalue()) ).split('\n') 
Trig_t= RE0_t= FE0_t= RE1_t= FE1_t= RE2_t= FE2_t= RE3_t= FE3_t = np.array([])
index = 0
ch0 = ch1 = ch2 = ch3 = True
# now we iterate over the file and print clean data in a tmp file
output_file = open('clean.tmp','w')
for l in bylines:
    if len(l)<40:continue
    line = lineread(l)
    if line!=0:
        output_file.write(line+' \n')
output_file.close()    

###################################################
end = time.time()                                 #
print "temp de nettoyage = {0:.2f} s".format(end-now)     #
now = end
###################################################
# read tmp data file and builds previous data structure
filein = np.loadtxt("clean.tmp",delimiter=',')
Trig_t, RE0_t, FE0_t, RE1_t, FE1_t  = filein[:,0], filein[:,1], filein[:,2], filein[:,3], filein[:,4]
RE2_t, FE2_t, RE3_t, FE3_t  = filein[:,5], filein[:,6], filein[:,7], filein[:,8]
os.system("rm clean.tmp")

Trig_time_multi = Trig_t
RE0_time_multi = RE0_t
FE0_time_multi = FE0_t
RE1_time_multi = RE1_t
FE1_time_multi = FE1_t
RE2_time_multi = RE2_t
FE2_time_multi = FE2_t
RE3_time_multi = RE3_t
FE3_time_multi = FE3_t
####################################################################################
#from now on is the same file as in V1
####################################################################################
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
