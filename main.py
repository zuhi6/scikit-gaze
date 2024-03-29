from skgaze.core.Dataset import Dataset
from skgaze.common_scanpath.STA import STA
from skgaze.common_scanpath.eMine import eMine
from skgaze.common_scanpath.Dotplots import Dotplots
from skgaze.pattern_search.SPAM import SPAM
from skgaze.EMDAT.BasicParticipant import BasicParticipant
from skgaze.core.RQA import RQA
from skgaze.core.EMDAT import EMDAT
from skgaze.EMDAT.BasicParticipant import BasicParticipant
from skgaze.similarity_algorithms import longest_common_substring as ld


dataset = Dataset('./data/DOD2016_fixations.tsv',
'./data/SegmentedPages.txt')

# dataset_2 = Dataset('./data/DOD2016_fixations_2_participants.tsv',
# './data/SegmentedPages.txt')


# dataset_5 = Dataset('./data/DOD2016_fixations_5_participants.tsv',
# './data/SegmentedPages.txt')

# dataset_10 = Dataset('./data/DOD2016_fixations_10_participants.tsv',
# './data/SegmentedPages.txt')

# print(SPAM(dataset_10).runSpam(minlength=3,minsup_percenta=0.7))

print(STA(dataset).run_sta())
# # print(dataset.participants[0].startTimestamp, dataset.participants[0].lastTimestamp)


# # part = EMDAT(dataset,'P61').createInstance()

# print(SPAM(dataset).runSpam())


# emdat = EMDAT(dataset,"P01m").createInstance()
# max_fixated = 0
# aoi_result = []
# for aoi in dataset.aoi_array:
#     numfixations = emdat.getAoiData(aoi.type_of_element)["numfixations"]
#     if numfixations == max_fixated:
#         aoi_result.append(aoi.type_of_element)
    
#     if numfixations > max_fixated:
#         max_fixated = numfixations
#         aoi_result = []
#         aoi_result.append(aoi.type_of_element)
    

# print(aoi_result)


# dataset = Dataset(pid='P61',eventfile='./data/emdat_test/P61-Event-Data.tsv',dataset_file_path='./data/emdat_test/P61-All-Data.tsv',fixfile='./data/emdat_test/P61-Fixation-Data.tsv',segfile='./data/emdat_test/P61.seg',emdat_aoifile='./data/emdat_test/general.aoi',filtered_dataset=True)

# dataset = Dataset('./data/template_sta/scanpaths/DOD2016_fixations_5_participants.tsv',
#     './data/template_sta/regions/SegmentedPages.txt',filtered_dataset=False)
# rqa_test = RQA(dataset)
# print(rqa_test.CalculateReoccurrenceFunction(5,"P01m"))

# print(eMine(dataset).run_emine())
# part = EMDAT(dataset).createInstance()
# print(part["P01m"].getAoiData("header"))
# # emdat = EMDAT(dataset)

# emdat = BasicParticipant('P61','./data/emdat_test/P61-Event-Data.tsv','./data/emdat_test/P61-All-Data.tsv','./data/emdat_test/P61-Fixation-Data.tsv','./data/emdat_test/P61.seg','./data/emdat_test/general.aoi')

# emdat_wrapper = EMDAT(dataset,"ID01",'./data/emdat_test/P61-Event-Data.tsv','./data/emdat_test/P61.seg')

# print(SPAM(dataset).runSpamExtended('./data/spam_test.tsv','./data/spam_result.txt'))

# rqa_test = RQA('./data/rqa_test/ScienceMultipliesEyePowerFixations_Subject01.txt')
# print(rqa_test.CalculateRecurrenceFunction(1,1,1))
# print(rqa_test.CalculateReoccurrenceFunction(5))