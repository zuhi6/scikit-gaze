
from skgaze.EMDAT.data_structures import Datapoint
from skgaze.EMDAT.BasicParticipant import BasicParticipant

class EMDAT:

    def __init__(self, dataset,pid=False):
        self.pid = pid
        self.dataset = dataset
       
        

    def createInstance(self):
        result = {}
        if self.pid:
           for participant in self.dataset.participants:
               if participant.id == self.pid:
                    result[participant.id] = BasicParticipant(self.pid,False,participant.fixations,participant.fixations,participant,aoifile=participant.aoi_array)
                    return result
        for participant in self.dataset.participants:
            result[participant.id] = BasicParticipant(participant.id,False,participant.fixations,participant.fixations,participant,aoifile=participant.aoi_array)
        return result
        