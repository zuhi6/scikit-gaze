from src.core.Dataset import Dataset

dataset = Dataset('../data/template_sta/eMINE_searching_tasks/AVG/Scanpaths.tsv',
'../data/template_sta/eMINE_searching_tasks/AVG/SegmentedPages.txt',filtered_dataset=True)

print(dataset.sta())
