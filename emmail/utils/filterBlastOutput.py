# import sys

# Main workhorse.

def filter(variable, header):
    # Change arguments here.
    # IMPORTANT TO KNOW: FUNCTIONS DO NOT AUTOMATICALLY RELATE TO EACH OTHER. USE ALL NEEDED.
    output = ""

    variableList = ['Query', 'Blast Hit', 'Identity', 'Alignment Length', 'Mismatch',
                       'Gap Open', 'Query Start', 'Query End', 'Hit Start', 'Hit End',
                       'E-Value', 'Bit Score', 'Subject Length']

    line = ""
    for i in range(len(variableList)):
        if i == (len(variableList) - 1):
            line += "{}\n".format(variableList[i])
        else:
            line += "{}\t".format(variableList[i])

    if header:
        output += line

    for line in variable:
        # Split line by tab, and build dictionary of variables in tab.
        line_tmp = line.split("\t")
        Vars = {}

        for i in range(len(variableList)):
            if line_tmp[i].isdigit():
                Vars[variableList[i]] = int(line_tmp[i])
            else:
                Vars[variableList[i]] = line_tmp[i]

        if mismatch_k(Vars, 4) and alignment_to_subject_length_k(Vars, 5) and gap_k(Vars, 2):
            output += str(line) + "\n"

    return output

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
