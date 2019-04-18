
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
        # return BasicParticipant(dataset.pid, dataset.data_file_path, dataset.fixfile, dataset.segfile, dataset.log_time_offset, dataset.emdat_aoi_file, dataset.prune_length, dataset.require_valid_segs, dataset.auto_partition_low_quality_segments)
