from KMP_search import KMPSearch

# chunks = ['HiShelia Lopez', ' my', ' nameShelia LopezShelia Lopez', ' is', ' Shel', 'ia', ' LopezLOLO', 'N', 'O', 'T', ' S', 'h', 'e', 'l', 'i', 'a', ' ', 'L', 'o', 'p', 'e', 'z']
chunks = ['Hi', ' my', ' name', ' is', ' Shel', 'ia', ' Lopez Shelia', ' LopezN', 'O', 'T', 'XXXShe', '', '', 'l', 'i', 'a', ' ', 'L', 'o', 'p', 'e', 'z']
# chunks = ['ha', 'jaha']

mappings = [["Shelia Lopez", "Mark"], ["Hi", "YOOOO"], ["N", "HAHAHAHHAHAHAH"]]

gener = KMPSearch(mappings, chunks)
for chunk in gener:
    print(f"'{chunk}'")
