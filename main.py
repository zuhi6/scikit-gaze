from src.core.Dataset import Dataset
from src.common_scanpath.STA import STA
from src.common_scanpath.eMine import eMine
from src.common_scanpath.Dotplots import Dotplots

dataset = Dataset('./data/template_sta/eMINE_searching_tasks/AVG/Scanpaths.tsv',
'./data/template_sta/eMINE_searching_tasks/AVG/SegmentedPages.txt',filtered_dataset=True)

print(Dotplots(dataset).run_dotplot())
