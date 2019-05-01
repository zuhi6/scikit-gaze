import copy
import math
from operator import itemgetter
from src.similarity_algorithms import similarity
	
class Dotplots:
    
    def __init__(self, dataset):
        self.dotplot_max_aois = 100
        self.dotplot_error_rate_area = 0
        self.raw_sequences = dataset.create_raw_sequences()
	
	
	# CODE ORIGIN: https://github.com/Groosling/DP_features_and_scanpaths
    def createSequencesBasedOnVisualElements(self, my_dataset):
	    Sequences = {}
	    Participants = my_dataset.scanpath_data_raw
	    myAoIs = my_dataset.aoi_data
	    keys = list(Participants.keys())
	    
	
	    for y in range(0, len(keys)):
	        sequence = ""
	        counter = 0
	        for z in range(0, len(Participants[keys[y]])):
	            if counter == self.dotplot_max_aois:
	                break
	            tempAoI = ""
	            tempDuration = 0
	
	            for k in range(0, len(myAoIs)):
	                if float(Participants[keys[y]][z][3]) >= (float(myAoIs[k][1]) - self.dotplot_error_rate_area) and float(
	                        Participants[keys[y]][z][3]) < (
	                ((float(myAoIs[k][1]) - self.dotplot_error_rate_area) + (float(myAoIs[k][2]) + 2 * self.dotplot_error_rate_area))) and float(
	                        Participants[keys[y]][z][4]) >= (float(myAoIs[k][3]) - self.dotplot_error_rate_area) and float(
	                        Participants[keys[y]][z][4]) < (
	                ((float(myAoIs[k][3]) - self.dotplot_error_rate_area) + (float(myAoIs[k][4]) + 2 * self.dotplot_error_rate_area))):
	                    tempAoI = tempAoI + myAoIs[k][5]
	                    tempDuration = int(Participants[keys[y]][z][2])
	
	
	            # my solution compare sum of distances to four corners
	            if len(tempAoI) > 1:
	                tempAoI = self.getCloserAOI(Participants[keys[y]][z],myAoIs, tempAoI)
	
	            if len(tempAoI) != 0:
	                counter = counter + 1
	                sequence = sequence + tempAoI + "-" + str(tempDuration) + "."
	                if counter == self.dotplot_max_aois:
	                    break
	
	        Sequences[keys[y]] = sequence
	    return Sequences
	
	
    def getCloserAOI(self,Participants_pos, myAoIs, tempAoI):
	    sums_of_distances = {}
	    for m in range(0, len(tempAoI)):
	        for n in range(0, len(myAoIs)):
	            if tempAoI[m] == myAoIs[n][5]:
	                temp_distance = []
	                # sum distance of all 4 corners
	                # up, left
	                temp_distance.append(math.sqrt(pow(float(Participants_pos[3]) - float(myAoIs[n][1]), 2) +
	                                               pow(float(Participants_pos[4]) - float(myAoIs[n][3]), 2)))
	                # up right
	                temp_distance.append(math.sqrt(pow(float(Participants_pos[3]) - (float(myAoIs[n][1]) + float(myAoIs[n][2])), 2) +
	                                               pow(float(Participants_pos[4]) - float(myAoIs[n][3]), 2)))
	                # down left
	                temp_distance.append(math.sqrt(pow(float(Participants_pos[3]) - (float(myAoIs[n][1])), 2) +
	                                               pow(float(Participants_pos[4]) - (float(myAoIs[n][3]) + float(myAoIs[n][4])), 2)))
	                # down, right
	                temp_distance.append(math.sqrt(pow(float(Participants_pos[3]) - (float(myAoIs[n][1]) + float(myAoIs[n][2])), 2) +
	                                               pow(float(Participants_pos[4]) - (float(myAoIs[n][3]) + float(myAoIs[n][4])), 2)))
	                sums_of_distances[tempAoI[m]] = sum(temp_distance)
	                break
	    # return key of minimal value in dictionary
	    return min(sums_of_distances, key=sums_of_distances.get)
	
    def getArrayRepresentationOfSequence(self, mySequences):
	    """
	    Args:
	        mySequences: String format of sequences
	    Returns: array representation of sequence
	    """
	    keys = list(mySequences.keys())
	    # odstranenie bodky na konci
	    for y in range(0, len(keys)):
	        mySequences[keys[y]] = mySequences[keys[y]].split('.')
	        del mySequences[keys[y]][len(mySequences[keys[y]]) - 1]
	    #  rozdeli D-100 na pole z dvomi prvkami D a 100
	    for y in range(0, len(keys)):
	        for z in range(0, len(mySequences[keys[y]])):
	            mySequences[keys[y]][z] = mySequences[keys[y]][z].split('-')
	    return mySequences
	
    def simplifySequence(self, aSequence):
	    """
	    Groups same fixation in a row AAABBB ->  AB and sums up the fixDur
	    Args:
	        aSequence: dictionary of array representation of sequences
	    Returns:
	        Processed sequence in array representation
	    """
	    keys = list(aSequence.keys())
	    for y in range(0, len(keys)):
	        simpleSequence = []
	        lastAOI = "0"
	        for z in range(0, len(aSequence[keys[y]])):
	            if aSequence[keys[y]][z][0] == lastAOI:
	                simpleSequence[len(simpleSequence) - 1][1] = str(int(simpleSequence[len(simpleSequence) - 1][1]) + int(aSequence[keys[y]][z][1]))
	            else:
	                simpleSequence.append([aSequence[keys[y]][z][0], aSequence[keys[y]][z][1]])
	                lastAOI = aSequence[keys[y]][z][0]
	        aSequence[keys[y]] = simpleSequence
	    return aSequence
	
	
    def applyFixDurationThreshold(self, aSequence, threshold = 80):
	    """
	    Delete fixations shorter than defined threshold
	    Args:
	        aSequence: dictionary of array representation of sequences
	        threshold: default 80 ms
	    Returns:
	        Processed sequence in array representation
	    """
	    keys = list(aSequence.keys())
	    for y in range(0, len(keys)):
	        processedArray = []
	        for z in range(0, len(aSequence[keys[y]])):
	            if int(aSequence[keys[y]][z][1]) > threshold:
	                processedArray.append(aSequence[keys[y]][z])
	        aSequence[keys[y]] = processedArray
	    return aSequence
	
    def getStringRepresentation(self, aSequence):
	    """
	    Returns string representation without duration of fixations
	    Args:
	        aSequence: dictionary of array representation of sequeces
	    """
	    newDict  = {}
	    keys = list(aSequence.keys())
	    for y in range(0, len(keys)):
	        sequence = ""
	        for z in range(0, len(aSequence[keys[y]])):
	            sequence = sequence + aSequence[keys[y]][z][0]
	        newDict[keys[y]] = sequence
	    return newDict
	
	
    def createSequencesBasedOnDistances(self, my_dataset):
	    """
	    Create Scanpath from sacade lengths(distances between fixations)
	    Args:
	        my_dataset: dataset
	    """
	    aoi_range = 300
	    sequences = {}
	    participants = my_dataset.scanpath_data_raw
	    myAoIs = my_dataset.aoi_data
	    keys = list(participants.keys())
	    for y in range(0, len(keys)):
	        sequence = ""
	        for z in range(0, min(len(participants[keys[y]]) - 1, self.dotplot_max_aois)):
	           tempdist = self.calculateDistance(int(float(participants[keys[y]][z][3])), int(float(participants[keys[y]][z][4])),
	                                        int(float(participants[keys[y]][z + 1][3])), int(float(participants[keys[y]][z + 1][4])))
	           sequence = sequence + self.getAOIBasedOnRange(tempdist, aoi_range) + "-" + str(int(float(participants[keys[y]][z + 1][1])) - int(float(participants[keys[y]][z][1]))) + "."
	        sequences[keys[y]] = sequence
	    return sequences
	
	
    def calculateDistance(self, xStart, yStart, xEnd, yEnd):
	    """
	    Calculate distance of 2D coordinates.
	    """
	    return math.sqrt(pow(xEnd - xStart, 2) + pow(yEnd - yStart, 2))
	
    def getAOIBasedOnRange(self, value, aoiRange):
	    """
	    Determine AOI based on range
	    Args:
	        value: distance between fixations
	        aoiRange: range of distance for single AOI
	    Returns: character representation of AOI
	    """
	    AOIS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
	    return AOIS[int(value / aoiRange)]
	
    def createSequencesBasedOnFixatonDurations(self, my_dataset):
	    """
	    Create Scanpath from fixations duration
	    Args:
	        my_dataset: dataset
	    """
	    aoi_range = 100
	    sequences = {}
	    participants = my_dataset.scanpath_data_raw
	    myAoIs = my_dataset.aoi_data
	    keys = list(participants.keys())
	    for y in range(0, len(keys)):
	        sequence = ""
	        for z in range(0, min(len(participants[keys[y]]) - 1, self.dotplot_max_aois)):
	           sequence = sequence + self.getAOIBasedOnRange(int(participants[keys[y]][z][2]), aoi_range) +\
	                      "-" + participants[keys[y]][z][2] + "."
	        sequences[keys[y]] = sequence
	    return sequences
	
	
    def calculateVector(self, xStart, yStart, xEnd, yEnd):
	    """
	    Calculate vector between two 2D coordinates.
	    """
	    return [xEnd - xStart, yEnd - yStart]
	
	
    def calculateAngle(self, vect1, vect2):
	    """
	    Calculates angle between 2 vector in 2D space
	    Args:
	        vect1: vector represented as list
	        vect2: vector represented as list
	    """
	    vect1Size = self.calculateDistance(0, 0, vect1[0], vect1[1])
	    vect2Size = self.calculateDistance(0, 0, vect2[0], vect2[1])
	    dotProduct = (vect1[0] * vect2[0]) + (vect1[1] * vect2[1])
	    return math.degrees(math.acos(dotProduct / (vect1Size * vect2Size)))
	
	
    def createSequencesBasedOnRelativeAngle(self, my_dataset):
	    """
	    Create Scanpath from absolute angles of saccades
	    Args:
	        my_dataset: dataset
	    """
	    aoi_range = 30
	    sequences = {}
	    participants = my_dataset.scanpath_data_raw
	    myAoIs = my_dataset.aoi_data
	    keys = list(participants.keys())
	    for y in range(0, len(keys)):
	        # TODO vec1 = vec2 at the beginning of the cycle ... better time complexity
	        # TODO add condition if sequence has two elements or so.. return empty sequence.. depends ond cycle
	        sequence = ""
	        for z in range(0, min(len(participants[keys[y]]) - 2, self.dotplot_max_aois)):
	            # calculates vector between curent point and next one
	            vec1 = self.calculateVector(int(float(participants[keys[y]][z][3])), int(float(participants[keys[y]][z][4])),
	                                   int(float(participants[keys[y]][z + 1][3])), int(float(participants[keys[y]][z + 1][4])))
	            # calculates vector between next point and next next one
	            vec2 = self.calculateVector(int(float(participants[keys[y]][z + 1][3])), int(float(participants[keys[y]][z + 1][4])),
	                                   int(float(participants[keys[y]][z + 2][3])), int(float(participants[keys[y]][z + 2][4])))
	            angle = self.calculateAngle(vec1, vec2)
	            # duration is calculated as sum of both sacades durations
	            sequence = sequence + self.getAOIBasedOnRange(angle, aoi_range) + "-" + str(int(float(participants[keys[y]][z + 2][1])) - int(float(participants[keys[y]][z][1]))) + "."
	        sequences[keys[y]] = sequence
	    return sequences
	
	
    def createSequencesBasedOnAbsoluteAngle(self, my_dataset):
	    """
	    Create Scanpath from absolute angles of saccades
	    Args:
	        my_dataset: dataset
	    """
	    aoi_range = 30
	    sequences = {}
	    participants = my_dataset.scanpath_data_raw
	    myAoIs = my_dataset.aoi_data
	    keys = list(participants.keys())
	    for y in range(0, len(keys)):
	        sequence = ""
	        for z in range(0, min(len(participants[keys[y]]) - 1, self.dotplot_max_aois)):
	            # calculates vector between curent point and next one
	            vec1 = self.calculateVector(int(float(participants[keys[y]][z][3])), int(float(participants[keys[y]][z][4])),
	                                   int(float(participants[keys[y]][z + 1][3])), int(float(participants[keys[y]][z + 1][4])))
	            # default vector (right direction)
	            vec2 = self.calculateVector(0, 0, 1, 0)
	            angle = self.calculateAngle(vec1, vec2)
	            # duration is calculated as sum of both sacades durations
	            sequence = sequence + self.getAOIBasedOnRange(angle, aoi_range) + "-" + str(int(float(participants[keys[y]][z + 1][1])) - int(float(participants[keys[y]][z][1]))) + "."
	        sequences[keys[y]] = sequence
	    return sequences
	
	
    def create_sequences_by_mod(self, my_dataset, mod):
	    """
	    Based on mod creates sequences from dataset
	    Args:
	        my_dataset: dataset
	        mod:     1 vytvori standardny scanpath z AOI
	                 2 vytvori scanpah na zaklade dlzky sakad
	                 3 vytvori scanpath na zaklade dlzky trvania fixacii
	                 4 vytvori scanpath na zaklade relativnych uhlov sakad0
	                 5 vytvori scanpath na zaklade absolutnych uhlov sakad
	    """
	
	    case = {
	      1: self.createSequencesBasedOnVisualElements,
	      2: self.createSequencesBasedOnDistances,
	      3: self.createSequencesBasedOnFixatonDurations,
	      4: self.createSequencesBasedOnRelativeAngle,
	      5: self.createSequencesBasedOnAbsoluteAngle,
	    }
	    my_func = case[mod]
	    return my_func(my_dataset)
	
	
    def dotplotListofLists(self, sequenceX, sequenceY):
	    # fill matrix with zeroes
	    dotplotMatrix = [[0 for x in sequenceX] for y in sequenceY]
	    # put 1 on matching positions
	    for xIndex, valueX in enumerate(sequenceX):
	        for yIndex, valueY in enumerate(sequenceY):
	            if valueX == valueY:
	                dotplotMatrix[yIndex][xIndex] = 1
	    return dotplotMatrix
	
	
    def findLongestCommonSequence(self, dotplotMatrix, sequenceX):
	
	    commonSubSequence = ""
	    lengthSubsequence = 0
	
	    # right part of matrix
	    for i in range(0, len(dotplotMatrix[0])):
	        # reamining x length or height of matrix
	        sum = 0
	        for j in range(0, min(len(dotplotMatrix[0]) - i, len(dotplotMatrix))):
	            sum += dotplotMatrix[j][i + j]
	
	        if sum > lengthSubsequence:
	            # sequence created by characters with value 1
	            lengthSubsequence = sum
	            commonSubSequence = ""
	            for j in range(0, min(len(dotplotMatrix[0]) - i, len(dotplotMatrix))):
	                if dotplotMatrix[j][i + j] == 1:
	                    commonSubSequence = commonSubSequence + sequenceX[i + j]
	
	
	    # left part of the matrix
	    for i in range(0, len(dotplotMatrix)):
	        sum = 0
	        for j in range(0, min(len(dotplotMatrix) - i, len(dotplotMatrix[0]))):
	            sum += dotplotMatrix[i + j][j]
	
	        if sum > lengthSubsequence:
	            # sequence created by characters with value 1
	            lengthSubsequence = sum
	            commonSubSequence = ""
	            for j in range(0, min(len(dotplotMatrix) - i, len(dotplotMatrix[0]))):
	                if dotplotMatrix[i + j][j] == 1:
	                    commonSubSequence = commonSubSequence + sequenceX[j]
	
	    return commonSubSequence
	
	
    def findCommonSequence(self, my_str_sequences):
	    """
	    Finds the most similar seqecnces in dictionary and determines their common scanpath
	    Args:
	        my_str_sequences: dictionary of sequences in string format
	    """
	    string_sequences = copy.deepcopy(my_str_sequences)
	    keys = list(string_sequences.keys())
	    while len(keys) > 1:
	        common_sequences = []
	        for y in range(0, len(keys)):
	            sequence = ""
	            for z in range(y + 1, len(keys)):
	                #  create matrix
	                matrix = self.dotplotListofLists(string_sequences[keys[y]], string_sequences[keys[z]])
	
	                # find longest common subsequence
	                subSequence = self.findLongestCommonSequence(matrix, string_sequences[keys[y]])
	                common_sequences.append([keys[y], keys[z], subSequence, len(subSequence)])
	
	        # replace 2 most similar sequences with their common sequence
	        common_sequences = sorted(common_sequences, reverse=True, key=itemgetter(3))
	        if common_sequences[0][2] == '':
	            return ''
	
	        del string_sequences[common_sequences[0][0]]
	        del string_sequences[common_sequences[0][1]]
	        string_sequences[common_sequences[0][0] + common_sequences[0][1]] = common_sequences[0][2]
	        keys = list(string_sequences.keys())
	    return string_sequences[keys[0]]
	
	
    def run_dotplot(self, simplify=True, fix_dur_threshold=None, mod=1):
	    """
	    Args:
	        raw_sequences: a Python dict of lists - {'ID1': [['F', '383'], ['G', '150']], 'ID2': .. }
	        simplify: simplify repeated fixations on the same AOI into one
	        fix_dur_threshold: minimum fixation duration threshold
	        mod: 1 - vytvori standardny scanpath z AOI
	             2 - vytvori scanpah na zaklade dlzky sakad (zatial nefunguje, nemame udaje o sakadach)
	             3 - vytvori scanpath na zaklade dlzky trvania fixacii
	             4 - vytvori scanpath na zaklade relativnych uhlov sakad (zatial nefunguje, nemame udaje o sakadach)
	             5 - vytvori scanpath na zaklade absolutnych uhlov sakad (zatial nefunguje, nemame udaje o sakadach)
	    Returns:
	        identifier: for client-side purposes
	        fixations: a list of lists representing the common scanpath - [['A', 150], ['B', 500] .. ]
	        similarity: a dict containing similarity of individual scanpaths to the common one - {'ID1': 66.66, 'ID2': ... }
	    """
	
	    # The dotplot author originally provided mods for simplifying sequences and setting their min threshold
	    # However, our system already does that automatically when uploading any scanpath data
	    """
	    my_sequences = create_sequences_by_mod(dataset_task, mod)
	    my_sequences = getArrayRepresentationOfSequence(my_sequences)
	    if fix_dur_threshold is not None:
	        my_sequences = applyFixDurationThreshold(my_sequences, fix_dur_threshold)
	    if simplify:
	        my_sequences = simplifySequence(my_sequences)
	    """
	
	    string_sequences = self.getStringRepresentation(self.raw_sequences)
	    common_scanpath_str = self.findCommonSequence(string_sequences)
	
	    common_scanpath = []
	    for fixation in common_scanpath_str:
	        common_scanpath.append([fixation, 0])
	
	    scanpath_strs = []
	    for participant_id in string_sequences:
	        scanpath_strs.append({
	            'identifier': participant_id,
	            'raw_str': string_sequences[participant_id]
	        })
	
	    res_data = {
	        'identifier': 'Dotplot',
	        'fixations': common_scanpath,
	        'similarity': similarity.calc_similarity_to_common(scanpath_strs, common_scanpath_str)
	    }
	
	    return res_data