
from src.EMDAT.data_structures import Datapoint
from src.EMDAT.BasicParticipant import BasicParticipant

class EMDAT:

    def __init__(self, dataset,pid=False):
        self.pid = pid
        self.dataset = dataset
       
        

    def createInstance(self):
        result = {}
        if self.pid:
           for participant in self.dataset.participants:
               if participant.id == self.pid:   
                    return BasicParticipant(self.pid,False,self.dataset.participants[0].fixations,self.dataset.participants[0].fixations,self.dataset.participants[0],aoifile=self.dataset.participants[0].aoi_array)
        for participant in self.dataset.participants:
            result[participant.id] = BasicParticipant(participant.id,False,participant.fixations,participant.fixations,participant,aoifile=participant.aoi_array)
        return result
        