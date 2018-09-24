





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
    ### print len(row),row
    doublePeak =  -1
    doubleDPeak = [-1,-1]
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
    elif len(row)==21:
        # two with two peaks
        # or one with three
        if row[18]!='':CH3 = row[18]+','+row[19]
        else:CH3 = '-1,-1'
        if row[7]==' ':
            # two double peaks
            extraCH_1 = row[4]+','+row[5]
            if row[8]!='':CH1 = row[8]+','+row[9]
            else:CH1 = '-1,-1'
            if row[13]==' ':
                # CH0, CH1
                doubleDpeak = [0,1]
                extraCH_2 = row[10]+','+row[11]
                if row[14]!='':CH2 = row[14]+','+row[15]
                else:CH2 = '-1,-1'
                # line is al possible combinations of coincidences
                line = row[0]+','+CH0+','+CH1+','+CH2+','+CH3
                line +=" \n"+ row[0]+','+extraCH_1+','+CH1+','+CH2+','+CH3
                line +=" \n"+ row[0]+','+CH0+','+extraCH_2+','+CH2+','+CH3
                line +=" \n"+ row[0]+','+extraCH_1+','+extraCH_2+','+CH2+','+CH3
            elif row[17]==' ':
                if row[12]!='':CH2 = row[12]+','+row[13]
                else:CH2 = '-1,-1'
                # CH0, CH2
                extraCH_2 = row[14]+','+row[15]
                # line is al possible combinations of coincidences
                line = row[0]+','+CH0+','+CH1+','+CH2+','+CH3
                line +=" \n"+ row[0]+','+extraCH_1+','+CH1+','+CH2+','+CH3
                line +=" \n"+ row[0]+','+CH0+','+CH1+','+extraCH_2+','+CH3
                line +=" \n"+ row[0]+','+extraCH_1+','+CH1+','+extraCH_2+','+CH3
            elif row[15]==' ':
                if row[12]!='':CH2 = row[12]+','+row[13]
                else:CH2 = '-1,-1'
                # CH0, CH3
                extraCH_2 = row[16]+','+row[17]
                # line is al possible combinations of coincidences
                line = row[0]+','+CH0+','+CH1+','+CH2+','+CH3
                line +=" \n"+ row[0]+','+extraCH_1+','+CH1+','+CH2+','+CH3
                line +=" \n"+ row[0]+','+CH0+','+CH1+','+CH2+','+extraCH_2
                line +=" \n"+ row[0]+','+extraCH_1+','+CH1+','+CH2+','+extraCH_2
        elif row[5]==' ':
            # three double peaks
            # three triple peak
            if row[6]!='':CH1 = row[6]+','+row[7]
            else:CH1 = '-1,-1'
            if row[11]==' ':
                extraCH_1 = row[8]+','+row[9]
                if row[6]!='':CH2 = row[6]+','+row[7]
                else:CH2 = '-1,-1'
                if row[17]==' ':
                    # doubles in
                    # CH1 CH2
                    extraCH_2 = row[14]+','+row[15]
                    # line is al possible combinations of coincidences
                    line = row[0]+','+CH0+','+CH1+','+CH2+','+CH3
                    line +=" \n"+ row[0]+','+CH0+','+extraCH_1+','+CH2+','+CH3
                    line +=" \n"+ row[0]+','+CH0+','+CH1+','+extraCH_2+','+CH3
                    line +=" \n"+ row[0]+','+CH0+','+extraCH_1+','+extraCH_2+','+CH3
                if row[15]==' ':
                    # doubles in
                    # CH1 CH3
                    extraCH_2 = row[16]+','+row[17]
                    # line is al possible combinations of coincidences
                    line = row[0]+','+CH0+','+CH1+','+CH2+','+CH3
                    line +=" \n"+ row[0]+','+CH0+','+extraCH_1+','+CH2+','+CH3
                    line +=" \n"+ row[0]+','+CH0+','+CH1+','+CH2+','+extraCH_2
                    line +=" \n"+ row[0]+','+CH0+','+extraCH_1+','+CH2+','+extraCH_2
            elif row[9]==' ':
                if row[10]!='':CH2 = row[10]+','+row[11]
                else:CH2 = '-1,-1'
                if row[15]==' ':
                    # doubles in
                    # CH2 CH3
                    extraCH_1 = row[12]+','+row[13]
                    extraCH_2 = row[16]+','+row[17]
                    # line is al possible combinations of coincidences
                    line = row[0]+','+CH0+','+CH1+','+CH2+','+CH3
                    line +=" \n"+ row[0]+','+CH0+','+CH1+','+extraCH_1+','+CH3
                    line +=" \n"+ row[0]+','+CH0+','+CH1+','+CH2+','+extraCH_2
                    line +=" \n"+ row[0]+','+CH0+','+CH1+','+extraCH_1+','+extraCH_2
                # now Triples
                elif row[17]==' ':
                    # triple in CH2
                    extraCH_1 = row[12]+','+row[13]
                    extraCH_2 = row[14]+','+row[15]
                    # line is al possible combinations of coincidences
                    line = row[0]+','+CH0+','+CH1+','+CH2+','+CH3
                    line +=" \n"+ row[0]+','+CH0+','+CH1+','+extraCH_1+','+CH3
                    line +=" \n"+ row[0]+','+CH0+','+CH1+','+extraCH_2+','+CH3
                elif row[13]==' ':
                    # triple in CH3
                    extraCH_1 = row[16]+','+row[17]
                    extraCH_2 = row[14]+','+row[15]
                    # line is al possible combinations of coincidences
                    line = row[0]+','+CH0+','+CH1+','+CH2+','+CH3
                    line +=" \n"+ row[0]+','+CH0+','+CH1+','+CH2+','+extraCH_1
                    line +=" \n"+ row[0]+','+CH0+','+CH1+','+CH2+','+extraCH_2
            elif row[13]==' ':
                if row[14]!='':CH2 = row[14]+','+row[15]
                else:CH2 = '-1,-1'
                # triple in CH1
                extraCH_1 = row[8]+','+row[9]
                extraCH_2 = row[10]+','+row[11]
                # line is al possible combinations of coincidences
                line = row[0]+','+CH0+','+CH1+','+CH2+','+CH3
                line +=" \n"+ row[0]+','+CH0+','+extraCH_1+','+CH2+','+CH3
                line +=" \n"+ row[0]+','+CH0+','+extraCH_2+','+CH2+','+CH3
        elif row[9]==' ':
            # triple in CH0
            if row[10]!='':CH1 = row[10]+','+row[11]
            else:CH1 = '-1,-1'
            if row[14]!='':CH2 = row[14]+','+row[15]
            else:CH2 = '-1,-1'
            extraCH_1 = row[4]+','+row[5]
            extraCH_2 = row[6]+','+row[7]
            # line is al possible combinations of coincidences
            line = row[0]+','+CH0+','+CH1+','+CH2+','+CH3
            line += " \n"+ row[0]+','+extraCH_1+','+CH1+','+CH2+','+CH3
            line += " \n"+ row[0]+','+extraCH_2+','+CH1+','+CH2+','+CH3
            #print len(row),row
        return line
    else:return 0


