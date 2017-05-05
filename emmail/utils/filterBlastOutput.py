# import sys

# Main workhorse.

def filter(variable):
    # Change arguments here.
    # IMPORTANT TO KNOW: FUNCTIONS DO NOT AUTOMATICALLY RELATE TO EACH OTHER. USE ALL NEEDED.

    variableList = ['Query', 'Blast Hit', 'Identity', 'Alignment Length', 'Mismatch',
                       'Gap Open', 'Query Start', 'Query End', 'Hit Start', 'Hit End',
                       'E-Value', 'Bit Score', 'Subject Length']

    line = ""
    for var in variableList:
        line += "{}\t".format(var)
    print line

    for line in variable:

        line_tmp = line.split("\t")

        # Build dictionary of variables in tab
        Vars = {}

        for i in range(len(variableList)):
            if line_tmp[i].isdigit():
                Vars[variableList[i]] = int(line_tmp[i])
            else:
                Vars[variableList[i]] = line_tmp[i]

        if mismatch_k(Vars, 4) and alignment_to_subject_length_k(Vars, 5) and gap_k(Vars, 2):
            print line[0:-1]

# Argument functions.

def alignment_to_subject_length_k(dict, k = 0):
    # Check whether alignment length is within minimum k threshold to subject length.

    return dict["Subject Length"] - dict["Alignment Length"] <= k

# Accounting for possible mismatches.

def mismatch_k(dict, k = 0):
    # Accounts possibility of k mismatch(es) as okay for classification.
    # 1 Gap open satisfies need.

    return dict["Mismatch"] <= k

def gap_k(dict, k = 0):
    # Default allows all ungapped lines.

    return dict["Gap Open"] <= k

def hit_start_end_k(dict, k = 0):
    # Reduces need for alignment length to be same as subject length by k value.
    # Requires other functions to work well, such as mismatch functions.

    start = 1 + k
    end = dict["Subject Length"] - k

    start_bool = dict["Hit Start"] <= start or dict["Hit Start"] >= end
    end_bool = dict["Hit End"] <= start or dict["Hit End"] >= end

    return start_bool and end_bool

def bit_score_346(dict, bit = 346):
    # Check whether bit score is full.

    return dict["Bit Score"] == bit

# Runs on terminal using command below.
"""
data = sys.stdin

BlastChecker(data)
"""
