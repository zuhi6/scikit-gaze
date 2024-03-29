from skgaze.similarity_algorithms import levenshtein_distance

def calc_similarity(scanpath1, scanpath2, algorithm=False):
    """ Calculates similarity between two scanpath strings represented as percentage. """
    if not algorithm:
        algorithm = levenshtein_distance.get_edit_distance
    
    # Calculate the similarity value based on the edit distance of given scanpaths
    edit_distance = algorithm(scanpath1, scanpath2)
    similarity = 1 - (edit_distance / (len(scanpath1) if len(scanpath1) > len(scanpath2) else len(scanpath2)))

    # Return similarity as percentage
    return similarity * 100

def calc_mutual_similarity(scanpath_strs):
    """ Calculates mutual similarity between all scanpaths of the formatted array. """

    for i_first in range(0, len(scanpath_strs)):
        # Each scanpath has a similarity object - similarity[id] represents
        # the level of similarity to the scanpath identified by id
        scanpath1 = scanpath_strs[i_first]

        # If the similarity object of first scanpath does not exist yet - create it
        if not scanpath1.get('similarity'):
            scanpath1['similarity'] = {}

        for i_second in range(i_first + 1, len(scanpath_strs)):
            scanpath2 = scanpath_strs[i_second]

            # Get the IDs of the current scanpath pair
            identifier_first = scanpath1['identifier']
            identifier_second = scanpath2['identifier']

            # Performance boost: skip if the similarity between current scanpath pair has already been calculated
            if scanpath1.get('similarity') and scanpath1['similarity'].get(identifier_second) and \
                    scanpath2.get('similarity') and scanpath2['similarity'].get(identifier_first):
                continue

            similarity = calc_similarity(scanpath1['raw_str'], scanpath2['raw_str'])

            # Set the similarity for the first scanpath
            scanpath1['similarity'][identifier_second] = similarity

            # If the similarity object of second scanpath does not exist yet - create it
            if not scanpath2.get('similarity'):
                scanpath2['similarity'] = {}

            # Set the same similarity as above for the second scanpath
            scanpath2['similarity'][identifier_first] = similarity


def calc_similarity_to_common(scanpath_strs, scanpath_common):
    """ Calculates similarity of each individual scanpath to the common one based on the defined similarity formula. """

    # Object storing similarities of each individual scanpath to the common one
    similarity_obj = {}
    len_common = len(scanpath_common)

    # If the common scanpath is not empty (there are cases of no common scanpath sometimes)
    if len_common:
        # Calculate similarity of each scanpath to the common (trending) scanpath
        for scanpath_str in scanpath_strs:
            similarity = calc_similarity(scanpath_common, scanpath_str['raw_str'])
            similarity_obj[scanpath_str['identifier']] = similarity

    return similarity_obj


def get_most_similar_pair(scanpath_strs):
    """ Method looks for the most similar pair of scanpath strings in the given set. """

    most_similar_pair = [scanpath_strs[0], scanpath_strs[0], -1]

    for scanpath in scanpath_strs:
        for scanpath_id in scanpath['similarity']:
            if scanpath['similarity'][scanpath_id] > most_similar_pair[2]:
                most_similar_pair = [
                    scanpath,
                    get_scanpath_str_by_id(scanpath_strs, scanpath_id),
                    scanpath['similarity'][scanpath_id]
                ]

    return most_similar_pair


def convert_to_str_array(scanpaths):
    """
    Converts the dict-formatted scanpaths into an array of strings for similarity calculations. Even though an array is
    not good for searching scanpath by IDs (O(n) time), it provides an easy way to get the size, n-th element or index.
    From: [{'fixations': [['A', '150'], ['B', '750'], ['C', '300']], 'identifier': '02'}, ..]
    To: [{'raw_str': 'ABC', 'identifier': '02'}, {'raw_str': 'AC', 'identifier': '03'}, .. ]
     """

    scanpath_strs = []
    # Extract scanpaths as raw string sequences with identifiers
    for act_scanpath in scanpaths:
        act_scanpath_str = ''
        for fixation in act_scanpath['fixations']:
            act_scanpath_str += fixation[0]
        # Store the identifier and extracted string sequence in an object
        temp_scanpath = {
            'identifier': act_scanpath['identifier'],
            'raw_str': act_scanpath_str
        }
        # Push the object to the array

        scanpath_strs.append(temp_scanpath)

    return scanpath_strs




def get_scanpath_str_by_id(scanpath_strs, identifier):
    """
    Since scanpaths are stored as an array of dicts (might be changed to a dict of dicts later), sometimes
    we need this function to fetch us a particular scanpath by its id.
    """

    for scanpath in scanpath_strs:
        if scanpath['identifier'] == identifier:
            return scanpath

    raise LookupError('No such identifier in scanpath strings array: ' + identifier)


def rem_scanpath_strs_by_id(scanpath_strs, ids_to_rem):
    """
    Function removes scanpaths from the list based on provided ids. It also deletes any references to
    these scanpaths from the existing similarity objects of remaining scanpaths.
    """

    # Delete scanpaths specified by id
    for identifier in ids_to_rem:
        scanpath_strs.remove(get_scanpath_str_by_id(scanpath_strs, identifier))

    # Delete existing references to previously deleted scanpaths
    for scanpath in scanpath_strs:
        for identifier in ids_to_rem:
            if scanpath.get('similarity') and identifier in scanpath['similarity']:
                scanpath['similarity'].pop(identifier, None)


def clear_mutual_similarity(scanpath_strs):
    """ Clears the similarity object of all scanpaths in the array. """

    for scanpath in scanpath_strs:
        scanpath.pop('similarity', None)