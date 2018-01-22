#This script rounds floats to the desired digits
#
#

import re

def replace_string(line,regex_iter,round_to):
    """ helper function, to round ifc-floats
        arg1: line of text
        arg2: regex_iter: regex object from re.finditer
        arg3: integer = digits to round float
        return: repl_line zo use in str.replace 
    """
    repl_line = line
    try:
        for z in regex_iter:
            
            if round_to == 0:
                repl =round(float(z.group()))
                repl = str(repl)+"." #is needed in ifc, when rounding to 0 digits
                line = line.replace(z.group(),repl)
            else:
                repl =round(float(z.group()),round_to)
                line = line.replace(z.group(),str(repl))
    except:
        repl_line = line

    repl_line = line
    
    return repl_line



input_file = "B:\test.ifc"

#Check for si-units of measurement 
check_line = (x for x in open(input_file, 'r'))

#define, to which accuracy to round
while next(check_line):
    x = next(check_line)
    if ".LENGTHUNIT.,.MILLI.,.METRE." in x:
        round_to = 0
        break
    elif ".LENGTHUNIT.,$,.METRE." in x:
        round_to = 2
        break

#round floats 
float_regex = r"\d+\.\d+"

with open(input_file, "r") as infile, open("B:\Output.ifc", "w") as outfile:
    for line in infile:
        if "#" in line:
            if "IFC" in line:
                #If multiple floats in line are possible
                y= re.finditer(float_regex,line)
                line1 = replace_string(line,y,round_to)
                line= line1
        outfile.write(line)
