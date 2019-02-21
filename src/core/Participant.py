
class Participant:

    def __init__(self,id,fixations,aoi_array):
        self.id = id
        self.fixations = fixations
        self.scanpath = []
        self.aoi_array = aoi_array
        self.load_scanpaths()

    def load_scanpaths(self):
        for row in self.fixations:
            for aoi in self.aoi_array:
                aoi_x = float(aoi.x)
                aoi_weight = float(aoi.weight)
                aoi_y = float(aoi.y)
                aoi_height = float(aoi.height)
                fixation_x = float(row[2])
                fixation_y = float(row[3])
                if (aoi_x <= fixation_x < aoi_x + aoi_weight) and \
                        (aoi_y <= fixation_y < aoi_y + aoi_height):
                    self.scanpath.append([aoi.aoi_char,row[1]])
