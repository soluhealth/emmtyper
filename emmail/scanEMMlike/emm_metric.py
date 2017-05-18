# ### SEPARATE DATA BY NUMBER OF BLAST HITS.

import sys
import pandas
from collections import defaultdict

# Supporting variables

suspectEMM_likes = [104, 141, 149, 156, 159, 170, 202, 203, 236, 240]
suspectEMM_likesAthey = [51, 138, 149, 156, 159, 164, 170, 202, 205, 240]

# Supporting functions used in this part.

def clean_keys(list, split):
    """
    We want to remove the contig number from the BLAST query hits.
    Inputting split number helps so we can erase the last number after the dot point.
    """
    var_we_want = split - 1
    new_list = []

    for key in list:
        tmp_list = key.split(".")
        str_we_want = ""

        for i in range(var_we_want):
            if i < (var_we_want - 1) and tmp_list[i] != "":
                str_we_want += str(tmp_list[i]) + "."
            else:
                str_we_want += str(tmp_list[i]) + "."

        new_list.append(str_we_want)

    return new_list

def defaultdict_it(list, split):
    """
    Tally the keys in the list to see occurences of each key.
    """
    tally = defaultdict(int)

    if split == 1:
        list_to_run = list

    elif (split == 2) or (split == 3):
        list_to_run = clean_keys(list, split)

    for key in list_to_run:
        tally[key] += 1

    return tally

def query_db(df, keyword, string):
    """
    Shorthand function to return part of the dataframe containing a specific string.
    str.contains() is a bit unreliable so use with care.
    """
    return df[df[keyword].str.contains(string)]

def clean_emm_keys(emm):
    """
    NOTE: FUNCTION WORKS WHERE EMM TYPES IS NOT IN THE RANGE OF THE STGs.

    Takes string input presumed to be emm types in "Blast Hits".
    Returns only the emm type, stripped from the word "EMM", "STG", and subtypes.
    """
    if type(emm) == str:
        cleaned_key = ""
        for i in emm:
            if i.isdigit():
                cleaned_key += i
            if i == ".":
                break

        return cleaned_key

    else:
        print("Something is wrong. Breaking")
        return

def sort_dict_by_occurence(dict):
    """
    The dictionary is tallied by counts of occurence in the dataframe.
    Instead of showing by key, show dictionary by occurence, sorted from max to min.
    Just prints output instead of returning.
    """
    reversed_tups = []

    for key, value in dict.items():
        reversed_tups.append((value, key))

    print("EMM\t \tCOUNT\n")
    for tup in sorted(reversed_tups, reverse=True):
        print("{}\t \t{}".format(tup[1], tup[0]))

def sort_dict_by_occ_emm_like(dict):
    """
    Modified sort_dict_by_occurence(dict) to show only the possible emm-likes occurences.
    Instead of showing by key, show dictionary by occurence, sorted from max to min.
    Just prints output instead of returning.
    """
    reversed_tups = []

    for key, value in dict.items():
        reversed_tups.append((value, key))

    print("EMM\t \tCOUNT\n")
    for tup in sorted(reversed_tups, reverse=True):
        if int(tup[1]) in suspectEMM_likes or int(tup[1]) in suspectEMM_likesAthey:
            print("{}\t \t{}".format(tup[1], tup[0]))


# Open the file as a pandas dataframe

df = pandas.read_table(sys.argv[1], sep="\t")

# We want to split the data into variables splitted by dot point.

total = 0
split1, split2, split3, weird = [], [], [] , []

for query in df["Query"]:
    total += 1
    if len(query.split(".")) == 1:
        split1.append(query)
    elif len(query.split(".")) == 2:
        split2.append(query)
    elif len(query.split(".")) == 3:
        split3.append(query)
    else:
        weird.append(query)

#print("total is {}". format(total))
#print("split1 is {}, split2 is {}, split3 is {}, and weird {}".format(len(split1), len(split2), len(split3), len(weird)))

# Make data frames based on counts of occurence of isolate in the database.

check_by = "Query"
to_extract = ["Query", "Blast Hit", "Mismatch", "Gap Open", "Identity", "Alignment Length", "Subject Length"]

dfVal1, dfVal2, dfVal3, dfVal4, dfValElse = [pandas.DataFrame(columns=to_extract)] * 5

# Build list of all name splits available to run.

list_to_traverse = [defaultdict_it(split1, 1), defaultdict_it(split2, 2), defaultdict_it(split3, 3)]

# For all dictionary in list, classify isolates based on occurence in database and append it to the provided data frames

for dictionary in list_to_traverse:
    for key, value in dictionary.items():
        if value == 1:
            tmp_df = query_db(df, check_by, key)[to_extract]
            dfVal1 = dfVal1.append(tmp_df[0:1], ignore_index=True)
        elif value == 2:
            tmp_df = query_db(df, check_by, key)[to_extract]
            dfVal2 = dfVal2.append(tmp_df[0:2], ignore_index=True)
        elif value == 3:
            tmp_df = query_db(df, check_by, key)[to_extract]
            dfVal3 = dfVal3.append(tmp_df[0:3], ignore_index=True)
        elif value == 4:
            tmp_df = query_db(df, check_by, key)[to_extract]
            dfVal4 = dfVal4.append(tmp_df[0:4], ignore_index=True)
        else:
            tmp_df = query_db(df, check_by, key)[to_extract]
            dfValElse = dfValElse.append(tmp_df, ignore_index=True)

# Build concatenated data frame of all data frames of occurence.
# Concatenated data frame will display isolates sorted by number of occurences in database.

dfCat = pandas.DataFrame(columns=["Query", "Blast Hit"])

dfCat = dfCat.append([dfVal1,
                      dfVal2,
                      dfVal3,
                      dfVal4,
                      dfValElse], ignore_index=True)

print(dfVal1.count()[0], dfVal2.count()[0], dfVal3.count()[0], dfVal4.count()[0], dfValElse.count()[0])

#print(dfCat.count()[0])

#dfCat.to_csv(path_or_buf="blastCheck.csv")

# Sort emms based on occurence, and punish emms that show up with other emms.
# This will not separate true emms that always relate with same emm-likes.

counter = 1
emm_occ = defaultdict(int)
emm_punish = defaultdict(float)

for df in [dfVal1, dfVal2, dfVal3]:
    for item in df["Blast Hit"]:
        emm_num = item.split(".")[0]
        emm_occ[emm_num] += 1
        emm_punish[emm_num] += counter
    counter += 1

emm_metric = defaultdict(float)

for key,val in emm_occ.items():
    val = emm_occ[key]
    emm_metric[key] = val/emm_punish[key]

####
tmp = []
for key,val in emm_metric.items():
    tmp.append((val, key))

for item in sorted(tmp, reverse=True):
    print item, emm_occ[item[1]]

####
for key in emm_metric.keys():
    emm = int(clean_emm_keys(key))
    if emm in suspectEMM_likes or emm in suspectEMM_likesAthey:
        print emm, emm_metric[key], emm_occ[key]
