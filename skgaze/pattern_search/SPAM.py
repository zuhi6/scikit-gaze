from collections import defaultdict
from skgaze.core.Dataset import Dataset
import os
import math

class SPAM:


    def __init__(self, dataset):
        self.raw_sequences = dataset.create_raw_sequences()
        self.listOfAois = self.simplify_aoi_array(dataset.aoi_array)
        self.listOfScanpaths = self.create_list_of_scanpaths(dataset)
        self.result = []

   
    def simplify_aoi_array(self, aoi_array):
        spam_aoi_array = []
        for aoi in aoi_array:
        	spam_aoi_array.append(aoi.aoi_char)
        return spam_aoi_array

    def create_list_of_scanpaths(self,dataset):
        result = []
        for participant in dataset.participants:
            result.append(participant.scanpath)
        return result


    def runSpam(self, minsup_percenta=0.5, minlength=1, maxlength=4, maxgap=1):
    
        dlzkasekvencii = []
        dlzkasuboru = 0
        SPAM.pocet_najdenych_vzorov = 0

        supportnumb = 0
        sid = 0  # id participanta
        tid = 0  # id AOI
        verticalDB = {}
        supportDB = {}
       
        # Krok 1 ulozime si poziciu prvej AOI kazdej sekvencie pohladu, a zaroven aj poslednu poslednej AOI
    
        for line in range(0,len(self.listOfScanpaths)):
            dlzkasekvencii.append(dlzkasuboru)
            for i in self.listOfScanpaths[line]:
                dlzkasuboru += 1
            #dlzkasekvencii.append(dlzkasuboru)
            #for ch in line:
            #    if ((ch >= 'A') and (ch <= 'Z')):
            #        dlzkasuboru += 1
        dlzkasekvencii.append(dlzkasuboru)  # ulozime si aj poziciu posledneho bitu
  


        #Krok 2 vypocitame si minsup
        minsup = math.ceil(float(minsup_percenta) * (len(dlzkasekvencii)-1))
        if minsup == 0:
            minsup = 1

        #Krok 3
        #vytvorime vertikalnu reprezentaciu databazy
        #ukladame poziciu kazdej AOI a poradie sekvencie kazdej AOI priradime
        #bitmapu (ak taka AOI este neexistuje, vytvorime ju a vlozime do vertikalnej reprezentacie databazy)
        #nasledne musime nastavit bit na 1 na takej pozicii v bitmape, v ktorej sa AOI vyskytuje

  
        for line in range(0,len(self.listOfScanpaths)):
            for i in self.listOfScanpaths[line]:
                if i[0] not in verticalDB:
                    
                    verticalDB[i[0]] = [0] * dlzkasekvencii[-1]
                    supportDB[i[0]] = 0
                verticalDB[i[0]][dlzkasekvencii[sid] + tid] = 1
                tid += 1
            tid = 0
            sid += 1    #posun na dalsi riadok/participanta
        sid -= 1
        #{'A': [1, 0, 0, 1, 0, 0...], 'B': [0, 1, 0, 0, 0, 0...], 'C': [0, 0, 1, 0, 1, 1...]}

        #Krok 4 zistime support jednotlivych oblasti zaujmu
        for i in verticalDB:
            for j in range(sid+1):
                for k in range(0, (dlzkasekvencii[j+1] - dlzkasekvencii[j])):
                    if verticalDB[i][dlzkasekvencii[j]+k] is 1:
                        supportnumb += 1
                        supportDB[i] = supportnumb
                        break
            supportnumb = 0

        #Krok 5
        #Ulozime si vzory, ktore sa nachadzaju vo viacerych sekvenciach ako je minsup
        frequentItems = []
        
        for i in supportDB:
            if int(supportDB.get(i)) >= int(minsup):
                if (int(minlength) <= 1) and (int(maxlength) >= 1):
                    #print('[\'',i,'\']', "support", supportDB[i])
                    SPAM.pocet_najdenych_vzorov += 1
                    self.result.append([SPAM.pocet_najdenych_vzorov, i, supportDB[i]])
                frequentItems.append(i)

        if (maxlength == 1):
            return
        #Krok 6
        #vyhladavanie do hlbky s vykonanim S-Step
        for i in verticalDB:
            prefix = []
            prefix.append(i)
            self.dfsPruning(prefix, verticalDB[i], frequentItems, 2, minsup, minlength, maxlength, dlzkasekvencii,
                             maxgap, verticalDB)

        return self.result
    supportWithoutGapTotal = 0
    

    #s_n = iba vzory, ktore vieme, ze sa budu urcite vyskytovat v najcastejsich vzoroch = frequentitems
    def dfsPruning(self,prefix, bitmap_prefix, s_n, m, minsup, minlength, maxlength, dlzkasekvencii,
                   maxgap, verticalDB):
        sTemp = []
        sTempBitmaps = {}
        supportDB2 = {}     ##ukladame si support prvkov

        for i in s_n:
            newBitmap = self.newBitmap(bitmap_prefix, dlzkasekvencii, maxgap, verticalDB[i])
            if (SPAM.supportWithoutGapTotal >= minsup):
                sTemp.append(i)
                sTempBitmaps[i] = newBitmap
                supportDB2[i] = SPAM.supportOfItem

            SPAM.supportWithoutGapTotal = 0
            SPAM.supportOfItem = 0

        for j in range(0, len(sTemp)):
            item = sTemp[j]

            prefixSStep = self.cloneSequence(prefix)
            prefixSStep.append(item)

            newBitmap = sTempBitmaps[sTemp[j]]
            if (supportDB2[item] >= minsup):
                if (m >= int(minlength)):
                    #print(prefixSStep, "support", supportDB2[item])
                    SPAM.pocet_najdenych_vzorov += 1
                    self.result.append([SPAM.pocet_najdenych_vzorov, prefixSStep, supportDB2[item]])
                if (int(maxlength) > m):
                    self.dfsPruning(prefixSStep, newBitmap, sTemp, m+1, minsup, minlength, maxlength, dlzkasekvencii,
                                    maxgap, verticalDB)

    #global parameters
    lastSID = -1
    supportOfItem = 0
    # SavePaterns
    pocet_najdenych_vzorov = 0
    najdeneVzory = {}

    def cloneSequence(self, items):
        sequence = []
        for i in items:
            sequence.append(i)
        return sequence

    #bitmapa_pismena = toho pismena, ktore sa vola v kroku 6; pri rekurzivnom volani je to novovzniknuta bitmapa
    #pismeno = bitmapa toho pismena, ktore sa prave nachadza v cykle frekventovanych AOI

    def newBitmap(self, bitmap_prefix, dlzkasekvencii, maxgap, pismeno):
        newBitmap = [0] * dlzkasekvencii[-1]
        #sid poslednej sekvencie, vlozenej do bitmapy, ktory obsahuje 1
        SPAM.lastSID = -1
        k = 0
        premenna = True
        #ak je maxgap 0, tak hladame spolocne vzory, ktore mozu mat medzi sebou lubovolne velku vzdialenost
        if int(maxgap) == 0:
            bitK = bitmap_prefix.index(1, k, dlzkasekvencii[-1])
            while True:
                sid = self.bitToSid(bitK, dlzkasekvencii)
                lastBitofSid = dlzkasekvencii.__getitem__(sid+1) - 1
                match = False
                if 1 not in pismeno[bitK+1:]:
                    premenna = False
                else:
                    bit = pismeno.index(1, bitK + 1, dlzkasekvencii[-1])

                while premenna and (bit <= lastBitofSid):
                    newBitmap[bit] = 1
                    match = True
                    if (1 not in pismeno[bit+1:]):
                        break
                    bit = pismeno.index(1, bit + 1, dlzkasekvencii[-1])

                if match == True:
                    if (sid != SPAM.lastSID):
                        SPAM.supportWithoutGapTotal += 1
                        SPAM.supportOfItem += 1
                        SPAM.lastSID = sid

                k = bitK + 1
                if 1 not in bitmap_prefix[k:]:
                    break
                else:
                    bitK = bitmap_prefix.index(1, k, dlzkasekvencii[-1])

        #ak je gap medzi AOI ziadna a vacsia
        else:
            previousSid = -1
            bitK = bitmap_prefix.index(1, k, dlzkasekvencii[-1])

            #AND medzi bitmapy (bitmap_prefix a pimeno)
            while True:
                sid = self.bitToSid(bitK, dlzkasekvencii)
                lastBitofSid = dlzkasekvencii.__getitem__(sid + 1) - 1
                match = False
                matchWithoutGap = False

                if 1 not in pismeno[bitK+1:]:
                    premenna = False
                else:
                    bit = pismeno.index(1, bitK + 1, dlzkasekvencii[-1])

                #jedtnotkovy bit sa nachadza este stale v tej istej sid (sekvencie pohladu),
                #ak nie, preskocim a idem na dalsiu sekvenciu
                while premenna and (bit <= lastBitofSid):
                    matchWithoutGap = True

                    if (bit - bitK > int(maxgap)):
                        break

                    newBitmap[bit] = 1
                    match = True
                    if (1 not in pismeno[bit+1:]):
                        break
                    #vyuzitie pri ak je maxgap > 1
                    bit = pismeno.index(1, bit + 1, dlzkasekvencii[-1])

                if matchWithoutGap and previousSid!= sid:
                    SPAM.supportWithoutGapTotal += 1
                    previousSid = sid

                if match == True:
                    #++support ak je to iny participant
                    if (sid != SPAM.lastSID):
                        SPAM.supportOfItem += 1
                    SPAM.lastSID = sid

                #Vyhladanie dalsieho najblizsie bitu v bitmape, nastaveneho na 1, ak taky neexistuje, koncime
                k = bitK + 1
                if 1 not in bitmap_prefix[k:]:
                    break
                else:
                    bitK = bitmap_prefix.index(1, k, dlzkasekvencii[-1])

        return newBitmap

    #SavePaterns
    pocet_najdenych_vzorov = 0
    najdeneVzory = {}

    def bitToSid(self, bitK, dlzkasekvencii):
        for i in range(1, len(dlzkasekvencii)):
            if bitK < dlzkasekvencii[i]:
                return i-1
        return i

    #Save patterns of length 1 to file