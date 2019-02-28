from src.common_scanpath import STA
from src.common_scanpath import eMine
from src.common_scanpath import Dotplots
from src.core.Aoi import Aoi
from src.core.Participant import Participant
import csv

class Dataset:

    def __init__(self,dataset_file_path,aoi_file_path=False,filtered_dataset=False):
        self.dataset_file_path = dataset_file_path
        self.aoi_file_path = aoi_file_path
        self.aoi_array = self.load_aoi()
        self.participants = []
        self.last_participant_name = ""
        self.filtered_dataset = filtered_dataset
        self.load_dataset()


    def load_dataset(self):
        data = open(self.dataset_file_path, 'r')
        reader = csv.DictReader(data, delimiter='\t')
        current_fix = 0;
        act_file_data = []
        for row in reader:
                    # if self.website_name not in row["MediaName"].split(" ")[0] :  # ignore non-recording data point
                    #     continue

            if not self.filtered_dataset and (not row["ValidityLeft"] or not row["ValidityRight"] or not row["FixationPointX (MCSpx)"] or not \
            row["FixationPointY (MCSpx)"]):  # ignore data point with no information
                continue
            if row["GazeEventType"] != "Fixation" or current_fix == int(row["FixationIndex"].split(".")[0]):
                            # if not a fixation or the current fixation
                continue
                        # clear data on visit of first line of new participant
            if self.last_participant_name !=row["ParticipantName"]:
                act_file_data = []
                self.last_participant_name = row["ParticipantName"]
            act_file_data.append([str(int(row["FixationIndex"].split(".")[0]) - 1),
                                        row["GazeEventDuration"],
                                        row["FixationPointX (MCSpx)"],
                                        row["FixationPointY (MCSpx)"],
                                        row["MediaName"].split(" ")[0],
                                     ])
            participant_identifier = row["ParticipantName"]
            self.participants.append(Participant(participant_identifier,act_file_data,self.aoi_array))
        return act_file_data

    def load_aoi(self):
        if(not self.aoi_file_path):
            return
        aoi_data = open(self.aoi_file_path)
        aoi_array = []
        for line in aoi_data:
            aoi = line.split()
            aoi_array.append(Aoi(aoi[0],aoi[1],aoi[2],aoi[3],aoi[4],aoi[5]))
        return aoi_array

    def create_raw_sequences(self):
        raw_sequences = {}
        for participant in self.participants:
            raw_sequences[participant.id] = participant.scanpath
        return raw_sequences

    
    
    # def create_aoi_array_simplified(self):
    #     for aoi in self.create_aoi_array()
