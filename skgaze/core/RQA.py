from skgaze.RQA.RQA_funcs import RQA as _RQA

class RQA:

    def __init__(self, dataset):
        self.dataset = dataset
        
    
    def CalculateRecurrenceFunction(self,timeDelayValue, numTimeDelaySample, phaseSpaceClusteringThreshold, pid=False):

        result = {}
        if pid:
            for participant in self.dataset.participants:
                if participant.id == pid:
                    return _RQA(participant.fixations).CalculateRecurrenceFunction(timeDelayValue, numTimeDelaySample, phaseSpaceClusteringThreshold)
                print("couldn't find participant with this id")
                return None
        
        for participant in self.dataset.participants:
            result[participant.id] = _RQA(participant.fixations).CalculateRecurrenceFunction(timeDelayValue, numTimeDelaySample, phaseSpaceClusteringThreshold)
        return result

    def CalculateReoccurrenceFunction(self, fixationSpaceDistanceRadius, pid=False):

        result = {}
        if pid:
            for participant in self.dataset.participants:
                if participant.id == pid:
                    return _RQA(participant.fixations).CalculateReoccurrenceFunction(fixationSpaceDistanceRadius)
                print("couldn't find participant with this id")
                return None
        
        for participant in self.dataset.participants:
            result[participant.id] = _RQA(participant.fixations).CalculateReoccurrenceFunction(fixationSpaceDistanceRadius)
        return result
