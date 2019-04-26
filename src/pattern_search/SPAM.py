from collections import defaultdict
from src.core.Dataset import Dataset
import os

class SPAM:


    def __init__(self, dataset):
        self.scanPaths = dataset.create_raw_sequences()
        self.listOfAois = self.simplify_aoi_array(dataset.aoi_array)

   
    def simplify_aoi_array(self, aoi_array):
        spam_aoi_array = []
        for aoi in aoi_array:
        	spam_aoi_array.append(aoi.aoi_char)
        return spam_aoi_array

    # Use threshold on each instance of each AOI to find only trending instance AOIs
    def find_trending_AOIs(self, AOIsInfo, threshold, countSequences):
        trendingAOIs = defaultdict(list)
        for AOI in AOIsInfo:
            for index in AOIsInfo[AOI]:
                if ((AOIsInfo[AOI][index][0] >= threshold[AOI][0] and AOIsInfo[AOI][index][1] >= threshold[AOI][1]) or (
                        AOIsInfo[AOI][index][3] == countSequences)):
                    trendingAOIs[AOI].append(index)
        return trendingAOIs

    # Find threshold for each AOI
    def find_thresholds(self, AOIsInfo):
        threshold = defaultdict(list)
        # Find threshold for each AOI (minDuration and minHits in all AOIs)
        for AOI in AOIsInfo:
            minDuration = 1000000
            minHits = 1000000
            for index in AOIsInfo[AOI]:
                if (AOIsInfo[AOI][index][2] == True):
                    if (AOIsInfo[AOI][index][0] < minDuration):
                        minDuration = AOIsInfo[AOI][index][0]
                    if (AOIsInfo[AOI][index][1] < minHits):
                        minHits = AOIsInfo[AOI][index][1]
            threshold[AOI] = [minDuration, minHits]

        return threshold

    # Count totalDuration, numberOfHits and number in how many rows occurs this instance
    def learn_info(self, listOfMaxIndexes, countSequences):
        AOIsInfo = defaultdict(list)
        for j in self.listOfAois:  # foreach AOI in list
            AOIsIndexes = defaultdict(list)
            for index in range(1, listOfMaxIndexes[j] + 1):
                totalDuration = 0
                numberOfHits = 0
                flagCounter = 0
                listInfo = []
                for i in self.scanPaths:  # foreach scanpath
                    occursInScanpath = False
                    for k in self.scanPaths[i]:  # foreach AOI in scanpath
                        if (j == k[0] and k[2] == index):
                            totalDuration += int(k[1])
                            numberOfHits += 1
                            occursInScanpath = True
                    if (occursInScanpath == True):
                        flagCounter += 1
                if (flagCounter > countSequences / 2):
                    listInfo.append(totalDuration)
                    listInfo.append(numberOfHits)
                    listInfo.append(True)
                    listInfo.append(flagCounter)
                    AOIsIndexes[index] = listInfo
                    AOIsInfo[j] = AOIsIndexes
                else:
                    listInfo.append(totalDuration)
                    listInfo.append(numberOfHits)
                    listInfo.append(False)
                    listInfo.append(flagCounter)
                    AOIsIndexes[index] = listInfo
                    AOIsInfo[j] = AOIsIndexes
        return AOIsInfo

    # find maxIndex in each AOI, (max index of instance of AOI)
    def find_max_indexes(self, AOIIndexes):
        listOfMaxIndexes = defaultdict(list)
        for AOI in self.listOfAois:
            maxIndex = 0
            for i in AOIIndexes:
                for j in AOIIndexes[i]:
                    if (j == AOI and maxIndex < max(AOIIndexes[i][j])):
                        maxIndex = max(AOIIndexes[i][j])
            listOfMaxIndexes[AOI] = maxIndex
        return listOfMaxIndexes

    

    
    #count rows/number of participants
    def countSeq(self):
        countSequences = 0
        for i in self.scanPaths:
            countSequences += 1
        return countSequences



    def runSpam(self):  
         # count sequences
        countSequences = self.countSeq()

        # we got dict {P07: [[IR08, 846], ['R00', 783]], 'P08': [['R00', 1717], ['R00', 117]...]}
        # Step 2 - Rate AOIs
        # Merge AOIs; for each scanpath and AOI save time to AOITimes P08: R00: [2736.0, 283.0, 3234.0, 434.0...]
        # In each scanpath index all AOIs | AOIIndexes P08: R00 [4, 14, 3, 12...]
        # Append index of instance to each [AOI, time] in scanpath
        AOITimes = defaultdict(list)
        AOIIndexes = defaultdict(list)

        for i in self.scanPaths:
            mergedScanpath = defaultdict(list)
            timesOfAOIs = defaultdict(list)
            timesOfAOIsTemp = defaultdict(list)
            indexOfAOIs = defaultdict(list)
            AOI = ''
            for j in self.scanPaths[i]:
                if j[0] not in mergedScanpath:
                    mergedScanpath[j[0]].append(j[1])  # add AOI + time (ms) to dict
                if (AOI == j[0]):
                    mergedScanpath[j[0]][-1] += j[1]
                else:
                    mergedScanpath[j[0]].append(j[1])
                AOI = j[0]
            for j in mergedScanpath:
                timesOfAOIs[j] = mergedScanpath[j][1:]
                timesOfAOIsTemp[j] = mergedScanpath[j][1:]
            AOITimes[i] = timesOfAOIs

            # foreach AOI index position
            for j in timesOfAOIsTemp:
                counterOfIndex = len(timesOfAOIsTemp[j])
                listOfIndexesofAOI = []
                listOfIndexesofAOI = [0] * len(timesOfAOIsTemp[j])
                for l in range(0, len(timesOfAOIsTemp[j])):
                    counter = 0
                    premenna = 0
                    minimum = 100000
                    for k in timesOfAOIsTemp[j]:
                        if int(k) <= minimum:
                            minimum = int(k)
                            premenna = counter
                        counter += 1
                    listOfIndexesofAOI[premenna] = counterOfIndex
                    timesOfAOIsTemp[j][premenna] = 1000000  # set value of this time to 1000000
                    counterOfIndex -= 1
                indexOfAOIs[j] = listOfIndexesofAOI
            AOIIndexes[i] = indexOfAOIs

            for l in self.listOfAois:  # foreach AOI    [IR00, IR01, IR02]
                counter = 0
                counter2 = 0
                for k in self.scanPaths[i]:  # foreach list in list (['R00', 867], [IR08, 846], ['R00', 783]], 'P08': [['R00', 1717])
                    if (k[0] == l):
                        self.scanPaths[i][counter].append(indexOfAOIs[l][counter2])
                        try:
                            if (self.scanPaths[i][counter + 1][0] != k[0]):  # if next AOI is different
                                counter2 += 1
                        except:
                            pass
                    counter += 1

        # Step 3 - Find and save only trending AOIs
        # find maxIndex in each AOI, (max index of instance of AOI)
        listOfMaxIndexes = defaultdict(list)
        listOfMaxIndexes = self.find_max_indexes(AOIIndexes)

        # Count totalDuration, numberOfHits and number in how many rows occurs this instance foreach instance of AOI
        AOIsInfo = defaultdict(list)
        AOIsInfo = self.learn_info(listOfMaxIndexes, countSequences)

        # AOI: instanceOfAOI(index): totalDuration, numbOfHits, in more than countSequences/2, numbOfSequence
        # Example: R00: 1: 5134, 12, True, 4
        threshold = defaultdict(list)
        threshold = self.find_thresholds(AOIsInfo)

        # Use threshold on each instance of each AOI to find only trending instance AOIs
        # Example of trending AOIs: R00: [1,2,3,4], IR03: [1,2]
        trendingAOIs = defaultdict(list)
        trendingAOIs = self.find_trending_AOIs(AOIsInfo, threshold, countSequences)

        print(trendingAOIs)
