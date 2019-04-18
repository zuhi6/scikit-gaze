from src.similarity_algorithms import similarity	

class STA:
    
    def __init__(self, dataset):
        self.raw_sequences = dataset.create_raw_sequences()
        self.aoi_data = self.create_aoi_array(dataset.aoi_array)

    def create_aoi_array(self, aoi_array):
    	sta_aoi_array = []
    	for aoi in aoi_array:
        	sta_aoi_array.append([aoi.type_of_element,float(aoi.x),float(aoi.width),float(aoi.y),float(aoi.height),aoi.aoi_char])
    	return sta_aoi_array

    def getNumberedSequence(self, Sequence, aoi_data):
	    numberedSequence = []
	    numberedSequence.append([Sequence[0][0], 1, Sequence[0][1]])
	
	    for y in range(1, len(Sequence)):
	        if Sequence[y][0] == Sequence[y - 1][0]:
	            numberedSequence.append([Sequence[y][0], numberedSequence[len(numberedSequence) - 1][1], Sequence[y][1]])
	        else:
	            numberedSequence.append([Sequence[y][0], self.getSequenceNumber(Sequence[0:y], Sequence[y][0]), Sequence[y][1]])
	
	    AoIList = self.getExistingAoIListForSequence(numberedSequence)
	    AoINames = aoi_data
	    AoINames = [w[5] for w in AoINames]
	    newSequence = []
	
	    myList = []
	    myDictionary = {}
	    replacementList = []
	
	    for x in range(0, len(AoIList)):
	        totalDuration = 0
	        for y in range(0, len(numberedSequence)):
	            if numberedSequence[y][0:2] == AoIList[x]:
	                totalDuration = totalDuration + int(numberedSequence[y][2])
	        myList.append([AoIList[x], totalDuration])
	
	    for x in range(0, len(AoINames)):
	        myAoIList = [w for w in myList if w[0][0] == AoINames[x]]
	        myAoIList.sort(key=lambda x: x[1])
	        myAoIList.reverse()
	        if len(myAoIList) > 0:
	            myDictionary[AoINames[x]] = myAoIList
	
	    for AoI in AoIList:
	        index = [w[0] for w in myDictionary[AoI[0]]].index(AoI)
	        replacementList.append([AoI, [AoI[0], (index + 1)]])
	
	    for x in range(0, len(numberedSequence)):
	        myReplacementList = [w[0] for w in replacementList]
	        index = myReplacementList.index(numberedSequence[x][0:2])
	        newSequence.append([replacementList[index][1][0]] + [replacementList[index][1][1]] + [numberedSequence[x][2]])
	
	    return newSequence
	
	
    def getSequenceNumber(self,Sequence, Item):
	    abstractedSequence = self.getAbstractedSequence(Sequence)
	    return abstractedSequence.count(Item) + 1
	
	
    def getAbstractedSequence(self,Sequence):
	    myAbstractedSequence = [Sequence[0]]
	    for y in range(1, len(Sequence)):
	        if myAbstractedSequence[len(myAbstractedSequence) - 1] != Sequence[y][0]:
	            myAbstractedSequence.append([Sequence[y][0], Sequence[y][1]])
	    return myAbstractedSequence
	
	
    def getExistingAoIListForSequence(self,Sequence):
	    AoIlist = []
	    for x in range(0, len(Sequence)):
	        try:
	            AoIlist.index(Sequence[x][0:2])
	        except:
	            AoIlist.append(Sequence[x][0:2])
	    return AoIlist
	
	
    def calculateImportanceThreshold(self,mySequences):
	    myAoICounter = self.getNumberDurationOfAoIs(mySequences)
	    commonAoIs = []
	    for myAoIdetail in myAoICounter:
	        if myAoIdetail[3] == True:
	            commonAoIs.append(myAoIdetail)
	
	    if len(commonAoIs) == 0:
	        print("No shared instances!")
	        exit(1)
	
	    minValueCounter = commonAoIs[0][1]
	    for AoIdetails in commonAoIs:
	        if minValueCounter > AoIdetails[1]:
	            minValueCounter = AoIdetails[1]
	
	    minValueDuration = commonAoIs[0][2]
	    for AoIdetails in commonAoIs:
	        if minValueDuration > AoIdetails[2]:
	            minValueDuration = AoIdetails[2]
	
	    return [minValueCounter, minValueDuration]
	
	
    def getNumberDurationOfAoIs(self,Sequences):
	    AoIs = self.getExistingAoIList(Sequences)
	    AoIcount = []
	    for x in range(0, len(AoIs)):
	        counter = 0
	        duration = 0
	        flagCounter = 0
	        keys = list(Sequences.keys())
	        for y in range(0, len(keys)):
	            if [s[0:2] for s in Sequences[keys[y]]].count(AoIs[x]) > 0:
	                counter = counter + [s[0:2] for s in Sequences[keys[y]]].count(AoIs[x])
	                duration = duration + sum([int(w[2]) for w in Sequences[keys[y]] if w[0:2] == AoIs[x]])
	                flagCounter = flagCounter + 1
	
	        if flagCounter > len(keys) / 2:
	            AoIcount.append([AoIs[x], counter, duration, True])
	        else:
	            AoIcount.append([AoIs[x], counter, duration, False])
	    return AoIcount
	
	
    def updateAoIsFlag(self, AoIs, threshold):
	    for AoI in AoIs:
	        if AoI[1] >= threshold[0] and AoI[2] >= threshold[1]:
	            AoI[3] = True
	    return AoIs
	
	
    def removeInsignificantAoIs(self, Sequences, AoIList):
	    significantAoIs = []
	    for AoI in AoIList:
	        if AoI[3] == True:
	            significantAoIs.append(AoI[0])
	
	    keys = list(Sequences.keys())
	    for y in range(0, len(keys)):
	        temp = []
	        for k in range(0, len(Sequences[keys[y]])):
	            try:
	                significantAoIs.index(Sequences[keys[y]][k][0:2])
	                temp.append(Sequences[keys[y]][k])
	            except:
	                continue
	        # Fix for scanpaths consisting only from insignificant aois - remove such scanpaths
	        if len(temp) > 0:
	            Sequences[keys[y]] = temp
	        else:
	            Sequences.pop(keys[y], None)
	    return Sequences
	
	
    def getExistingAoIList(self, Sequences):
	    AoIlist = []
	    keys = list(Sequences.keys())
	    for y in range(0, len(keys)):
	        for x in range(0, len(Sequences[keys[y]])):
	            try:
	                AoIlist.index(Sequences[keys[y]][x][0:2])
	            except:
	                AoIlist.append(Sequences[keys[y]][x][0:2])
	    return AoIlist
	
	
    def calculateNumberDurationOfFixationsAndNSV(self, Sequences):
	    keys = list(Sequences.keys())
	    for x in range(0, len(keys)):
	        myAbstractedSequence = []
	        myAbstractedSequence = [Sequences[keys[x]][0][0:2] + [1] + [int(Sequences[keys[x]][0][2])]]
	        for y in range(1, len(Sequences[keys[x]])):
	            if myAbstractedSequence[len(myAbstractedSequence) - 1][0:2] != Sequences[keys[x]][y][0:2]:
	                myAbstractedSequence.append(Sequences[keys[x]][y][0:2] + [1] + [int(Sequences[keys[x]][y][2])])
	            else:
	                myAbstractedSequence[len(myAbstractedSequence) - 1][2] = \
	                myAbstractedSequence[len(myAbstractedSequence) - 1][2] + 1
	                myAbstractedSequence[len(myAbstractedSequence) - 1][3] = \
	                myAbstractedSequence[len(myAbstractedSequence) - 1][3] + int(Sequences[keys[x]][y][2])
	
	        Sequences[keys[x]] = myAbstractedSequence
	
	    keys = list(Sequences.keys())
	
	    for x in range(0, len(keys)):
	        for y in range(0, len(Sequences[keys[x]])):
	            if len(Sequences[keys[x]]) < 2:
	                value = 0
	            else:
	                value = 0.9 / (len(Sequences[keys[x]]) - 1)
	            NSV = 1 - round(y, 2) * value
	            Sequences[keys[x]][y] = Sequences[keys[x]][y] + [NSV]
	    return Sequences
	
	
    def calculateTotalNumberDurationofFixationsandNSV(self, AoIList, Sequences):
	    for x in range(0, len(AoIList)):
	        duration = 0
	        counter = 0
	        totalNSV = 0
	
	        flag = 0
	        keys = list(Sequences.keys())
	        for y in range(0, len(keys)):
	            for k in range(0, len(Sequences[keys[y]])):
	                if Sequences[keys[y]][k][0:2] == AoIList[x]:
	                    counter += Sequences[keys[y]][k][2]
	                    duration += Sequences[keys[y]][k][3]
	                    totalNSV += Sequences[keys[y]][k][4]
	                    flag += 1
	        if flag == len(Sequences):
	            AoIList[x] = AoIList[x] + [counter] + [duration] + [totalNSV] + [True]
	        else:
	            AoIList[x] = AoIList[x] + [counter] + [duration] + [totalNSV] + [False]
	
	    return AoIList
	
	
    def getValueableAoIs(self, AoIList):
	    commonAoIs = []
	    valuableAoIs = []
	    for myAoIdetail in AoIList:
	        if myAoIdetail[5] == True:
	            commonAoIs.append(myAoIdetail)
	
	    minValue = commonAoIs[0][4] if len(commonAoIs) > 0 else 0
	    for AoIdetails in commonAoIs:
	        if minValue > AoIdetails[4]:
	            minValue = AoIdetails[4]
	
	    for myAoIdetail in AoIList:
	        if myAoIdetail[4] >= minValue:
	            valuableAoIs.append(myAoIdetail)
	
	    return valuableAoIs
	
    def format_sequences(self, raw_sequences):
	    """
	    {'01': [[A, 150], [B, 250]], '02': ...} gets transformed into:
	    [{'identifier': '01', 'fixations': [[A, 150], [B, 250]]}, {'identifier': '02' ... }]
	    """
	    formatted_sequences = []
	    keys = list(raw_sequences.keys())
	    for it in range(0, len(raw_sequences)):
	        act_rec = {
	            'identifier': keys[it],
	            'fixations': raw_sequences[keys[it]]
	        }
	        formatted_sequences.append(act_rec)
	
	    return formatted_sequences
	# STA Algorithm
    def run_sta(self):
	    """
	    Args:
	        raw_sequences: a Python dict of lists - {'ID1': [['F', '383'], ['G', '150']], 'ID2': .. }
	        aoi_data: for additional scanpath processing - [['fullAoiName', xFrom, width, yFrom, height, 'shortName'] .. ]
	    Returns:
	        identifier: for client-side purposes
	        fixations: a list of lists representing the common scanpath - [['A', 150], ['B', 500] .. ]
	        similarity: a dict containing similarity of individual scanpaths to the common one - {'ID1': 66.66, 'ID2': ... }
	    """
	
	    # Preliminary Stage is already complete - sequences are passed in via arguments
	
	    # First-Pass
	    mySequences_num = {}
	    keys = list(self.raw_sequences.keys())
	    for y in range(0, len(keys)):
	        mySequences_num[keys[y]] = self.getNumberedSequence(self.raw_sequences[keys[y]], self.aoi_data)
	
	    myImportanceThreshold = self.calculateImportanceThreshold(mySequences_num)
	    myImportantAoIs = self.updateAoIsFlag(self.getNumberDurationOfAoIs(mySequences_num), myImportanceThreshold)
	    myNewSequences = self.removeInsignificantAoIs(mySequences_num, myImportantAoIs)
	    # Second-Pass
	    myNewAoIList = self.getExistingAoIList(myNewSequences)
	    myNewAoIList = self.calculateTotalNumberDurationofFixationsandNSV(
	        myNewAoIList,
	        self.calculateNumberDurationOfFixationsAndNSV(myNewSequences)
	    )
	    myFinalList = self.getValueableAoIs(myNewAoIList)
	
	    myFinalList.sort(key=lambda x: (x[4], x[3], x[2]))
	    myFinalList.reverse()
	
	    commonSequence = []
	
	    for y in range(0, len(myFinalList)):
	        commonSequence.append([myFinalList[y][0], int(myFinalList[y][3] / myFinalList[y][2])])
	
	    formatted_sequences = self.format_sequences(self.raw_sequences)
	
	    # Store scanpaths as an array of string-converted original scanpaths
	    scanpath_strs = similarity.convert_to_str_array(formatted_sequences)
	
	    common_scanpath = self.getAbstractedSequence(commonSequence)
	    common_scanpath_str = ''
	
	    # For determining get_edit_distance distance we need a pure string version of the common scanpath ('ABC')
	    for fixation in common_scanpath:
	        common_scanpath_str += fixation[0]
	
	    res_data = {
	        'identifier': 'STA',
	        'fixations': common_scanpath,
	        'similarity': similarity.calc_similarity_to_common(scanpath_strs, common_scanpath_str)
	    }
	
	    return res_data
	